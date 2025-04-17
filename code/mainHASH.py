import os
import shutil
from PIL import Image
import imagehash

# Thư mục chứa ảnh gốc
SOURCE_DIR = r"E:\no"
# Thư mục để lưu ảnh nghi là trùng
DUPLICATE_DIR = r"E:\duplicate"
# Thư mục để lưu ảnh không trùng
NON_DUPLICATE_DIR = r"E:\non duplicate"
# Ngưỡng hash để xem là trùng (0 = giống hệt, 5-10 = khá giống)
HASH_THRESHOLD = 5

# Tạo thư mục lưu ảnh trùng và không trùng nếu chưa có
os.makedirs(DUPLICATE_DIR, exist_ok=True)
os.makedirs(NON_DUPLICATE_DIR, exist_ok=True)

# Dạng ảnh hỗ trợ
SUPPORTED = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

hash_dict = {}
duplicates = 0
non_duplicates = 0

for file in os.listdir(SOURCE_DIR):
    if not file.lower().endswith(SUPPORTED):
        continue

    path = os.path.join(SOURCE_DIR, file)

    try:
        img = Image.open(path)
        img_hash = imagehash.phash(img)

        # Kiểm tra ảnh đã có hash trùng chưa
        is_duplicate = False
        for existing_path, existing_hash in hash_dict.items():
            if abs(img_hash - existing_hash) <= HASH_THRESHOLD:
                print(f"🔁 Trùng: {file} giống với {os.path.basename(existing_path)}")
                shutil.copy2(path, os.path.join(DUPLICATE_DIR, file))
                duplicates += 1
                is_duplicate = True
                break

        # Nếu không trùng, lưu vào thư mục non-duplicate
        if not is_duplicate:
            print(f"✅ Không trùng: {file}")
            shutil.copy2(path, os.path.join(NON_DUPLICATE_DIR, file))
            non_duplicates += 1
            hash_dict[path] = img_hash

    except Exception as e:
        print(f"Lỗi khi xử lý {file}: {e}")

print(f"\n✅ Hoàn tất. Tìm thấy {duplicates} ảnh trùng/na ná và {non_duplicates} ảnh không trùng.")
