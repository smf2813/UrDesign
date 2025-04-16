import os
import cv2
import torch
import sqlite3
import shutil
from ultralytics import YOLO
from PIL import Image

# הגדרות ראשוניות
CATEGORY = "chair"  # הקטגוריה שברצונך לסנן
STYLE = "pop art"   # הסגנון הספציפי שברצונך לבדוק

data_dir = os.path.join("data", "images", CATEGORY, STYLE)
rejected_dir = os.path.join(data_dir, "rejected")
os.makedirs(rejected_dir, exist_ok=True)

# טען את YOLO
model = YOLO("yolo11n.pt")  # או כל מודל אחר שלך

# 🔍 הצגת הקטגוריות ש-YOLO מזהה
print("📋 YOLO מזהה את הקטגוריות הבאות:")
print(model.names)

# טען את מסד הנתונים
conn = sqlite3.connect("data/products.db")
cursor = conn.cursor()

# השג את כל התמונות של הקטגוריה והסגנון הנוכחיים
cursor.execute("SELECT id, local_path FROM products WHERE category = ? AND style = ?", (CATEGORY, STYLE))
images = cursor.fetchall()

# סריקה ומיון
for img_id, path in images:
    try:
        results = model(path)
        names = results[0].names
        classes = [names[int(cls)] for cls in results[0].boxes.cls]

        # אם הקטגוריה לא זוהתה - מחק מהמסד והעבר לתיקיית rejected
        if CATEGORY.lower() not in [c.lower() for c in classes]:
            print(f"🛑 תמונה לא מתאימה: {path} (זוהו: {classes})")
            cursor.execute("DELETE FROM products WHERE id = ?", (img_id,))
            conn.commit()
            shutil.move(path, os.path.join(rejected_dir, os.path.basename(path)))
        else:
            print(f"✅ תמונה מתאימה: {path} (זוהו: {classes})")
    except Exception as e:
        print(f"⚠️ שגיאה בעיבוד {path}: {e}")

conn.close()
print("🎯 סינון YOLO הסתיים.")


