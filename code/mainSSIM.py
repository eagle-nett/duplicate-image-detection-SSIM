import os
import shutil
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
# (có lưu lại ảnh gốc của các ảnh trùng)
# Thư mục chứa ảnh gốc 
SOURCE_DIR = r"C:\tdat\CODE\lọc ảnh_py\images test code"
# Thư mục lưu ảnh trùng
DUPLICATE_DIR = r"C:\tdat\CODE\lọc ảnh_py\images_project\1604\aa"
# Thư mục lưu ảnh không trùng
NON_DUPLICATE_DIR = r"C:\tdat\CODE\lọc ảnh_py\images_project\1604\ab"
# Ngưỡng SSIM để xem là trùng (1.0 là giống hệt)
SSIM_THRESHOLD = 0.97

# Tạo thư mục nếu chưa có
os.makedirs(DUPLICATE_DIR, exist_ok=True)
os.makedirs(NON_DUPLICATE_DIR, exist_ok=True)

SUPPORTED = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

images = []  # Lưu (ảnh xám, đường dẫn)
duplicates = 0
non_duplicates = 0
error_files = []  # Danh sách lưu lỗi

def image_to_gray_array(path, size=(256, 256)):
    """Mở ảnh, resize và chuyển sang ảnh xám numpy"""
    try:
        img = Image.open(path).convert('L').resize(size)
        return np.array(img)
    except Exception as e:
        print(f" Lỗi khi đọc ảnh: {path} ({e})")
        error_files.append((path, f"Lỗi đọc ảnh: {e}"))
        return None

def safe_copy(src_path, dst_dir):
    """Sao chép file và xử lý lỗi nếu có"""
    try:
        shutil.copy2(src_path, os.path.join(dst_dir, os.path.basename(src_path)))
    except Exception as e:
        print(f" Lỗi khi sao chép file: {src_path} ({e})")
        error_files.append((src_path, f"Lỗi sao chép: {e}"))

for file in os.listdir(SOURCE_DIR):
    if not file.lower().endswith(SUPPORTED):
        continue

    path = os.path.join(SOURCE_DIR, file)
    img_array = image_to_gray_array(path)

    if img_array is None:
        continue  # Bỏ qua file lỗi

    is_duplicate = False
    for existing_array, existing_path in images:
        try:
            score = ssim(img_array, existing_array)
            if score >= SSIM_THRESHOLD:
                print(f"+ Trùng: {file} giống với {os.path.basename(existing_path)} (SSIM: {score:.3f})")
                safe_copy(path, DUPLICATE_DIR)
                duplicates += 1
                is_duplicate = True
                break
        except Exception as e:
            print(f" Lỗi SSIM: {file} ({e})")
            error_files.append((path, f"Lỗi SSIM: {e}"))
            is_duplicate = True  # Đánh dấu là lỗi, không xử lý tiếp
            break

    if not is_duplicate:
        images.append((img_array, path))
        print(f"- Không trùng: {file}")
        safe_copy(path, NON_DUPLICATE_DIR)
        non_duplicates += 1

print(f"\n => Hoàn tất. Tìm thấy {duplicates} ảnh trùng và {non_duplicates} ảnh không trùng.")

# Ghi lỗi vào file log (nếu có)
if error_files:
    log_path = os.path.join(r"C:\tdat\CODE\lọc ảnh_py\images_project\1604\error.txt")
    try:
        with open(log_path, 'w', encoding='utf-8') as f:
            for err_path, err_msg in error_files:
                f.write(f"{err_path}: {err_msg}\n")
        print(f" Đã lưu log lỗi vào: {log_path}")
    except Exception as e:
        print(f" Không ghi được file log: {e}")
