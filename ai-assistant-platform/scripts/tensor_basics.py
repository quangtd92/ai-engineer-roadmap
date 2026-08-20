import torch


def main():
    tensor = torch.tensor([[[123.0, 23.0]],[[1., 2.]]])

    shape = tensor.shape
    device = tensor.device
    dtype = tensor.dtype

    print(f"xxx: {[[[123.0, 23.0]],[[1., 2.]]]}")
    print(f"tensor: {tensor}")
    print(f"shape: {shape}")
    print(f"device: {device}")
    print(f"dtype: {dtype}")
    # get item (chỉ áp dụng cho tensor 1 phần tử, ví dụ phần tử đầu tiên tensor[0, 0])
    print(tensor[0, 0].item())


if __name__ == "__main__":
    main()
