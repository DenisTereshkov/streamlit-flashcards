from pathlib import Path
from typing import List, Dict


def get_markdown_files(folder: str = "cards") -> List[Path]:
    """
    Возвращает список .md файлов в папке.
    Args: folder (str): Имя папки с файлами (по умолчанию "cards").
    Returns: List[Path]: Список путей к .md файлам.
    """

    cards_dir = Path(folder)
    return list(cards_dir.glob("*.md"))


def parse_questions(content: str) -> List[Dict]:
    """
    Парсит .md файл и возвращает список словарей с вопросами и ответами.

    Структура файла:
    # Заголовок темы (игнорируется)

    ### Вопрос 1
    #### Короткий ответ
    Текст ответа...
    #### Развернутый ответ
    Текст ответа...

    ### Вопрос 2
    #### Короткий ответ
    Текст ответа...
    #### Развернутый ответ
    Текст ответа...



    Args: content (str): Содержимое .md файла.
    Returns: List[Dict]: Список словарей с вопросами и ответами.
    """
    questions = []
    lines = content.split('\n')
    current_question = None
    current_short_answer = []
    current_full_answer = []
    in_short_answer = False
    in_full_answer = False
    for line in lines:
        line = line.rstrip()
        if line.startswith('### '):
            if current_question is not None:
                questions.append({
                    'question': current_question,
                    'short_answer': '\n'.join(current_short_answer).strip(),
                    'full_answer': '\n'.join(current_full_answer).strip()
                })
            current_question = line[4:].strip()
            current_short_answer = []
            current_full_answer = []
            in_short_answer = False
            in_full_answer = False
        elif line.startswith('#### Короткий ответ'):
            in_short_answer = True
            in_full_answer = False
        elif line.startswith('#### Развернутый ответ'):
            in_short_answer = False
            in_full_answer = True
        elif current_question is not None and line:
            if in_short_answer:
                current_short_answer.append(line)
            elif in_full_answer:
                current_full_answer.append(line)
    if current_question is not None:
        questions.append({
            'question': current_question,
            'short_answer': '\n'.join(current_short_answer).strip(),
            'full_answer': '\n'.join(current_full_answer).strip()
        })
    return questions
