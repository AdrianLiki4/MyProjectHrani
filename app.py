import streamlit as st
import easyocr
import numpy as np
from PIL import Image

st.set_page_config(page_title="Food Scanner AI", page_icon="🥗")

harmful_ingredients = {
    "BG": {
        "E621": "Натриев глутамат", "E407": "Карагенан", "E250": "Натриев нитрит",
        "ПАЛМОВО МАСЛО": "Палмово масло", "ХИДРОГЕНИРАНИ": "Трансмазнини"
    },
    "EN": {
        "E621": "MSG", "E407": "Carrageenan", "E250": "Sodium Nitrite",
        "PALM OIL": "Palm Oil", "HYDROGENATED": "Trans fats"
    }
}

@st.cache_resource
def load_reader():
    # Ако тук даде грешка, значи липсва torch или torchvision
    return easyocr.Reader(['bg', 'en'], gpu=False) # gpu=False за по-голяма съвместимост

try:
    reader = load_reader()

    st.title("🔍 Скенер за вредни съставки")
    lang = st.radio("Език / Language:", ("BG", "EN"))

    uploaded_file = st.file_uploader("Качете снимка / Upload image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Снимка', use_container_width=True)
        
        with st.spinner("Анализиране..."):
            img_array = np.array(image.convert('RGB')) # Подсигуряваме RGB формат
            results = reader.readtext(img_array, detail=0)
            full_text = " ".join(results).upper()

        st.subheader("Резултати:")
        found_any = False
        db = harmful_ingredients[lang]
        
        for key, description in db.items():
            if key in full_text:
                st.error(f"⚠️ **{key}**: {description}")
                found_any = True
                
        if not found_any:
            st.success("✅ Не са открити критични съставки.")

        with st.expander("Виж текста"):
            st.write(full_text)

except Exception as e:
    st.error(f"Възникна техническа грешка: {e}")
