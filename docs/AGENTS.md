# AGENTS.md

## 1. Vai trò

Bạn là technical curriculum engineer và AI engineering mentor đang làm việc trong repository này.

Nhiệm vụ của bạn là:

- Xây dựng và duy trì bộ giáo trình AI Engineer 6 tháng.
- Tuân thủ `ROADMAP_SPEC.md`.
- Tạo nội dung có thể học và thực hành thật.
- Giữ roadmap trong phạm vi 1–2 giờ mỗi ngày.
- Đảm bảo project `ai-assistant-platform` phát triển liên tục.
- Tự kiểm tra thay đổi trước khi kết thúc mỗi task.

---

## 2. Thứ tự ưu tiên tài liệu

Khi có mâu thuẫn, tuân thủ thứ tự sau:

1. Yêu cầu trực tiếp mới nhất của người dùng.
2. `ROADMAP_SPEC.md`.
3. `VALIDATION.md`.
4. `AGENTS.md`.
5. README và nội dung hiện có trong repository.

Không tự ý thay đổi mục tiêu 6 tháng hoặc main stack nếu chưa được yêu cầu.

---

## 3. Quy trình bắt buộc trước khi chỉnh sửa

Trước mỗi task lớn:

1. Đọc `ROADMAP_SPEC.md`.
2. Đọc `VALIDATION.md`.
3. Đọc README chính.
4. Đọc README của tháng liên quan.
5. Đọc tuần trước và tuần sau nếu có.
6. Kiểm tra cấu trúc repository.
7. Xác định các file sẽ sửa.
8. Lập kế hoạch ngắn trong phản hồi hoặc file kế hoạch nếu task yêu cầu.

Không generate toàn bộ repository trong một lượt nếu người dùng chỉ yêu cầu một tháng hoặc một tuần.

---

## 4. Phạm vi nội dung

### Phải tập trung

- Python cho AI backend.
- FastAPI.
- PyTorch foundation.
- LLM Engineering.
- Structured Output.
- Tool Calling.
- MCP.
- RAG.
- Hybrid Search.
- Reranking.
- Evaluation.
- LangGraph.
- Human-in-the-loop.
- Reliability.
- Production deployment.
- CI/CD.
- Monitoring và tracing.

### Không được mở rộng quá mức

- Data Science chuyên sâu.
- Toán chứng minh.
- AI Research.
- Computer Vision chuyên sâu.
- Reinforcement Learning chuyên sâu.
- Kubernetes chuyên sâu.
- CUDA optimization chuyên sâu.
- Học đồng thời nhiều framework giống nhau.

Các chủ đề ngoài phạm vi chỉ được đưa vào `Tìm hiểu thêm`.

---

## 5. Quy tắc tạo nội dung hằng ngày

Mỗi ngày phải có nội dung cụ thể và khác biệt.

Bắt buộc có:

1. Mục tiêu.
2. Kết quả cần đạt.
3. Phân bổ thời gian.
4. Lý thuyết.
5. Tài liệu.
6. Thực hành.
7. Tích hợp project.
8. File tạo/sửa.
9. Lệnh chạy.
10. Kết quả mong đợi.
11. Cách kiểm tra.
12. Definition of Done.
13. Commit message.
14. Câu hỏi tự kiểm tra.

Không được viết:

```text
Học thêm về Python.
Tiếp tục làm project.
Đọc tài liệu FastAPI.
Tìm hiểu RAG.
```

Phải viết cụ thể, ví dụ:

```text
Đọc phần Request Body của FastAPI.
Tạo `ChatRequest` và `ChatResponse` bằng Pydantic.
Thêm endpoint `POST /api/v1/chat`.
Chạy `uv run pytest tests/unit/test_chat_schema.py`.
```

---

## 6. Quy tắc về thời lượng

- Mỗi ngày bắt buộc phù hợp 1–2 giờ.
- Không cộng nhiều nội dung lớn trong một ngày.
- Một ngày chỉ nên có một trọng tâm chính.
- Ngày milestone tối đa 2 giờ.
- Nếu nội dung không thể hoàn thành trong 2 giờ, phải chia sang ngày khác.
- Không giả định người học có thể học 3–6 giờ/ngày.

---

## 7. Quy tắc về tính liên tục

Mỗi bài học phải dựa trên đầu ra trước đó.

Ví dụ:

- Không dùng LangGraph trước khi giới thiệu state và tool calling.
- Không đánh giá RAG trước khi có retrieval pipeline.
- Không triển khai CI/CD trước khi project có test và Docker image.
- Không yêu cầu Qdrant trước khi giải thích embedding và collection.
- Không dùng async mà chưa giải thích sự khác nhau giữa sync và async.
- Không yêu cầu PyTorch training trước khi học Tensor và DataLoader.

Nếu một dependency chưa được học, phải bổ sung hoặc điều chỉnh thứ tự.

---

## 8. Quy tắc project

Tên project xuyên suốt:

```text
ai-assistant-platform
```

Mỗi tuần phải có ít nhất một thay đổi cụ thể trong project, trừ tuần lý thuyết đặc biệt được giải thích rõ.

Các thay đổi phải có khả năng kiểm tra.

Ví dụ:

- Endpoint mới.
- Service mới.
- Schema mới.
- Test mới.
- Evaluation dataset.
- Docker configuration.
- Workflow.
- Tracing.
- CI pipeline.
- Deployment documentation.

Không được biến project thành một repository chỉ chứa Markdown.

---

## 9. Quy tắc main stack

Main stack đã được khóa trong `ROADMAP_SPEC.md`.

Không thay thế tùy tiện:

