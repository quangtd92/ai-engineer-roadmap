# Tháng 2 - Tuần 1: NumPy, pandas, cleaning, split và data leakage

## Mục tiêu tuần

Xây nền data pipeline cho `ai-assistant-platform`: đọc dữ liệu intent nhỏ, kiểm tra chất lượng, làm sạch, encoding đơn giản, scaling đúng chỗ, tách train/validation/test và ghi tài liệu về data leakage.

## Kiến thức cần đạt

- Dùng NumPy array để hiểu shape, dtype, vectorization và aggregation.
- Dùng pandas `DataFrame` để đọc CSV/JSON, inspect dữ liệu, xử lý missing value và duplicate.
- Phân biệt cleaning trước split với transformation phải `fit` trên train.
- Tạo split reproducible bằng seed, stratify theo label.
- Nhận diện data leakage thường gặp trong pipeline ML.

## Module project sẽ bổ sung

`data/raw/intent_samples.csv`, `scripts/prepare_intent_data.py`, `src/ai_assistant_platform/ml/preprocessing.py`, test cho preprocessing và tài liệu `docs/data-pipeline.md`.

## Kế hoạch từng ngày

### Ngày 1 - Tạo dataset intent và đọc bằng pandas

**Mục tiêu cụ thể:** Tạo dataset nhỏ cho intent classification của assistant. **Kết quả cần đạt:** CSV có ít nhất 40 dòng với các cột `text`, `intent`, `source`, `created_at`, cố tình có vài missing/duplicate để luyện cleaning. **Phân bổ thời gian:** 15 phút ôn Month-01 handoff, 20 phút đọc pandas DataFrame, 45 phút tạo CSV và script đọc, 15 phút kiểm tra, 10 phút ghi chú. **Lý thuyết:** DataFrame, schema dữ liệu, label classification và vì sao fixture phải nhỏ nhưng đại diện. **Tài liệu:** pandas 10 minutes trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `data/raw/intent_samples.csv` và `scripts/inspect_intent_data.py` in số dòng, số label, missing count. **Tích hợp project:** Dataset này sẽ dùng cho baseline, PyTorch training và endpoint intent. **File tạo/sửa:** `data/raw/intent_samples.csv`, `scripts/inspect_intent_data.py`, `README.md` của project nếu cần ghi cách chạy. **Lệnh chạy:** `uv add pandas numpy`; `uv run python scripts/inspect_intent_data.py`. **Kết quả mong đợi:** Console in số dòng, distribution của `intent` và cảnh báo có missing/duplicate. **Cách kiểm tra:** Thêm một dòng thiếu `intent` rồi chạy lại để thấy cảnh báo tăng. **Definition of Done:** Dataset không chứa thông tin nhạy cảm và script đọc được từ relative path. **Commit message:** `data(intent): add raw intent samples`. **Câu hỏi tự kiểm tra:** Label `intent` khác text output ở đâu? Vì sao dataset nhỏ vẫn cần schema? Dòng duplicate ảnh hưởng train/test thế nào?

### Ngày 2 - NumPy shape, dtype và vectorization cho feature đơn giản

**Mục tiêu cụ thể:** Dùng NumPy tạo feature numeric từ text mà không viết loop phức tạp. **Kết quả cần đạt:** Script tạo mảng `text_length`, `word_count`, `has_question_mark` với shape rõ ràng. **Phân bổ thời gian:** 25 phút đọc NumPy basics, 40 phút code feature, 20 phút so sánh shape/dtype, 10 phút ghi chú. **Lý thuyết:** `ndarray`, shape, dtype, axis, vectorized operations. **Tài liệu:** NumPy absolute beginners và quickstart trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `scripts/numpy_text_features.py` đọc CSV và xuất array feature 2D. **Tích hợp project:** Các feature này là baseline trước khi có embedding. **File tạo/sửa:** `scripts/numpy_text_features.py`, `docs/data-pipeline.md`. **Lệnh chạy:** `uv run python scripts/numpy_text_features.py`. **Kết quả mong đợi:** In `X.shape == (n_rows, 3)` và dtype numeric. **Cách kiểm tra:** Đổi thứ tự dòng trong CSV, feature vẫn tương ứng đúng từng text. **Definition of Done:** Không dùng NumPy cho text processing phức tạp; chỉ dùng để hiểu numeric matrix. **Commit message:** `feat(data): add numpy text feature exploration`. **Câu hỏi tự kiểm tra:** Vì sao model cần input dạng ma trận numeric? `shape[0]` và `shape[1]` biểu diễn gì? Dtype object gây khó khăn gì?

### Ngày 3 - Missing values, duplicate và cleaning contract

