from database.dataclasses import User as UserDC
from logic import admin as logic


def start_logged(nick: str, pr_text: str | None) -> str:
    if pr_text:
        pr = f'Проходка до {pr_text} 🗝️\nВы администратор 🛠️'
    else:
        pr = 'Но нужна проходка 🔒\nДаже если вы администратор 🛠️'
    return (
        f'<b>С возвращением, {nick} 😄</b>\n\n'
        'Адрес сервера всё тот же:\n'
        '<code>mc.server53.ru</code>\n\n'
        f'{pr}'
    )


def admin_panel(super: bool = False) -> str:
    com_text = (
        '• <code>/access</code> - даровать проходку (1 месяц)\n'
        '• <code>/remove_access</code> - отобрать проходку\n'
        '• <code>/ban</code> - забанить\n'
        '• <code>/unban</code> - разбанить\n\n'
    )
    if super:
        s_text = 'Супер Админ Панель 👑\n<blockquote>Пользоваться осторожно</blockquote>\n'
        com_text += (
            '• <code>/admin</code> - сделать админом\n'
            '• <code>/super_admin</code> - сделать <b><i>супер</i></b> админом\n'
            '• <code>/remove_admin</code> - разжаловать\n'
            '• <code>/block</code> - запретить пользоваться ботом\n'
            '• <code>/unblock</code> - разрешить пользоваться ботом\n'
        )
    else:
        s_text = 'Админ Панель 🛠️\n<blockquote>Не зазнавайтесь</blockquote>\n'
    return (
        f'{s_text}\n'
        '<b>Команды:</b>\n'
        f'{com_text}\n'
    )
    

async def online(players: list[UserDC]) -> str:
    message = 'Игроки онлайн 🕹️\n\n'
    p_text = []
    for p in players:
        if p.nick is None: continue
        is_admin = await logic.is_admin(p.id)
        is_super = await logic.is_admin(p.id, super=True)
        icon = '👑' if is_super else '🛠️' if is_admin else '👤'
        p_text.append(f'{icon} <code>{p.nick}</code> - <a href="tg://user?id={p.id}">{p.username if p.username else p.first_name}</a>\n')
    p_text = logic.sort_users_by_icon(p_text)
    for p in p_text: message += p
    return message


async def all_players(players: list[UserDC]) -> str:
    message = 'Все игроки 👥\n\n'
    p_text = []
    for p in players:
        if p.nick is None: continue
        is_admin = await logic.is_admin(p.id)
        is_super = await logic.is_admin(p.id, super=True)
        icon = '👑' if is_super else '🛠️' if is_admin else '👤'
        access = '🔒' if p.whitelisted_till is None else f'🗝️ ({p.whitelisted_till.strftime("%d.%m.%Y")})'
        p_text.append(f'{icon} <code>{p.nick}</code> - ' + (f'@{p.username}' if p.username else f'<a href="tg://user?id={p.id}"<a href="tg://user?id={p.id}">{p.first_name}</a>') + f' {access}\n')
    p_text = logic.sort_users_by_icon(p_text)
    for p in p_text: message += p
    return message


def no_user_with_nick(nick: str) -> str:
    return f'У нас нет игрока с ником <code>{nick}</code> ❌'


def access_granted(nick: str, result_code: bool) -> str:
    if result_code:
        return f'Проходка для <code>{nick}</code> продлена ✅'
    else:
        return f'Проходка выдана игроку <code>{nick}</code> ✅'


def access_removed(nick: str) -> str:
    return f'Проходка изъята у игрока <code>{nick}</code> ✅'


def banned(nick: str, reason: str = None) -> str:
    if reason:
        return f'Игрок {nick} забанен с сервера 🚫\nПо причине:\n<i>{reason}</i>'
    return f'Игрок {nick} забанен с сервера 🚫'


def unbanned(nick: str) -> str:
    return f'Игрок {nick} разбанен на сервере 🕊️'


def adminned(nick: str) -> str:
    return f'Игрок {nick} становится администратором 🛠️'


def super_adminned(nick: str) -> str:
    return f'Игрок {nick} становится супер-админом 👑'


def unadminned(nick: str) -> str:
    return f'Игрок {nick} разжалован с должности администратора 🕊️'


def cant_unadmin(nick: str) -> str:
    return f'Вы не можете разжаловать супер-админа {nick} ❌\n<blockquote>Вам об этом кто-нибудь говорил..?</blockquote>'


def blocked(nick: str) -> str:
    return f'Игроку {nick} теперь запрещено пользоваться ботом 🚫'


def unblocked(nick: str) -> str:
    return f'Игрок {nick} снова может пользоваться ботом ✅'


def cant_block(nick: str) -> str:
    return f'Вы не можете заблокировать супер-админа {nick} ❌\n<blockquote>Вам об этом кто-нибудь говорил...?</blockquote>'