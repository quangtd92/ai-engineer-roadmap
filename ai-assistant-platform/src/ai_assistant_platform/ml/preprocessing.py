import logging


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
    