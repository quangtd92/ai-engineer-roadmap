from pathlib import Path

import numpy as np
import pandas as pd

from ai_assistant_platform.ml.preprocessing import IntentPreprocessor

TRAIN_DATA_PATH = Path("data/splits/train.csv")
TEST_DATA_PATH = Path("data/splits/test.csv")
VALIDATION_DATA_PATH = Path("data/splits/validation.csv")


def main():
    df_train = pd.read_csv(TRAIN_DATA_PATH)
    df_test = pd.read_csv(TEST_DATA_PATH)
    df_validate = pd.read_csv(VALIDATION_DATA_PATH)

    df_train_text_set = set(df_train["text"])
    df_test_text_set = set(df_test["text"])
    df_validate_text_set = set(df_validate["text"])

    if df_train_text_set.intersection(df_test_text_set):
        print("df_train_text_set intersection df_test_text_set")
        print(df_train_text_set.intersection(df_test_text_set))
        raise AssertionError("df_train_text_set intersection df_test_text_set")
    
    if df_train_text_set.intersection(df_validate_text_set):
        print("df_train_text_set intersection df_validate_text_set")
        print(df_train_text_set.intersection(df_validate_text_set))
        raise AssertionError("df_train_text_set intersection df_validate_text_set")
    
    if df_test_text_set.intersection(df_validate_text_set):
        print("df_test_text_set intersection df_validate_text_set")
        print(df_test_text_set.intersection(df_validate_text_set))
        raise AssertionError("df_test_text_set intersection df_validate_text_set")

    df_train_intent_set = set(df_train["intent"])
    df_test_intent_set = set(df_test["intent"])
    df_validate_intent_set = set(df_validate["intent"])

    unseen_test_intents = df_test_intent_set - df_train_intent_set
    if unseen_test_intents:
        print(f"df_test_intent_set - df_train_intent_set: {unseen_test_intents}")
        raise AssertionError("df_test_intent_set - df_train_intent_set")

    unseen_validate_intents = df_validate_intent_set - df_train_intent_set
    if unseen_validate_intents:
        print(f"df_validate_intent_set - df_train_intent_set: {unseen_validate_intents}")
        raise AssertionError("df_validate_intent_set - df_train_intent_set")

    intent_preprocessor = IntentPreprocessor()
    intent_preprocessor.fit(df_train)
    x_train = intent_preprocessor.transform(df_train)
    x_test = intent_preprocessor.transform(df_test)
    x_validate = intent_preprocessor.transform(df_validate)
    print(f"\n x_train: \n{x_train}")
    print(f"\n x_train: \n{x_train.shape[0]}")
    print(f"\n x_train: \n{x_train.shape[1]}")

    if x_train.shape[1] == x_test.shape[1] == x_validate.shape[1]:
        print("x_train.shape[1] == x_test.shape[1] == x_validate.shape[1]")
        print(f"x_train.shape[1] {x_train.shape[1]}")
    else:
        print("x_train.shape[1] != x_test.shape[1] or x_train.shape[1] != x_validate.shape[1]")
        print(f"x_train.shape[1] {x_train.shape[1]}")
        print(f"x_test.shape[1] {x_test.shape[1]}")
        print(f"x_validate.shape[1] {x_validate.shape[1]}")
        raise AssertionError("x_train.shape[1] != x_test.shape[1] or x_train.shape[1] != x_validate.shape[1]")

    if x_train.shape[0] == len(df_train):
        print("x_train.shape[0] == len(df_train)")
    else:
        print("x_train.shape[0] != len(df_train)")
        print(f"x_train.shape[0] {x_train.shape[0]}")
        print(f"len(df_train) {len(df_train)}")
        raise AssertionError("x_train.shape[0] != len(df_train)")

    if x_test.shape[0] == len(df_test):
        print("x_test.shape[0] == len(df_test)")
    else:
        print("x_test.shape[0] != len(df_test)")
        print(f"x_test.shape[0] {x_test.shape[0]}")
        print(f"len(df_test) {len(df_test)}")
        raise AssertionError("x_test.shape[0] != len(df_test)")

    if x_validate.shape[0] == len(df_validate):
        print("x_validate.shape[0] == len(df_validate)")
    else:
        print("x_validate.shape[0] != len(df_validate)")
        print(f"x_validate.shape[0] {x_validate.shape[0]}")
        print(f"len(df_validate) {len(df_validate)}")
        raise AssertionError("x_validate.shape[0] != len(df_validate)")

    if x_train.dtype == np.float32:
        print("x_train.dtype == np.float32")
    else:
        print("x_train.dtype != np.float32")
        print(f"x_train.dtype {x_train.dtype}")
        raise AssertionError("x_train.dtype != np.float32")

    if x_test.dtype == np.float32:
        print("x_test.dtype == np.float32")
    else:
        print("x_test.dtype != np.float32")
        print(f"x_test.dtype {x_test.dtype}")
        raise AssertionError("x_test.dtype != np.float32")

    if x_validate.dtype == np.float32:
        print("x_validate.dtype == np.float32")
    else:
        print("x_validate.dtype != np.float32")
        print(f"x_validate.dtype {x_validate.dtype}")
        raise AssertionError("x_validate.dtype != np.float32")

    if np.isfinite(x_train).all():
        print("x_train.isfinite")
    else:
        print("x_train.not isfinite")
        raise AssertionError("x_train.not isfinite")

    if np.isfinite(x_test).all():
        print("x_test.isfinite")
    else:
        print("x_test.not isfinite")
        raise AssertionError("x_test.not isfinite")

    if np.isfinite(x_validate).all():
        print("x_validate.isfinite")
    else:
        print("x_validate.not isfinite")
        raise AssertionError("x_validate.not isfinite")

    return 0

if __name__ == "__main__":
    main()

