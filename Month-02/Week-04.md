# Tháng 2 - Tuần 4: Tokenization, embedding, attention và Transformer foundation

## Mục tiêu tuần

Hiểu nền tảng Transformer bằng các demo nhỏ và tài liệu tự viết: tokenization, embedding, attention, self-attention, multi-head attention, positional encoding, encoder/decoder và vì sao LLM dự đoán token tiếp theo. Không tự train LLM và không thay stack chính.

## Kiến thức cần đạt

- Phân biệt raw text, token, token id, embedding vector và attention mask.
- Hiểu embedding lookup ở mức tensor shape.
- Tự tính scaled dot-product attention trên ma trận nhỏ.
- Giải thích multi-head attention và positional encoding ở mức trực giác.
- Phân biệt encoder-only, decoder-only, encoder-decoder.
- Chuẩn bị handoff sang Month-03 LLM Engineering.

## Module project sẽ bổ sung

`scripts/tokenization_overview.py`, `scripts/embedding_overview.py`, `scripts/attention_shapes.py`, `scripts/transformer_shapes.py`, `docs/transformer-foundation.md` và cập nhật `docs/month-03-handoff.md`.

## Kế hoạch từng ngày

### Ngày 22 - Tokenization và vocabulary nhỏ

**Mục tiêu cụ thể:** Tự viết tokenizer whitespace đơn giản để hiểu token id và vocabulary. **Kết quả cần đạt:** Script biến câu thành tokens, ids và attention mask giả lập. **Phân bổ thời gian:** 25 phút đọc Hugging Face overview/glossary, 40 phút code tokenizer nhỏ, 20 phút ghi ví dụ, 10 phút tự kiểm tra. **Lý thuyết:** Token, vocabulary, unknown token, padding, attention mask. **Tài liệu:** Hugging Face Glossary và How do Transformers work trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `scripts/tokenization_overview.py` với vocab từ vài câu trong intent dataset. **Tích hợp project:** Giải thích vì sao classifier Week-03 dùng numeric feature còn LLM dùng token ids/embedding. **File tạo/sửa:** `scripts/tokenization_overview.py`, `docs/transformer-foundation.md`. **Lệnh chạy:** `uv run python scripts/tokenization_overview.py`. **Kết quả mong đợi:** In tokens, ids, padded ids và attention mask cho 2 câu dài ngắn khác nhau. **Cách kiểm tra:** Thêm từ chưa có trong vocab và xác nhận thành `<unk>`. **Definition of Done:** Ghi rõ tokenizer này chỉ để học, không dùng cho production LLM. **Commit message:** `docs(transformer): add tokenization overview`. **Câu hỏi tự kiểm tra:** Token khác word ở đâu? Vì sao cần padding khi batch? Attention mask bảo vệ điều gì?

### Ngày 23 - Embedding lookup và vector meaning

**Mục tiêu cụ thể:** Dùng `torch.nn.Embedding` để chuyển token id thành vector. **Kết quả cần đạt:** Script in shape `(batch, sequence_length, embedding_dim)` và giải thích embedding là tham số học được. **Phân bổ thời gian:** 20 phút đọc lại PyTorch tensors/model, 45 phút code embedding demo, 20 phút shape notes, 10 phút commit. **Lý thuyết:** Embedding matrix, lookup, dimension, batch và sequence length. **Tài liệu:** PyTorch Build Model và Hugging Face Glossary trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `scripts/embedding_overview.py` dùng token ids từ ngày 22 và embedding dim nhỏ như 4 hoặc 8. **Tích hợp project:** So sánh hand-crafted features Week-01 với learned representation trong LLM. **File tạo/sửa:** `scripts/embedding_overview.py`, `docs/transformer-foundation.md`. **Lệnh chạy:** `uv run python scripts/embedding_overview.py`. **Kết quả mong đợi:** In embedding weight shape và output shape. **Cách kiểm tra:** Đổi vocab size hoặc embedding dim và dự đoán shape trước khi chạy. **Definition of Done:** Không diễn giải embedding random như semantic thật nếu chưa train. **Commit message:** `feat(transformer): demonstrate embedding lookup shapes`. **Câu hỏi tự kiểm tra:** Embedding vector được học khi nào? Vì sao cùng token id luôn lookup cùng vector trước context? Embedding dim lớn hơn có luôn tốt hơn không?

### Ngày 24 - Scaled dot-product attention bằng ma trận nhỏ

