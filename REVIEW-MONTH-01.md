# Review Month 01

## Status

PASS_WITH_NOTES

## Scope

Review riêng Month-01 sau khi hoàn thiện README tháng, Week-01 đến Week-04, tài liệu tham khảo và báo cáo tự review theo `VALIDATION.md`.

## Files reviewed

- `Month-01/README.md`
- `Month-01/Week-01.md`
- `Month-01/Week-02.md`
- `Month-01/Week-03.md`
- `Month-01/Week-04.md`
- `Month-01/RESOURCES.md`
- `REVIEW-MONTH-01.md`

## Deliverables verified

- Month-01 có README tháng, 4 tuần chính và tài liệu tham khảo riêng.
- Mỗi tuần có 7 ngày học hoặc review/milestone, tổng cộng 28 ngày.
- Mỗi ngày có mục tiêu, kết quả cần đạt, phân bổ thời gian, lý thuyết, tài liệu, bài thực hành, thay đổi project, file tạo/sửa, lệnh chạy, kết quả mong đợi, cách kiểm tra, Definition of Done, commit message và câu hỏi tự kiểm tra.
- Tất cả bài tập đều phát triển `ai-assistant-platform`.
- Project progression liên tục: `uv` skeleton -> Python service -> FastAPI -> config/error handling -> async/HTTPX -> Docker -> PyTorch inference.
- Không chỉnh sửa Month-02 đến Month-06.

## Validation summary

### Repository structure

PASS_WITH_NOTES

Month-01 có `README.md`, `Week-01.md` đến `Week-04.md` và `RESOURCES.md`. Báo cáo review được ghi vào `REVIEW-MONTH-01.md` theo yêu cầu trực tiếp của người dùng. `ROADMAP_SPEC.md` mong đợi thêm `Month-01/REVIEW.md`; chưa tạo file đó để tránh lệch tên file review mà người dùng đã chỉ định.

### Daily completeness

PASS

Toàn bộ 28 ngày có đủ các mục bắt buộc theo `VALIDATION.md`. Nội dung từng ngày có trọng tâm riêng, không chỉ là template chung.

### Time budget

PASS

Các ngày được thiết kế trong khoảng 60-120 phút. Ngày milestone không vượt 120 phút. Các nội dung dễ quá tải như Docker nâng cao, GPU, training loop và nhiều service hạ tầng đã được loại khỏi Month-01.

### Technical sequence

PASS

Thứ tự kiến thức hợp lý:

1. `uv`, Python module, type hint và service thuần.
2. Dataclass, exception, logging, fixture và unit test.
3. FastAPI, Pydantic, router, config, dependency injection và error handling.
4. Async endpoint, HTTPX timeout, middleware, Docker và integration test.
5. PyTorch Tensor, inference mode, inference service và API endpoint.

Không dùng LangGraph, RAG, Qdrant, OpenAI API, PostgreSQL hoặc Redis trong Month-01.

### Project progression

PASS

Mỗi tuần có thay đổi project kiểm tra được:

- Week 1: skeleton, chat service, domain object, fixture, unit test và Ruff.
- Week 2: FastAPI health/chat endpoint, schema, config, dependency và error contract.
- Week 3: async status endpoint, HTTPX client, request ID middleware, Docker và integration test.
- Week 4: PyTorch scripts, deterministic scoring service, inference API và Docker smoke test.

### Internal links

PASS

Các link nội bộ của Month-01 trỏ đúng tới:

- `./Week-01.md`
- `./Week-02.md`
- `./Week-03.md`
- `./Week-04.md`
- `./RESOURCES.md`

Không phát hiện link nội bộ hỏng trong các file Month-01.

### References

PASS_WITH_NOTES

`Month-01/RESOURCES.md` ưu tiên nguồn chính thức: Python, uv, pytest, Ruff, FastAPI, Pydantic, HTTPX, Docker và PyTorch. Đã thử kiểm tra URL bằng `Invoke-WebRequest` và `curl.exe -I -L`, nhưng môi trường terminal trả lỗi TLS/connection đồng loạt cho tất cả URL. Vì vậy trạng thái để `PASS_WITH_NOTES`: danh sách nguồn là official docs, nhưng external URL cần được click kiểm tra lại trước khi xuất bản public.

### Security

PASS

Month-01 nhắc đúng thời điểm:

- Không commit `.env`.
- Dùng `.env.example`.
- Không hard-code secret.
- Không log raw request body hoặc secret.
- Dockerfile và `.dockerignore` tránh copy `.env`, `.venv`, `.git`.
- HTTPX client có timeout.

### Evaluation

NOT_APPLICABLE

LLM/RAG evaluation chưa bắt buộc ở Month-01. Tháng này đã đặt nền bằng unit test, integration test và smoke test để chuẩn bị cho prompt/RAG/agent evaluation ở các tháng sau.

## Issues found

- README tháng cũ chưa nêu đủ kiến thức đầu vào, kiến trúc trước/sau, rủi ro quá tải và nội dung được phép bỏ qua theo `ROADMAP_SPEC.md`.
- Week files đã chi tiết nhưng cần được kiểm tra lại về liên kết nội bộ và tính liên tục.
- Workspace không phải Git repository, nên không thể dùng `git status` để xác nhận diff.
- Các file spec như `ROADMAP_SPEC.md`, `VALIDATION.md` và `IMPLEMENTATION_PLAN.md` hiển thị lỗi encoding trong terminal PowerShell, dù nội dung chính vẫn đọc được.
- Không xác minh được external URL bằng terminal do lỗi TLS/connection đồng loạt.

## Issues fixed

- Hoàn thiện `Month-01/README.md` theo cấu trúc tháng trong `ROADMAP_SPEC.md`.
- Xác nhận 4 tuần Month-01 có đủ 28 ngày, mỗi ngày có đầu ra cụ thể và command kiểm tra.
- Xác nhận tất cả bài tập Month-01 đều phát triển `ai-assistant-platform`.
- Kiểm tra internal links trong Month-01.
- Cập nhật `REVIEW-MONTH-01.md` theo format review trong `VALIDATION.md`.

## Open issues

- Chưa tạo code thật cho `ai-assistant-platform`; Month-01 hiện là giáo trình hướng dẫn người học tự xây project.
- Chưa tạo `Month-01/REVIEW.md` vì yêu cầu trực tiếp chỉ định ghi review vào `REVIEW-MONTH-01.md`.
- Chưa sửa encoding hiển thị của các file đặc tả nền vì đó là thay đổi ngoài phạm vi Month-01.
- Chưa chỉnh README root để link chi tiết tới Month-01 vì yêu cầu hiện tại tập trung riêng Month-01.
- External URL trong `Month-01/RESOURCES.md` cần được kiểm tra bằng trình duyệt hoặc môi trường mạng khác trước khi publish.

## Recommendation for next month

Khi triển khai Month-02, bắt đầu từ trạng thái cuối Month-01: project đã có FastAPI service, schema, config, logging, test, Docker và toy inference endpoint. Month-02 nên thêm data processing, classification metrics, PyTorch training loop và Transformer foundation mà không thay đổi stack chính.
