# Tháng 2 - Data processing, ML foundation, Neural Network và Transformer foundation

Tháng 2 tiếp nối nền tảng FastAPI, Docker, test và toy PyTorch inference của Month-01. Trọng tâm không phải trở thành Data Scientist, mà là đủ hiểu dữ liệu, training, evaluation và Transformer để bước sang LLM Engineering ở Month-03 với nền móng chắc.

## Mục tiêu tháng

- Xây pipeline xử lý dữ liệu nhỏ cho `ai-assistant-platform` bằng NumPy, pandas và scikit-learn.
- Biết làm sạch dữ liệu, tách train/validation/test và tránh data leakage.
- Huấn luyện baseline Linear Regression và Logistic Regression ở mức nền tảng, có metric rõ ràng.
- Viết PyTorch `Dataset`, `DataLoader`, model neural network nhỏ, training loop và validation loop.
- Lưu model artifact, report evaluation và tích hợp endpoint dự đoán intent đơn giản vào FastAPI.
- Giải thích được tokenization, embedding, self-attention, multi-head attention, positional encoding và vì sao LLM dự đoán token tiếp theo.

## Kiến thức đầu vào

- Đã hoàn thành Month-01 hoặc có project FastAPI tương đương.
- Biết Python type hint, Pydantic schema, service layer, pytest, Ruff và Docker cơ bản.
- Đã có endpoint toy inference, nhưng chưa cần biết training loop.
- Biết đọc CSV/JSON ở mức cơ bản.

Không yêu cầu biết xác suất thống kê sâu, calculus, SVM, XGBoost, NLP nâng cao hay tự code Transformer hoàn chỉnh.

## Kết quả đầu ra

Sau tháng 2, `ai-assistant-platform` cần có:

- `data/raw/`, `data/processed/`, `data/splits/` và fixture nhỏ dùng được trong test.
- Module `src/ai_assistant_platform/services/preprocessing/` hoặc `src/ai_assistant_platform/ml/preprocessing.py` có thể tái sử dụng cho training và API.
- Script tạo dataset sạch, tách train/validation/test có stratify và seed cố định.
- Baseline classification bằng Logistic Regression, report có confusion matrix, precision, recall, F1.
- PyTorch training script cho intent classifier nhỏ, có validation loop và lưu `models/intent_classifier.pt`.
- Endpoint `POST /api/v1/ml/intent` dùng model đã lưu hoặc fallback deterministic khi artifact chưa có.
- Tài liệu `docs/ml-evaluation-report.md` và `docs/transformer-foundation.md`.
- Test cho preprocessing, metric calculation, training smoke test và API contract.

## Kiến trúc trước tháng

Cuối Month-01, project đã có FastAPI service, schema, route, service layer, test, Docker và toy PyTorch inference:

```text
ai-assistant-platform/
├── src/ai_assistant_platform/
│   ├── api/
│   ├── core/
│   ├── domain/
│   ├── services/
│   └── main.py
├── docs/month-02-handoff.md
├── scripts/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

Toy inference ở Month-01 chỉ chứng minh API boundary và PyTorch inference mode, chưa có data pipeline, training hoặc evaluation thật.

## Kiến trúc sau tháng

Cuối Month-02, project nên mở rộng tối thiểu như sau:

```text
ai-assistant-platform/
├── src/ai_assistant_platform/
│   ├── api/
│   │   ├── routes/ml.py
│   │   └── schemas/ml.py
│   ├── ml/
│   │   ├── dataset.py
│   │   ├── intent_model.py
│   │   ├── metrics.py
│   │   └── preprocessing.py
│   └── services/
│       └── intent_service.py
├── data/
│   ├── raw/intent_samples.csv
│   ├── processed/intent_samples_clean.csv
│   └── splits/
├── docs/
│   ├── ml-evaluation-report.md
│   └── transformer-foundation.md
├── models/
│   └── intent_classifier.pt
├── scripts/
│   ├── prepare_intent_data.py
│   ├── train_sklearn_baseline.py
│   ├── train_torch_intent.py
│   └── transformer_shapes.py
└── tests/
    ├── integration/test_ml_intent_api.py
    └── unit/test_preprocessing.py