**Mục tiêu cụ thể:** Tính attention với Q, K, V nhỏ để hiểu cơ chế “nhìn vào token khác”. **Kết quả cần đạt:** Script in attention scores, weights sau softmax và output context vector. **Phân bổ thời gian:** 25 phút đọc attention explanation, 50 phút code attention mini, 20 phút giải thích từng shape, 10 phút ghi docs. **Lý thuyết:** Query, Key, Value, dot product, scale, softmax, weighted sum. **Tài liệu:** Hugging Face How do Transformers work và The Illustrated Transformer trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `scripts/attention_shapes.py` không dùng model lớn, chỉ tensor nhỏ và `torch.softmax`. **Tích hợp project:** Dùng ví dụ câu trong assistant để giải thích token nào attend token nào. **File tạo/sửa:** `scripts/attention_shapes.py`, `docs/transformer-foundation.md`. **Lệnh chạy:** `uv run python scripts/attention_shapes.py`. **Kết quả mong đợi:** Attention weight mỗi hàng cộng gần 1 và output shape đúng. **Cách kiểm tra:** Thay một vector key để xem attention weight đổi. **Definition of Done:** Không cần chứng minh toán, nhưng phải giải thích được shape. **Commit message:** `feat(transformer): add scaled dot product attention demo`. **Câu hỏi tự kiểm tra:** Q/K/V đại diện vai trò gì? Vì sao cần softmax? Scale theo căn bậc hai của dimension để làm gì ở mức trực giác?

### Ngày 25 - Multi-head attention và positional encoding

**Mục tiêu cụ thể:** Hiểu vì sao nhiều head và position signal cần thiết. **Kết quả cần đạt:** Script hoặc notes mô phỏng split embedding dim thành nhiều head và cộng positional encoding nhỏ. **Phân bổ thời gian:** 25 phút đọc Illustrated Transformer, 45 phút code shape demo, 25 phút cập nhật docs, 10 phút tự kiểm tra. **Lý thuyết:** Multiple attention heads, concat heads, positional encoding, thứ tự token. **Tài liệu:** The Illustrated Transformer và PyTorch `torch.nn.Transformer` shape notes trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Tạo `scripts/multihead_position_shapes.py` reshape tensor `(batch, seq, embed_dim)` thành `(batch, heads, seq, head_dim)`. **Tích hợp project:** Ghi vào docs vì bag-of-features baseline không nắm thứ tự tốt như Transformer. **File tạo/sửa:** `scripts/multihead_position_shapes.py`, `docs/transformer-foundation.md`. **Lệnh chạy:** `uv run python scripts/multihead_position_shapes.py`. **Kết quả mong đợi:** In shape trước/sau split head và sau concat; positional vector có cùng embedding dim. **Cách kiểm tra:** Thử `embed_dim` không chia hết cho `num_heads` và xử lý lỗi rõ. **Definition of Done:** Không tự implement full `nn.MultiheadAttention` nếu vượt thời gian. **Commit message:** `docs(transformer): explain multihead and positional shapes`. **Câu hỏi tự kiểm tra:** Vì sao Transformer cần thông tin vị trí? Multi-head có thể học nhiều quan hệ khác nhau như thế nào? Điều kiện shape nào bắt buộc khi chia head?

### Ngày 26 - Encoder, decoder và next-token prediction

**Mục tiêu cụ thể:** Phân biệt các kiến trúc Transformer và cách decoder-only LLM sinh token. **Kết quả cần đạt:** `docs/transformer-foundation.md` có bảng encoder-only, decoder-only, encoder-decoder và use case. **Phân bổ thời gian:** 30 phút đọc Hugging Face architectures, 35 phút viết bảng so sánh, 20 phút vẽ flow text bằng Markdown, 10 phút review. **Lý thuyết:** Encoder-only, decoder-only, encoder-decoder, causal mask, next-token prediction. **Tài liệu:** Hugging Face Transformer Architectures trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Viết ví dụ prompt `"Summarize this ticket"` thành chuỗi token và minh họa model dự đoán token tiếp theo từng bước. **Tích hợp project:** Chuẩn bị ngôn ngữ cho Month-03 khi gọi LLM API thay vì tự train. **File tạo/sửa:** `docs/transformer-foundation.md`, `docs/month-03-handoff.md`. **Lệnh chạy:** Không có code bắt buộc; chạy `uv run ruff check .` nếu docs command trong project có lint Markdown thì dùng command đó. **Kết quả mong đợi:** Docs giải thích được vì sao GPT-style model là decoder-only/autoregressive ở mức khái niệm. **Cách kiểm tra:** Tự giải thích khác nhau giữa BERT-style và GPT-style trong 5 câu. **Definition of Done:** Không đưa fine-tuning, RLHF hoặc serving local model vào phần bắt buộc. **Commit message:** `docs(transformer): compare encoder decoder architectures`. **Câu hỏi tự kiểm tra:** Causal mask ngăn điều gì? Encoder-only phù hợp task nào? Vì sao LLM có thể sinh câu bằng next-token prediction?

### Ngày 27 - Milestone: Transformer foundation report

