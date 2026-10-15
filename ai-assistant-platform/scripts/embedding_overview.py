import sys

import torch
from tokenization_overview import build_vocabulary, encode, pad_batch, tokenize
from torch import nn

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


# ?? l?m g?: Minh h?a c? ch? Embedding Lookup v? k?ch th??c tensor ??u ra.
# C?n l?m g?: Chuy?n chu?i th?nh token ID qua vocabulary, th?c hi?n padding,
# ??a v?o nn.Embedding v? in ra shape c?a tr?ng s? c?ng tensor k?t qu?.
# ??u v?o: Kh?ng nh?n tham s?; s? d?ng c?c c?u m?u khai b?o trong h?m.
# ??u ra: Kh?ng tr? v? gi? tr?; in th?ng tin embedding v? tensor shape ra terminal.
def main():
    sequence_1 = "H?m nay c? s? ki?n g? quan tr?ng kh?ng?"
    sequence_2 = "G?i th? ph?n h?i cho ??i t?c"
    sequence_3 = "T?o m?t cu?c h?p v?i ??i marketing v?o 2h chi?u nay"

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