**Mục tiêu cụ thể:** Làm sạch dataset theo rule rõ ràng thay vì sửa tay tùy hứng. **Kết quả cần đạt:** `data/processed/intent_samples_clean.csv` không có text rỗng, label rỗng hoặc duplicate exact. **Phân bổ thời gian:** 20 phút đọc missing data, 50 phút viết cleaning function, 20 phút test, 10 phút ghi notes. **Lý thuyết:** Missing value, duplicate, normalization nhẹ, audit log khi drop row. **Tài liệu:** pandas Working with missing data trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Viết `clean_intent_dataframe(df)` trim text, chuẩn hóa intent lowercase, drop invalid rows và trả kèm summary. **Tích hợp project:** Cleaning function nằm trong module tái sử dụng, không chỉ trong script. **File tạo/sửa:** `src/ai_assistant_platform/ml/preprocessing.py`, `scripts/prepare_intent_data.py`, `tests/unit/test_preprocessing.py`, `data/processed/intent_samples_clean.csv`. **Lệnh chạy:** `uv run python scripts/prepare_intent_data.py`; `uv run pytest tests/unit/test_preprocessing.py -q`. **Kết quả mong đợi:** File processed được tạo, test xác nhận missing/duplicate bị xử lý. **Cách kiểm tra:** Tạo fixture DataFrame trong test có text `"  "` và duplicate. **Definition of Done:** Cleaning summary cho biết đã drop bao nhiêu dòng, không âm thầm mất dữ liệu. **Commit message:** `feat(data): add intent data cleaning pipeline`. **Câu hỏi tự kiểm tra:** Khi nào nên drop missing, khi nào nên fill? Vì sao phải log số dòng bị loại? Cleaning có được dùng label test set không?

### Ngày 4 - Encoding categorical và scaling numeric đúng boundary

**Mục tiêu cụ thể:** Tách feature extraction, encoder và scaler thành pipeline có thể fit/transform. **Kết quả cần đạt:** Preprocessor chỉ `fit` trên train trong ngày 5, hôm nay mới chuẩn bị API. **Phân bổ thời gian:** 20 phút đọc OneHotEncoder/StandardScaler, 45 phút thiết kế class/function, 25 phút unit test, 10 phút ghi chú. **Lý thuyết:** Categorical encoding, numeric scaling, `fit` vs `transform`, unknown category. **Tài liệu:** OneHotEncoder và StandardScaler trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `IntentPreprocessor` với `fit`, `transform`, `fit_transform`; numeric text features và optional one-hot `source`. **Tích hợp project:** Module sẽ dùng cho scikit-learn baseline và PyTorch dataset. **File tạo/sửa:** `src/ai_assistant_platform/ml/preprocessing.py`, `tests/unit/test_preprocessing.py`. **Lệnh chạy:** `uv run pytest tests/unit/test_preprocessing.py -q`. **Kết quả mong đợi:** Unknown `source` ở validation không làm pipeline crash nếu dùng `handle_unknown="ignore"`. **Cách kiểm tra:** Test train chỉ có `web`, validation có `mobile`; transform vẫn chạy. **Definition of Done:** Không fit scaler/encoder trên toàn bộ dataset. **Commit message:** `feat(ml): add reusable intent preprocessor`. **Câu hỏi tự kiểm tra:** `fit` học thông tin gì từ dữ liệu? Vì sao scaling trước split có thể leak? Unknown category nên xử lý thế nào trong API?

### Ngày 5 - Train/validation/test split có stratify

**Mục tiêu cụ thể:** Tạo split reproducible cho dataset intent. **Kết quả cần đạt:** `data/splits/train.csv`, `validation.csv`, `test.csv` có phân bố label hợp lý và không overlap text. **Phân bổ thời gian:** 20 phút đọc `train_test_split`, 45 phút viết split script, 25 phút test overlap/distribution, 10 phút ghi chú. **Lý thuyết:** Train/validation/test, random seed, stratify, class imbalance. **Tài liệu:** scikit-learn `train_test_split` trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Cập nhật `scripts/prepare_intent_data.py` để tạo split 70/15/15 hoặc gần nhất với dataset nhỏ. **Tích hợp project:** Tất cả training script sau này chỉ đọc từ `data/splits/`. **File tạo/sửa:** `scripts/prepare_intent_data.py`, `data/splits/train.csv`, `data/splits/validation.csv`, `data/splits/test.csv`, `tests/unit/test_data_split.py`. **Lệnh chạy:** `uv run python scripts/prepare_intent_data.py`; `uv run pytest tests/unit/test_data_split.py -q`. **Kết quả mong đợi:** Chạy lại cùng seed tạo cùng số dòng và không có text trùng giữa splits. **Cách kiểm tra:** Hash nội dung split trước/sau khi chạy lại. **Definition of Done:** Script fail rõ ràng nếu label có quá ít sample để stratify. **Commit message:** `feat(data): create reproducible intent splits`. **Câu hỏi tự kiểm tra:** Validation và test khác nhau thế nào? Vì sao seed quan trọng? Khi label quá ít sample thì stratify gặp lỗi gì?

### Ngày 6 - Data leakage checklist và pipeline smoke test