**Mục tiêu cụ thể:** Hoàn thiện tài liệu Transformer bằng lời của người học, có liên hệ project. **Kết quả cần đạt:** `docs/transformer-foundation.md` có ví dụ tokenization, embedding, attention, multi-head, positional encoding và next-token prediction. **Phân bổ thời gian:** 20 phút gom script outputs, 45 phút viết/refactor docs, 25 phút chạy scripts, 20 phút review nội dung. **Lý thuyết:** Từ data feature đến representation learning và attention. **Tài liệu:** Xem lại nhóm Tuần 4 trong [RESOURCES.md](./RESOURCES.md). **Thực hành:** Chạy tất cả scripts tuần 4 và chèn summary ngắn vào docs, không paste output quá dài. **Tích hợp project:** Docs chỉ ra Month-03 sẽ dùng LLM API thật, không tự build Transformer. **File tạo/sửa:** `docs/transformer-foundation.md`, `README.md` nếu cần link docs. **Lệnh chạy:** `uv run python scripts/tokenization_overview.py`; `uv run python scripts/embedding_overview.py`; `uv run python scripts/attention_shapes.py`; `uv run python scripts/multihead_position_shapes.py`. **Kết quả mong đợi:** Tất cả script chạy CPU, docs không có placeholder. **Cách kiểm tra:** Nhờ chính mình đọc lại và trả lời: input text đi qua những bước nào trước khi thành logits? **Definition of Done:** Nội dung không copy dài từ nguồn và có link tham khảo. **Commit message:** `docs(month-02): complete transformer foundation report`. **Câu hỏi tự kiểm tra:** Token id thành logits qua những tầng khái niệm nào? Attention khác hand-crafted feature thế nào? Month-03 sẽ dùng kiến thức này ở đâu?

### Ngày 28 - Review tháng 2 và handoff sang LLM Engineering

**Mục tiêu cụ thể:** Chốt toàn bộ Month-02: data, baseline, PyTorch training, endpoint và Transformer docs. **Kết quả cần đạt:** Test/lint pass, report evaluation cập nhật, handoff sang Month-03 rõ ràng. **Phân bổ thời gian:** 20 phút review checklist tháng, 30 phút chạy test/lint, 30 phút sửa docs nhỏ, 25 phút viết handoff, 15 phút commit plan. **Lý thuyết:** ML evaluation là thói quen trước khi đánh giá LLM workflow. **Tài liệu:** Không đọc nguồn mới; đối chiếu [README tháng](./README.md) và [RESOURCES.md](./RESOURCES.md). **Thực hành:** Chạy data pipeline, baseline, PyTorch smoke train, API test và transformer scripts. **Tích hợp project:** Tạo `docs/month-03-handoff.md` ghi endpoint hiện có, model limitation và kỳ vọng khi thay bằng LLM. **File tạo/sửa:** `docs/month-03-handoff.md`, `docs/ml-evaluation-report.md`, `docs/transformer-foundation.md`, `README.md`. **Lệnh chạy:** `uv run python scripts/prepare_intent_data.py`; `uv run python scripts/train_sklearn_baseline.py --write-report`; `uv run python scripts/train_torch_intent.py --epochs 5 --save-model`; `uv run ruff check .`; `uv run pytest`. **Kết quả mong đợi:** Các command chính pass; docs ghi rõ phần nào còn hạn chế do dataset nhỏ. **Cách kiểm tra:** Đọc Month-03 handoff và xác nhận không yêu cầu OpenAI API key ở Month-02. **Definition of Done:** Month-02 hoàn thành nhưng không chạm vào Month-03 đến Month-06 trong roadmap repo. **Commit message:** `docs(month-02): finalize ml foundation handoff`. **Câu hỏi tự kiểm tra:** Deliverable tháng 2 nào sẽ dùng trực tiếp ở Month-03? Vì sao evaluation report quan trọng trước LLM? Nếu có thêm 1 giờ, cải tiến nào có giá trị nhất?

## Milestone cuối tuần

Người học có `docs/transformer-foundation.md` và các script shape demo đủ để giải thích luồng text -> token ids -> embeddings -> attention -> logits, đồng thời có handoff rõ ràng sang Month-03.

## Review checklist

- [ ] Scripts tuần 4 chạy được trên CPU.
- [ ] Docs giải thích tokenization, embedding, attention, multi-head, positional encoding.
- [ ] Có bảng encoder-only, decoder-only, encoder-decoder.
- [ ] Có liên hệ giữa baseline/PyTorch Month-02 và LLM Month-03.
- [ ] Không yêu cầu train Transformer hoặc dùng API key thật.

## Definition of Done

Tuần 4 hoàn thành khi learner giải thích được Transformer foundation bằng lời của mình, có script shape minh họa và project có handoff sang Month-03 LLM Engineering.

## Lỗi thường gặp

- Nhầm tokenization với embedding.
- Nghĩ embedding random đã có nghĩa semantic.
- Quên attention mask khi padding.
- Cố tự implement Transformer hoàn chỉnh.
- Dùng Hugging Face model thật quá sớm khiến scope vượt 2 giờ/ngày.

## Tài liệu chính thức và nguồn uy tín

Xem nhóm Tuần 4 trong [RESOURCES.md](./RESOURCES.md).

## Tùy chọn nếu còn thời gian

- Thêm diagram Mermaid trong `docs/transformer-foundation.md`.
- Thử `torch.nn.MultiheadAttention` với tensor nhỏ.
- Đọc thêm bài Attention Is All You Need, nhưng chỉ ở mức skim abstract/architecture nếu còn sức.
