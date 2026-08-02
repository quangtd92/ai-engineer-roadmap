# Tháng 1 - Tuần 1: Python backend foundation và `uv`

## Mục tiêu tuần

Khởi tạo `ai-assistant-platform` bằng `uv` và tạo mock chat service có typing, dataclass, logging, JSON fixture cùng unit test.

## Kiến thức cần đạt

- Phân biệt `uv run`, dependency trong `pyproject.toml` và virtual environment.
- Dùng type hint, `dataclass`, exception riêng, `pathlib` và `logging` trong Python backend.
- Viết pytest cho hành vi thành công và input không hợp lệ.

## Tính năng project sẽ bổ sung

`services/chat_service.py` trả mock reply; đây là logic sẽ được bọc thành FastAPI endpoint ở tuần 2.

## Kế hoạch từng ngày

### Ngày 1 - Khởi tạo project với `uv`

- **Mục tiêu cụ thể:** Tạo Python app có entry point tối thiểu.
- **Kết quả cần đạt:** Có `pyproject.toml`, `.python-version`, `src/ai_assistant_platform/main.py` và README project.
- **Phân bổ thời gian:** 15 phút đọc, 45 phút khởi tạo, 20 phút chạy thử, 10 phút ghi chú.
- **Nội dung lý thuyết:** `uv init`, lockfile và khác biệt giữa `uv run` với gọi Python hệ thống.
- **Tài liệu cần đọc:** uv: “Working on projects” trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Tạo hàm `main()` in tên service.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Khởi tạo project bằng `uv`.
- **File dự kiến tạo hoặc sửa:** `pyproject.toml`, `.python-version`, `README.md`, `src/ai_assistant_platform/main.py`.
- **Lệnh chạy:** `uv init ai-assistant-platform --app`; `uv run python -m ai_assistant_platform.main`.
- **Kết quả mong đợi:** Terminal in `ai-assistant-platform ready`.
- **Cách kiểm tra kết quả:** Mở `pyproject.toml`, xác nhận project name và Python version.
- **Definition of Done:** Lệnh chạy lại được từ thư mục project mà không kích hoạt virtualenv thủ công.
- **Commit message gợi ý:** `chore(project): initialize ai assistant platform with uv`
- **Câu hỏi tự kiểm tra:** Vì sao không nên dùng `pip install` ngoài môi trường project?

### Ngày 2 - Type hint cho chat service

- **Mục tiêu cụ thể:** Viết hàm `build_mock_reply(message: str) -> str`.
- **Kết quả cần đạt:** Input chuỗi hợp lệ tạo reply có nội dung ổn định.
- **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 20 phút chạy thử, 10 phút ghi chú.
- **Nội dung lý thuyết:** Parameter type, return type, docstring và ranh giới giữa type hint với validation runtime.
- **Tài liệu cần đọc:** Python: “Defining Functions” trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Thêm `src/ai_assistant_platform/services/chat_service.py`, cắt khoảng trắng đầu/cuối trước khi tạo reply.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Có service thuần Python chưa phụ thuộc FastAPI.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/services/__init__.py`, `src/ai_assistant_platform/services/chat_service.py`, `src/ai_assistant_platform/main.py`.
- **Lệnh chạy:** `uv run python -c "from ai_assistant_platform.services.chat_service import build_mock_reply; print(build_mock_reply('Xin chào'))"`.
- **Kết quả mong đợi:** In một mock reply chứa `Xin chào`.
- **Cách kiểm tra kết quả:** Thử input có khoảng trắng và xác nhận reply không giữ khoảng trắng thừa.
- **Definition of Done:** Hàm có type hint, docstring và không đọc input từ `input()`.
- **Commit message gợi ý:** `feat(chat): add typed mock reply service`
- **Câu hỏi tự kiểm tra:** Type hint có tự chặn `None` khi chạy Python không?

### Ngày 3 - Dataclass cho message nội bộ

- **Mục tiêu cụ thể:** Mô hình hóa message nội bộ bằng `@dataclass(frozen=True)`.
- **Kết quả cần đạt:** `ChatMessage(role, content)` có thể tạo và không bị sửa sau khi khởi tạo.
- **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 20 phút thử nghiệm, 10 phút ghi chú.
- **Nội dung lý thuyết:** Khi dùng dataclass cho domain object và khi để Pydantic xử lý biên API.
- **Tài liệu cần đọc:** Python: `dataclasses` trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Thêm `src/ai_assistant_platform/domain/chat.py`; đổi service nhận `ChatMessage`.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Tách domain object khỏi service logic.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/domain/__init__.py`, `src/ai_assistant_platform/domain/chat.py`, `src/ai_assistant_platform/services/chat_service.py`.
- **Lệnh chạy:** `uv run python -c "from ai_assistant_platform.domain.chat import ChatMessage; print(ChatMessage('user', 'Xin chào'))"`.
- **Kết quả mong đợi:** In biểu diễn `ChatMessage` với role và content.
- **Cách kiểm tra kết quả:** Thử gán lại `message.content`; Python phải báo lỗi do `frozen=True`.
- **Definition of Done:** Service vẫn trả reply với instance `ChatMessage`.
- **Commit message gợi ý:** `feat(chat): add immutable chat message domain model`
- **Câu hỏi tự kiểm tra:** Vì sao không dùng Pydantic model này trước khi có HTTP boundary?

