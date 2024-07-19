# Локальные модули
from utils.funcs import escape_mdv2


# Простые тексты
image_no_name = (
    'Получил картинку 🌄\n'
    'Хотите добавить её на сервер?'
)

image_naming = 'Введите название для картинки ✏️'

no_space = 'В названии не должно быть пробелов ❌'

not_unique = 'Картинка с таким названием уже есть ❌'


# Конфигурируемые тексты
def image_with_name(caption: str):
    name = escape_mdv2(caption)
    return f'Хотите добавить на сервер картинку под названием `{name}`?'


def image_success(name: str):
    name = escape_mdv2(name)
    return f'Картинка `{name}` на серверe ✅'
