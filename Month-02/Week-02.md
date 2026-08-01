# Tháng 2 - Tuần 2: Supervised learning, baseline và classification metrics

## Mục tiêu tuần

Huấn luyện baseline ML cổ điển vừa đủ cho `ai-assistant-platform`: hiểu supervised learning, thử Linear Regression ở mức nền, dùng Logistic Regression cho intent classification, đo confusion matrix, precision, recall, F1 và ghi evaluation report.

## Kiến thức cần đạt

- Phân biệt regression và classification.
- Hiểu baseline model, feature matrix `X`, label `y`, training, prediction và threshold.
- Biết đọc confusion matrix, precision, recall, F1 theo từng intent.
- Biết vì sao accuracy một mình không đủ.
- Biết đóng gói baseline thành service có thể test.

## Module project sẽ bổ sung

`scripts/train_sklearn_baseline.py`, `app/ml/metrics.py`, `app/services/intent_baseline_service.py`, `docs/ml-evaluation-report.md` và test cho metric/report.

## Kế hoạch từng ngày

### Ngày 8 - Supervised learning và Linear Regression ở mức nền

**Mục tiêu cụ thể:** Dùng một ví dụ numeric nhỏ để hiểu model học quan hệ input-output. **Kết quả cần đạt:** Script Linear Regression dự đoán toy latency từ `text_length` và ghi rõ đây không phải model chính của tháng. **Phân bổ thời gian:** 25 phút đọc Linear Models, 40 phút code toy regression, 20 phút so sánh prediction/residual, 10 phút ghi chú. **Lý thuyết:** Feature, target, fit, predict, residual, overfitting ở mức trực giác. **Tài liệu:** scikit-learn Linear Models trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `scripts/linear_regression_overview.py` dùng vài dòng dữ liệu tổng hợp, in coefficient và MAE đơn giản. **Tích hợp project:** Bài này giúp hiểu training API của scikit-learn trước khi làm classification. **File tạo/sửa:** `scripts/linear_regression_overview.py`, `docs/ml-evaluation-report.md`. **Lệnh chạy:** `uv add scikit-learn`; `uv run python scripts/linear_regression_overview.py`. **Kết quả mong đợi:** Script in prediction và cảnh báo không dùng regression để phân loại intent. **Cách kiểm tra:** Thay đổi một feature numeric và quan sát prediction đổi. **Definition of Done:** Không mở rộng sang nhiều thuật toán regression. **Commit message:** `docs(ml): add linear regression overview script`. **Câu hỏi tự kiểm tra:** Regression trả output dạng gì? Classification khác regression ở target như thế nào? Vì sao toy regression không nên đưa vào API?

### Ngày 9 - Logistic Regression baseline cho intent

**Mục tiêu cụ thể:** Huấn luyện Logistic Regression trên feature từ Week-01. **Kết quả cần đạt:** Baseline train được, dự đoán validation và lưu label mapping. **Phân bổ thời gian:** 20 phút đọc LogisticRegression, 50 phút viết training script, 20 phút chạy validation, 10 phút ghi chú. **Lý thuyết:** Logistic Regression là classifier tuyến tính, probability, regularization default. **Tài liệu:** LogisticRegression API và Linear Models trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `scripts/train_sklearn_baseline.py` load splits, fit preprocessor trên train, train model, predict validation. **Tích hợp project:** Baseline này là mốc so sánh cho PyTorch model tuần 3. **File tạo/sửa:** `scripts/train_sklearn_baseline.py`, `app/ml/label_mapping.py`, `models/sklearn_intent_baseline.joblib` nếu dùng joblib. **Lệnh chạy:** `uv run python scripts/train_sklearn_baseline.py`. **Kết quả mong đợi:** Console in validation accuracy và predicted labels. **Cách kiểm tra:** Chạy lại cùng seed cho kết quả giống nhau hoặc sai khác được giải thích. **Definition of Done:** Script không đọc test set trong quá trình chọn model. **Commit message:** `feat(ml): train logistic regression intent baseline`. **Câu hỏi tự kiểm tra:** Vì sao Logistic Regression vẫn hữu ích khi sau này dùng LLM? Regularization mặc định giúp gì? Validation set dùng ở bước nào?

### Ngày 10 - Confusion matrix và lỗi theo class

