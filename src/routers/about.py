# Python модули
from aiogram import Router, F
from aiogram.types import *


# Локальные модули
from messages import about as ms
from keyboards import about as kb


# Переменные
router = Router(name='about')


# Функции
@router.callback_query(F.data == 'about_main')
async def query_about_mods(query: CallbackQuery):
    await query.message.edit_text(
        text=ms.main,
        reply_markup=kb.main('about_main')
    )


@router.callback_query(F.data == 'about_mods')
async def query_about_mods(query: CallbackQuery):
    await query.message.edit_text(
        text=ms.mods,
        reply_markup=kb.main('about_mods')
    )


@router.callback_query(F.data == 'about_elyby')
async def query_about_mods(query: CallbackQuery):
    await query.message.edit_text(
        text=ms.elyby,
        reply_markup=kb.main('about_elyby')
    )


@router.callback_query(F.data == 'about_launcher')
async def query_about_mods(query: CallbackQuery):
    await query.message.edit_text(
        text=ms.launcher,
        reply_markup=kb.main('about_launcher')
    )


@router.callback_query(F.data == 'about_current')
async def query_about_current(query: CallbackQuery):
    await query.answer('Вы уже читаете об этом')
