# VALIDATION.md

## 1. Mục đích

Tài liệu này dùng để kiểm tra chất lượng của bộ roadmap trước khi coi một tuần, một tháng hoặc toàn bộ repository là hoàn chỉnh.

Validation gồm hai loại:

- **Automated checks:** có thể kiểm tra bằng script.
- **Manual review:** cần người hoặc agent đọc và đánh giá.

Không được chỉ kiểm tra số lượng file mà bỏ qua chất lượng nội dung.

---

## 2. Trạng thái đánh giá

Dùng một trong các trạng thái:

- `PASS`: đạt yêu cầu.
- `PASS_WITH_NOTES`: đạt nhưng có điểm cần lưu ý.
- `FAIL`: không đạt, phải sửa.
- `NOT_APPLICABLE`: chưa áp dụng ở giai đoạn này.

Mỗi review file phải ghi:

```text
Status:
Scope:
Files reviewed:
Issues found:
Issues fixed:
Open issues:
```

---

## 3. Validation cấp repository

### 3.1 Cấu trúc file

- [ ] Có `README.md`.
- [ ] Có `ROADMAP_SPEC.md`.
- [ ] Có `AGENTS.md`.
- [ ] Có `VALIDATION.md`.
- [ ] Có `00-Prerequisites.md`.
- [ ] Có thư mục `Month-01` đến `Month-06`.
- [ ] Mỗi tháng có `README.md`.
- [ ] Mỗi tháng có `Week-01.md` đến `Week-04.md`.
- [ ] Mỗi tháng có `REVIEW.md`.
- [ ] Mỗi tháng có `RESOURCES.md`.
- [ ] Không có file Markdown rỗng.
- [ ] Không có file chỉ chứa template hoặc placeholder.
- [ ] README chính có link đến toàn bộ tháng.
- [ ] Internal links không bị hỏng.

### 3.2 Tính nhất quán

- [ ] Tên project luôn là `ai-assistant-platform`.
- [ ] Main stack nhất quán với `ROADMAP_SPEC.md`.
- [ ] Không đổi framework chính giữa các tháng.
- [ ] Heading và format nhất quán.
- [ ] Thuật ngữ kỹ thuật nhất quán.
- [ ] Ngôn ngữ chính là tiếng Việt.
- [ ] Không có nội dung quảng cáo.
- [ ] Không cam kết chắc chắn có việc sau 6 tháng.

### 3.3 Tính liên tục

- [ ] Kiến thức tháng sau dựa trên tháng trước.
- [ ] Không sử dụng công nghệ trước khi giới thiệu.
- [ ] Project được nâng cấp liên tục.
- [ ] Không có sáu project độc lập không liên quan.
- [ ] Có mô tả kiến trúc trước và sau mỗi tháng.
- [ ] Có milestone rõ ràng theo tháng.

---

## 4. Validation cấp tháng

Mỗi tháng phải đạt:

### 4.1 Nội dung bắt buộc

- [ ] Có mục tiêu tháng.
- [ ] Có prerequisite.
- [ ] Có đầu ra tháng.
- [ ] Có 4 tuần.
- [ ] Có milestone từng tuần.
- [ ] Có Definition of Done tháng.
- [ ] Có rủi ro và cách giảm tải.
- [ ] Có tài liệu tham khảo.
- [ ] Có review cuối tháng.
- [ ] Có thay đổi project cụ thể.

### 4.2 Khối lượng

- [ ] Không có tuần vượt quá mức hợp lý.
- [ ] Không có ngày bắt buộc trên 2 giờ.
- [ ] Nội dung tháng có thể hoàn thành với 1–2 giờ/ngày.
- [ ] Các chủ đề nâng cao được đánh dấu tùy chọn.
- [ ] Không nhồi nhiều framework giống nhau.
- [ ] Có ngày review hoặc buffer.

### 4.3 Chất lượng đầu ra

- [ ] Deliverable có thể kiểm tra.
- [ ] Có command hoặc bước chạy.
- [ ] Có test hoặc manual verification.
- [ ] Có tiêu chí pass/fail.
- [ ] Có README hoặc tài liệu demo.
- [ ] Có commit progression hợp lý.

---

## 5. Validation cấp tuần

Mỗi tuần phải có:

- [ ] Mục tiêu tuần.
- [ ] Kiến thức cần đạt.
- [ ] Feature hoặc module sẽ thêm.
- [ ] 7 ngày hoặc lịch tương đương được giải thích.
- [ ] Milestone cuối tuần.
- [ ] Review checklist.
- [ ] Definition of Done.
- [ ] Lỗi thường gặp.
- [ ] Tài liệu tham khảo.
- [ ] Nội dung tùy chọn nếu còn thời gian.

Kiểm tra chất lượng:

- [ ] Mỗi ngày có trọng tâm riêng.
- [ ] Không sao chép cùng nội dung giữa các ngày.
- [ ] Nội dung nối tiếp hợp lý.
- [ ] Có ít nhất một output chạy được.
- [ ] Có ít nhất một test hoặc cách xác minh.
- [ ] Có cập nhật project chính.
- [ ] Không dùng khái niệm chưa được giới thiệu.

