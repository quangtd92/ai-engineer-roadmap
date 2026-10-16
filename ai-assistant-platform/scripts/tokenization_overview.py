

# Để làm gì: Chuyển một câu văn bản thô thành các token đơn giản.
# Cần làm gì: Chuẩn hóa chữ thường rồi tách câu theo khoảng trắng.
# Đầu vào: text - một câu ở dạng chuỗi.
# Đầu ra: Danh sách token theo đúng thứ tự xuất hiện trong câu.
def tokenize(text: str) -> list[str]:
    text_lower = text.lower().strip()
    tokens = text_lower.split()
    return tokens


# Để làm gì: Tạo bảng ánh xạ mỗi token sang một token ID duy nhất.
# Cần làm gì: Tokenize các câu, lấy token không trùng, sắp xếp ổn định và dành
# ID 0 cho <pad>, ID 1 cho <unk>.
# Đầu vào: texts - danh sách các câu dùng để xây dựng vocabulary.
# Đầu ra: Dictionary có key là token và value là token ID.
def build_vocabulary(texts: list[str]) -> dict[str, int]:
    token_batch = []
    for text in texts:
        token = tokenize(text)
        token_batch.append(token)

    result = sorted(set(
        item for batch in token_batch
        for item in batch
        if (item != "<pad>" and item != "<unk>")
    ))

    vocab = {
        "<pad>": 0,
        "<unk>": 1,
    }
    for idx, value in enumerate(result, start=2):
        vocab[value] = idx
    return vocab
    

# Để làm gì: Chuyển danh sách token thành dữ liệu số mà model có thể nhận.
# Cần làm gì: Tra ID của từng token trong vocabulary; token chưa biết dùng ID
# của <unk>.
# Đầu vào: tokens - danh sách token; vocabulary - bảng token sang token ID.
# Đầu ra: Danh sách token ID có cùng thứ tự và số phần tử với tokens.
def encode(tokens: list[str], vocabulary: dict[str, int]) -> list[int]:
    token_ids = []
    for value in tokens:
        token_ids.append(vocabulary.get(value, vocabulary['<unk>']))
    return token_ids


# Để làm gì: Đưa các chuỗi token ID về cùng độ dài để có thể tạo một batch.
# Cần làm gì: Tìm chuỗi dài nhất, thêm pad_id vào bên phải các chuỗi ngắn hơn
# và tạo attention mask (1 cho token thật, 0 cho padding).
# Đầu vào: sequences - các chuỗi token ID; pad_id - ID dùng để padding.
# Đầu ra: Tuple gồm batch token ID đã padding và batch attention mask.
def pad_batch(
    sequences: list[list[int]],
    pad_id: int,
) -> tuple[list[list[int]], list[list[int]]]:
    if not sequences:
        return [], []
    max_length = len(max(sequences, key=len))
    padded_ids = [seq + [pad_id] * (max_length - len(seq)) for seq in sequences]
    attention_masks = [[1] * len(seq) + [0] * (max_length - len(seq)) for seq in sequences]
    return padded_ids, attention_masks


# Để làm gì: Minh họa toàn bộ luồng text -> tokens -> IDs -> padding -> mask.
# Cần làm gì: Chuẩn bị câu mẫu, gọi các function phía trên và in từng kết quả.
# Đầu vào: Không nhận tham số; sử dụng các câu mẫu được khai báo trong hàm.
# Đầu ra: Không trả về giá trị; kết quả minh họa được in ra terminal.
def main() -> None:
    sequence_a = "Cho tôi xem các cuộc họp trong tuần này"
    sequence_b = "Tôi muốn biết lịch trình hôm nay"
    sequence_c = "Lịch trình buổi chiều có bận không?"

    vocabulary = build_vocabulary([sequence_a, sequence_b])
    print(vocabulary)
    vocab_encode_a = encode(tokenize(sequence_a), vocabulary)
    print('vocab_encode_a', vocab_encode_a)
    vocab_encode_b = encode(tokenize(sequence_b), vocabulary)
    print('vocab_encode_b', vocab_encode_b)
    vocab_encode_c = encode(tokenize(sequence_c), vocabulary)
    print('vocab_encode_c', vocab_encode_c)
    vocab_pad_batch, attention_mask = pad_batch([vocab_encode_a, vocab_encode_b, vocab_encode_c], 0)
    print('vocab_pad_batch', vocab_pad_batch)
    print('attention_mask', attention_mask)

if __name__ == "__main__":
    main()
