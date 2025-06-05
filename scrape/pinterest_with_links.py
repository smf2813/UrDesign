from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import os
import time
from PIL import Image
from io import BytesIO
import sqlite3

# ================= הגדרות =================
CATEGORY = "rug"
STYLE = "rug"

# ================= נתיבים =================
db_path = os.path.join("data", "products.db")
image_folder = os.path.join("data", "images", CATEGORY, STYLE)
os.makedirs(image_folder, exist_ok=True)

# ================= חיבור למסד נתונים =================
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        style TEXT,
        image_url TEXT UNIQUE,
        pinterest_url TEXT UNIQUE,
        external_url TEXT,
        price TEXT,
        local_path TEXT,
        cloud_url TEXT,
        embedding_path TEXT
    )
''')
conn.commit()

# ================= הגדרת הדפדפן =================
options = Options()
options.add_argument("--disable-gpu")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ================= התחברות לפינטרסט =================
login_url = "https://www.pinterest.com/login/"
driver.get(login_url)
print("🔐 התחבר/י ל-Pinterest ואז חזרי לכאן.")
while "login" in driver.current_url:
    time.sleep(2)
print("✅ התחברת. ממשיך...")

# ================= חיפוש פריטים =================
search_url = "https://www.pinterest.com/search/pins/?q=rug&rs=shopping_filter&filter_location=0&on_sale=20&commerce_only=true"
driver.get(search_url)
time.sleep(3)

products = set()
scroll_attempts = 0
max_scrolls = 50

while scroll_attempts < max_scrolls:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    pins = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='pin']")
    new_items = 0

    for pin in pins:
        try:
            img_element = pin.find_element(By.TAG_NAME, "img")
            img_url = img_element.get_attribute("src")

            a_element = pin.find_element(By.TAG_NAME, "a")
            pinterest_url = a_element.get_attribute("href")

            if img_url and pinterest_url and (img_url, pinterest_url) not in products:
                products.add((img_url, pinterest_url))
                new_items += 1
        except:
            continue

    if new_items == 0:
        print(f"⚠️ אין יותר פריטים חדשים אחרי {scroll_attempts} גלילות.")
        break
    else:
        print(f"🔽 גלילה {scroll_attempts + 1}, נוספו {new_items} פריטים, סה\"כ: {len(products)}")

    scroll_attempts += 1

# ================= פונקציה למציאת קישור חיצוני ומחיר =================
def get_external_link_and_price(driver):
    try:
        time.sleep(2)
        external_link = None
        price_text = None

        all_links = driver.find_elements(By.XPATH, "//a[@href]")
        for link in all_links:
            href = link.get_attribute("href")
            if href and "pinterest.com" not in href and "javascript:void" not in href:
                external_link = href
                break

        price_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '$')]")
        for elem in price_elements:
            text = elem.text.strip()
            if "$" in text and len(text) < 20:
                price_text = text
                break

        return external_link, price_text

    except Exception as e:
        print(f"❌ שגיאה בזמן סריקת קישורים/מחיר: {e}")
        return None, None

    except Exception as e:
        print(f"❌ שגיאה בזמן סריקת קישורים/מחיר: {e}")
        return None, None

# ================= הורדה, קישור, שמירה =================
for index, (img_url, pinterest_url) in enumerate(products):
    try:
        # בדיקת כפילויות במסד נתונים
        cursor.execute('''
            SELECT COUNT(*) FROM products
            WHERE image_url = ? OR pinterest_url = ?
        ''', (img_url, pinterest_url))
        exists = cursor.fetchone()[0]

        if exists > 0:
            print(f"⚠️ פריט כפול, מדלגים עליו.")
            continue

        # קישור חיצוני ומחיר
        driver.get(pinterest_url)
        time.sleep(5)
        external_url, price = get_external_link_and_price(driver)

        if not external_url:
            print(f"⚠️ אין קישור חיצוני, מדלגים על הפריט.")
            continue

        print(f"🔗 קישור חיצוני: {external_url}")
        print(f"💲 מחיר: {price if price else 'לא נמצא'}")

        # הורדת תמונה ושמירה
        img_data = requests.get(img_url).content
        img = Image.open(BytesIO(img_data)).convert("RGB")
        img = img.resize((800, 800))
        local_path = os.path.join(image_folder, f"image_{index}.jpg")
        img.save(local_path)
        print(f"✅ נשמרה תמונה: {local_path}")

        # שמירה למסד נתונים
        cursor.execute('''
            INSERT INTO products (category, style, image_url, pinterest_url, external_url, price, local_path, cloud_url, embedding_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (CATEGORY, STYLE, img_url, pinterest_url, external_url, price, local_path, "", ""))
        conn.commit()

    except Exception as e:
        print(f"❌ שגיאה בתמונה {index}: {e}")

print(f"🎉 סיימת להוריד ולשמור {len(products)} פריטים כולל קישורים חיצוניים.")
driver.quit()
conn.close()
