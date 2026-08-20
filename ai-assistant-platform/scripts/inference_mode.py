import torch
from torch import nn

torch.manual_seed(2)
x = torch.tensor([1.0, 2.0])
model = nn.Linear(2, 3)
model_eval = model.eval()

with torch.no_grad():
    prediction = model(x)

prediction_shape = prediction.shape

print(f"model_eval={model_eval}")
print(f"prediction={prediction.requires_grad}")
print(f"prediction shape={prediction.shape}")
print(f"prediction device={prediction.device}")
print(f"prediction dtype={prediction.dtype}")
