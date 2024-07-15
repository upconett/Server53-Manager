from aiogram import Router, F
from aiogram.types import *
from aiogram.filters import *

from messages import about as ms
from keyboards import about as kb


router = Router(name='about')


@router.callback_query(F.data == 'about_main')
async def query_about_mods(query: CallbackQuery):
    await query.message.edit_text(
        text=ms.main,
        reply_markup=kb.main('about_main'),
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

@router.callback_query(F.data == 'about_mods')
async def query_about_mods(query: CallbackQuery):
    await query.message.edit_text(
        text=ms.mods,
        reply_markup=kb.main('about_mods'),
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )
