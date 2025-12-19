import streamlit as st

from session_state import (
    get_current_question,
    navigate_to_previous_question,
    navigate_to_next_question,
    toggle_answer
)


def render_main_content():
    """Рендерит основную зону"""
    if not st.session_state.selected_file:
        render_welcome_screen()
    else:
        render_question_screen()


def render_welcome_screen():
    """Экран приветствия (когда файл не выбран)"""
    st.title("Карточки для обучения")
    st.info("Выберите тему в боковой панели")


def render_question_screen():
    """Экран с вопросом"""
    questions = st.session_state.questions
    if not questions:
        render_no_questions()
        return
    render_question_header()
    render_question_card()
    render_navigation_panel()
    render_answer_section()


def render_no_questions():
    """Сообщение, если в файле нет вопросов"""
    st.error("В этом файле нет вопросов")


def render_question_header():
    """Заголовок с названием темы и номером вопроса"""
    file_name = st.session_state.selected_file.stem
    current_idx = st.session_state.q_index
    total_questions = len(st.session_state.questions)
    st.title(f"{file_name}")
    st.subheader(f"Вопрос {current_idx + 1} из {total_questions}")


def render_question_card():
    """Карточка с вопросом"""
    q = get_current_question()
    if q:
        st.info(q['question'])


def render_navigation_panel():
    """Панель навигации с кнопками"""
    col1, col2, col3 = st.columns(3)
    with col1:
        render_previous_button()
    with col2:
        render_answer_toggle()
    with col3:
        render_next_button()


def render_previous_button():
    """Кнопка 'Назад'"""
    idx = st.session_state.q_index
    if st.button("◀ Назад", disabled=idx == 0):
        navigate_to_previous_question()
        st.rerun()


def render_next_button():
    """Кнопка 'Вперед'"""
    idx = st.session_state.q_index
    questions = st.session_state.questions
    if st.button("Вперед ▶", disabled=(idx >= len(questions) - 1)):
        navigate_to_next_question()
        st.rerun()


def render_answer_toggle():
    """Кнопка показа/скрытия ответа"""
    btn_text = get_answer_button_text()
    btn_type = "secondary"
    if st.button(btn_text, type=btn_type):
        toggle_answer()
        st.rerun()


def get_answer_button_text():
    """Текст для кнопки ответа"""
    if st.session_state.show_answer:
        return "Скрыть ответ"
    return "Показать ответ"


def render_answer_section():
    """Секция с ответом (если показывается)"""
    if not st.session_state.show_answer:
        return
    q = get_current_question()
    if not q:
        return
    st.markdown("---")
    if q.get('short_answer'):
        render_short_answer(q['short_answer'])
    if q.get('full_answer'):
        render_full_answer(q['full_answer'])


def render_short_answer(text):
    """Отображает короткий ответ"""
    st.write("#### Короткий ответ:")
    st.write(text)
    if st.session_state.get('full_answer'):
        st.markdown("---")


def render_full_answer(text):
    """Отображает развернутый ответ"""
    st.write("#### Развернутый ответ:")
    st.write(text)
