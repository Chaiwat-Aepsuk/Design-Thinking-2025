import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. ตั้งค่า Chrome Options
chrome_options = Options()
# chrome_options.add_argument("--headless") # เปิดบรรทัดนี้หากไม่ต้องการให้หน้าต่างเด้ง

# 2. เริ่มต้น WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

csv_filename = "practice_laptops.csv"

try:
    # 3. ไปยังหน้าเว็บเป้าหมาย (เว็บสำหรับฝึก Web Scraping โดยเฉพาะ)
    url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
    driver.get(url)
    time.sleep(3) # รอให้หน้าเว็บโหลด

    # 4. ดึงข้อมูล
    # เว็บนี้จะเก็บโน้ตบุ๊กแต่ละเครื่องไว้ในกรอบที่ชื่อ Class ว่า .card
    laptops = driver.find_elements(By.CSS_SELECTOR, ".card")
    print(f"พบโน้ตบุ๊กทั้งหมด {len(laptops)} เครื่องในหน้านี้\n")

    # --- เริ่มต้นกระบวนการเปิดไฟล์และเขียน CSV ---
    with open(csv_filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        
        # เขียนหัวตาราง (มีแถมดึงรายละเอียดสเปคย่อยๆ ให้ด้วย)
        writer.writerow(["Model", "Price", "Description"]) 

        for item in laptops:
            try:
                # ดึงชื่อ ราคา และรายละเอียดสเปค
                title = item.find_element(By.CSS_SELECTOR, ".title").text
                price = item.find_element(By.CSS_SELECTOR, ".price").text
                desc = item.find_element(By.CSS_SELECTOR, ".description").text
                
                # ปริ้นท์โชว์ใน Terminal
                print(f"รุ่น: {title}")
                print(f"ราคา: {price}")
                print(f"สเปค: {desc}")
                print("-" * 20)
                
                # นำข้อมูลเขียนลงไฟล์ CSV
                writer.writerow([title, price, desc])
            except Exception:
                pass
                
    print(f"✅ ดึงข้อมูลสำเร็จเรียบร้อย! ลองเปิดไฟล์ '{csv_filename}' ดูได้เลยครับ")

except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")

finally:
    # 5. ปิด Browser
    time.sleep(2)
    driver.quit()