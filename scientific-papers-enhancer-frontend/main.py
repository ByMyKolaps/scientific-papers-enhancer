import streamlit as st
import requests
import pyperclip
from datetime import datetime
from config import API_URL, MAX_WORDS

st.title("Автоматическое улучшение научных текстов")

# Описание
st.write("""
Преобразуйте свой разговорный текст в профессиональный академический стиль с помощью нашего продвинутого ИИ-редактора.
""")

# Разделение на две колонки
col1, col2 = st.columns(2)

# Левая колонка - ввод текста
with col1:
    st.subheader("Введите ваш текст")
    
    # Выбор языка
    language = st.selectbox("Выберите язык:", ["Русский", "Английский"])
    
    # Поле для ввода текста
    user_input = st.text_area(
        "Вставьте сюда ваш разговорный текст...",
        height=200,
        value="Я думаю, что изменение климата - это большая проблема..."
    )
    
    # Счетчик слов
    word_count = len(user_input.split()) if user_input else 0
    st.write(f"Количество слов: {word_count}. Максимум: {MAX_WORDS} слов")

    # Кнопка преобразования
    if st.button("Преобразовать"):
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
                            "text": user_input
                            # "language": language
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

# Правая колонка - результат
with col2:
    st.subheader("Результат в академическом стиле")
    
    if 'processed_text' in st.session_state:
        st.write(st.session_state.processed_text)
        
        # Отображение времени обработки
        if 'last_processed' in st.session_state:
            st.caption(f"Обработано в {st.session_state.last_processed}")
        
        # Кнопки для копирования и скачивания
        col_copy, col_download = st.columns(2)
        with col_copy:
            if st.button("Копировать"):
                pyperclip.copy(st.session_state.processed_text)
                st.success("Текст скопирован в буфер обмена!") 
        with col_download:
            st.download_button(
                label="Скачать",
                data=st.session_state.processed_text,
                file_name="enhanced_text.txt",
                mime="text/plain"
            )
    else:
        st.info("Здесь будет отображен преобразованный текст после обработки.")
