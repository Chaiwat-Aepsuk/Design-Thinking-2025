from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

url = "https://notebookspec.com/pc/spec"

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get(url)

wait = WebDriverWait(driver, 15)

# รอให้การ์ดสินค้าขึ้นก่อน (li.builder-item)
rows = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.builder-item-list li.builder-item"))
)

data = []
for row in rows:
    try:
        # ✅ ชื่ออยู่ใน <div class="item-title"><a>...</a></div>
        name_el = row.find_element(By.CSS_SELECTOR, ".item-title a")
        name = name_el.get_attribute("textContent").strip()

        # ✅ ราคาอยู่ใน <div class="item-price">...</div> (บางที .text ว่าง ใช้ textContent)
        price_el = row.find_element(By.CSS_SELECTOR, ".item-price")
        price = price_el.get_attribute("textContent").strip()

        # ✅ สเปคโดนซ่อน(display:none) ต้องใช้ textContent อยู่แล้ว
        spec_el = row.find_element(By.CSS_SELECTOR, ".item-spec")
        spec = spec_el.get_attribute("textContent").strip()
        spec = " ".join(spec.split())

        data.append([name, spec, price])
        print("ชื่อ:", name, "สเปค:", spec, "ราคา:", price)

    except Exception as e:
        # อย่ากลืน error เงียบ ๆ ไม่งั้นจะดูเหมือนไม่มีอะไรเกิดขึ้น
        print("SKIP row เพราะ:", e)

driver.quit()

# บันทึก CSV
with open("practice_laptops.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "spec", "price"])
    writer.writerows(data)

print("saved -> practice_laptops.csv")





