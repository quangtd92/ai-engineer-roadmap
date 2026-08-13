import torch

def main():
    tensor = torch.tensor([[1.0, 2.0]])

    shape = tensor.shape
    device = tensor.device
    dtype = tensor.dtype

    print(shape)
    print(device)
    print(dtype)
    # get item (chỉ áp dụng cho tensor 1 phần tử, ví dụ phần tử đầu tiên tensor[0, 0])
    print(tensor[0, 0].item())

if __name__ == "__main__":
    main()