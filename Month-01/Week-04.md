# Tháng 1 - Tuần 4: PyTorch Tensor và inference endpoint

## Mục tiêu tuần

Học PyTorch ở mức inference: Tensor, shape, dtype, device, inference mode và một endpoint chấm điểm toy model. Không huấn luyện model trong tháng này.

## Kiến thức cần đạt

- Đọc được shape, dtype và device của Tensor.
- Phân biệt train mode với `eval()`; hiểu vì sao inference dùng `torch.no_grad()`.
- Tách schema, inference service và HTTP route.

## Tính năng project sẽ bổ sung

`POST /api/v1/inference/score` nhận danh sách số, trả score xác định từ PyTorch toy model; Docker demo chạy end-to-end.

## Kế hoạch từng ngày

### Ngày 22 - Tensor, shape và dtype

**Mục tiêu cụ thể:** Tạo Tensor từ dữ liệu request giả lập và quan sát shape/dtype. **Kết quả cần đạt:** Script in đúng `shape`, `dtype`, `device`. **Phân bổ thời gian:** 25 phút đọc, 45 phút thực hành, 20 phút kiểm tra, 10 phút ghi chú. **Nội dung lý thuyết:** scalar, vector, matrix, batch dimension, `float32`. **Tài liệu cần đọc:** PyTorch Tensors trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Cài `torch`, tạo `scripts/tensor_basics.py` với `torch.tensor([[1.0, 2.0]])`. **Thay đổi cần áp dụng vào ai-assistant-platform:** Có script nền cho service ngày 24. **File dự kiến tạo hoặc sửa:** `pyproject.toml`, `uv.lock`, `scripts/tensor_basics.py`. **Lệnh chạy:** `uv run python scripts/tensor_basics.py`. **Kết quả mong đợi:** Shape là `(1, 2)`, dtype là `torch.float32`. **Cách kiểm tra kết quả:** Đổi list một chiều và giải thích shape khác nhau. **Definition of Done:** Không cần GPU để hoàn thành. **Commit message gợi ý:** `feat(torch): add tensor basics exploration`. **Câu hỏi tự kiểm tra:** Vì sao batch dimension hữu ích cho API inference?

### Ngày 23 - Device và inference mode

**Mục tiêu cụ thể:** Chạy một `torch.nn.Linear` ở eval mode không tính gradient. **Kết quả cần đạt:** Output có shape dự đoán và `requires_grad=False`. **Phân bổ thời gian:** 20 phút đọc, 55 phút code, 25 phút kiểm tra. **Nội dung lý thuyết:** CPU/GPU device, `model.eval()` và `torch.no_grad()`. **Tài liệu cần đọc:** PyTorch Quickstart và no_grad trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Tạo model với seed cố định, gọi trong context `no_grad`. **Thay đổi cần áp dụng vào ai-assistant-platform:** Quy ước inference an toàn trước khi tạo endpoint. **File dự kiến tạo hoặc sửa:** `scripts/inference_mode.py`. **Lệnh chạy:** `uv run python scripts/inference_mode.py`. **Kết quả mong đợi:** In device, output shape và `False` cho gradient. **Cách kiểm tra kết quả:** Bỏ `no_grad()` tạm thời để so sánh `requires_grad`. **Definition of Done:** Không tự động tải model hoặc dùng GPU bắt buộc. **Commit message gợi ý:** `feat(torch): demonstrate eval mode inference`. **Câu hỏi tự kiểm tra:** `eval()` tự tắt gradient không?

### Ngày 24 - Inference schema và service

**Mục tiêu cụ thể:** Tạo contract input vector và service chấm điểm. **Kết quả cần đạt:** `InferenceRequest(values)` chỉ nhận 2 số hữu hạn; service trả float. **Phân bổ thời gian:** 20 phút thiết kế, 55 phút code, 25 phút test. **Nội dung lý thuyết:** Validate ở boundary và kiểm tra shape trước model. **Tài liệu cần đọc:** Pydantic Models và PyTorch Tensors trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Tạo `InferenceRequest`, `InferenceResponse`, `InferenceService`; dùng linear layer seed cố định. **Thay đổi cần áp dụng vào ai-assistant-platform:** Model logic không nằm trong FastAPI route. **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/api/schemas/inference.py`, `src/ai_assistant_platform/services/inference_service.py`, `tests/unit/test_inference_service.py`. **Lệnh chạy:** `uv run pytest tests/unit/test_inference_service.py -q`. **Kết quả mong đợi:** Test cùng input trả cùng score; sai độ dài bị từ chối. **Cách kiểm tra kết quả:** Thử `[1, 2, 3]` và giá trị `NaN`. **Definition of Done:** Service gọi `model.eval()` và `torch.no_grad()`. **Commit message gợi ý:** `feat(inference): add deterministic torch scoring service`. **Câu hỏi tự kiểm tra:** Vì sao seed giúp test toy model?

### Ngày 25 - Inference endpoint trong FastAPI

**Mục tiêu cụ thể:** Expose service qua `POST /api/v1/inference/score`. **Kết quả cần đạt:** JSON vector hợp lệ trả score theo `response_model`. **Phân bổ thời gian:** 15 phút đọc, 60 phút code, 25 phút test. **Nội dung lý thuyết:** response model và lỗi 422 trước route. **Tài liệu cần đọc:** FastAPI Response Model trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Tạo route, include vào main, thêm integration test. **Thay đổi cần áp dụng vào ai-assistant-platform:** API có inference capability đầu tiên, chưa phải LLM. **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/api/routes/inference.py`, `src/ai_assistant_platform/main.py`, `tests/integration/test_inference_api.py`. **Lệnh chạy:** `curl -X POST http://127.0.0.1:8000/api/v1/inference/score -H "Content-Type: application/json" -d '{"values":[1.0,2.0]}'`. **Kết quả mong đợi:** HTTP 200 và JSON chứa `score`. **Cách kiểm tra kết quả:** Request sai shape trả 422, không 500. **Definition of Done:** Route không load model mỗi request. **Commit message gợi ý:** `feat(inference): expose torch score endpoint`. **Câu hỏi tự kiểm tra:** Vì sao model phải được giữ trong service lifecycle?

