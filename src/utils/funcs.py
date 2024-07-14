from const import md_chars

def escape_mdv2(text):
    escaped_text = []

    for char in text:
        if char in md_chars:
            escaped_text.append(f'\\{char}')
        else:
            escaped_text.append(char)

    return ''.join(escaped_text)