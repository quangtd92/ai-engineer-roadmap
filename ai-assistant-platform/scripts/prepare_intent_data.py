from pathlib import Path

import pandas as pd

from ai_assistant_platform.ml.preprocessing import clean_intent_dataframe

RAW_DATA_PATH = Path("data/raw/intent_samples.csv")
CLEAN_DATA_PATH = Path("data/processed/intent_samples_clean.csv")


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

if __name__ == "__main__":
    main()
