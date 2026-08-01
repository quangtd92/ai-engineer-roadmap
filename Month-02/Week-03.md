# Tháng 2 - Tuần 3: PyTorch Dataset, Neural Network và training loop

## Mục tiêu tuần

Chuyển bài toán intent classification từ baseline scikit-learn sang PyTorch: tạo `Dataset`, `DataLoader`, model neural network nhỏ, training loop, validation loop, lưu model artifact và tích hợp endpoint dự đoán.

## Kiến thức cần đạt

- Viết custom `Dataset` từ feature matrix và label.
- Dùng `DataLoader` với batch, shuffle và validation không shuffle.
- Hiểu `nn.Module`, activation, loss, optimizer, gradient và `model.train()`/`model.eval()`.
- Viết training loop và validation loop có metric, không chỉ in loss.
- Lưu/load model state dict và dùng inference mode trong API.

## Module project sẽ bổ sung

`app/ml/dataset.py`, `app/ml/intent_model.py`, `scripts/train_torch_intent.py`, `app/services/intent_service.py`, `app/api/routes/ml.py`, `models/intent_classifier.pt` và integration test cho endpoint intent.

## Kế hoạch từng ngày

### Ngày 15 - Custom Dataset cho intent features

**Mục tiêu cụ thể:** Tạo PyTorch `Dataset` đọc feature/label từ split đã chuẩn bị. **Kết quả cần đạt:** Dataset trả `(features, label)` với dtype đúng và shape ổn định. **Phân bổ thời gian:** 25 phút đọc Dataset/DataLoader, 45 phút code dataset, 20 phút test shape/dtype, 10 phút ghi chú. **Lý thuyết:** `__len__`, `__getitem__`, tensor dtype cho feature và class label. **Tài liệu:** PyTorch Datasets and DataLoaders trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Viết `IntentDataset` nhận DataFrame, preprocessor đã fit và label mapping. **Tích hợp project:** Dùng lại preprocessing Week-01, không tạo pipeline riêng cho PyTorch. **File tạo/sửa:** `app/ml/dataset.py`, `tests/unit/test_intent_dataset.py`. **Lệnh chạy:** `uv run pytest tests/unit/test_intent_dataset.py -q`. **Kết quả mong đợi:** Feature tensor là `torch.float32`, label tensor là `torch.long`. **Cách kiểm tra:** Test `len(dataset)` bằng số dòng train và sample đầu tiên có đúng dimension. **Definition of Done:** Dataset không tự fit preprocessor bên trong `__getitem__`. **Commit message:** `feat(torch): add intent dataset wrapper`. **Câu hỏi tự kiểm tra:** Vì sao label cho CrossEntropyLoss thường là `long`? `__getitem__` có nên đọc file mỗi lần không? Batch dimension xuất hiện ở đâu?

### Ngày 16 - DataLoader và batch sanity check

**Mục tiêu cụ thể:** Tạo DataLoader train/validation và kiểm tra batch trước khi train. **Kết quả cần đạt:** Script in batch shape, label distribution trong batch và số batch. **Phân bổ thời gian:** 20 phút đọc DataLoader, 40 phút code loader factory, 25 phút sanity checks, 10 phút ghi chú. **Lý thuyết:** Batch size, shuffle, deterministic seed, last batch. **Tài liệu:** PyTorch Datasets and DataLoaders trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `create_intent_dataloaders()` và `scripts/check_intent_dataloader.py`. **Tích hợp project:** Training script ngày 18 dùng lại loader factory. **File tạo/sửa:** `app/ml/dataset.py`, `scripts/check_intent_dataloader.py`, `tests/unit/test_intent_dataloader.py`. **Lệnh chạy:** `uv run python scripts/check_intent_dataloader.py`; `uv run pytest tests/unit/test_intent_dataloader.py -q`. **Kết quả mong đợi:** Train loader shuffle, validation loader không shuffle, feature batch shape `(batch_size, n_features)`. **Cách kiểm tra:** Chạy hai lần với seed cố định và xác nhận behavior được giải thích. **Definition of Done:** Không train model khi batch sanity chưa rõ. **Commit message:** `feat(torch): add intent dataloader checks`. **Câu hỏi tự kiểm tra:** Vì sao validation không cần shuffle? Batch cuối có thể nhỏ hơn batch size không? Dataloader có giải quyết class imbalance không?

### Ngày 17 - Neural network nhỏ và forward pass

