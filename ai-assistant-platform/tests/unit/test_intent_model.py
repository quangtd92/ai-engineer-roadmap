import pytest
import torch

from ai_assistant_platform.ml.intent_model import IntentClassifier


def test_intent_classifier_forward_shape():
    input_dim = 10
    hidden_dim = 16
    num_classes = 3
    input = torch.randn(4, input_dim)

    model = IntentClassifier(input_dim=input_dim, hidden_dim=hidden_dim, num_classes=num_classes)

    output = model(input)
    assert output.shape == (4, num_classes)

def test_intent_classifier_no_nan():
    input_dim = 10
    hidden_dim = 16
    num_classes = 3
    input = torch.randn(4, input_dim)

    model = IntentClassifier(input_dim=input_dim, hidden_dim=hidden_dim, num_classes=num_classes)

    output = model(input)
    print(f"{output=}")
    assert not torch.isnan(output).any()

def test_intent_classifier_invalid_input_dim():
    input_dim = 10
    hidden_dim = 16
    num_classes = 3
    input = torch.randn(4, 8)

    model = IntentClassifier(input_dim=input_dim, hidden_dim=hidden_dim, num_classes=num_classes)
    
    with pytest.raises(RuntimeError):
        model(input)
