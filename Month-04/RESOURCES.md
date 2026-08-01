# Tháng 4 - Tài liệu tham khảo

Chỉ đọc phần được nêu trong ngày học; ưu tiên tài liệu chính thức. URL dưới đây là nguồn kỹ thuật trực tiếp, không yêu cầu tạo tài khoản hay đưa API key vào repository.

## Tuần 1

- [Qdrant - Points](https://qdrant.tech/documentation/concepts/points/): point ID, vector và payload.
- [Qdrant - Payload](https://qdrant.tech/documentation/concepts/payload/): metadata, indexing và filter.
- [Python - hashlib](https://docs.python.org/3/library/hashlib.html): SHA-256 fingerprint.
- [Python - pathlib](https://docs.python.org/3/library/pathlib.html): allowlist đường dẫn và duyệt file.

## Tuần 2

- [Qdrant Python client - Quickstart](https://python-client.qdrant.tech/quickstart): tạo collection và upsert.
- [Qdrant - Search](https://qdrant.tech/documentation/concepts/search/): top-k, score và filter.
- [Qdrant - Hybrid Queries](https://qdrant.tech/documentation/concepts/hybrid-queries/): prefetch và fusion.
- [rank-bm25](https://pypi.org/project/rank-bm25/): API BM25 nhỏ dùng cho corpus local.

## Tuần 3

- [OpenAI - File search](https://platform.openai.com/docs/guides/tools-file-search): nguyên tắc grounding và citation (tham khảo khái niệm, không thay Qdrant).
- [OpenAI - Safety best practices](https://platform.openai.com/docs/guides/safety-best-practices): prompt injection và ranh giới tin cậy.
- [Qdrant - Filtering](https://qdrant.tech/documentation/concepts/filtering/): điều kiện metadata an toàn.

## Tuần 4

- [RAGAS - Get started](https://docs.ragas.io/en/stable/getstarted/): dataset, evaluate và metrics.
- [RAGAS - Metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/): faithfulness, context precision/recall, answer relevancy.
- [DeepEval - RAG evaluation](https://deepeval.com/docs/getting-started-rag): lựa chọn thay thế nếu không dùng RAGAS.
- [pytest - Parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html): regression cases dữ liệu-driven.

## Tìm hiểu thêm

- [Qdrant - Multitenancy](https://qdrant.tech/documentation/guides/multiple-partitions/): chỉ đọc sau khi pipeline local ổn định.
- [OpenAI - Embeddings](https://platform.openai.com/docs/guides/embeddings): chọn embedding model và kích thước vector.