**Mục tiêu cụ thể:** Đọc lỗi classification bằng confusion matrix. **Kết quả cần đạt:** Report nêu class nào hay bị nhầm với class nào. **Phân bổ thời gian:** 20 phút đọc classification metrics, 40 phút code metric function, 25 phút phân tích lỗi, 10 phút ghi docs. **Lý thuyết:** True positive, false positive, false negative, confusion matrix theo label. **Tài liệu:** scikit-learn Model evaluation classification metrics trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `app/ml/metrics.py` và cập nhật training script xuất confusion matrix validation. **Tích hợp project:** Metric code dùng lại cho PyTorch Week-03. **File tạo/sửa:** `app/ml/metrics.py`, `tests/unit/test_metrics.py`, `docs/ml-evaluation-report.md`. **Lệnh chạy:** `uv run pytest tests/unit/test_metrics.py -q`; `uv run python scripts/train_sklearn_baseline.py`. **Kết quả mong đợi:** Confusion matrix có label order cố định và test pass. **Cách kiểm tra:** Dùng y_true/y_pred toy để tự tính một ô trong matrix. **Definition of Done:** Report không chỉ ghi một số accuracy. **Commit message:** `feat(eval): add classification confusion matrix reporting`. **Câu hỏi tự kiểm tra:** False negative của intent `create_ticket` có rủi ro gì? Vì sao label order phải cố định? Accuracy cao có thể che lỗi nào?

### Ngày 11 - Precision, recall, F1 và threshold thinking

**Mục tiêu cụ thể:** Tính precision/recall/F1 và hiểu trade-off trong assistant intent. **Kết quả cần đạt:** `docs/ml-evaluation-report.md` có bảng metric theo class và macro average. **Phân bổ thời gian:** 25 phút đọc metric, 40 phút cập nhật report, 20 phút diễn giải trade-off, 10 phút ghi commit. **Lý thuyết:** Precision, recall, F1, macro vs weighted average, threshold ở binary/multiclass probability. **Tài liệu:** Classification metrics trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Dùng `classification_report` hoặc hàm tự bọc để xuất JSON/Markdown summary. **Tích hợp project:** Định nghĩa tiêu chí baseline: macro F1 là metric chính cho dataset nhỏ, kèm lỗi quan sát được. **File tạo/sửa:** `app/ml/metrics.py`, `scripts/train_sklearn_baseline.py`, `docs/ml-evaluation-report.md`. **Lệnh chạy:** `uv run python scripts/train_sklearn_baseline.py --write-report`. **Kết quả mong đợi:** Report có macro F1, per-class precision/recall/F1 và nhận xét không quá tự tin. **Cách kiểm tra:** Đảo một prediction đúng thành sai để F1 giảm. **Definition of Done:** Không kết luận chất lượng toàn hệ thống bằng một metric duy nhất. **Commit message:** `docs(eval): record baseline precision recall f1`. **Câu hỏi tự kiểm tra:** Khi nào ưu tiên recall hơn precision? Macro F1 khác weighted F1 thế nào? Vì sao validation metric không phải production monitoring?

### Ngày 12 - Đóng gói baseline service

**Mục tiêu cụ thể:** Tạo service dự đoán intent bằng baseline để API dùng được sau này. **Kết quả cần đạt:** `IntentBaselineService.predict(text)` trả `intent`, `confidence`, `model_version`. **Phân bổ thời gian:** 15 phút thiết kế contract, 50 phút code service, 25 phút test, 10 phút ghi docs. **Lý thuyết:** Service boundary, model artifact, fallback, confidence calibration ở mức cảnh báo. **Tài liệu:** Xem lại LogisticRegression `predict_proba` trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Lưu model/preprocessor bằng joblib hoặc pickle có kiểm soát; service load artifact một lần. **Tích hợp project:** Chuẩn bị cho endpoint ngày 20 ở Week-03, nhưng hôm nay chưa cần route. **File tạo/sửa:** `app/services/intent_baseline_service.py`, `app/api/schemas/ml.py`, `tests/unit/test_intent_baseline_service.py`. **Lệnh chạy:** `uv run pytest tests/unit/test_intent_baseline_service.py -q`. **Kết quả mong đợi:** Test với text mẫu trả schema ổn định, artifact missing được báo lỗi rõ. **Cách kiểm tra:** Đổi path artifact sai và xác nhận exception có thông điệp hữu ích. **Definition of Done:** Không load model trong mỗi lần gọi predict nếu có thể cache ở service. **Commit message:** `feat(intent): wrap sklearn baseline in service`. **Câu hỏi tự kiểm tra:** Confidence từ Logistic Regression có phải xác suất đáng tin tuyệt đối không? Vì sao service cần `model_version`? Artifact missing nên fail thế nào?

### Ngày 13 - Milestone baseline và test set lần đầu

