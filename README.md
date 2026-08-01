# AI Engineer Roadmap (6 tháng)

## Mục tiêu và cách dùng

Lộ trình này xây một ứng dụng GenAI có thể kiểm thử qua một project xuyên suốt: `ai-assistant-platform`. Học theo thứ tự tháng → tuần → ngày; mỗi ngày giới hạn 1–2 giờ và có đầu ra, lệnh chạy, cách kiểm tra cùng commit message gợi ý.

Đọc [điều kiện đầu vào](./00-Prerequisites.md), sau đó dùng [ROADMAP_SPEC.md](./ROADMAP_SPEC.md) làm đặc tả và [VALIDATION.md](./VALIDATION.md) làm checklist chất lượng.

## Điều hướng 6 tháng và 24 tuần

| Tháng | Trọng tâm | Tuần học |
| --- | --- | --- |
| [Tháng 01](./Month-01/README.md) | Python, FastAPI, Docker, PyTorch foundation | [Tuần 01](./Month-01/Week-01.md) · [02](./Month-01/Week-02.md) · [03](./Month-01/Week-03.md) · [04](./Month-01/Week-04.md) |
| [Tháng 02](./Month-02/README.md) | Data processing, ML foundation, neural network, Transformer | [Tuần 01](./Month-02/Week-01.md) · [02](./Month-02/Week-02.md) · [03](./Month-02/Week-03.md) · [04](./Month-02/Week-04.md) |
| [Tháng 03](./Month-03/README.md) | LLM, Structured Output, Tool Calling, MCP | [Tuần 01](./Month-03/Week-01.md) · [02](./Month-03/Week-02.md) · [03](./Month-03/Week-03.md) · [04](./Month-03/Week-04.md) |
| [Tháng 04](./Month-04/README.md) | RAG, hybrid retrieval, reranking, evaluation | [Tuần 01](./Month-04/Week-01.md) · [02](./Month-04/Week-02.md) · [03](./Month-04/Week-03.md) · [04](./Month-04/Week-04.md) |
| [Tháng 05](./Month-05/README.md) | LangGraph agent, reliability, human-in-the-loop | [Tuần 01](./Month-05/Week-01.md) · [02](./Month-05/Week-02.md) · [03](./Month-05/Week-03.md) · [04](./Month-05/Week-04.md) |
| [Tháng 06](./Month-06/README.md) | Production, AWS EC2, CI/CD, observability | [Tuần 01](./Month-06/Week-01.md) · [02](./Month-06/Week-02.md) · [03](./Month-06/Week-03.md) · [04](./Month-06/Week-04.md) |

## Project progression

1. Tháng 01 tạo API FastAPI có test, cấu hình và Docker.
2. Tháng 02 thêm pipeline dữ liệu và baseline ML nhỏ, không biến thành lộ trình Data Science.
3. Tháng 03 thay mock bằng LLM, structured output, evaluation prompt và tool read-only có giới hạn.
4. Tháng 04 thêm ingestion, hybrid RAG, citation và RAG evaluation.
5. Tháng 05 điều phối capability đã có bằng LangGraph, persistence và approval cho hành động nhạy cảm.
6. Tháng 06 đóng gói, kiểm tra, triển khai một EC2 đơn và vận hành bằng observability/quality regression.

## Báo cáo review

Xem [final review](./FINAL_REVIEW.md) để biết trạng thái audit toàn repository, các sửa đổi và giới hạn xác minh runtime/cloud.
