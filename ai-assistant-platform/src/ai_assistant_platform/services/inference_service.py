import torch
from torch import nn


class InferenceService:
    def __init__(self):
        self.model = self.build_model()
        self.model.eval()

    def build_model(self):
        torch.manual_seed(2)
        model = nn.Linear(2, 1)

        return model

    def run_inference(self, values: list[float]) -> float:
        x = torch.tensor(values, dtype=torch.float32)
        with torch.no_grad():
            prediction = self.model(x)
        return float(prediction.item())
