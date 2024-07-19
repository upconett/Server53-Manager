# Конфигурируемые тексты
def success(till: str, was_whitelisted: bool) -> str:
    wh_text = 'Вы уже добавлены в WhiteList' if was_whitelisted else 'Теперь вы добавлены в WhiteList'
    return (
        f'Подписка продлена до {till} ⭐\n'
        f'{wh_text}\n'
        'Играйте с удовольствием ☺️'
    )