---

## 6. Validation cấp ngày

Mỗi ngày phải có:

- [ ] Mục tiêu cụ thể.
- [ ] Kết quả cần đạt.
- [ ] Phân bổ thời gian.
- [ ] Lý thuyết cần học.
- [ ] Tài liệu cần đọc.
- [ ] Bài thực hành.
- [ ] Áp dụng vào project.
- [ ] File tạo hoặc sửa.
- [ ] Lệnh cần chạy.
- [ ] Kết quả mong đợi.
- [ ] Cách kiểm tra.
- [ ] Definition of Done.
- [ ] Commit message gợi ý.
- [ ] 2–5 câu hỏi tự kiểm tra.

Ngày đó bị đánh `FAIL` nếu có một trong các lỗi:

- Chỉ ghi “đọc tài liệu”.
- Chỉ ghi “học chủ đề”.
- Không có đầu ra cụ thể.
- Không có cách kiểm tra.
- Không thể hoàn thành trong 2 giờ.
- Lặp gần như nguyên văn ngày khác.
- Dùng công nghệ chưa được giới thiệu.
- Có link bịa hoặc không đáng tin cậy.
- Yêu cầu secret thật trong tài liệu.
- Không có liên hệ với project hoặc mục tiêu tuần.

---

## 7. Validation theo từng tháng

# Tháng 1

- [ ] Dùng `uv`, không dùng `pip` làm package manager chính.
- [ ] Có Python typing.
- [ ] Có FastAPI.
- [ ] Có Pydantic.
- [ ] Có configuration.
- [ ] Có logging.
- [ ] Có Docker.
- [ ] Có async cơ bản.
- [ ] Có test cơ bản.
- [ ] Có PyTorch inference.
- [ ] Không dạy lại quá sâu REST API và Git.

# Tháng 2

- [ ] Có NumPy và pandas.
- [ ] Có data cleaning.
- [ ] Có train/validation/test split.
- [ ] Có data leakage.
- [ ] Có Linear Regression ở mức nền tảng.
- [ ] Có Logistic Regression.
- [ ] Có classification metrics.
- [ ] Có Neural Network.
- [ ] Có training loop.
- [ ] Có Transformer foundation.
- [ ] Không quá tải ML cổ điển.
- [ ] Không bắt buộc SVM, KNN, PCA hoặc XGBoost tuning.

# Tháng 3

- [ ] Có LLM API integration.
- [ ] Có streaming.
- [ ] Có Structured Output.
- [ ] Có Pydantic validation.
- [ ] Có timeout và retry.
- [ ] Có Tool Calling.
- [ ] Có tool error handling.
- [ ] Có tool budget hoặc giới hạn vòng lặp.
- [ ] Có MCP Server đơn giản.
- [ ] Có prompt regression test.
- [ ] Có usage, latency và error logging.

# Tháng 4

- [ ] Có ingestion pipeline.
- [ ] Có chunking strategy.
- [ ] Có metadata.
- [ ] Có Qdrant.
- [ ] Có dense retrieval.
- [ ] Có BM25.
- [ ] Có Hybrid Search.
- [ ] Có reranking.
- [ ] Có query rewriting.
- [ ] Có citation.
- [ ] Có prompt injection defense cho tài liệu.
- [ ] Có RAGAS hoặc DeepEval.
- [ ] Có evaluation dataset.
- [ ] Có so sánh retrieval configuration.

# Tháng 5

- [ ] Có sự phân biệt rõ giữa Tool Calling và Agent.
- [ ] Có LangGraph state.
- [ ] Có node và edge.
- [ ] Có conditional routing.
- [ ] Có checkpoint.
- [ ] Có persistence.
- [ ] Có Human-in-the-loop.
- [ ] Có interrupt/resume.
- [ ] Có retry và timeout.
- [ ] Có max steps.
- [ ] Có tool budget.
- [ ] Có guardrails.
- [ ] Có tracing.
- [ ] Có Agent Evaluation.

# Tháng 6

- [ ] Có production Docker image.
- [ ] Có secret handling.
- [ ] Có health/readiness check.
- [ ] Có AWS EC2 deployment.
- [ ] Có Nginx.
- [ ] Có HTTPS.
- [ ] Có GitHub Actions.
- [ ] Có lint, test và build.
- [ ] Có deployment workflow.
- [ ] Có monitoring.
- [ ] Có tracing.
- [ ] Có cost và token usage.
- [ ] Có quality regression.
- [ ] Có runbook.
- [ ] Có final architecture document.
- [ ] Ollama/vLLM chỉ học ở mức phù hợp.
- [ ] Không yêu cầu hiểu sâu SGLang, TensorRT hoặc Kubernetes.

---

## 8. Kiểm tra tài liệu tham khảo

Mỗi link phải đáp ứng:

