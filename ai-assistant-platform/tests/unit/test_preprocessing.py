import pandas as pd

from ai_assistant_platform.ml.preprocessing import clean_intent_dataframe


def test_clean_intent_dataframe_valid_data():
    """Kiểm tra dữ liệu hợp lệ: chuẩn hóa khoảng trắng text và lowercase intent."""
    df_raw = pd.DataFrame(
        {
            "id": [1, 2],
            "text": ["  Tôi muốn xem lịch hôm nay  ", "Gửi email báo cáo "],
            "intent": ["INTENT.SCHEDULE", "intent.send_email "],
            "source": ["web_ui", "web_ui"],
            "created_at": ["2023-10-27 10:00:00", "2023-10-27 10:01:00"],
        }
    )
    df_clean, summary = clean_intent_dataframe(df_raw)

    assert len(df_clean) == 2
    assert df_clean.iloc[0]["text"] == "Tôi muốn xem lịch hôm nay"
    assert df_clean.iloc[0]["intent"] == "intent.schedule"
    assert df_clean.iloc[1]["text"] == "Gửi email báo cáo"
    assert df_clean.iloc[1]["intent"] == "intent.send_email"
    assert summary["dropped_text_rows"] == 0
    assert summary["dropped_intent_rows"] == 0
    assert summary["dropped_duplicate_rows"] == 0


def test_clean_intent_dataframe_removes_missing_and_empty_text():
    """Kiểm tra loại bỏ dòng có text là None, NaN hoặc chuỗi toàn khoảng trắng."""
    df_raw = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "text": ["Hợp lệ", None, "   ", ""],
            "intent": [
                "intent.valid",
                "intent.valid",
                "intent.valid",
                "intent.valid",
            ],
            "source": ["web_ui", "web_ui", "web_ui", "web_ui"],
            "created_at": [
                "2023-10-27 10:00:00",
                "2023-10-27 10:01:00",
                "2023-10-27 10:02:00",
                "2023-10-27 10:03:00",
            ],
        }
    )
    df_clean, summary = clean_intent_dataframe(df_raw)

    assert len(df_clean) == 1
    assert df_clean.iloc[0]["text"] == "Hợp lệ"
    assert summary["dropped_text_rows"] == 3


def test_clean_intent_dataframe_removes_missing_and_empty_intent():
    """Kiểm tra loại bỏ dòng có intent là None, NaN hoặc chuỗi toàn khoảng trắng."""
    df_raw = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "text": ["Text 1", "Text 2", "Text 3", "Text 4"],
            "intent": ["intent.valid", None, "  ", ""],
            "source": ["web_ui", "web_ui", "web_ui", "web_ui"],
            "created_at": [
                "2023-10-27 10:00:00",
                "2023-10-27 10:01:00",
                "2023-10-27 10:02:00",
                "2023-10-27 10:03:00",
            ],
        }
    )
    df_clean, summary = clean_intent_dataframe(df_raw)

    assert len(df_clean) == 1
    assert df_clean.iloc[0]["text"] == "Text 1"
    assert summary["dropped_intent_rows"] == 3


def test_clean_intent_dataframe_removes_duplicates():
    """Kiểm tra loại bỏ các dòng bị trùng lặp hoàn toàn."""
    df_raw = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "text": ["Đặt lịch họp", "Đặt lịch họp", "Tạo file mới"],
            "intent": ["intent.meeting", "intent.meeting", "intent.file"],
            "source": ["web_ui", "web_ui", "web_ui"],
            "created_at": [
                "2023-10-27 10:00:00",
                "2023-10-27 10:00:00",
                "2023-10-27 10:01:00",
            ],
        }
    )
    df_clean, summary = clean_intent_dataframe(df_raw)

    assert len(df_clean) == 2
    assert summary["dropped_duplicate_rows"] == 1


def test_clean_intent_dataframe_summary_report():
    """Kiểm tra tính chính xác của summary audit report."""
    df_raw = pd.DataFrame(
        {
            "id": [1, 2, 3, 3],
            "text": ["Text 1", None, "Text 3", "Text 3"],
            "intent": ["intent.a", "intent.b", "intent.c", "intent.c"],
            "source": ["web", "web", "web", "web"],
            "created_at": ["t1", "t2", "t3", "t3"],
        }
    )
    df_clean, summary = clean_intent_dataframe(df_raw)

    assert summary["initial_rows"] == 4
    assert summary["dropped_text_rows"] == 1
    assert summary["dropped_intent_rows"] == 0
    assert summary["dropped_duplicate_rows"] == 1
    assert len(df_clean) == 2
