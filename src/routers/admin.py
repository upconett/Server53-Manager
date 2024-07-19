from aiogram import Router, F
from aiogram.types import *
from aiogram.filters import *
from aiogram.fsm.context import FSMContext

from create_bot import rcon
from utils.filters import ElyBy, IsAdmin
from utils.exceptions import NoUserWithNick, IsSuperAdmin
from logic import core as logic_core
from logic import admin as logic
from messages import admin as ms
from keyboards import admin as kb 
from keyboards import core as kb_core


router = Router(name='admin')
router.message.filter(ElyBy(registered=True), IsAdmin())
router.callback_query.filter(ElyBy(registered=True), IsAdmin())


@router.message(CommandStart())
@router.message(F.text == 'Домой 🏠')
async def message_start(message: Message, state: FSMContext):
    user = message.from_user
    await logic_core.update_user(user)
    data = await state.get_data()

    u = await logic_core.get_user_data(user)

    if u.whitelisted_till: pr_text = u.whitelisted_till.strftime('%d.%m.%Y')
    else: pr_text = None

    to_del = await message.answer(
            text=ms.start_logged(u.nick, pr_text),
            reply_markup=kb.main_menu
        )

    await message.delete()
    await logic_core.delete_extra(user, data)

    data['start_id'] = to_del.message_id
    await state.set_data(data)


@router.message(F.text == 'Панель 🛠️')
async def message_admin_panel(message: Message, state: FSMContext):
    user = message.from_user
    await logic_core.update_user(user)
    
    is_super = await logic.is_admin(user.id, super=True)

    await message.answer(
        text=ms.admin_panel(super=is_super),
        reply_markup=kb.admin_panel(exc='admin_commands')
    )
    await message.delete()


