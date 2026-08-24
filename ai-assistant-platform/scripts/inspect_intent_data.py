from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/raw/intent_samples.csv")


def main():
    df = pd.read_csv(DATA_PATH)

    shape = df.shape
    size = df.size
    print(f"shape: {shape}")
    print(f"size: {size}")

    value_count = df["intent"].value_counts()
    print(f"value_count: {value_count}")
    duplicate_count = df.duplicated().sum()
    print(f"duplicate_count: {duplicate_count}")

    empty_count = df.isna().sum()
    print(f"empty_count: {empty_count}")

    empty_texts = df["text"].astype(str).str.strip().eq("").sum()
    print(f"empty_texts: {empty_texts}")


if __name__ == "__main__":
    main()
