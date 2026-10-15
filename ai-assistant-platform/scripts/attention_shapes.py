import sys

import torch

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


# Để làm gì: Tự cài đặt cơ chế Scaled Dot-Product Attention bằng các phép toán tensor cơ bản.
# Cần làm gì: Tính tích vô hướng Q @ K^T, chia tỉ lệ căn(d_k), áp dụng softmax và nhân với V.
# Đầu vào: q, k, v (Tensor) và mask tùy chọn.
# Đầu ra: Tuple gồm tensor ngữ cảnh (output) và ma trận trọng số (attention_weights).
def scaled_dot_product_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    mask: torch.Tensor | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    d_k = q.size(-1)

    # 1. Tính attention scores thô: (seq_len, d_k) @ (d_k, seq_len) -> (seq_len, seq_len)
    scores = torch.matmul(q, k.transpose(-2, -1))

    # 2. Chia tỉ lệ căn bậc hai của d_k để tránh bão hòa Softmax
    scores = scores / (d_k**0.5)

    # 3. Áp dụng mask nếu được cung cấp
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))

    # 4. Tính ma trận trọng số xác suất chú ý: tổng mỗi hàng bằng 1.0
    weights = torch.softmax(scores, dim=-1)

    # 5. Tổng hợp thông tin từ Value: (seq_len, seq_len) @ (seq_len, d_v) -> (seq_len, d_v)
    output = torch.matmul(weights, v)

    return output, weights


# Để làm gì: Chạy thử nghiệm và in các kích thước tensor của Scaled Dot-Product Attention.
# Cần làm gì: Khởi tạo Q, K, V ngẫu nhiên cho 3 token (d_k=4), tính toán và in kết quả kiểm chứng.
# Đầu vào: Không nhận tham số; dùng dữ liệu mẫu tạo bởi torch.randn.
# Đầu ra: In các tensor và shape ra terminal.
def main() -> None:
    torch.manual_seed(42)

    seq_len = 3
    d_k = 4
    d_v = 4

    q = torch.randn(seq_len, d_k)
    k = torch.randn(seq_len, d_k)
    v = torch.randn(seq_len, d_v)

    print("--- 1. Đầu vào (Inputs) ---")
    print(f"Q shape: {q.shape}")
    print(f"K shape: {k.shape}")
    print(f"V shape: {v.shape}\n")

    output, weights = scaled_dot_product_attention(q, k, v)

    print("--- 2. Trọng số Attention (Weights) ---")
    print("Attention Weights matrix (shape:", weights.shape, "):")
    print(weights)
    print("Tổng mỗi hàng (kiểm chứng Softmax sum ≈ 1.0):", weights.sum(dim=-1))

    print("\n--- 3. Đầu ra Ngữ cảnh (Context Output) ---")
    print(f"Output shape: {output.shape}")
    print(output)


if __name__ == "__main__":
    main()