- [ ] Là URL thật.
- [ ] Dùng HTTPS.
- [ ] Nguồn chính thức hoặc uy tín.
- [ ] Có mô tả phần cần đọc.
- [ ] Không chỉ trỏ tới homepage nếu có thể trỏ tới tutorial cụ thể.
- [ ] Không dẫn tới nội dung lỗi thời rõ ràng.
- [ ] Không có quá nhiều nguồn bắt buộc trong một tuần.

Nếu chưa xác minh được:

```text
Cần xác minh trước khi xuất bản.
```

Không được tạo URL theo suy đoán.

---

## 9. Kiểm tra tính thực thi của command

- [ ] Command dùng đúng toolchain.
- [ ] Python command ưu tiên `uv run`.
- [ ] Không hard-code API key.
- [ ] Không commit `.env`.
- [ ] Có `.env.example`.
- [ ] Docker command chạy hợp lý.
- [ ] Test command tồn tại.
- [ ] Command không xóa dữ liệu.
- [ ] Có output mong đợi.
- [ ] Có hướng dẫn xử lý lỗi phổ biến.

---

## 10. Kiểm tra bảo mật

- [ ] Có secret management.
- [ ] Không log secret.
- [ ] Có input validation.
- [ ] Có file upload validation nếu có upload.
- [ ] Có giới hạn file size.
- [ ] Có timeout.
- [ ] Retry có giới hạn.
- [ ] Agent có max steps.
- [ ] Tool có permission boundary.
- [ ] Hành động nhạy cảm có human approval.
- [ ] Có prompt injection awareness.
- [ ] Có rate limiting ở production.

---

## 11. Kiểm tra evaluation

- [ ] Có dataset.
- [ ] Có baseline.
- [ ] Có metric.
- [ ] Có threshold hoặc tiêu chí.
- [ ] Có error analysis.
- [ ] Có so sánh trước/sau.
- [ ] Không phụ thuộc một metric duy nhất.
- [ ] Phân biệt test và evaluation.
- [ ] Evaluation có thể chạy lại.
- [ ] Kết quả được ghi thành report.

---

## 12. Kiểm tra trùng lặp

Đánh `FAIL` nếu:

- Hai ngày có nội dung giống nhau trên 70%.
- Definition of Done được sao chép nguyên văn mà không phù hợp ngữ cảnh.
- Tất cả ngày đều dùng cùng một cấu trúc câu.
- Tài liệu tham khảo lặp không cần thiết.
- Cùng một khái niệm được dạy lại mà không tăng độ sâu.
- Tool Calling tháng 3 và Agent tháng 5 không được phân biệt rõ.

---

## 13. Kiểm tra thời lượng

Mỗi ngày cần ghi rõ thời lượng.

Tổng mặc định:

- 60–75 phút: ngày nhẹ.
- 75–100 phút: ngày thường.
- 100–120 phút: ngày milestone.
- Không quá 120 phút bắt buộc.

Đánh `FAIL` nếu một ngày gồm đồng thời nhiều hơn hai nhiệm vụ lớn, ví dụ:

```text
Học attention + xây Transformer + tích hợp model + viết test + deploy Docker
```

Nội dung đó phải được chia nhỏ.

---

## 14. Báo cáo review tháng

Mỗi `REVIEW.md` nên dùng format:

```markdown
# Month XX Review

## Status
PASS | PASS_WITH_NOTES | FAIL

## Files reviewed

## Deliverables verified

## Validation summary

### Repository structure
### Daily completeness
### Time budget
### Technical sequence
### Project progression
### References
### Security
### Evaluation

## Issues found

## Issues fixed

## Open issues

## Recommendation for next month
```

---

## 15. Final validation

Toàn bộ roadmap chỉ được coi là hoàn thành khi:

- [ ] Tất cả tháng đạt `PASS` hoặc `PASS_WITH_NOTES`.
- [ ] Không còn placeholder.
- [ ] Không còn link giả.
- [ ] Không còn internal link hỏng.
- [ ] Không có tháng bị quá tải nghiêm trọng.
- [ ] Project progression hợp lý.
- [ ] Main stack nhất quán.
- [ ] Evaluation xuất hiện từ tháng 3–4.
- [ ] RAG có advanced retrieval.
- [ ] Agent có reliability và human approval.
- [ ] Production scope thực tế.
- [ ] Có `FINAL_REVIEW.md`.
- [ ] README chính mô tả cách sử dụng roadmap.
- [ ] Người học có thể bắt đầu từ Day 1 mà không cần tự lên kế hoạch lại.

---

## 16. Gợi ý automated validation script

Có thể tạo script kiểm tra:

- File tồn tại.
- File rỗng.
- Placeholder như `TODO`, `TBD`, `...`.
- Số lượng tuần.
- Heading bắt buộc.
- Internal links.
- URL format.
- Sự xuất hiện của các section bắt buộc.
- Số ngày trong mỗi tuần.
- Các ngày thiếu time budget.
- Các ngày thiếu Definition of Done.
- Các ngày thiếu commit message.
- Các file có độ trùng lặp cao.

Automated check không thay thế manual curriculum review.
