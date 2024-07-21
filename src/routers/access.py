# Python модули
from aiogram import Router, F
from aiogram.types import *
from aiogram.fsm.context import FSMContext


# Локальные модули
from create_bot import bot
from logic import core as logic_core
from logic import access as logic
from messages import access as ms
from keyboards import core as kb


# Переменные
router = Router(name='access')


# Функции
@router.pre_checkout_query(F.invoice_payload.endswith('access'))
async def pre_checkout(pre_checkout_query: PreCheckoutQuery, user: User, state: FSMContext):
    data = await state.get_data()
    
    try:
        days = int(pre_checkout_query.invoice_payload.split('_')[0])
        await logic.buy_access(user, days)
        was_whitelisted = await logic_core.add_to_whitelist(user)

        u = await logic_core.get_user_data(user)
        data['access_till'] = u.access.whitelisted_till.strftime('%d.%m.%Y') if u.access else None
        data['was_whitelisted'] = was_whitelisted
        await state.set_data(data)
        await pre_checkout_query.answer(ok=True)
    except Exception as e:
        await pre_checkout_query.answer(ok=False, error_message=str(e))


@router.message(F.successful_payment)
async def successful_donation(message: Message, user: User, state: FSMContext):
    data = await state.get_data()

    till = data.get('access_till')
    was_whitelisted = data.get('was_whitelisted', False)

    if 'access_to_edit' in data:
        await bot.edit_message_text(
            chat_id=user.id,
            message_id=data['access_to_edit'],
            text=ms.success(till, was_whitelisted),
            reply_markup=kb.back
        )
    else:
        await message.answer(
            text=ms.success(till, was_whitelisted),
            reply_markup=kb.back
        )
