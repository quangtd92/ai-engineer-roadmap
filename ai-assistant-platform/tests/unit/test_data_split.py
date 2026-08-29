
import pandas as pd
import pytest

from ai_assistant_platform.ml.preprocessing import train_test_split_stratified


def test_splits_reproducible():
    df_raw = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            "text": [
                "Text 1",
                "Text 2",
                "Text 3",
                "Text 4",
                "Text 5",
                "Text 6",
                "Text 7",
                "Text 8",
                "Text 9",
                "Text 10",
                "Text 11",
                "Text 12",
                "Text 13",
                "Text 14",
                "Text 15",
                "Text 16",
            ],
            "intent": [
                "intent.a",
                "intent.b",
                "intent.a",
                "intent.c",
                "intent.c",
                "intent.b",
                "intent.a",
                "intent.c",
                "intent.a",
                "intent.b",
                "intent.c",
                "intent.b",
                "intent.a",
                "intent.b",
                "intent.c",
                "intent.b",
            ],
            "source": [
                "web",
                "phone",
                "app",
                "app",
                "chat",
                "email",
                "message",
                "social",
                "voice",
                "video",
                "email",
                "chat",
                "message",
                "social",
                "voice",
                "video",
            ],
            "created_at": [
                "t1",
                "t2",
                "t3",
                "t4",
                "t5",
                "t6",
                "t7",
                "t8",
                "t9",
                "t10",
                "t11",
                "t12",
                "t13",
                "t14",
                "t15",
                "t16",
            ],
        }
    )
    train_1, df_tmp_1 = train_test_split_stratified(df_raw, test_size=0.4)
    df_test_1, df_validate_1 = train_test_split_stratified(df_tmp_1, test_size=0.5)

    train_2, df_tmp_2 = train_test_split_stratified(df_raw, test_size=0.4)
    df_test_2, df_validate_2 = train_test_split_stratified(df_tmp_2, test_size=0.5)

    assert train_1.equals(train_2)
    assert df_test_1.equals(df_test_2)
    assert df_validate_1.equals(df_validate_2)

def test_splits_raw_count():
    raw_data = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "text": ["Text 1", "Text 2", "Text 3", "Text 4", "Text 5", "Text 6", "Text 7", "Text 8", "Text 9", "Text 10", "Text 11", "Text 12", "Text 13", "Text 14", "Text 15", "Text 16", "Text 17", "Text 18", "Text 19", "Text 20"],
        "intent": ["a"] * 7 + ["b"] * 7 + ["c"] * 6,
    }
    df_raw = pd.DataFrame(raw_data)

    train_1, df_tmp_1 = train_test_split_stratified(df_raw, test_size=0.4)
    df_test_1, df_validate_1 = train_test_split_stratified(df_tmp_1, test_size=0.5)

    assert len(df_raw) == len(train_1) + len(df_test_1) + len(df_validate_1)

def test_splits_raises_error_on_too_few_samples():
    raw_data = {
        "id": [1, 2],
        "text": ["Text 1", "Text 2"],
        "intent": ["a", "b"],
    }
    df_raw = pd.DataFrame(raw_data)

    with pytest.raises(ValueError):
        train_test_split_stratified(df_raw, test_size=0.5)
    
def test_splits_no_overlap():
    raw_data = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "text": ["Text 1", "Text 2", "Text 3", "Text 4", "Text 5", "Text 6", "Text 7", "Text 8", "Text 9", "Text 10", "Text 11", "Text 12", "Text 13", "Text 14", "Text 15", "Text 16", "Text 17", "Text 18", "Text 19", "Text 20"],
        "intent": ["a"] * 7 + ["b"] * 7 + ["c"] * 6,
    }
    df_raw = pd.DataFrame(raw_data)

    train_1, df_tmp_1 = train_test_split_stratified(df_raw, test_size=0.4)
    df_test_1, df_validate_1 = train_test_split_stratified(df_tmp_1, test_size=0.5)

    train_set = set(train_1["id"])
    test_set = set(df_test_1["id"])
    validate_set = set(df_validate_1["id"])

    assert len(train_set.intersection(test_set)) == 0
    assert len(train_set.intersection(validate_set)) == 0
    assert len(test_set.intersection(validate_set)) == 0