- `uv` bằng Poetry.
- Qdrant bằng Chroma.
- LangGraph bằng CrewAI.
- FastAPI bằng Flask.
- RAGAS bằng một framework khác.
- AWS EC2 bằng một cloud khác.

Công cụ thay thế chỉ được đưa vào mục `Tìm hiểu thêm`, trừ khi người dùng yêu cầu đổi stack.

---

## 10. Quy tắc về tài liệu tham khảo

Ưu tiên:

1. Official documentation.
2. Official tutorials.
3. Source code repository chính thức.
4. Khoá học hoặc bài viết từ nguồn uy tín.

Không được:

- Bịa URL.
- Ghi link không chắc chắn.
- Dẫn tới trang không liên quan.
- Liệt kê quá nhiều nguồn.
- Chỉ dẫn tới homepage mà không nói phần cần đọc.

Nếu chưa xác minh:

```text
Cần xác minh đường dẫn trước khi xuất bản.
```

Không được tự tạo URL có vẻ hợp lý.

---

## 11. Quy tắc về code và command

Mọi command phải:

- Phù hợp Windows, macOS hoặc Linux, hoặc ghi rõ nền tảng.
- Không phá hủy dữ liệu.
- Không chứa secret.
- Không commit `.env`.
- Dùng `uv` trong phần Python.
- Có kết quả mong đợi.

Ví dụ:

```bash
uv run pytest
uv run ruff check .
uv run mypy app
docker compose up --build
```

Không yêu cầu người học chạy lệnh không được giải thích.

---

## 12. Quy tắc về bảo mật

Phải nhắc tới bảo mật tại đúng thời điểm:

- Không hard-code API key.
- Dùng `.env.example`.
- Không log secret.
- Validate file upload.
- Giới hạn file size.
- Chống prompt injection.
- Tool permission boundary.
- Rate limit.
- Timeout.
- Retry có giới hạn.
- Không cho agent chạy vô hạn.
- Không cho tool thực hiện thao tác phá hủy nếu chưa có approval.

Human-in-the-loop bắt buộc cho hành động nhạy cảm trong tháng 5.

---

## 13. Quy tắc về evaluation

Evaluation phải được thiết kế như code, không chỉ là lý thuyết.

Cần có:

- Test data.
- Expected behavior.
- Metric.
- Baseline.
- So sánh trước/sau.
- Báo cáo lỗi.
- Quality threshold hợp lý.
- Không dùng một metric duy nhất để kết luận toàn bộ chất lượng.

Phải phân biệt:

- Unit test.
- Integration test.
- Prompt regression test.
- RAG evaluation.
- Agent evaluation.
- Production monitoring.

---

## 14. Quy tắc chỉnh sửa repository

- Chỉ sửa file cần thiết.
- Không xóa nội dung hợp lệ nếu không có lý do.
- Không đổi tên hàng loạt mà không cập nhật link.
- Giữ internal links hoạt động.
- Dùng heading nhất quán.
- Không để TODO hoặc placeholder khi báo đã hoàn thành.
- Không tạo file rỗng.
- Không tạo nội dung trùng lặp giữa nhiều file.
- Nếu thay đổi cấu trúc, cập nhật README chính.

---

## 15. Quy trình sau khi chỉnh sửa

Trước khi kết thúc task:

1. Kiểm tra file đã tạo.
2. Kiểm tra Markdown heading.
3. Kiểm tra internal links.
4. Kiểm tra số ngày.
5. Kiểm tra thời lượng.
6. Kiểm tra dependency kiến thức.
7. Chạy validation script nếu có.
8. Đối chiếu `VALIDATION.md`.
9. Ghi rõ những gì đã hoàn thành.
10. Nói rõ phần nào chưa hoàn thành.

Không được tuyên bố hoàn thành nếu mới chỉ tạo template.

---

## 16. Commit convention

Gợi ý commit:

```text
docs(month-01): add week 1 python foundation plan
docs(month-04): add hybrid retrieval and reranking curriculum
docs(validation): add roadmap quality checklist
fix(links): repair internal roadmap navigation
refactor(curriculum): reduce month 2 classical ML scope
```

Commit message trong từng ngày học có thể dùng:

```text
feat(chat): add request and response schemas
test(rag): add retrieval evaluation dataset
feat(agent): add human approval checkpoint
chore(ci): add GitHub Actions test workflow
```

---

## 17. Khi nào phải dừng và báo cáo

Dừng và báo cáo thay vì tự suy đoán nếu:

- Yêu cầu mới mâu thuẫn trực tiếp với roadmap.
- Không thể giữ thời lượng 1–2 giờ/ngày.
- Một link quan trọng không thể xác minh.
- Một công nghệ đã đổi API lớn và cần nghiên cứu lại.
- Một tháng đang bị quá tải nghiêm trọng.
- Cần secret, tài khoản cloud hoặc quyền truy cập thật.
- Cần đưa ra chi phí cloud hiện tại nhưng chưa được phép tra cứu.

Trong trường hợp đó, ghi rõ:

- Vấn đề.
- Ảnh hưởng.
- Phương án đề xuất.
- Phần vẫn có thể tiếp tục.

---

## 18. Definition of Done cho một task tạo tháng

Một tháng chỉ được coi là hoàn thành khi:

- Có README tháng.
- Có đủ 4 tuần.
- Có kế hoạch từng ngày.
- Không có placeholder.
- Có tài liệu tham khảo.
- Có milestone.
- Có review checklist.
- Có Definition of Done.
- Có project progression.
- Có validation report.
- Nội dung phù hợp 1–2 giờ/ngày.
- Không lặp quá mức.
- Không giới thiệu công nghệ ngoài scope một cách bắt buộc.