**Mục tiêu cụ thể:** Ghi checklist chống leakage và chạy pipeline từ raw đến feature matrix. **Kết quả cần đạt:** `docs/data-pipeline.md` mô tả input, output, split và rule fit/transform. **Phân bổ thời gian:** 20 phút đọc lại code, 35 phút viết tài liệu, 35 phút smoke test, 10 phút ghi nhận lỗi. **Lý thuyết:** Data leakage qua scaling, duplicate, timestamp, target-derived feature và test set reuse. **Tài liệu:** Xem lại `train_test_split`, OneHotEncoder, StandardScaler trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo script `scripts/check_data_pipeline.py` load train/validation/test, fit preprocessor trên train, transform cả ba split. **Tích hợp project:** Có command duy nhất kiểm tra data readiness cho Week-02. **File tạo/sửa:** `scripts/check_data_pipeline.py`, `docs/data-pipeline.md`. **Lệnh chạy:** `uv run python scripts/check_data_pipeline.py`; `uv run pytest tests/unit -q`. **Kết quả mong đợi:** In shape của từng split và pass leakage checks cơ bản. **Cách kiểm tra:** Cố tình duplicate một text giữa train/test để script fail. **Definition of Done:** Checklist nêu rõ điều không được làm với test set. **Commit message:** `docs(data): document leakage checks for intent pipeline`. **Câu hỏi tự kiểm tra:** Feature nào có thể chứa label trá hình? Vì sao test set không dùng để chọn threshold? Smoke test khác unit test thế nào?

### Ngày 7 - Review tuần 1 và chuẩn bị baseline

**Mục tiêu cụ thể:** Chốt data pipeline đủ sạch cho ML baseline. **Kết quả cần đạt:** Cleaning, split, preprocessing và docs đều chạy lại được từ clone mới. **Phân bổ thời gian:** 20 phút review checklist, 30 phút refactor nhỏ, 30 phút chạy test/lint, 20 phút ghi handoff sang Week-02. **Lý thuyết:** Reproducibility và dữ liệu là dependency của model. **Tài liệu:** Không đọc nguồn mới; chỉ xem lại [RESOURCES.md](./RESOURCES.md) nhóm Tuần 1. **Thực hành:** Chạy toàn bộ command tuần 1, sửa lỗi path hoặc import. **Tích hợp project:** Ghi `docs/week-02-baseline-plan.md` mô tả feature matrix và label mapping sẽ dùng. **File tạo/sửa:** `docs/week-02-baseline-plan.md`, các test liên quan nếu cần. **Lệnh chạy:** `uv run python scripts/prepare_intent_data.py`; `uv run python scripts/check_data_pipeline.py`; `uv run ruff check .`; `uv run pytest`. **Kết quả mong đợi:** Lint/test pass, docs nêu rõ output của pipeline. **Cách kiểm tra:** Xóa `data/processed/` và `data/splits/`, chạy lại script để tái tạo. **Definition of Done:** Không còn placeholder trong docs tuần 1 và Week-02 có input rõ ràng. **Commit message:** `chore(data): validate intent pipeline milestone`. **Câu hỏi tự kiểm tra:** Nếu baseline Week-02 tệ, bạn sẽ nghi ngờ dữ liệu ở đâu trước? Output bắt buộc của pipeline là gì? Leakage nào dễ bỏ sót nhất?

## Milestone cuối tuần

Từ raw CSV có thể tạo processed dataset, split reproducible, feature matrix và leakage checklist. Week-02 có thể bắt đầu huấn luyện baseline mà không phải sửa lại cấu trúc dữ liệu.

## Review checklist

- [ ] `scripts/prepare_intent_data.py` chạy lại được từ raw data.
- [ ] Train/validation/test không overlap.
- [ ] Preprocessor có unit test cho missing, duplicate, unknown category và fit/transform.
- [ ] Không fit scaler/encoder trên validation hoặc test.
- [ ] `docs/data-pipeline.md` có input/output và leakage checklist.

## Definition of Done

Tuần 1 hoàn thành khi data pipeline của `ai-assistant-platform` tạo ra dữ liệu sạch, split ổn định và feature matrix dùng được cho scikit-learn baseline ở tuần 2.

## Lỗi thường gặp

- Tạo feature sau khi gộp train/test rồi mới split.
- Drop duplicate sau split làm mất cân bằng label.
- Lưu path tuyệt đối trong script.
- Dùng dataset quá nhỏ khiến validation/test không có đủ class.
- Coi cleaning là sửa tay trong CSV thay vì code chạy lại được.

## Tài liệu chính thức

Xem nhóm Tuần 1 trong [RESOURCES.md](./RESOURCES.md).

## Tùy chọn nếu còn thời gian

- Thêm `make` hoặc script alias cho data pipeline.
- Ghi data dictionary ngắn cho từng cột.
- Thử đọc JSON fixture rồi convert sang cùng schema CSV.