### Ngày 26 - Dataset và DataLoader overview

**Mục tiêu cụ thể:** Hiểu input batching mà không bắt đầu training. **Kết quả cần đạt:** Script duyệt được `DataLoader` từ toy dataset. **Phân bổ thời gian:** 25 phút đọc, 45 phút code, 20 phút kiểm tra, 10 phút ghi chú. **Nội dung lý thuyết:** `Dataset.__getitem__`, `__len__`, batch và shuffle. **Tài liệu cần đọc:** PyTorch Quickstart trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Viết `scripts/dataloader_overview.py` cho ba vector 2 chiều, batch size 2. **Thay đổi cần áp dụng vào ai-assistant-platform:** Ghi chú design cho data processing tháng 2, không thêm endpoint mới. **File dự kiến tạo hoặc sửa:** `scripts/dataloader_overview.py`, `docs/month-02-handoff.md`. **Lệnh chạy:** `uv run python scripts/dataloader_overview.py`. **Kết quả mong đợi:** In hai batch có shape lần lượt `(2, 2)` và `(1, 2)`. **Cách kiểm tra kết quả:** Đổi batch size và giải thích kết quả. **Definition of Done:** Không viết training loop, optimizer hay loss. **Commit message gợi ý:** `docs(torch): add dataloader handoff notes`. **Câu hỏi tự kiểm tra:** Vì sao batch cuối có thể nhỏ hơn batch size?

### Ngày 27 - Milestone: demo Docker end-to-end

**Mục tiêu cụ thể:** Chạy cả chat và inference từ Docker image. **Kết quả cần đạt:** Hai curl request thành công sau `docker compose up --build`. **Phân bổ thời gian:** 15 phút chuẩn bị, 65 phút chạy/sửa, 25 phút ghi README, 15 phút kiểm tra. **Nội dung lý thuyết:** Reproducible runtime và smoke test. **Tài liệu cần đọc:** Docker Compose trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Build lại image, gọi `/health`, chat và inference; ghi command vào README. **Thay đổi cần áp dụng vào ai-assistant-platform:** Milestone tháng 1 có demo chạy lại được. **File dự kiến tạo hoặc sửa:** `README.md`, `docker-compose.yml`, test hoặc Dockerfile khi cần. **Lệnh chạy:** `docker compose up --build`; `curl http://localhost:8000/health`; gọi chat và inference. **Kết quả mong đợi:** Cả ba endpoint trả response đúng schema. **Cách kiểm tra kết quả:** `docker compose down` rồi chạy lại từ image mới. **Definition of Done:** Không cần API key, GPU hay network ngoài để demo. **Commit message gợi ý:** `chore(demo): verify containerized chat and inference APIs`. **Câu hỏi tự kiểm tra:** Smoke test khác integration test ở đâu?

### Ngày 28 - Review, refactor và chuẩn bị tháng 2

**Mục tiêu cụ thể:** Chốt Month 01 và ghi điểm nối sang data/ML foundation. **Kết quả cần đạt:** Test/lint pass, kiến trúc và giới hạn toy model được nêu rõ. **Phân bổ thời gian:** 25 phút review, 35 phút refactor, 25 phút kiểm tra, 15 phút kế hoạch. **Nội dung lý thuyết:** Phân biệt inference demo với model có chất lượng nghiệp vụ. **Tài liệu cần đọc:** Xem lại PyTorch Quickstart trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Xóa code thử, rà type hint, cập nhật README và `docs/month-02-handoff.md`. **Thay đổi cần áp dụng vào ai-assistant-platform:** Có baseline ổn định trước data processing. **File dự kiến tạo hoặc sửa:** `README.md`, `docs/month-02-handoff.md`, test liên quan. **Lệnh chạy:** `uv run ruff check .`; `uv run pytest`; `docker compose up --build`. **Kết quả mong đợi:** Lint/test pass và API chạy trong container. **Cách kiểm tra kết quả:** Đọc README theo vai trò người mới clone project. **Definition of Done:** Không có TODO, secret hoặc tuyên bố toy score là model AI hoàn chỉnh. **Commit message gợi ý:** `docs(month-01): record inference baseline and month two handoff`. **Câu hỏi tự kiểm tra:** Tháng 2 cần data contract nào từ endpoint hiện tại?

## Milestone cuối tuần

Dockerized API trả health, mock chat và deterministic PyTorch score; learner giải thích được giới hạn của toy inference.

## Review checklist

- [ ] `uv run pytest` và `uv run ruff check .` pass.
- [ ] Input sai shape/dtype bị schema từ chối thay vì 500.
- [ ] Inference dùng `eval()` và `no_grad()`.
- [ ] Docker demo không cần API key hoặc GPU.

## Definition of Done

Project có FastAPI, test, Docker và một baseline PyTorch inference đủ nhỏ để hiểu trước khi học Neural Network ở tháng 2.

## Những lỗi thường gặp

- Dùng inference endpoint để bắt đầu training.
- Load model trong mỗi request.
- Nhầm `model.eval()` với việc tắt gradient.
- Gọi toy score là dự đoán đáng tin cậy cho nghiệp vụ.

## Tài liệu tham khảo chính thức

Xem nhóm Tuần 4 trong [RESOURCES.md](./RESOURCES.md).
