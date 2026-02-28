import streamlit as st
import pandas as pd
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบแนะนำคอมเซ็ท", layout="centered")

# 1. หน้าเว็บมีหัวข้อว่า "ระบบแนะนำคอมเซ็ทตามงบประมาณ"
st.title("ระบบแนะนำคอมเซ็ทตามงบประมาณ")

# 2. มีตัวเลือกสไตล์การใช้งาน
style_option = st.selectbox(
    "เลือกสไตล์การใช้งาน",
    ["เล่นเกม", "สายครีเอเตอร์ / กราฟฟิก / ตัดต่อ", "ทำงานใช้งานทั่วไป"]
)

# 3. มีตัวเลือกงบประมาณ ใช้ Slider ตั้งแต่ 10,000 ถึง 200,000 บาท
budget = st.slider("เลือกงบประมาณ (บาท)", min_value=10000, max_value=200000, value=30000, step=1000)

# 4. มีปุ่ม "ค้นหา" หรือ "ประมวลผล"
if st.button("ค้นหา"):
    # 5. เลือกไฟล์ CSV ตามสไตล์ที่เลือก
    file_mapping = {
        "เล่นเกม": "comset_game.csv",
        "สายครีเอเตอร์ / กราฟฟิก / ตัดต่อ": "comset_Creator.csv",
        "ทำงานใช้งานทั่วไป": "comset_officer.csv"
    }
    
    filename = file_mapping[style_option]
    # ใช้ path แบบ relative เพราะตอนรัน streamlit จะอยู่ในโฟลเดอร์เดียวกัน
    
    if os.path.exists(filename):
        # 7. อ่านไฟล์ CSV ด้วย pandas
        try:
            df = pd.read_csv(filename)
            
            # แปลง price เป็นตัวเลข
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            
            # กรองข้อมูลเฉพาะสินค้าที่มีราคา <= งบประมาณที่เลือก
            filtered_df = df[df['price'] <= budget]
            
            # เรียงสินค้าจากราคาน้อยไปมาก
            filtered_df = filtered_df.sort_values(by='price', ascending=True)
            
            # 9. แสดงจำนวนสินค้าที่พบ
            count = len(filtered_df)
            
            if count > 0:
                st.success(f"พบสินค้า {count} รายการ")
                
                # 8. แสดงผลลัพธ์บนหน้าเว็บในรูปแบบตาราง
                # เตรียมข้อมูลสำหรับแสดงผล
                display_df = filtered_df.copy()
                display_df['price'] = display_df['price'].map('{:,.0f}'.format)
                display_df.columns = ['ชื่อสินค้า', 'ราคา (บาท)']
                
                # รีเซ็ต index ก่อน
                display_df = display_df.reset_index(drop=True)
                
                # ให้เริ่มที่ 1
                display_df.index = range(1, len(display_df) + 1)
                
                # แสดงตาราง
                st.dataframe(display_df)

            else:
                # 10. ถ้าไม่พบสินค้า
                st.warning("ไม่พบสินค้าที่อยู่ในงบประมาณนี้")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการอ่านข้อมูล: {e}")
    else:
        st.error(f"ไม่พบไฟล์ข้อมูล: {filename}")

# ส่วนท้าย
st.markdown("---")
st.caption("จัดทำโดยระบบแนะนำคอมพิวเตอร์อัจฉริยะ")




