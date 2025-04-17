# Phân loại hình ảnh trùng lặp và không trùng lặp
Dùng SSIM (Structural Similarity Index) sẽ cho độ chính xác cao hơn khi so sánh ảnh — đặc biệt tốt khi ảnh có thay đổi nhẹ về kích thước, độ sáng hoặc nén với thư viện scikit-image.

## Cài thư viện
pip install scikit-image Pillow
pip install imagehash Pillow

## Giải thích:
  image_to_gray_array: chuyển ảnh về grayscale, resize để so sánh đồng đều.
  
  ssim(...): so sánh ảnh hiện tại với các ảnh trước đó.
  
  Ngưỡng SSIM ~0.97: khá chính xác nhưng vẫn có độ "mềm" cho ảnh giống gần như tuyệt đối.

## 🧪 Gợi ý điều chỉnh:
  Nếu quá "nhạy", bạn có thể tăng lên 0.98–0.99.
  
  Nếu bỏ sót một số ảnh "na ná", bạn có thể giảm xuống 0.95 hoặc thấp hơn.