```

## Milestone từng tuần

| Tuần | Trọng tâm | Đầu ra kiểm tra được |
| --- | --- | --- |
| [Tuần 1](./Week-01.md) | NumPy, pandas, cleaning, split và leakage | Dataset intent sạch, split reproducible, preprocessing module có test |
| [Tuần 2](./Week-02.md) | Supervised learning và classification metrics | Logistic Regression baseline, confusion matrix, F1 report và service baseline |
| [Tuần 3](./Week-03.md) | PyTorch Dataset, DataLoader, neural network và training loop | Intent classifier nhỏ có training/validation loop, model artifact và API endpoint |
| [Tuần 4](./Week-04.md) | Tokenization, embedding, attention và Transformer foundation | Shape demo, tài liệu Transformer bằng lời của người học, handoff sang Month-03 |

## Nhịp học

Mỗi tuần có 7 ngày:

- 5 ngày học và thực hành tính năng nhỏ.
- 1 ngày milestone kiểm tra tích hợp.
- 1 ngày review, refactor, tài liệu hoặc buffer.

Mỗi ngày giới hạn 60-120 phút. Nội dung nâng cao được đưa vào mục tùy chọn, không bắt buộc hoàn thành trong ngày.

## Tài liệu tham khảo

Tài liệu chính thức và nguồn uy tín được gom trong [RESOURCES.md](./RESOURCES.md). Các file tuần chỉ yêu cầu đọc phần cụ thể, tránh đọc tràn lan.

## Definition of Done tháng

- Hoàn thành đủ 28 ngày trong [Week-01.md](./Week-01.md), [Week-02.md](./Week-02.md), [Week-03.md](./Week-03.md) và [Week-04.md](./Week-04.md).
- Không có ngày nào vượt 120 phút bắt buộc.
- Data pipeline tạo được dữ liệu sạch và split chạy lại được.
- Baseline scikit-learn và model PyTorch đều có metric, không chỉ có loss.
- `uv run pytest`, `uv run ruff check .` và các script smoke test cuối tháng pass.
- API `POST /api/v1/ml/intent` có schema, test và fallback rõ ràng.
- `docs/ml-evaluation-report.md` ghi metric, baseline, lỗi quan sát được và giới hạn dữ liệu.
- `docs/transformer-foundation.md` giải thích Transformer bằng lời của người học, không copy dài từ nguồn.
- Không hard-code path tuyệt đối, secret hoặc dữ liệu nhạy cảm.
- Không bắt buộc SVM, KNN, PCA, XGBoost tuning hoặc tự code Transformer production.

## Rủi ro quá tải và cách giảm tải

- **ML cổ điển lan quá rộng:** chỉ học Linear Regression để hiểu prediction/loss và Logistic Regression cho classification baseline.
- **Dữ liệu giả quá lớn:** dùng dataset intent nhỏ 40-80 dòng, đủ có lỗi missing/duplicate/category.
- **Metric bị học như công thức:** gắn trực tiếp vào confusion matrix và lỗi của intent classifier.
- **Training loop quá nặng:** model PyTorch nhỏ, vài epoch, chạy CPU được trong vài phút.
- **Transformer quá sâu:** chỉ học shape, attention intuition và kiến trúc; không tự train LLM.

## Nội dung được phép bỏ qua nếu thiếu thời gian

- Parquet chỉ đọc overview, không bắt buộc thêm dependency.
- ROC-AUC chỉ ở mức khái niệm nếu dataset quá nhỏ.
- Plot visualization của metric.
- Hyperparameter tuning nâng cao.
- Viết tokenizer BPE hoàn chỉnh.
- Dùng Hugging Face model thật trong API.

Không được bỏ qua: cleaning, split, data leakage, Logistic Regression, classification metrics, PyTorch training loop, validation loop, embedding và self-attention foundation.

## Cầu nối sang Month-03

Month-03 sẽ tích hợp LLM API thật, Structured Output, Tool Calling và MCP. Month-02 chuẩn bị cho việc đó bằng cách tạo thói quen: dữ liệu có contract, output có schema, model có evaluation, endpoint có test, tài liệu có giới hạn rõ ràng. Khi bước sang LLM, người học sẽ biết không đánh giá hệ thống chỉ bằng cảm giác “trả lời nghe ổn”.