**Mục tiêu cụ thể:** Tạo `nn.Module` đủ nhỏ để học intent baseline. **Kết quả cần đạt:** Forward pass nhận batch feature và trả logits shape `(batch_size, num_classes)`. **Phân bổ thời gian:** 25 phút đọc Build Model, 45 phút code model, 20 phút unit test, 10 phút ghi notes. **Lý thuyết:** Linear layer, ReLU, logits, softmax chỉ dùng khi diễn giải probability. **Tài liệu:** PyTorch Build the Neural Network trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Viết `IntentClassifier(input_dim, hidden_dim, num_classes)` và test output shape. **Tích hợp project:** Model nhỏ thay thế toy inference Month-01 bằng classifier có training. **File tạo/sửa:** `app/ml/intent_model.py`, `tests/unit/test_intent_model.py`. **Lệnh chạy:** `uv run pytest tests/unit/test_intent_model.py -q`. **Kết quả mong đợi:** Output không NaN, shape đúng, số class khớp label mapping. **Cách kiểm tra:** Đưa input_dim sai để test fail rõ ràng. **Definition of Done:** Không thêm kiến trúc sâu, dropout phức tạp hoặc tuning dài. **Commit message:** `feat(torch): add compact intent classifier`. **Câu hỏi tự kiểm tra:** Logits khác probability thế nào? Vì sao output dimension bằng số class? Activation dùng ở hidden layer để làm gì?

### Ngày 18 - Loss, optimizer và một training step

**Mục tiêu cụ thể:** Chạy một batch training step đúng thứ tự. **Kết quả cần đạt:** Script thực hiện `zero_grad`, forward, loss, backward, optimizer step và loss là số hữu hạn. **Phân bổ thời gian:** 25 phút đọc Autograd/Optimization, 45 phút code training step, 20 phút test smoke, 10 phút ghi chú. **Lý thuyết:** Autograd, gradient accumulation, CrossEntropyLoss, optimizer. **Tài liệu:** PyTorch Automatic Differentiation và Optimizing Model Parameters trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `train_one_epoch()` bản đầu, log loss trung bình. **Tích hợp project:** Training logic tách khỏi script để test được. **File tạo/sửa:** `app/ml/training.py`, `scripts/train_torch_intent.py`, `tests/unit/test_training_step.py`. **Lệnh chạy:** `uv run pytest tests/unit/test_training_step.py -q`; `uv run python scripts/train_torch_intent.py --epochs 1`. **Kết quả mong đợi:** Một epoch chạy xong trên CPU, loss không NaN. **Cách kiểm tra:** Bỏ `optimizer.zero_grad()` tạm thời và giải thích gradient accumulation. **Definition of Done:** Không cần loss giảm mạnh trong một epoch trên dataset nhỏ. **Commit message:** `feat(torch): implement one epoch training step`. **Câu hỏi tự kiểm tra:** Vì sao phải gọi `zero_grad()`? CrossEntropyLoss kỳ vọng input/target gì? `loss.backward()` làm gì?

### Ngày 19 - Validation loop và metric so sánh baseline

**Mục tiêu cụ thể:** Thêm validation loop dùng `model.eval()` và `torch.no_grad()`. **Kết quả cần đạt:** Sau mỗi epoch in train loss, validation loss, macro F1 và so sánh với baseline Week-02. **Phân bổ thời gian:** 20 phút đọc optimization loop, 50 phút code validation, 25 phút cập nhật report, 10 phút ghi chú. **Lý thuyết:** Train mode vs eval mode, no_grad, early stopping ở mức khái niệm. **Tài liệu:** PyTorch Optimizing Model Parameters trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Viết `evaluate_model()` trả predictions, loss và metrics; cập nhật `docs/ml-evaluation-report.md`. **Tích hợp project:** Dùng chung `app/ml/metrics.py` với baseline để so sánh công bằng. **File tạo/sửa:** `app/ml/training.py`, `scripts/train_torch_intent.py`, `docs/ml-evaluation-report.md`, `tests/unit/test_training_eval.py`. **Lệnh chạy:** `uv run python scripts/train_torch_intent.py --epochs 5`; `uv run pytest tests/unit/test_training_eval.py -q`. **Kết quả mong đợi:** Report có bảng baseline vs PyTorch validation metric. **Cách kiểm tra:** Đảm bảo validation không gọi `optimizer.step()`. **Definition of Done:** Metric được ghi cùng data version và seed. **Commit message:** `feat(eval): add torch validation metrics`. **Câu hỏi tự kiểm tra:** `eval()` và `no_grad()` khác nhau thế nào? Vì sao so sánh phải dùng cùng split? Nếu PyTorch tệ hơn baseline thì có sao không?

### Ngày 20 - Lưu model artifact và intent API endpoint

