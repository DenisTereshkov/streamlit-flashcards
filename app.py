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
if not st.session_state.selected_file and md_files:
    first_file = md_files[0]
    content = first_file.read_text(encoding='utf-8')
    questions = parse_questions(content)
    st.session_state.selected_file = first_file
    st.session_state.questions = questions
    st.session_state.q_index = 0


# САЙДБАР
with st.sidebar:
    st.title("Темы")

    for file_path in md_files:
        file_name = file_path.stem
        with st.expander(f"{file_name}", expanded=False):
            content = file_path.read_text(encoding='utf-8')
            questions = parse_questions(content)
            for i, q in enumerate(questions):
                q_text = q['question']
                if st.button(
                    f"• {q_text}",
                    key=f"{file_name}_q{i}",
                    type="secondary" if st.session_state.selected_file != file_path or st.session_state.q_index != i else "primary",
                    use_container_width=True
                ):
                    st.session_state.selected_file = file_path
                    st.session_state.questions = questions
                    st.session_state.q_index = i
                    st.session_state.show_answer = False
                    st.rerun()

# ОСНОВНАЯ ЗОНА
if st.session_state.selected_file:
    file_name = st.session_state.selected_file.stem
    current_idx = st.session_state.q_index
    total_questions = len(st.session_state.questions)
    page_title = f"{file_name}"
    st.title(page_title)
else:
    st.title("Карточки для обучения")

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
                st.session_state.show_answer = False
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
                st.session_state.show_answer = False
                st.rerun()

        if st.session_state.show_answer:
            st.markdown("---")
            if q['short_answer']:
                st.write("#### **Короткий ответ:**")
                st.write(q['short_answer'])
            if q['full_answer']:
                st.write("#### **Полный ответ:**")
                st.write(q['full_answer'])