### Ngày 4 - Logging và exception có chủ đích

- **Mục tiêu cụ thể:** Từ chối message rỗng bằng exception riêng và log sự kiện an toàn.
- **Kết quả cần đạt:** `InvalidMessageError` được raise; log không ghi secret hay toàn bộ payload.
- **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 20 phút thử lỗi, 10 phút ghi chú.
- **Nội dung lý thuyết:** Log level, exception domain và thông tin nào không nên log.
- **Tài liệu cần đọc:** Python Logging HOWTO trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Thêm `src/ai_assistant_platform/core/errors.py`, `src/ai_assistant_platform/core/logging.py`; log độ dài message thay vì nội dung.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Chat service có validation nhỏ trước khi xử lý.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/core/errors.py`, `src/ai_assistant_platform/core/logging.py`, `src/ai_assistant_platform/services/chat_service.py`.
- **Lệnh chạy:** `uv run python -c "from ai_assistant_platform.services.chat_service import build_mock_reply; build_mock_reply('   ')"`.
- **Kết quả mong đợi:** Process báo `InvalidMessageError`, không in stack trace secret.
- **Cách kiểm tra kết quả:** Chạy input hợp lệ và rỗng; kiểm tra log có level phù hợp.
- **Definition of Done:** Không dùng `ValueError` chung chung cho message rỗng.
- **Commit message gợi ý:** `feat(chat): validate empty messages with domain error`
- **Câu hỏi tự kiểm tra:** Khi nào log `warning` phù hợp hơn `error`?

### Ngày 5 - JSON fixture với `pathlib`

- **Mục tiêu cụ thể:** Đọc danh sách message mẫu từ JSON có đường dẫn ổn định.
- **Kết quả cần đạt:** Service load được fixture độc lập với working directory.
- **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 20 phút kiểm tra, 10 phút ghi chú.
- **Nội dung lý thuyết:** `Path(__file__)`, encoding UTF-8 và lỗi parse JSON.
- **Tài liệu cần đọc:** Python `pathlib` và `json` trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Tạo `tests/fixtures/chat_messages.json` và hàm `load_messages()`.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Có dữ liệu mẫu tái sử dụng cho test ngày 6.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/services/fixture_loader.py`, `tests/fixtures/chat_messages.json`.
- **Lệnh chạy:** `uv run python -c "from ai_assistant_platform.services.fixture_loader import load_messages; print(len(load_messages()))"`.
- **Kết quả mong đợi:** In số message đúng bằng nội dung fixture.
- **Cách kiểm tra kết quả:** Chạy lệnh từ thư mục project và từ `tests/`; kết quả giống nhau.
- **Definition of Done:** File mở rõ `encoding='utf-8'` và lỗi JSON được nêu tên file.
- **Commit message gợi ý:** `test(fixtures): add chat message json fixture`
- **Câu hỏi tự kiểm tra:** Vì sao không ghép path bằng chuỗi `../`?

