import torch
from torch.utils.data import DataLoader, Dataset


class ToyVectorDataset(Dataset):
    def __init__(self, data: list[list[float]]):
        self.data = torch.tensor(data, dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx) -> torch.Tensor:
        return self.data[idx]


def main():
    data = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]]

    dataset = ToyVectorDataset(data)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
    print(f"{dataloader=}")

    for batch_idx, batch in enumerate(dataloader, start=1):
        print(f"Batch index: {batch_idx}, batch: {batch}")


if __name__ == "__main__":
    main()
