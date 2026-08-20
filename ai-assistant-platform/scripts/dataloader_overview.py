import torch
from torch.utils.data import Dataset, DataLoader 

class ToyVectorDataset(Dataset):
    def __init__(self, data: list[list[float]]):
        self.data = torch.tensor(data, dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx) -> torch.Tensor:
        return self.data[idx]

def main():
    data = [
        [1., 2.],
        [3., 4.],
        [5., 6.],
        [7., 8.]
    ]

    dataset = ToyVectorDataset(data)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
    print(f"{dataloader=}")

    for batch_idx, batch in enumerate(dataloader, start=1):
        print(f"Batch index: {batch_idx}, batch: {batch}")


if __name__ == "__main__":
    main()