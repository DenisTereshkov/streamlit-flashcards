import streamlit as st
from md_parser import get_markdown_files, parse_questions

st.set_page_config(layout="wide")


if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0


md_files = get_markdown_files()

# САЙДБАР
with st.sidebar:
    st.title("Темы")

    for file_path in md_files:
        file_name = file_path.stem

        if st.button(file_name, key=f"btn_{file_name}"):
            content = file_path.read_text(encoding='utf-8')
            questions = parse_questions(content)

            st.session_state.selected_file = file_path
            st.session_state.questions = questions
            st.session_state.q_index = 0
            st.rerun()

    if st.session_state.selected_file:
        st.markdown("---")
        for i, q in enumerate(st.session_state.questions):
            if st.button(f"{i+1}. {q['question']}", key=f"q_btn_{i}", type="tertiary"):
                st.session_state.q_index = i
                st.rerun()

# ОСНОВНАЯ ЗОНА
st.title("Вопрос")

if not st.session_state.selected_file:
    st.info("Выберите тему слева")
else:
    questions = st.session_state.questions
    idx = st.session_state.q_index
    if not questions:
        st.error("В файле нет вопросов")
    else:
        q = questions[idx]
        st.header(f"Вопрос {idx + 1} из {len(questions)}")
        st.subheader(q['question'])

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("◀ Назад") and idx > 0:
                st.session_state.q_index = idx - 1
                st.rerun()

        with col2:
            if 'show_answer' not in st.session_state:
                st.session_state.show_answer = False

            if st.session_state.show_answer:
                btn_text = "Скрыть ответ"
                btn_type = "secondary"
            else:
                btn_text = "Показать ответ"
                btn_type = "secondary"

            if st.button(btn_text, type=btn_type):
                st.session_state.show_answer = not st.session_state.show_answer
                st.rerun()

        with col3:
            if st.button("Вперед ▶") and idx < len(questions) - 1:
                st.session_state.q_index = idx + 1
                st.rerun()

        if st.session_state.show_answer:
            st.markdown("---")
            if q['short_answer']:
                st.write("#### **Короткий ответ:**")
                st.write(q['short_answer'])
            if q['full_answer']:
                st.write("#### **Полный ответ:**")
                st.write(q['full_answer'])
