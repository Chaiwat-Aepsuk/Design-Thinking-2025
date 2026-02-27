from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time

url = "https://www.bnn.in.th/th/mkt/comset-creator"

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get(url)

# 1. รอเว็บโหลดและเลื่อนจอลงหลายๆ รอบ เพื่อให้โหลดข้อมูลและรูปภาพครบทุกกล่อง
time.sleep(5)
for _ in range(4):
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(2)

rows = driver.find_elements(By.CSS_SELECTOR, ".product-item")
print(f"กำลังเริ่มดึงข้อมูล... พบกล่องสินค้าเบื้องต้น {len(rows)} กล่อง\n")
print("-" * 50)

data = []
for index, row in enumerate(rows, start=1):
    try:
        name_el = row.find_element(By.CSS_SELECTOR, ".product-name")
        name = name_el.get_attribute("textContent").strip()
        name = " ".join(name.split())

        price_el = row.find_element(By.CSS_SELECTOR, ".product-price")
        price = price_el.get_attribute("textContent").strip()
        price = price.replace("฿", "").replace(",", "")
        
        if name and price:
            data.append([name, price])
            print(f"ชื่อ: {name} ราคา: {price}")

    except Exception as e:
        # ✅ เปิดแจ้งเตือน: ถ้าหาไม่เจอ จะดึงข้อความดิบ (Raw Text) มาโชว์
        # จะได้รู้ว่าเว็บ BaNANA ซ่อนข้อมูลไว้แบบไหน
        print(f"❌ กล่องที่ {index} ดึงไม่สำเร็จ")
        raw_text = row.get_attribute("innerText").strip().replace("\n", " | ")
        print(f"   [ข้อมูลดิบ]: {raw_text}")

driver.quit()

print("-" * 50)

# บันทึก CSV
with open("comset_Creator.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "price"])
    writer.writerows(data)

print("saved -> comset_Creator.csv")