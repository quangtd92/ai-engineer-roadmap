import sys

import torch
from tokenization_overview import build_vocabulary, encode, pad_batch, tokenize
from torch import nn

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


# Để làm gì: Minh họa cơ chế Embedding Lookup và kích thước tensor đầu ra.
# Cần làm gì: Chuyển chuỗi thành token ID qua vocabulary, thực hiện padding,
# đưa vào nn.Embedding và in ra shape của trọng số tensor kết quả.
# Đầu vào: Không nhận tham số; sử dụng các cấu mẫu khai báo trong hàm.
# Đầu ra: Không trả về giá trị; in thông tin embedding và tensor shape ra terminal.
def main():
    sequence_1 = "Hôm nay có sự kiện gì quan trọng không?"
    sequence_2 = "Gửi thư phản hồi cho đối tác"
    sequence_3 = "Tạo một cuộc họp với đội marketing vào 2h chiều nay"

    vocabulary = build_vocabulary([sequence_1, sequence_2, sequence_3])
    print(vocabulary, "len", len(vocabulary))
    vocab_encode_1 = encode(tokenize(sequence_1), vocabulary)
    print("vocab_encode_1", vocab_encode_1)
    vocab_encode_2 = encode(tokenize(sequence_2), vocabulary)
    print("vocab_encode_2", vocab_encode_2)
    vocab_encode_3 = encode(tokenize(sequence_3), vocabulary)
    print("vocab_encode_3", vocab_encode_3)
    vocab_pad_batch, _ = pad_batch([vocab_encode_1, vocab_encode_2, vocab_encode_3], vocabulary["<pad>"])

    print("vocab_pad_batch", vocab_pad_batch)

    tensor_vocab_pad_batch = torch.tensor(vocab_pad_batch)
    print("tensor_vocab_pad_batch", tensor_vocab_pad_batch)

    embedding = nn.Embedding(
        num_embeddings=len(vocabulary),
        embedding_dim=4,
        padding_idx=vocabulary["<pad>"],
    )
    print("embedding", embedding)
    print("embedding weight.shape", embedding.weight.shape)

    embedded = embedding(tensor_vocab_pad_batch)
    print("embedded", embedded)
    print("embedded.shape", embedded.shape)


if __name__ == "__main__":
    main()
