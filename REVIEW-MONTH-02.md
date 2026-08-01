# Month 02 Review

## Status

PASS_WITH_NOTES

## Scope

Review cho riêng Month-02 sau khi triển khai chi tiết:

- `Month-02/README.md`
- `Month-02/Week-01.md`
- `Month-02/Week-02.md`
- `Month-02/Week-03.md`
- `Month-02/Week-04.md`
- `Month-02/RESOURCES.md`

Không chỉnh sửa Month-03 đến Month-06.

## Files reviewed

- `ROADMAP_SPEC.md`
- `VALIDATION.md`
- `IMPLEMENTATION_PLAN.md`
- `README.md`
- `Month-01/README.md`
- `Month-01/Week-04.md`
- `Month-02/README.md`
- `Month-02/Week-01.md`
- `Month-02/Week-02.md`
- `Month-02/Week-03.md`
- `Month-02/Week-04.md`
- `Month-02/RESOURCES.md`

## Deliverables verified

- Month README hoàn chỉnh với mục tiêu, prerequisite, đầu ra, kiến trúc trước/sau, milestone tuần, Definition of Done, rủi ro quá tải và nội dung được phép bỏ qua.
- 4 tuần đã có nội dung chi tiết.
- 28 ngày học có trọng tâm riêng, không còn template chung kiểu "Learn one focused topic".
- Mỗi ngày có mục tiêu, kết quả, thời lượng, lý thuyết, tài liệu, thực hành, tích hợp project, file tạo/sửa, lệnh chạy, kết quả mong đợi, cách kiểm tra, Definition of Done, commit message và câu hỏi tự kiểm tra.
- Tất cả bài tập đều phát triển `ai-assistant-platform`.
- Có resource file riêng cho Month-02.
- Có nội dung liên tục từ Month-01 toy inference sang Month-02 data/training và sang Month-03 LLM Engineering.

## Validation summary

### Repository structure

PASS_WITH_NOTES

- `Month-02/README.md` và `Week-01.md` đến `Week-04.md` đã hoàn thiện.
- Đã thêm `Month-02/RESOURCES.md` để đáp ứng yêu cầu tài liệu tham khảo cấp tháng.
- Review được ghi ở root `REVIEW-MONTH-02.md`, nhất quán với file `REVIEW-MONTH-01.md` đang tồn tại.
- Chưa tạo `Month-02/REVIEW.md` vì yêu cầu trực tiếp mới nhất chỉ định `REVIEW-MONTH-02.md`.

### Daily completeness

PASS

- Có đủ 28 ngày.
- Mỗi ngày có đầy đủ các mục bắt buộc theo `VALIDATION.md`.
- Nội dung từng ngày khác nhau theo progression: dataset -> cleaning -> split -> baseline -> metrics -> PyTorch training -> endpoint -> Transformer foundation.

### Time budget

PASS

- Mỗi ngày nằm trong khoảng 90-120 phút.
- Ngày milestone/review không vượt 120 phút.
- Nội dung nâng cao được đưa vào mục tùy chọn hoặc ghi rõ không bắt buộc.

### Technical sequence

PASS

- Tuần 1 tạo dữ liệu và preprocessing trước khi training.
- Tuần 2 dùng scikit-learn baseline và metric trước PyTorch training.
- Tuần 3 xây Dataset/DataLoader, model, training loop, validation loop rồi mới API endpoint.
- Tuần 4 chỉ học Transformer foundation, không yêu cầu tự train Transformer hoặc dùng LLM API trước Month-03.

### Project progression

PASS

- Mọi ngày đều có thay đổi cụ thể cho `ai-assistant-platform`.
- Project progression tạo data pipeline, baseline, evaluation report, model artifact, intent endpoint, Transformer docs và handoff sang Month-03.
- Không tạo project phụ rời rạc.

### References

PASS_WITH_NOTES

- `Month-02/RESOURCES.md` dùng nguồn chính thức hoặc uy tín: NumPy, pandas, scikit-learn, PyTorch, Hugging Face và The Illustrated Transformer.
- Các tuần trỏ về resource file thay vì bịa link rải rác.
- Link đã được chọn từ nguồn công khai ổn định; vẫn nên kiểm tra lại version docs trước khi xuất bản chính thức dài hạn.

### Security

PASS

- Nội dung nhắc không dùng dữ liệu nhạy cảm, không hard-code secret, không yêu cầu API key thật.
- Endpoint ML có fallback/error contract và không train model trong request.
- Month-02 chưa có upload file hoặc agent/tool permission nên các mục bảo mật đó chưa áp dụng.

### Evaluation

PASS

- Có train/validation/test split.
- Có baseline Logistic Regression.
- Có confusion matrix, precision, recall, F1, macro F1.
- Có validation/test distinction và cảnh báo không chọn model theo test set.
- Có report so sánh baseline với PyTorch model.
- Phân biệt unit test, smoke test, API integration test và evaluation report.

## Issues found

- Nội dung Month-02 ban đầu là template tiếng Anh chung chung.
- Thiếu tài liệu tham khảo riêng cho Month-02.
- Chưa có review Month-02.
- Chưa có validation script tự động trong repository.

## Issues fixed

- Thay toàn bộ placeholder Month-02 bằng nội dung tiếng Việt chi tiết.
- Thêm `Month-02/RESOURCES.md`.
- Tạo `REVIEW-MONTH-02.md`.
- Kiểm tra đủ 28 heading ngày bằng command tìm kiếm.
- Kiểm tra placeholder cũ không còn xuất hiện.
- Kiểm tra link nội bộ chính trong Month-02 trỏ tới file có thật.

## Open issues

- Repository hiện vẫn chưa có automated validation script; review này là manual review theo `VALIDATION.md`.
- Root README còn ngắn và chưa phải mục tiêu của task này.
- Month-03 đến Month-06 vẫn giữ nguyên trạng thái hiện có theo yêu cầu không chỉnh sửa.

## Recommendation for next month

Khi triển khai Month-03, bắt đầu từ `docs/month-03-handoff.md` mà Month-02 yêu cầu người học tạo: dùng endpoint intent, evaluation mindset và Transformer foundation làm nền để tích hợp OpenAI API, Structured Output, Tool Calling và prompt regression test.
