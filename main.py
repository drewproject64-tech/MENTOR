"""ASISTENTE MR MENTOR — Spanish educational Telegram bot (aiogram 3)."""

import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from planner import make_plan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = Router()

# TELEGRAM PROFILE: configured automatically every time the bot starts.
# BOT_ABOUT is the short About text (Telegram limit: 120 characters).
# BOT_DESCRIPTION is the full description users see before starting (limit: 512).
BOT_NAME = "ASISTENTE MR MENTOR"
BOT_ABOUT = (
    "Organiza tus estudios con planes de 30, 60 o 90 minutos, "
    "consejos prácticos y ayuda en español."
)
BOT_DESCRIPTION = (
    "ASISTENTE MR MENTOR es un bot educativo en español para planificar "
    "sesiones de estudio. Pulsa «Crear plan», escribe "
    "una materia o tema y elige una duración de 30, 60 o 90 minutos. "
    "Recibirás un horario con bloques de lectura, práctica, pausas y repaso. "
    "En «Consejo de estudio» encontrarás sugerencias para organizarte y "
    "repasar mejor. «Ayuda» explica las funciones "
    "y comandos disponibles. Es una herramienta de organización, no "
    "un sustituto de la enseñanza. No requiere pagos ni enlaces externos."
)

WELCOME = (
    "¡Bienvenido a ASISTENTE MR MENTOR!\n\n"
    "Este bot te ayuda a organizar el tiempo de estudio. Escribe un tema, "
    "elige una sesión de 30, 60 o 90 minutos y recibe un plan por etapas.\n\n"
    "También puedes leer consejos prácticos o consultar las instrucciones.\n"
    "Selecciona una de las tres opciones para comenzar."
)
TIPS = [
    "Empieza con un objetivo concreto, como resolver cinco ejercicios.",
    "Después de estudiar, explica el tema con tus propias palabras.",
    "Alterna lectura y preguntas prácticas para comprobar lo que recuerdas.",
    "Prepara tus materiales y evita cambiar de tarea constantemente.",
    "Dedica los últimos minutos a resumir las ideas principales.",
    "Si un ejercicio se complica, anota la duda y continúa con otra actividad.",
]

MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Crear plan")],
        [KeyboardButton(text="Consejo de estudio")],
        [KeyboardButton(text="Ayuda")],
    ],
    resize_keyboard=True,
    is_persistent=True,
)
DURATIONS = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="30 min", callback_data="duration:30"),
        InlineKeyboardButton(text="60 min", callback_data="duration:60"),
        InlineKeyboardButton(text="90 min", callback_data="duration:90"),
    ]]
)


class PlanFlow(StatesGroup):
    waiting_topic = State()
    waiting_duration = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(WELCOME, reply_markup=MENU)


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Acción cancelada. Elige una opción del menú.", reply_markup=MENU)


@router.message(Command("about"))
async def about(message: Message):
    await message.answer(BOT_DESCRIPTION, reply_markup=MENU)


@router.message(Command("help"))
@router.message(F.text == "Ayuda")
async def help_text(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Cómo usar ASISTENTE MR MENTOR:\n"
        "1. Pulsa «Crear plan».\n"
        "2. Escribe una materia o un tema (entre 2 y 80 caracteres).\n"
        "3. Selecciona 30, 60 o 90 minutos.\n"
        "4. Sigue los bloques del plan a tu ritmo.\n\n"
        "«Consejo de estudio» muestra una recomendación breve.\n"
        "Usa /cancel para cancelar y /start para abrir el menú.\n"
        "El bot es una herramienta de organización; no sustituye a un profesor.",
        reply_markup=MENU,
    )


@router.message(F.text == "Consejo de estudio")
async def study_tip(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Consejo de estudio:\n" + random.choice(TIPS), reply_markup=MENU)


@router.message(F.text == "Crear plan")
async def ask_topic(message: Message, state: FSMContext):
    await state.set_state(PlanFlow.waiting_topic)
    await message.answer(
        "¿Qué tema quieres estudiar? Por ejemplo: álgebra, historia o inglés.\n"
        "Escribe entre 2 y 80 caracteres o pulsa /cancel para salir."
    )


@router.message(PlanFlow.waiting_topic, F.text)
async def receive_topic(message: Message, state: FSMContext):
    topic = " ".join(message.text.strip().split())
    if not 2 <= len(topic) <= 80:
        await message.answer("Escribe un tema entre 2 y 80 caracteres.")
        return
    await state.update_data(topic=topic)
    await state.set_state(PlanFlow.waiting_duration)
    await message.answer("¿Cuánto tiempo tienes disponible?", reply_markup=DURATIONS)


@router.message(PlanFlow.waiting_topic)
async def require_topic_text(message: Message):
    await message.answer("Escribe el nombre del tema como texto para continuar.")


@router.callback_query(
    PlanFlow.waiting_duration,
    F.data.in_({"duration:30", "duration:60", "duration:90"}),
)
async def receive_duration(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    topic = data.get("topic")
    if not topic:
        await state.clear()
        await callback.answer("La sesión caducó. Pulsa Crear plan.", show_alert=True)
        return
    duration = int(callback.data.split(":", 1)[1])
    text = make_plan(topic, duration)
    await state.clear()
    # Display user-provided topics as plain text, not HTML.
    await callback.message.answer(text, reply_markup=MENU)
    await callback.answer()


@router.message(PlanFlow.waiting_duration)
async def require_duration_button(message: Message):
    await message.answer("Elige 30, 60 o 90 minutos con los botones.", reply_markup=DURATIONS)


@router.callback_query(F.data.startswith("duration:"))
async def expired_duration(callback: CallbackQuery):
    await callback.answer("Este plan ya caducó. Pulsa Crear plan.", show_alert=True)


@router.message()
async def unknown_message(message: Message):
    await message.answer("Elige una opción del menú o pulsa /start.", reply_markup=MENU)


async def configure_profile(bot: Bot):
    # The profile PHOTO must still be uploaded manually using @BotFather.
    fields = [
        ("name", bot.set_my_name(name=BOT_NAME)),
        ("about", bot.set_my_short_description(short_description=BOT_ABOUT)),
        ("description", bot.set_my_description(description=BOT_DESCRIPTION)),
    ]
    for label, operation in fields:
        try:
            await operation
            logger.info("Updated Telegram profile field: %s", label)
        except Exception:
            logger.exception("Could not update Telegram profile field: %s", label)
    try:
        await bot.set_my_commands([
            BotCommand(command="start", description="Abrir el menú principal"),
            BotCommand(command="help", description="Ver las instrucciones"),
            BotCommand(command="about", description="Información sobre el bot"),
            BotCommand(command="cancel", description="Cancelar el plan actual"),
        ])
    except Exception:
        logger.exception("Could not update bot commands")


async def main():
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")
    if len(BOT_ABOUT) > 120 or len(BOT_DESCRIPTION) > 512:
        raise RuntimeError("Telegram profile text exceeds API length limits")
    bot = Bot(token=token)
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(router)
    try:
        await configure_profile(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Starting ASISTENTE MR MENTOR polling")
        await dispatcher.start_polling(
            bot, allowed_updates=dispatcher.resolve_used_update_types()
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