### Ngày 6 - Milestone: unit test đầu tiên

- **Mục tiêu cụ thể:** Test hành vi chat service thay vì chỉ chạy thủ công.
- **Kết quả cần đạt:** Có test cho reply hợp lệ, trim khoảng trắng và exception message rỗng.
- **Phân bổ thời gian:** 15 phút đọc, 70 phút viết test, 20 phút sửa lỗi, 15 phút ghi chú.
- **Nội dung lý thuyết:** Arrange-Act-Assert và test độc lập.
- **Tài liệu cần đọc:** pytest “Getting Started” trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Cài `pytest` bằng `uv add --dev pytest`, tạo `tests/unit/test_chat_service.py`.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Milestone service được bảo vệ bởi unit test.
- **File dự kiến tạo hoặc sửa:** `pyproject.toml`, `uv.lock`, `tests/unit/test_chat_service.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_chat_service.py -q`.
- **Kết quả mong đợi:** Ba test `passed`.
- **Cách kiểm tra kết quả:** Cố ý bỏ validation rỗng; test tương ứng phải fail rồi khôi phục code.
- **Definition of Done:** Test không phụ thuộc network, thời gian chạy dưới vài giây.
- **Commit message gợi ý:** `test(chat): cover mock reply service behavior`
- **Câu hỏi tự kiểm tra:** Vì sao test không nên kiểm tra log text nguyên văn?

### Ngày 7 - Review và refactor nhẹ

- **Mục tiêu cụ thể:** Dọn cấu trúc tuần 1 và thêm lint trước tuần FastAPI.
- **Kết quả cần đạt:** Test và Ruff cùng chạy; import, tên hàm, docstring nhất quán.
- **Phân bổ thời gian:** 20 phút review, 40 phút refactor, 20 phút lint, 20 phút ghi README hoặc nghỉ bù.
- **Nội dung lý thuyết:** Refactor không đổi hành vi và linter khác unit test.
- **Tài liệu cần đọc:** Ruff Tutorial trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** `uv add --dev ruff`; thêm cấu hình Ruff tối thiểu trong `pyproject.toml`.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Có quality gate local cho code Python hiện tại.
- **File dự kiến tạo hoặc sửa:** `pyproject.toml`, `src/ai_assistant_platform/services/chat_service.py`, `tests/unit/test_chat_service.py`, `README.md`.
- **Lệnh chạy:** `uv run ruff check .`; `uv run pytest`.
- **Kết quả mong đợi:** Ruff không báo lỗi; tất cả test pass.
- **Cách kiểm tra kết quả:** Xem diff, xác nhận không thêm FastAPI hay feature ngoài phạm vi tuần 1.
- **Definition of Done:** README nêu được lệnh test và lint.
- **Commit message gợi ý:** `chore(quality): add ruff and review week one`
- **Câu hỏi tự kiểm tra:** Refactor nào nên để lại sang tuần 2?

## Milestone cuối tuần

Mock chat service nhận `ChatMessage`, từ chối content rỗng, đọc fixture JSON và có unit test chạy qua `uv`.

## Review checklist

- [ ] `uv run pytest` pass.
- [ ] `uv run ruff check .` pass.
- [ ] Không có secret trong fixture hoặc log.
- [ ] Service không import FastAPI trước tuần 2.

## Definition of Done

Người học có một Python service nhỏ, testable và hiểu mỗi module tồn tại để làm gì.

## Những lỗi thường gặp

- Cài package bằng `pip` ngoài project khiến dependency không vào lockfile.
- Dùng `print()` thay logging cho mọi lỗi.
- Ghi đường dẫn fixture tương đối với thư mục đang chạy.

## Tài liệu tham khảo chính thức

Xem nhóm Tuần 1 trong [RESOURCES.md](./RESOURCES.md).