**Mục tiêu cụ thể:** Đánh giá baseline trên test set một lần sau khi đã chốt model. **Kết quả cần đạt:** Report phân biệt validation result và test result. **Phân bổ thời gian:** 15 phút review quyết định model, 45 phút chạy test evaluation, 25 phút cập nhật report, 20 phút kiểm tra command. **Lý thuyết:** Test set chỉ dùng để ước lượng chất lượng cuối sau khi chọn model. **Tài liệu:** Xem lại Model evaluation trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Thêm option `--evaluate-test` vào script, xuất metric test vào report. **Tích hợp project:** Baseline test result là mốc so sánh cho PyTorch Week-03. **File tạo/sửa:** `scripts/train_sklearn_baseline.py`, `docs/ml-evaluation-report.md`, `models/README.md` nếu cần. **Lệnh chạy:** `uv run python scripts/train_sklearn_baseline.py --write-report --evaluate-test`; `uv run pytest`. **Kết quả mong đợi:** Report ghi rõ ngày chạy, data version và test macro F1. **Cách kiểm tra:** Đảm bảo script mặc định không evaluate test nếu không truyền flag. **Definition of Done:** Không quay lại tuning baseline sau khi nhìn test nếu không ghi nhận bias. **Commit message:** `docs(eval): add held-out baseline test result`. **Câu hỏi tự kiểm tra:** Vì sao không nhìn test set mỗi ngày? Nếu test thấp hơn validation nhiều, nguyên nhân có thể là gì? Data version nên ghi gì?

### Ngày 14 - Review tuần 2 và handoff sang PyTorch

**Mục tiêu cụ thể:** Chốt baseline cổ điển và chuẩn bị PyTorch training. **Kết quả cần đạt:** Baseline script, service, metric và report pass review. **Phân bổ thời gian:** 20 phút review code, 30 phút refactor nhỏ, 30 phút chạy test/lint, 20 phút viết handoff. **Lý thuyết:** Baseline là điểm tựa, không phải sản phẩm cuối. **Tài liệu:** Không đọc nguồn mới; xem lại [RESOURCES.md](./RESOURCES.md) nhóm Tuần 2. **Thực hành:** Tạo `docs/week-03-training-plan.md` mô tả input tensor, label mapping và metric cần giữ. **Tích hợp project:** PyTorch model tuần 3 phải so sánh với scikit-learn baseline trong cùng report. **File tạo/sửa:** `docs/week-03-training-plan.md`, `docs/ml-evaluation-report.md`, test liên quan. **Lệnh chạy:** `uv run ruff check .`; `uv run pytest`; `uv run python scripts/train_sklearn_baseline.py --write-report`. **Kết quả mong đợi:** Lint/test pass và report không còn placeholder. **Cách kiểm tra:** Đọc report như người mới: có hiểu model đang tốt/xấu ở đâu không? **Definition of Done:** Week-03 có đủ dữ liệu, metric và baseline để train neural network nhỏ. **Commit message:** `chore(ml): validate sklearn baseline milestone`. **Câu hỏi tự kiểm tra:** Baseline giúp phát hiện lỗi PyTorch như thế nào? Metric nào sẽ giữ nguyên ở Week-03? Điều gì không nên tối ưu khi dataset còn quá nhỏ?

## Milestone cuối tuần

`ai-assistant-platform` có Logistic Regression baseline chạy lại được, metric classification rõ ràng, report validation/test và service wrapper để tích hợp API.

## Review checklist

- [ ] Baseline chỉ fit trên train.
- [ ] Validation dùng để phân tích và test chỉ dùng sau khi chốt.
- [ ] Report có confusion matrix, precision, recall, F1.
- [ ] Service trả schema ổn định và xử lý artifact missing rõ ràng.
- [ ] Không bắt buộc SVM, KNN, PCA hoặc XGBoost.

## Definition of Done

Tuần 2 hoàn thành khi baseline scikit-learn có thể train, evaluate, lưu artifact và được dùng như chuẩn so sánh cho PyTorch training ở tuần 3.

## Lỗi thường gặp

- Chạy test set nhiều lần rồi chọn model theo test.
- Chỉ nhìn accuracy.
- Quên lưu label order khiến confusion matrix khó đọc.
- Dùng confidence như xác suất đã calibration.
- Tối ưu thuật toán cổ điển quá lâu thay vì chuyển sang training loop.

## Tài liệu chính thức

Xem nhóm Tuần 2 trong [RESOURCES.md](./RESOURCES.md).

## Tùy chọn nếu còn thời gian

- Thêm JSON output cho evaluation report.
- Thử class weight nếu class imbalance rõ.
- Vẽ confusion matrix bằng matplotlib, nhưng không bắt buộc.
