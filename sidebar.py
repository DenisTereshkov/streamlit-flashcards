import streamlit as st

from md_parser import get_markdown_files, parse_questions
from session_state import update_selected_file


def render_sidebar():
    """Рендерит всю боковую панель"""
    with st.sidebar:
        render_sidebar_header()
        render_file_list()


def render_sidebar_header():
    """Заголовок сайдбара"""
    st.title("Темы")
    st.markdown("---")


def render_file_list():
    """Список файлов с вопросами"""
    md_files = get_markdown_files()
    for file_path in md_files:
        render_file_expander(file_path)


def render_file_expander(file_path):
    """Рендерит аккордеон для одного файла"""
    file_name = file_path.stem
    is_expanded = is_file_selected(file_path)
    with st.expander(f"{file_name}", expanded=is_expanded):
        render_questions_list(file_path, file_name)


def is_file_selected(file_path):
    """Проверяет, выбран ли файл"""
    if not st.session_state.selected_file:
        return False
    return st.session_state.selected_file == file_path


def render_questions_list(file_path, file_name):
    """Рендерит список вопросов для файла"""
    content = file_path.read_text(encoding='utf-8')
    questions = parse_questions(content)
    for i, q in enumerate(questions):
        render_question_button(file_path, file_name, q, i, questions)


def render_question_button(file_path, file_name, question, index, questions):
    """Рендерит кнопку для одного вопроса"""
    q_text = question['question']
    if len(q_text) > 50:
        q_text = q_text[:50] + "..."
    btn_type = get_button_type(file_path, index)
    if st.button(
        f"• {q_text}",
        key=f"{file_name}_q{index}",
        type=btn_type,
        use_container_width=True
    ):
        update_selected_file(file_path, questions, index)
        st.rerun()


def get_button_type(file_path, index):
    """Определяет тип кнопки (primary для текущего вопроса)"""
    is_current_file = (st.session_state.selected_file == file_path)
    is_current_question = (st.session_state.q_index == index)
    if is_current_file and is_current_question:
        return "primary"
    return "secondary"
