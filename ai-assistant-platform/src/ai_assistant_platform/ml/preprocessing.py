import logging

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def clean_intent_dataframe(df):
    logger = logging.getLogger(__name__)
    logger.info(f"df info {df.info()}")
    logger.info(f"sum column is nan {df.isna().sum()}")
    logger.info(f"sum row is duplicate {df.duplicated().sum()}")

    df = df.copy()
    df['text'] = df['text'].apply(lambda x: x.strip() if isinstance(x, str) and x.strip() != "" else None)
    df['intent'] = df['intent'].apply(lambda x: x.strip().lower() if isinstance(x, str) and x.strip() != "" else None)

    before = len(df)
    logger.info(f"before dropna {before}")

    df = df.dropna(subset=['text'])

    after_dropna_text = len(df)

    logger.info(f"after_dropna_text dropna {after_dropna_text}")
    dropna_text_count = before - after_dropna_text

    logger.info(f"Dropped {dropna_text_count} rows")
    
    df = df.dropna(subset=['intent'])
    after_dropna_intent = len(df)
    logger.info(f"after_dropna_intent dropna {after_dropna_intent}")
    dropna_intent_count = after_dropna_text - after_dropna_intent
    logger.info(f"Dropped {dropna_intent_count} rows")
    
    df = df.drop_duplicates()
    after_drop_duplicate = len(df)
    logger.info(f"after drop_duplicates {after_drop_duplicate}")
    dropduplicate_count = after_dropna_intent - after_drop_duplicate
    logger.info(f"Dropped {dropduplicate_count} rows")

    summary = {
        'initial_rows': before,
        'rows_after_dropna_text': after_dropna_text,
        'rows_after_dropna_intent': after_dropna_intent,
        'rows_after_drop_duplicate': after_drop_duplicate,
        'dropped_text_rows': dropna_text_count,
        'dropped_intent_rows': dropna_intent_count,
        'dropped_duplicate_rows': dropduplicate_count
    }

    return df, summary
    
class IntentPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.is_fitted = False

    def extract_numeric_features_from_text(self, df):
        cleaned_texts = [str(t) if pd.notna(t) else "" for t in df['text']]
        text_lengths = np.array([len(t) for t in cleaned_texts], dtype=np.int32)
        word_counts = np.array([len(t.split()) for t in cleaned_texts], dtype=np.int32)
        has_question_marks = np.array(
            ["?" in t for t in cleaned_texts], dtype=np.int32
        )

        return np.column_stack([text_lengths, word_counts, has_question_marks])

    def fit(self, df):
        result_extracted = self.extract_numeric_features_from_text(df)
        self.scaler.fit(result_extracted)
        self.encoder.fit(df[['source']])
        self.is_fitted = True

        return self

    def transform(self, df):
        if not self.is_fitted:
            raise ValueError("You must fit the preprocessor before transforming data")
        
        result_extracted = self.extract_numeric_features_from_text(df)
        scaled_features = self.scaler.transform(result_extracted)
        encoded_source = self.encoder.transform(df[['source']])
        print(f"result_extracted {result_extracted}")
        print(f"scaled_features {scaled_features}")
        print(f"encoded_source {encoded_source}")

        df_transformed = np.hstack([scaled_features, encoded_source]).astype(np.float32)
        # print(f"df_transformed {df_transformed}")
        # print(f"df_transformed shape {df_transformed.shape}")
        # print(f"df_transformed info {df_transformed.info()}")
        
        return df_transformed

    def fit_transform(self, df):
        return self.fit(df).transform(df)
