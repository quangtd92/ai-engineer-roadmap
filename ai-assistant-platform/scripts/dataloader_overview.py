import torch
from torch.utils.data import DataLoader, Dataset


class ToyVectorDataset(Dataset):
    def __init__(self, data: list[list[float]]):
        print(f"{data=}")
        self.data = torch.tensor(data, dtype=torch.float32)
        print(f"{self.data=}")

    def __len__(self) -> int:
        print(f"{len(self.data)=}")
        return len(self.data)

    def __getitem__(self, idx) -> torch.Tensor:
        print(f"{idx=}")
        return self.data[idx]


def main():
    data = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]]

    dataset = ToyVectorDataset(data)
    print(f"{dataset=}")
    dataloader = DataLoader(data, batch_size=3, shuffle=True)
    print(f"{dataloader=}")

    for batch_idx, batch in enumerate(dataloader, start=1):
        print(f"Batch index: {batch_idx}, batch: {batch}")


if __name__ == "__main__":
    main()
