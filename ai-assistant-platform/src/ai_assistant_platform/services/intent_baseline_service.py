from pathlib import Path

import joblib
import pandas as pd

from ai_assistant_platform.api.schemas.ml import PredictionResponse
from ai_assistant_platform.core.errors import NotFoundError


class IntentBaselineService:
    def __init__(self, artifact_path: str | Path):
        self.artifact_path = Path(artifact_path)

        if not self.artifact_path.exists():
            raise NotFoundError(f"Model not found at {self.artifact_path}")

        model = joblib.load(self.artifact_path)
        if not isinstance(model, dict):
            raise TypeError(f"Invalid model artifact format at {self.artifact_path}")

        self.intent_preprocessor = model["preprocessor"]
        self.model = model["model"]
        self.label_mapping = model["label_mapping"]
        self.model_version = model["model_version"]

    def predict(self, text: str) -> PredictionResponse:
        raw_data = pd.DataFrame({"text": [text], "source": "web"})
        processed_data = self.intent_preprocessor.transform(raw_data)
        label = self.model.predict(processed_data)[0]
        confidence = self.model.predict_proba(processed_data)[0]

        return PredictionResponse(
            intent=self.label_mapping.classes_[label],
            confidence=float(confidence[label]),
            model_version=self.model_version,
        )
