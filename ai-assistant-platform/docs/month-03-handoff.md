# Month 03 Handoff & Technical Baseline

Tài liệu này tổng kết toàn bộ kết quả kỹ thuật đạt được sau **Month 02** (Data Processing, ML Foundation, PyTorch Training và Transformer Foundation) và xác định hợp đồng kỹ thuật (contracts), baseline cùng các điểm chuyển giao cho **Month 03** (LLM Engineering, Structured Output, Tool Calling và MCP).

---

## 1. Tổng kết Nền tảng Kỹ thuật Month 02 (Baseline Architecture)

Trong Month 02, dự án `ai-assistant-platform` đã mở rộng từ khung backend ban đầu thành một nền tảng tích hợp Machine Learning và Deep Learning hoàn chỉnh:

1. **Data Processing Pipeline**:
   - Quy trình làm sạch dữ liệu tái sử dụng được: `src/ai_assistant_platform/ml/preprocessing.py`.
   - Phân chia tập dữ liệu chuẩn mực (Train / Validation / Test sets) có stratify và seed cố định trong `data/splits/`, triệt tiêu hoàn toàn rủi ro rò rỉ dữ liệu (data leakage).
2. **Scikit-learn Classical ML Baseline**:
   - Mô hình Logistic Regression baseline đánh giá hiệu năng bài toán phân loại ý định qua Confusion Matrix, Precision, Recall, Macro-F1.
   - Báo cáo đánh giá chi tiết được lưu trữ tại `docs/ml-evaluation-report.md`.
3. **PyTorch Deep Learning & Intent Classifier**:
   - Cài đặt đầy đủ `Dataset`, `DataLoader`, mô hình nơ-ron phân loại đa lớp `IntentClassifierMLP`.
   - Chu trình huấn luyện (training loop) và đánh giá (validation loop) hoàn chỉnh, lưu trữ artifact tại `models/intent_classifier.pt`.
   - Tích hợp endpoint API `POST /api/v1/ml/intent` trong FastAPI với fallback deterministic an toàn khi chưa có trọng số model.
4. **Transformer & Deep Learning Foundations**:
   - Hệ thống script thực nghiệm trực quan:
     - [tokenization_overview.py](../scripts/tokenization_overview.py): Token, vocabulary, padding và attention mask.
     - [embedding_overview.py](../scripts/embedding_overview.py): Tra cứu vector nhúng learned embeddings qua `nn.Embedding`.
     - [attention_shapes.py](../scripts/attention_shapes.py): Scaled dot-product self-attention với Q, K, V.
     - [multihead_position_shapes.py](../scripts/multihead_position_shapes.py): Multi-Head attention reshaping và Learned Positional Embedding.
   - Tài liệu chuyên sâu [transformer-foundation.md](./transformer-foundation.md) phân tích toàn diện cơ chế Attention, Causal Masking và chu trình Next-token prediction.
5. **Quality Assurance & Testing**:
   - Unit tests và integration tests bao phủ toàn bộ pipeline xử lý, metric calculation và endpoint ML (`tests/unit/test_preprocessing.py`, `tests/integration/test_ml_intent_api.py`).
   - Linting 100% đạt chuẩn với `ruff`.

---

## 2. Giới Hạn Kỹ Thuật Của Mô Hình Nội Bộ (Disclaimer & Technical Limits)

Các mô hình được xây dựng trong Month 02 phục vụ mục tiêu nắm vững phương pháp luận khoa học dữ liệu và cơ chế mạng nơ-ron, có các giới hạn thực tế cần lưu ý:

- **Quy mô dữ liệu nhỏ (Toy Dataset)**: Tập dữ liệu intent 40-80 dòng chỉ đủ để kiểm chứng tính đúng đắn của pipeline và hiện tượng overfitting/underfitting, không đại diện cho phân phối ngôn ngữ tự nhiên thực tế.
- **Không gian nhãn đóng (Closed-set Classification)**: Mô hình MLP chỉ phân loại trong số các nhãn định trước (`greeting`, `book_meeting`, `cancel`, `other`), không có khả năng sinh ngôn ngữ (NLG) hay xử lý câu lệnh ngoài phạm vi.
- **Không tự huấn luyện Transformer từ đầu**: Huấn luyện một LLM từ đầu đòi hỏi hàng triệu USD và cụm tính toán GPU quy mô lớn. Việc này nằm ngoài mục tiêu kỹ thuật và không mang tính khả thi kinh tế cho ứng dụng thực tế.

---

## 3. Định Hướng & Hợp Đồng Chuyển Giao Cho Month 03 (LLM Engineering)

Month 03 sẽ đưa `ai-assistant-platform` bước vào thế giới **Kỹ thuật LLM hiện đại (LLM Engineering)** bằng cách tích hợp trực tiếp các mô hình ngôn ngữ lớn tiên tiến (OpenAI GPT-4o, Anthropic Claude 3.5, Google Gemini 1.5/2.0) thông qua API:

### 3.1. Structured Outputs & Data Contracts
- Thay thế heuristic parsing bằng **Structured Outputs** (JSON Schema bắt buộc qua Pydantic).
- Đảm bảo phản hồi của LLM luôn tuân thủ nghiêm ngặt schema định sẵn, loại bỏ hoàn toàn lỗi vỡ cấu trúc JSON khi gọi API.

### 3.2. Function Calling & Tool Calling
- Cho phép LLM trở thành bộ điều phối thông minh (Agent Controller), tự động quyết định khi nào cần gọi các tool/service nội bộ của hệ thống (ví dụ: truy vấn cơ sở dữ liệu lịch họp, gửi email, gọi API bên thứ ba).

### 3.3. Tận Dụng Nền Tảng Transformer Vào Tối Ưu LLM
- **Kiểm soát Context Window & Token Budget**: Hiểu rõ tokenization để ước tính chính xác chi phí API và ngăn ngừa lỗi tràn cửa sổ ngữ cảnh.
- **Tối ưu Prompt & Attention Intuition**: Ứng dụng hiểu biết về Causal Masking và Attention để đặt các chỉ dẫn quan trọng ở đầu hoặc cuối prompt (giảm hiện tượng "Lost in the Middle").
- **Chuẩn bị cho RAG (Retrieval-Augmented Generation)**: Tận dụng các mô hình Encoder-only (như `text-embedding-3-small`) để vector hóa tài liệu doanh nghiệp và tra cứu ngữ nghĩa.

### 3.4. Model Context Protocol (MCP)
- Chuẩn hóa các kết nối công cụ và tài nguyên ngữ cảnh cho Assistant Platform theo chuẩn MCP.

---

## 4. Checklist Sẵn Sàng Chuyển Giao (Handoff Checklist)

- [x] Linter pass 100%: `uv run ruff check .`
- [x] Test suite pass 100%: `uv run pytest`
- [x] Baseline scikit-learn và PyTorch training script chạy độc lập, reproducible.
- [x] Tài liệu đánh giá ML [ml-evaluation-report.md](./ml-evaluation-report.md) ghi nhận đầy đủ metric và sai số.
- [x] Tài liệu nền tảng [transformer-foundation.md](./transformer-foundation.md) hoàn thiện, giải thích được cơ chế sinh token tự hồi quy.
- [x] Không hard-code API keys, token bí mật hoặc đường dẫn tuyệt đối trong mã nguồn.
