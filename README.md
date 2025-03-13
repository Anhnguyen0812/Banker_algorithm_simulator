# Banker Algorithm Simulator

## 📌 Cách chạy chương trình

1. **Tải project về máy**.
2. **Mở bằng VS Code** hoặc trình soạn thảo tùy thích.
3. **Cài đặt thư viện cần thiết** bằng lệnh:
   ```bash
   pip install matplotlib numpy
   ```
4. **Chạy chương trình** để mô phỏng thuật toán Banker.

---

## 🔹 System State & Execution Steps

### Trạng thái hệ thống và các bước thực thi:
![System State](https://github.com/user-attachments/assets/9e5230fb-3aa9-469e-860f-743a059938ba)

---

## 🔹 Request Resources

### ✅ Trạng thái an toàn:

Khi yêu cầu tài nguyên có thể được cấp phát mà vẫn đảm bảo hệ thống ở trạng thái an toàn.

![Safe State](https://github.com/user-attachments/assets/b58bc3fa-d161-4b93-b065-109832a77216)

### ❌ Trạng thái không an toàn:

Khi yêu cầu tài nguyên có thể dẫn đến deadlock, hệ thống không thể đảm bảo trạng thái an toàn.

![Unsafe State](https://github.com/user-attachments/assets/78c3dc3b-5bf0-4f96-a2f3-5b6279ec4540)

---

## 📝 Giới thiệu thuật toán Banker

Thuật toán Banker là một thuật toán quản lý tài nguyên được sử dụng để ngăn chặn deadlock. Nó hoạt động bằng cách kiểm tra xem một yêu cầu cấp phát tài nguyên có thể được thực hiện mà vẫn đảm bảo hệ thống ở trạng thái an toàn hay không.

**Nguyên tắc hoạt động:**
- Xác định tổng số tài nguyên hệ thống có thể cấp phát.
- Kiểm tra yêu cầu từ tiến trình.
- Cấp phát tài nguyên nếu hệ thống vẫn ở trạng thái an toàn sau khi cấp phát.
- Nếu yêu cầu không thể đảm bảo an toàn, từ chối cấp phát.

📌 **Ứng dụng thực tế:**
- Quản lý tài nguyên CPU và bộ nhớ trong hệ điều hành.
- Phân bổ tài nguyên trong hệ thống ngân hàng (do đó có tên gọi "Banker's Algorithm").

---

🚀 **Hãy thử chạy chương trình và khám phá cách thuật toán Banker hoạt động!**
