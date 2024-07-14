from aiogram import Router, F
from aiogram.types import *
from aiogram.fsm.context import FSMContext

from create_bot import bot
from logic import core as logic
from messages import donation as ms
from keyboards import core as kb


router = Router(name='donation')


@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery, state: FSMContext):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_donation(message: Message, state: FSMContext):
    user = message.from_user
    await logic.update_user(user)

    data = await state.get_data()

    if 'donation_to_edit' in data:
        await bot.edit_message_text(
            chat_id=user.id,
            message_id=data['donation_to_edit'],
            text=ms.thanks,
            reply_markup=kb.back
        )
    else:
        await message.answer(
            text=ms.thanks,
            reply_markup=kb.back
        )
