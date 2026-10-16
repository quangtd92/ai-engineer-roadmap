import torch
from torch import nn


def split_heads(x: torch.Tensor, num_heads: int) -> torch.Tensor:
    """(batch, seq, embed) -> (batch, heads, seq, head_dim)."""
    print('x 1', x)
    batch_size, seq_len, embed_dim = x.shape
    # print('batch_size', batch_size)
    # print('seq_len', seq_len)
    # print('embed_dim', embed_dim)
    # kiểm tra embed_dim có chia hết cho num_heads không
    if embed_dim % num_heads != 0:
        raise ValueError("embed_dim must be divisible by num_heads")
    head_dim = embed_dim // num_heads

    # reshape thành (batch, seq, heads, head_dim)
    x = x.view(batch_size, seq_len, num_heads, head_dim)
    print('x', x.shape)
    # đổi thứ tự dimension thành (batch, heads, seq, head_dim)
    x = x.permute(0, 2, 1, 3)
    print('x 2', x)
    return x


def combine_heads(x: torch.Tensor) -> torch.Tensor:
    """(batch, heads, seq, head_dim) -> (batch, seq, embed)."""
    batch_size, num_heads, seq_len, head_dim = x.shape
    print('x', x)
    print('batch_size', batch_size)
    print('seq_len', seq_len)
    print('num_heads', num_heads)
    print('head_dim', head_dim)

    # đảo ngược thứ tự dimension
    x = x.permute(0, 2, 1, 3)
    print('x', x.shape)

    # 2. embed_dim chuẩn = số heads * kích thước mỗi head (2 * 4 = 8)
    embed_dim = num_heads * head_dim  
    
    # 3. Gộp 2 chiều cuối (num_heads, head_dim) thành embed_dim
    x = x.reshape(batch_size, seq_len, embed_dim)
    print('x', x)

    return x


def main() -> None:
    torch.manual_seed(42)

    x = torch.randn(2, 4, 8)

    # split heads
    x_split = split_heads(x, 2)
    print('x_split', x_split.shape)
    #combine heads
    x_combine = combine_heads(x_split)
    print('x_combine.shape', x_combine.shape)
    print('x_combine', x_combine)
    # tạo position IDs từ 0 đến seq_len - 1
    _batch_size, seq_len, embed_dim = x_combine.shape
    print('x_combine.shape', x_combine.shape)
    position_ids = torch.arange(seq_len)
    print('position_ids', position_ids)
    # dùng nn.Embedding để tạo positional embedding
    positional_embedding = nn.Embedding(seq_len, embed_dim)
    print('positional_embedding', positional_embedding)
    # cộng positional embedding vào x
    pos = positional_embedding(position_ids)  # shape: (seq_len, embed_dim)
    print('pos.shape:', pos.shape)

    # Broadcast pos (seq_len, embed_dim) vào x_combine (batch_size, seq_len, embed_dim)
    x_with_positional_embedding = x_combine + pos
    print('x_with_positional_embedding.shape:', x_with_positional_embedding)

    # In shape và viết assertion kiểm tra
    assert x_with_positional_embedding.shape == x_combine.shape
    assert torch.allclose(x, x_combine), 'x_combine phai giong het x ban dau!'
    print('Tat ca cac assertions deu PASS thanh cong!')


if __name__ == "__main__":
    main()