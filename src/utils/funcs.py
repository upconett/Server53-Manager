# Локальные модули
from const import md_chars


# Функции
def escape_mdv2(text: str) -> str:
    """
    Форматирование текста для исключения конфликтов с MarkdownV2
    :param text: Текст для форматирования
    :return: Отформатированный текст
    """
    escaped_text = []

    for char in text:
        if char in md_chars:
            escaped_text.append(f'\\{char}')
        else:
            escaped_text.append(char)

    return ''.join(escaped_text)
