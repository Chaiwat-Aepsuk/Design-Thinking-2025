from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time

DEBUG = True  # ✅ True = โชว์ error + raw text, False = เงียบๆ

pages = [
    {"label": "Creator", "url": "https://www.bnn.in.th/th/mkt/comset-creator", "csv": "comset_Creator.csv"},
    {"label": "Gamer",   "url": "https://www.bnn.in.th/th/mkt/comset-gamer",   "csv": "comset_Game.csv"},
    {"label": "Officer", "url": "https://www.bnn.in.th/th/mkt/comset-officer", "csv": "comset_Officer.csv"},
]

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

try:
    for page in pages:
        label, url, out_csv = page["label"], page["url"], page["csv"]

        driver.get(url)

        # รอเว็บโหลด + scroll ให้ของโหลดครบ
        time.sleep(5)
        for _ in range(4):
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(2)

        rows = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        print(f"\n[{label}] กำลังเริ่มดึงข้อมูล... พบกล่องสินค้าเบื้องต้น {len(rows)} กล่อง\n")
        print("-" * 50)

        data = []
        for index, row in enumerate(rows, start=1):
            try:
                name_el = row.find_element(By.CSS_SELECTOR, ".product-name")
                name = " ".join(name_el.get_attribute("textContent").strip().split())

                price_el = row.find_element(By.CSS_SELECTOR, ".product-price")
                price = price_el.get_attribute("textContent").strip()
                price = price.replace("฿", "").replace(",", "").strip()

                if name and price:
                    data.append([name, price])
                    print(f"ชื่อ: {name} ราคา: {price}")

            except Exception as e:
                if DEBUG:
                    print(f"❌ กล่องที่ {index} ดึงไม่สำเร็จ | error: {e}")
                    raw_text = row.get_attribute("innerText").strip().replace("\n", " | ")
                    print(f"   [ข้อมูลดิบ]: {raw_text}")

        print("-" * 50)

        # บันทึก CSV
        with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "price"])
            writer.writerows(data)

        print(f"saved -> {out_csv}")

finally:
    driver.quit()