import streamlit as st
import easyocr
import numpy as np
from PIL import Image

st.set_page_config(page_title="Food Scanner AI", page_icon="🥗")

harmful_ingredients = {
    "bg": {
        "E621": "Натриев глутамат (MSG) - Може да причини главоболие и алергични реакции.",
        "E407": "Карагенан - Свързва се с храносмилателни възпаления.",
        "E250": "Натриев нитрит - Потенциален канцероген, използва се в колбаси.",
        "E951": "Аспартам - Изкуствен подсладител, обект на дискусии за невротоксичност.",
        "E171": "Титанов диоксид - Забранен в ЕС като хранителна добавка (риск за ДНК).",
        "ПАЛМОВО МАСЛО": "Високо съдържание на наситени мазнини; риск за сърдечно-съдовата система.",
        "ХИДРОГЕНИРАНИ": "Трансмазнини - Повишават лошия холестерол (LDL).",
        "FRUCTOSE SYRUP": "Глюкозо-фруктозен сироп - Риск от затлъстяване и диабет.",
        "E102": "Тартразин - Изкуствен оцветител, свързан с хиперактивност при деца."
    },
    "en": {
        "E621": "Monosodium Glutamate (MSG) - May cause headaches and allergic reactions.",
        "E407": "Carrageenan - Linked to digestive tract inflammation.",
        "E250": "Sodium Nitrite - Potential carcinogen, common in processed meats.",
        "E951": "Aspartame - Artificial sweetener; potential neurotoxicity concerns.",
        "E171": "Titanium Dioxide - Banned in EU (genotoxicity concerns).",
        "PALM OIL": "High saturated fats; concerns for heart health.",
        "HYDROGENATED": "Trans fats - Increases risk of heart disease and LDL cholesterol.",
        "FRUCTOSE SYRUP": "High Fructose Corn Syrup - Linked to obesity and metabolic issues.",
        "E102": "Tartrazine - Linked to hyperactivity in children."
    }
}

# Функция за разпознаване на текст
@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])
reader = load_reader()

st.title("🔍 Скенер за вредни съставки")
st.write("Качете снимка на етикета със съдържанието, за да проверим за опасни добавки.")

lang = st.radio("Изберете език на интерфейса / Choose language:", ("BG", "EN"))

label_upload = "Качете снимка (JPG, PNG)" if lang == "BG" else "Upload an image (JPG, PNG)"
label_analysis = "Анализиране..." if lang == "BG" else "Analyzing..."
label_results = "Резултати от анализа:" if lang == "BG" else "Analysis Results:"
label_no_harmful = "✅ Не са открити критични вредни съставки от списъка." if lang == "BG" else "✅ No critical harmful ingredients found from the list."

uploaded_file = st.file_uploader(label_upload, type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качена снимка', use_container_width=True)
    
    with st.spinner(label_analysis):
        # Конвертиране за EasyOCR
        img_array = np.array(image)
        results = reader.readtext(img_array, detail=0)
        full_text = " ".join(results).upper()

    st.subheader(label_results)
    
    found_any = False
    current_db = harmful_ingredients["bg"] if lang == "BG" else harmful_ingredients["en"]
    
  for key description in current_db.items():
    if key in full_text:
    st.error(f"⚠️ **{key}**: {description}")
            found_any = True
            
    if not found_any:
        st.success(label_no_harmful)

    with st.expander("Виж разпознатия текст (Raw Text)"):
        st.write(full_text)
