from pathlib import Path

import pandas as pd

from ai_assistant_platform.ml.preprocessing import (
    clean_intent_dataframe,
    train_test_split_stratified,
)

RAW_DATA_PATH = Path("data/raw/intent_samples.csv")
CLEAN_DATA_PATH = Path("data/processed/intent_samples_clean.csv")
TRAIN_DATA_PATH = Path("data/splits/train.csv")
TEST_DATA_PATH = Path("data/splits/test.csv")
VALIDATION_DATA_PATH = Path("data/splits/validation.csv")


def main():
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"df size {df.size}")
    print(f"df shape {df.shape}")
    print(f"df info {df.info()}")

    df, summary = clean_intent_dataframe(df)

    print(f"df shape {df.shape}")
    print(f"summary {summary}")

    CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"Saved cleaned data to {CLEAN_DATA_PATH}")

    print(f"df len: {len(df)}")

    df_train, df_tmp = train_test_split_stratified(df, test_size=0.3)
    print(f"df_tmp: \n\n {(df_tmp)}")
    print(f"df_train len: {len(df_train)}")
    df_test, df_validate = train_test_split_stratified(df_tmp, test_size=0.5)
    print(f"df_test: {(df_test)}")
    print(f"df_test len: {len(df_test)}")
    print(f"df_validate len: {len(df_validate)}")

    TRAIN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    TEST_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    df_train.to_csv(TRAIN_DATA_PATH, index=False)
    df_test.to_csv(TEST_DATA_PATH, index=False)
    df_validate.to_csv(VALIDATION_DATA_PATH, index=False)

    return df_train, df_test, df_validate

if __name__ == "__main__":
    main()
