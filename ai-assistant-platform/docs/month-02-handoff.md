# Month 02 Handoff & Data Processing Design Notes

## 1. PyTorch Dataset & DataLoader Baseline
- **Đã hoàn thành ở Tháng 1 (Tuần 4):**
  - Hiểu cấu trúc Tensor: `shape`, `dtype`, `device`.
  - Tách biệt `model.eval()` và `torch.no_grad()` cho quy trình inference an toàn.
  - Cơ chế bọc dữ liệu (`Dataset`) và chia lô (`DataLoader`) với `batch_size`.

## 2. Kế hoạch dữ liệu cho Tháng 2 (Neural Networks & Training Pipeline)
- **Dataset Contract:** Dữ liệu đầu vào cần chuẩn hóa sang `torch.float32` Tensor trước khi chuyển vào `DataLoader`.
- **Batching Strategy:**
  - Trong training: Sử dụng `shuffle=True` và cấu hình `batch_size` phù hợp (ví dụ: 16, 32, 64).
  - Trong inference API: Giữ batch dimension cho input (`(batch_size, input_dim)` hoặc `(1, input_dim)` với single request).
- **Tránh rò rỉ bộ nhớ (Memory Management):** Không lưu trữ `requires_grad=True` trong các schema response của API.
