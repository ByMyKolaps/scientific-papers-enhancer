from dotenv import load_dotenv
import os
import streamlit as st
import requests
import pyperclip
from datetime import datetime

def clear_text():
    st.session_state.user_input = ""
    st.session_state.processed_text = ""

# Маппинг языков для интерфейса и API
LANGUAGE_MAPPING = {
    "Русский": "ru",
    "Английский": "eng"
}

# Загрузка конфигурации
load_dotenv()

API_URL = os.getenv("API_URL")
MAX_WORDS = int(os.getenv("MAX_WORDS"))


# Настройка отображения во вкладке браузера
st.set_page_config(
    page_title="Scihancer",
    page_icon="🧪")

# Кастомные стили
st.markdown(
    """
    <style>
    .main > div {
        max-width: 80%;
        padding: 1rem 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Описание
st.title("Автоматическое улучшение научных текстов")
st.write("""
Преобразуйте свой разговорный текст в профессиональный академический стиль с помощью нашего продвинутого ИИ-редактора.
""")

# Выбор языка
selected_display_language = st.selectbox(
        "Выберите язык:", 
        list(LANGUAGE_MAPPING.keys())
    )
language_code = LANGUAGE_MAPPING[selected_display_language]

# Разделение на две колонки
col1, col2 = st.columns(2)

# Левая колонка - ввод текста
with col1:
    st.subheader("Введите ваш текст")
        
    # Поле для ввода текста
    user_input = st.text_area(
        "Вставьте сюда ваш разговорный текст...",
        height=300,
        value="Я думаю, что изменение климата - это большая проблема...",
        key="user_input",
        label_visibility="collapsed",
        placeholder="Введите текст для преобразования...",
        help="Введите текст, который вы хотите преобразовать в академический стиль. Максимум 1000 слов."
    )
    
    # Счетчик слов
    word_count = len(user_input.split()) if user_input else 0
    st.caption(f"Количество слов: {word_count}. Максимум: {MAX_WORDS} слов")

    col_transform, col_clear = st.columns(2)
    with col_transform:
    # Кнопка преобразования
        if st.button("Преобразовать 🚀", type="primary", use_container_width=True):
            if user_input:
                if word_count > MAX_WORDS:
                        st.error(f"Превышен максимальный объем текста ({word_count} > {MAX_WORDS} слов). Сократите текст и попробуйте снова.")
                else:
                    # Сброс предыдущего результата
                    st.session_state.processed_text = ""
                    st.session_state.last_processed = None
                    with st.spinner("Обработка текста..."):
                        try:
                            # Подготовка данных для API
                            payload = {
                                "text": user_input,
                                "language": language_code
                            }
                            
                            # Отправка запроса к API
                            response = requests.post(
                                API_URL,
                                json=payload,
                                headers={"Content-Type": "application/json"}
                            )
                            
                            # Проверка ответа
                            if response.status_code == 200:
                                result = response.json()
                                st.session_state.processed_text = result.get("text", "")
                                st.session_state.last_processed = datetime.now().strftime("%H:%M:%S")
                            else:
                                st.error(f"Ошибка API: {response.status_code} - {response.text}")
                                
                        except requests.exceptions.RequestException as e:
                            st.error(f"Ошибка соединения с API: {str(e)}")
            else:
                st.warning("Пожалуйста, введите текст для преобразования")
    with col_clear:
        st.button("Очистить 🧹", on_click=clear_text, use_container_width=True)


# Правая колонка - результат
with col2:
    st.subheader("Результат в академическом стиле")
    
    if 'processed_text' in st.session_state and st.session_state.processed_text != "":
        st.markdown(
            f"""
            <div style="
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 10px;
                border-left: 4px solid #3498db;
                min-height: 300px;
                margin-bottom: 1.1rem;
                placeholder: 'Здесь будет отображен преобразованный текст после обработки...';
            ">
            {st.session_state.processed_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Альтернативный вариант отображения результата
        # st.text_area(
        #     "Результат", 
        #     value=st.session_state.processed_text,
        #     height=300,
        #     key="result_area",
        #     label_visibility="collapsed",
        #     disabled=True,
        # )
        
        # Отображение времени обработки
        if 'last_processed' in st.session_state:
            st.caption(f"Обработано в {st.session_state.last_processed}")
        
        col_copy, col_download = st.columns([1, 1])
        with col_copy:
            if st.button("Копировать 📝", use_container_width=True):
                pyperclip.copy(st.session_state.processed_text)
                st.success("Текст скопирован в буфер обмена!") 
        with col_download:
            st.download_button(
                label="Скачать 💾",
                data=st.session_state.processed_text,
                file_name="enhanced_text.txt",
                mime="text/plain",
                key="download_button",
                use_container_width=True
            )
    else:
        st.info("Здесь будет отображен преобразованный текст после обработки.")