**Mục tiêu cụ thể:** Lưu PyTorch model và expose endpoint dự đoán intent. **Kết quả cần đạt:** `POST /api/v1/ml/intent` nhận text, trả intent/confidence/source model. **Phân bổ thời gian:** 20 phút thiết kế schema, 45 phút service/route, 30 phút integration test, 15 phút manual curl. **Lý thuyết:** State dict, model metadata, inference mode, API fallback khi artifact chưa có. **Tài liệu:** PyTorch Quickstart phần Save/Load trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Cập nhật training script lưu `models/intent_classifier.pt` và `models/intent_metadata.json`; tạo `IntentService`. **Tích hợp project:** API có ML capability thực sự đầu tiên dựa trên model được train. **File tạo/sửa:** `app/services/intent_service.py`, `app/api/routes/ml.py`, `app/api/schemas/ml.py`, `app/main.py`, `tests/integration/test_ml_intent_api.py`, `models/intent_metadata.json`. **Lệnh chạy:** `uv run python scripts/train_torch_intent.py --epochs 5 --save-model`; `uv run pytest tests/integration/test_ml_intent_api.py -q`; `curl -X POST http://127.0.0.1:8000/api/v1/ml/intent -H "Content-Type: application/json" -d "{\"text\":\"please summarize this\"}"`. **Kết quả mong đợi:** HTTP 200 và response có `intent`, `confidence`, `model_version`. **Cách kiểm tra:** Xóa artifact trong môi trường test và xác nhận fallback/error contract đúng. **Definition of Done:** Route không train model trong request. **Commit message:** `feat(intent): expose torch intent prediction api`. **Câu hỏi tự kiểm tra:** Vì sao training không được chạy trong API request? Metadata model cần lưu gì? Confidence nên hiển thị với cảnh báo nào?

### Ngày 21 - Review tuần 3 và Docker smoke test

**Mục tiêu cụ thể:** Chạy lại training, test, API và Docker để chốt PyTorch milestone. **Kết quả cần đạt:** Endpoint intent chạy được trong local hoặc container, docs nêu giới hạn model. **Phân bổ thời gian:** 20 phút review checklist, 35 phút sửa lỗi nhỏ, 35 phút test/lint, 25 phút Docker smoke test. **Lý thuyết:** Reproducible training vs reproducible serving. **Tài liệu:** Không đọc nguồn mới; xem lại nhóm Tuần 3 trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Cập nhật README project với lệnh train và predict; chạy Docker nếu project đã có Dockerfile từ Month-01. **Tích hợp project:** ML endpoint trở thành một phần của `ai-assistant-platform`, không phải script rời. **File tạo/sửa:** `README.md`, `docs/ml-evaluation-report.md`, Docker config nếu cần copy model artifact. **Lệnh chạy:** `uv run ruff check .`; `uv run pytest`; `docker compose up --build`; curl endpoint health và intent. **Kết quả mong đợi:** Lint/test pass, Docker API trả health và intent prediction. **Cách kiểm tra:** Clone-clean mental check: README có đủ lệnh tái tạo artifact chưa? **Definition of Done:** Không tuyên bố model tốt nếu dataset còn nhỏ; report nêu giới hạn. **Commit message:** `chore(torch): validate intent classifier milestone`. **Câu hỏi tự kiểm tra:** Model artifact có nên commit không trong project thật? Docker image cần biết path model thế nào? Giới hạn lớn nhất của classifier hiện tại là gì?

## Milestone cuối tuần

`ai-assistant-platform` có PyTorch intent classifier nhỏ, training/validation loop, model artifact, evaluation report và endpoint dự đoán intent có test.

## Review checklist

- [ ] Dataset/DataLoader dùng lại split Week-01.
- [ ] Training loop có `zero_grad`, `backward`, `step`.
- [ ] Validation loop dùng `eval()` và `no_grad()`.
- [ ] Metric so sánh với baseline Week-02.
- [ ] API không train model trong request.
- [ ] Docker smoke test không cần GPU.

## Definition of Done

Tuần 3 hoàn thành khi người học có thể train một neural network nhỏ, đánh giá nó bằng cùng metric baseline và gọi được endpoint intent trong FastAPI.

## Lỗi thường gặp

- Fit preprocessor lại trong Dataset.
- Dùng `softmax` trước `CrossEntropyLoss`.
- Quên `model.eval()` khi validation/inference.
- So sánh model bằng loss nhưng không có F1.
- Thêm model quá lớn khiến ngày học vượt 2 giờ.

## Tài liệu chính thức

Xem nhóm Tuần 3 trong [RESOURCES.md](./RESOURCES.md).

## Tùy chọn nếu còn thời gian

- Thêm early stopping đơn giản theo validation macro F1.
- Lưu training history JSON.
- Thử hidden size khác nhưng không tuning quá 30 phút.
