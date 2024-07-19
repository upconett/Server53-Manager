# Необходимые переменные окружения
env_variables = [
    'BOT_TOKEN', 'BOT_USERNAME', 'DBFILE', 
    'IMAGEMAPS_PATH', 'RCON_HOST', 'RCON_PORT', 
    'RCON_PASSWORD', 'ACCESS_CHECK_FREQUENCY'
]

# Символы, которые нужно переформатировать
md_chars = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', 
    '*', '+', ',', '-', '.', '/', ':', ';', '<',
    '=', '>', '?', '@', '[', '\\', ']', '^', '_', 
    '`', '{', '|', '}', '~'
]

# Ссылка авторизации через Ely.by
elyby_url = 'https://account.ely.by/oauth2/v1?client_id=server53bot&redirect_uri=https://auth.server53.ru/oauth&response_type=code&scope=account_info'

# << Что-то >>
# Это секции для about вкладки, 
# прописывай их сюда и будут 
# появляться соответсвующие инлайн кнопки
about_sections = {
    'about_main': 'О Нас',
    'about_mods': 'Моды',
    'about_elyby': 'Ely.by',
    'about_launcher': 'Лаунчер'
}

admin_sections = {
    'admin_commands': 'Команды',
    'admin_online': 'Онлайн',
    'admin_players': 'Игроки'
}
