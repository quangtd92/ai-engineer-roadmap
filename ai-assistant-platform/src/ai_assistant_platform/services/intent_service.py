

import json
from pathlib import Path

import joblib
import pandas as pd
import torch

from ai_assistant_platform.api.schemas.ml import PredictionResponse
from ai_assistant_platform.core.errors import NotFoundError
from ai_assistant_platform.ml.intent_model import IntentClassifier


class IntentService:
    def __init__(self, classifier_path: str | Path, metadata_path: str | Path, preprocessor_path: str | Path):
        self.classifier_path = Path(classifier_path)
        self.metadata_path = Path(metadata_path)
        self.preprocessor_path = Path(preprocessor_path)
        
        for path in (self.classifier_path, self.metadata_path, self.preprocessor_path):
            if not path.exists():
                raise NotFoundError(f"Artifact not found at {path}")
        
        # 1. Đọc metadata
        with open(self.metadata_path, encoding="utf-8") as f:
            self.metadata = json.load(f)
        
        # 2. Đọc preprocessor
        self.preprocessor = joblib.load(self.preprocessor_path)

        
        # 3. Khởi tạo model với dimensions từ metadata và load state dict
        model = IntentClassifier(
            input_dim=self.metadata["input_dim"],
            hidden_dim=self.metadata["hidden_dim"],
            num_classes=self.metadata["num_classes"],
        )
        model.load_state_dict(
            torch.load(self.classifier_path, map_location=torch.device("cpu"))
        )
        model.eval()
        self.model = model

    def predict(self, text: str, source: str = "web_ui") -> PredictionResponse:
        raw_data = pd.DataFrame({"text": [text], "source": [source]})
        features = self.preprocessor.transform(raw_data)
        features_tensor = torch.tensor(features, dtype=torch.float32)

        self.model.eval()
        with torch.no_grad():
            logits = self.model(features_tensor)
            probs = torch.softmax(logits, dim=1)[0]
            pred_idx = torch.argmax(probs).item()
            confidence = float(probs[pred_idx].item())


        predicted_intent = self.metadata["classes"][pred_idx]
        return PredictionResponse(
            intent=predicted_intent,
            confidence=confidence,
            model_version=self.metadata["model_version"],
        )
