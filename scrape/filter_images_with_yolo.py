import os
import shutil
from ultralytics import YOLO
from PIL import Image

# ================= הגדרות =================
CATEGORY = "chair"  # קטגוריה לסינון (למשל: chair, table, lamp)
YOLO_MODEL_PATH = "yolov8l-oiv7.pt"  # מודל YOLOv8 שאומן על Open Images V7

# ================= נתיב תיקייה =================
data_dir = r"C:\Users\sharon\Desktop\ScrapingFromPinterest\ScrapingFromPinterest\data\images\chair\pop art"
rejected_dir = os.path.join(data_dir, "rejected")
invalid_format_dir = os.path.join(rejected_dir, "invalid_format")
processing_error_dir = os.path.join(rejected_dir, "processing_error")
os.makedirs(rejected_dir, exist_ok=True)
os.makedirs(invalid_format_dir, exist_ok=True)
os.makedirs(processing_error_dir, exist_ok=True)

# ================= טעינת YOLO =================
yolo_model = YOLO(YOLO_MODEL_PATH)

# ================= אתחול מונים =================
total = 0
saved = 0
rejected = 0
invalid_format = 0
processing_error = 0

# ================= הרצת YOLO =================
for filename in os.listdir(data_dir):
    if not filename.endswith(".jpg"):
        continue

    path = os.path.join(data_dir, filename)
    total += 1

    # בדיקת תקינות תמונה לפני עיבוד
    try:
        with Image.open(path) as img:
            img.verify()
    except Exception as e:
        print(f"⚠️ קובץ פגום או לא נתמך: {filename} ({e})")
        shutil.move(path, os.path.join(invalid_format_dir, filename))
        invalid_format += 1
        continue

    try:
        # בדיקת YOLO לקטגוריה
        results = yolo_model(path)
        result = results[0]
        boxes = result.boxes
        names = yolo_model.names

        if boxes is None or len(boxes) == 0:
            labels = []
        else:
            labels = [names[int(cls)] for cls in boxes.cls]

        category_ok = CATEGORY in labels

        # סינון לפי YOLO בלבד
        if category_ok:
            print(f"🟢 נשמר: {path} (זוהו: {labels})")
            saved += 1
        else:
            print(f"🔴 נדחה (YOLO): {path} (זוהו: {labels})")
            shutil.move(path, os.path.join(rejected_dir, filename))
            rejected += 1

    except Exception as e:
        print(f"⚠️ שגיאה בעיבוד {filename}: {e}")
        shutil.move(path, os.path.join(processing_error_dir, filename))
        processing_error += 1

# ================= סיכום =================
print("\n========= סיכום =========")
print(f"סה\"כ תמונות: {total}")
print(f"✅ נשמרו: {saved}")
print(f"❌ נדחו: {rejected}")
print(f"⚠️ קבצים פגומים: {invalid_format}")
print(f"⚠️ שגיאות עיבוד: {processing_error}")
