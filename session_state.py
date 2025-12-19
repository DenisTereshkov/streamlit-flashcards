import streamlit as st


def init_session_state():
    """Инициализирует все состояния приложения"""
    defaults = {
        'selected_file': None,
        'questions': [],
        'q_index': 0,
        'show_answer': False,
        'dark_mode': False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def update_selected_file(file_path, questions, index=0):
    """
    Обновляет выбранный файл и вопросы
    Args:
        file_path: Path к файлу
        questions: список вопросов
        index: начальный индекс вопроса
    """
    st.session_state.selected_file = file_path
    st.session_state.questions = questions
    st.session_state.q_index = index
    st.session_state.show_answer = False


def navigate_to_previous_question():
    """Переход к предыдущему вопросу"""
    if st.session_state.q_index > 0:
        st.session_state.q_index -= 1
        st.session_state.show_answer = False


def navigate_to_next_question():
    """Переход к следующему вопросу"""
    if st.session_state.q_index < len(st.session_state.questions) - 1:
        st.session_state.q_index += 1
        st.session_state.show_answer = False


def toggle_answer():
    """Переключает показ ответа"""
    st.session_state.show_answer = not st.session_state.show_answer


def toggle_dark_mode():
    """Переключает тёмную тему"""
    st.session_state.dark_mode = not st.session_state.dark_mode


def get_current_question():
    """Возвращает текущий вопрос или None"""
    questions = st.session_state.questions
    idx = st.session_state.q_index
    if questions and 0 <= idx < len(questions):
        return questions[idx]
    return None