@router.callback_query(F.data == 'admin_commands')
async def message_admin_panel(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await logic_core.update_user(user)
    
    is_super = await logic.is_admin(user.id, super=True)

    await query.message.edit_text(
        text=ms.admin_panel(super=is_super),
        reply_markup=kb.admin_panel(exc='admin_commands')
    )


@router.callback_query(F.data == 'admin_online')
async def query_players_online(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await logic_core.update_user(user)

    online = await logic.get_players(online=True)

    await query.message.edit_text(
        text=await ms.online(online),
        reply_markup=kb.admin_panel(exc='admin_online')
    )


@router.callback_query(F.data == 'admin_players')
async def query_players_online(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await logic_core.update_user(user)

    players = await logic.get_players()

    await query.message.edit_text(
        text=await ms.all_players(players),
        reply_markup=kb.admin_panel(exc='admin_players')
    )


@router.message(Command('access'), F.text.count(' ') > 0)
async def command_give_access(message: Message):
    user = message.from_user
    await logic_core.update_user(user)
    nick = message.text.split()[1]

    try:
        res_code = await logic.give_access(nick)
        await message.answer(
            text=ms.access_granted(nick, res_code),
            reply_markup=kb_core.back
        )
        await message.delete()
    except NoUserWithNick:
        await message.answer(
            text=ms.no_user_with_nick(nick),
            reply_markup=kb_core.back
        )
        await message.delete()


@router.message(Command('remove_access'), F.text.count(' ') > 0)
async def command_remove_access(message: Message):
    user = message.from_user
    await logic_core.update_user(user)
    nick = message.text.split()[1]

    try:
        await logic.remove_access(nick)
        await message.answer(
            text=ms.access_removed(nick),
            reply_markup=kb_core.back
        )
        await message.delete()
    except NoUserWithNick:
        await message.answer(
            test=ms.no_user_with_nick(nick),
            reply_markup=kb_core.back
        )
        await message.delete()
    

@router.message(Command('ban'), F.text.count(' ') > 0)
async def command_ban(message: Message):
    user = message.from_user
    await logic_core.update_user(user)
    nick = message.text.split()[1]
    reason = ' '.join(message.text.split()[2:])

    if not await logic.is_user(nick):
        await message.answer(
            text=ms.no_user_with_nick(nick),
            reply_markup=kb_core.back
        )
    else:
        await rcon.send_cmd(f'ban {nick} {reason}')
        await message.answer(
            text=ms.banned(nick, reason),
            reply_markup=kb_core.back
        )
    await message.delete()


@router.message(Command('unban'), F.text.count(' ') > 0)
async def command_unban(message: Message):
    user = message.from_user
    await logic_core.update_user(user)
    nick = message.text.split()[1]

    if not await logic.is_user(nick):
        await message.answer(
            text=ms.no_user_with_nick(nick),
            reply_markup=kb_core.back
        )
    else:
        await rcon.send_cmd(f'pardon {nick}')
        await message.answer(
            text=ms.unbanned(nick),
            reply_markup=kb_core.back
        )
    await message.delete()


@router.message(Command('admin'), F.text.count(' ') > 0)
async def command_admin(message: Message):
    user = message.from_user
    await logic_core.update_user(user)
    nick = message.text.split()[1]

    try:
        await logic.add_admin(nick)
        await rcon.send_cmd(f'op {nick}')
        await message.answer(
            text=ms.adminned(nick),
            reply_markup=kb_core.back
        )
    except NoUserWithNick:
        await message.answer(
            text=ms.no_user_with_nick(nick),
            reply_markup=kb_core.back
        )
    await message.delete()


@router.message(Command('super_admin'), F.text.count(' ') > 0)
async def command_super_admin(message: Message):
    user = message.from_user
    await logic_core.update_user(user)
    nick = message.text.split()[1]

    try:
        await logic.add_admin(nick, is_super=True)
        await rcon.send_cmd(f'op {nick}')
        await message.answer(
            text=ms.super_adminned(nick),
            reply_markup=kb_core.back
        )
    except NoUserWithNick:
        await message.answer(
            text=ms.no_user_with_nick(nick),
            reply_markup=kb_core.back
        )
    await message.delete()


@router.message(Command('remove_admin'), F.text.count(' ') > 0)
async def command_remove_admin(message: Message):
    user = message.from_user
    await logic_core.update_user(user)
    nick = message.text.split()[1]

    try:
        await logic.remove_admin(nick)
        await rcon.send_cmd(f'op {nick}')
        await message.answer(
            text=ms.unadminned(nick),
            reply_markup=kb_core.back
        )
    except NoUserWithNick:
        await message.answer(
            text=ms.no_user_with_nick(nick),
            reply_markup=kb_core.back
        )
    except IsSuperAdmin:
        await message.answer(
            text=ms.cant_unadmin(nick),
            reply_markup=kb_core.back
        )
    await message.delete()


@router.message(Command('block'), F.text.count(' ') > 0)
async def command_block(message: Message):
    user = message.from_user
    await logic_core.update_user(user)
    nick = message.text.split()[1]

    try:
        await logic.block_user(nick)
        await message.answer(
            text=ms.blocked(nick),
            reply_markup=kb_core.back
        )
    except NoUserWithNick:
        await message.answer(
            text=ms.no_user_with_nick(nick),
            reply_markup=kb_core.back
        )
    except IsSuperAdmin:
        await message.answer(
            text=ms.cant_block(nick),
            reply_markup=kb_core.back
        )
    await message.delete()


@router.message(Command('unblock'), F.text.count(' ') > 0)
async def command_block(message: Message):
    user = message.from_user
    await logic_core.update_user(user)
    nick = message.text.split()[1]

    try:
        await logic.unblock_user(nick)
        await message.answer(
            text=ms.unblocked(nick),
            reply_markup=kb_core.back
        )
    except NoUserWithNick:
        await message.answer(
            text=ms.no_user_with_nick(nick),
            reply_markup=kb_core.back
        )
    await message.delete()


@router.callback_query(F.data == 'admin_current')
async def query_about_current(query: CallbackQuery):
    await query.answer('Вы уже в этом разделе')
