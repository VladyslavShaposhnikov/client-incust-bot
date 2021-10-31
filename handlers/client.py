from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from create_bot import bot
from config import SERVER_BOT_TOKEN
from markup import keyboard, cancel_keyboard, keyboard2, pagin, delete_ivent, serv_keyboard, nnn
from database import sqlite_db


# FSM class to create event
class Create_ivent(StatesGroup):
    ivent_name = State()
    ivent_title = State()
    ivent_description = State()
    ivent_media = State()
    ivent_data = State()

# FSM class to send message in server bot
class Messages(StatesGroup):
    messages_name = State()

#@dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.message):
    await message.answer('Добро пожаловать {}!'.format(message.from_user.full_name), reply_markup=keyboard)
    args = message.get_args()
    if args:
        iv = await sqlite_db.sql_get_ivent(int(args))
        await bot.send_photo(message.chat.id, iv.media,f'{iv.name}\nTitle: {iv.title}\ndescription: {iv.description}\n')

#@dp.message_handler(Text(equals="Каталог"))
async def katalog(message: types.MessageAutoDeleteTimerChanged):
    ls = []
    list_of_ivents = await sqlite_db.sql_read(limit=2)
    for ivent in list_of_ivents:
        await bot.send_photo(message.chat.id, ivent.media,f'{ivent.name}\nЗаголовок: {ivent.title}\nОписание: {ivent.description}\n', reply_markup=nnn('chat'+str(ivent.id), 'delet'+str(ivent.id), int(ivent.i_id), int(message.from_user.id)))
        ls.append(ivent.id)
    count_of_db_elem = await sqlite_db.sql_all()
    if count_of_db_elem > 2:
        await message.answer('Показать больше', reply_markup=pagin(num1='one'+str(ls[-1]), num5='five'+str(ls[-1])))

#@dp.callback_query_handler(text_contains='one')
# pagination [+1]button
async def one(call: CallbackQuery):
    last_id = int(call.data.replace('one', ''))
    ivent = await sqlite_db.sql_read2(last_id=last_id, limit=1)
    await bot.send_photo(call.message.chat.id, ivent.media,f'{ivent.name}\nЗаголовок: {ivent.title}\nОписание: {ivent.description}\n', reply_markup=nnn('chat'+str(ivent.id), 'delet'+str(ivent.id), int(ivent.i_id), int(call.from_user.id)))
    greatest_id = await sqlite_db.sql_latest_id()
    if ivent.id != greatest_id:
        await call.message.answer('Показать больше', reply_markup=pagin(num1='one'+str(ivent.id), num5='five'+str(ivent.id)))

#@dp.callback_query_handler(text_contains='five')
# pagination [+5]button
async def five(call: CallbackQuery):
    last_id = int(call.data.replace('five', ''))
    ivents = await sqlite_db.sql_read2(last_id=last_id, limit=5)
    ls = []
    for ivent in ivents:
        await bot.send_photo(call.message.chat.id, ivent.media,f'{ivent.name}\nЗаголовок: {ivent.title}\nОписание: {ivent.description}\n', reply_markup=nnn('chat'+str(ivent.id), 'delet'+str(ivent.id), int(ivent.i_id), int(call.from_user.id)))
        ls.append(ivent.id)
    greatest_id = await sqlite_db.sql_latest_id()
    if ls[-1] != greatest_id:
        await call.message.answer('Показать больше', reply_markup=pagin(num1='one'+str(ls[-1]), num5='five'+str(ls[-1])))

#@dp.callback_query_handler(text_contains='btn')
# inline button [Связатся]
#async def callb(call: CallbackQuery):
#    ivent = await sqlite_db.sql_get_ivent(int(call.data.replace('btn', '')))
#    await call.message.answer(text='Выберите действие', reply_markup=keyboard3('id'+str(ivent.id), 'chat'+str(ivent.id)))

#@dp.callback_query_handler(text_contains='chat')
# inline button [Войти в чат]
async def new_callb(call: CallbackQuery, state: FSMContext):
    ivent = await sqlite_db.sql_get_ivent(int(call.data.replace('chat', '')))
    await call.message.answer(text=f'Bы вошли в чат с владельцем события "{ivent.title}"', reply_markup=keyboard2)
    await Messages.messages_name.set()
    async with state.proxy() as data1:
        data1['ivent_id'] = ivent.id
        data1['ivent_title'] = ivent.title
        data1['user_id'] = ivent.i_id

#@dp.message_handler(state=Messages.messages_name)
# sending message to ivent owner
async def messages_name(message:types.Message,state:FSMContext):
    async with state.proxy() as data1:
        data1['user_name'] = message.from_user.full_name
        data1['ivent_owner_id'] = message.from_user.id
        data1['message_name'] = message.text

        with bot.with_token(SERVER_BOT_TOKEN):
            await bot.send_message(data1['user_id'], f'#Сообщение {data1["ivent_title"]}\n{data1["user_name"]}: {data1["message_name"]}', reply_markup=serv_keyboard(data1['user_name'], data1['ivent_title'], data1['ivent_id'], data1['ivent_owner_id']))
    #await message.answer('Сообщение доставлено')
    await new_callb()
    await state.finish()

# @dp.callback_query_handler(text_contains='id')
# inline button [Показать событие]
async def get_ivent(call: CallbackQuery):
    iv = await sqlite_db.sql_get_ivent(call.data.replace('id', ''))
    await bot.send_photo(call.message.chat.id, iv.media,f'{iv.name}\nЗаголовок: {iv.title}\nОписание: {iv.description}\n')

# @dp.message_handler(lambda message: message.text == "❌Выйти из чата", state='*')
# cancel chat
async def cancel_chat(message:types.Message,state:FSMContext):
    current_state = await state.get_state()
    await message.answer('Вы вышли из чата', reply_markup=keyboard)
    if current_state is None:
        return
    await state.finish()

# @dp.callback_query_handler(text_contains='delet')
# delete ivent
async def del_ivent(call: CallbackQuery):
    post_id = call.data.replace('delet', '')
    await call.message.reply(text='Вы уверены что хотите удалить это событие?', reply_markup=delete_ivent(arg='yes'+str(post_id), arg2='no'+str(post_id)))
#    await sqlite_db.sql_del_ivent((call.data.replace('delet', '')))
#    await call.answer(text='событие удалено')

# @dp.callback_query_handler(text_contains='yes')
# if user relly want delete ivent
async def del_yes(call: CallbackQuery):
    await sqlite_db.sql_del_ivent(call.data.replace('yes', ''))
    await call.message.edit_text(text='событие удалено')

# @dp.callback_query_handler(text_contains='no')
# if user relly want delete ivent
async def del_no(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

#@dp.message_handler(lambda message: message.text == "❌ Отменить операцию", state='*')
# stop create ivent
async def cansel_handler(message:types.Message,state:FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Операция была отменина', reply_markup=keyboard)

#@dp.message_handler(lambda message: message.text == "Добавить событие  📌", state=None)
# create new ivent
async def add_ivent(message: types.Message):
    await message.answer("Вы создаете событие\n1. Имя события:", reply_markup=cancel_keyboard)
    await Create_ivent.ivent_name.set()

#@dp.message_handler(state=Create_ivent.ivent_name)
# ivent name
async def process_name(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['ivent_name'] = message.text
        data['u_id'] = message.from_user.id

    await message.answer("2. Заголовок:")
    await Create_ivent.next()

#@dp.message_handler(state=Create_ivent.ivent_title)
# ivent title
async def process_title(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['ivent_title'] = message.text

    await message.answer("3. Описание:")
    await Create_ivent.next()

#@dp.message_handler(state=Create_ivent.ivent_description)
# ivent description
async def process_description(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['ivent_description'] = message.text

    await message.answer("4. Медиа:\n(Загрузите фотографию)")
    await Create_ivent.next()

#@dp.message_handler(content_types=['photo'] ,state=Create_ivent.ivent_media)
# ivent photo
async def process_media(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['ivent_media'] = message.photo[0].file_id
        photo = data['ivent_media']
        name = data['ivent_name']
        title = data['ivent_title']
        description = data['ivent_description']
        await bot.send_photo(message.chat.id, photo, '{}\nTitle: {}\ndescription: {}\nВы создали событие👆👆👆\nДля того, чтобы получать уведомления о сообщениях перейдите в  @Server_incust_bot и напишите старт'.format(name, title, description), reply_markup=keyboard)

    await sqlite_db.sql_add_command(state)
    await state.finish()


def register_hendlers(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(cancel_chat, lambda message: message.text == "❌Выйти из чата", state='*')
    dp.register_message_handler(katalog, Text(equals="Каталог"))
    dp.register_message_handler(cansel_handler, lambda message: message.text == "❌ Отменить операцию", state='*')
    dp.register_message_handler(add_ivent, lambda message: message.text == "Добавить событие  📌", state=None)
    dp.register_message_handler(process_name, state=Create_ivent.ivent_name)
    dp.register_message_handler(process_title, state=Create_ivent.ivent_title)
    dp.register_message_handler(process_description, state=Create_ivent.ivent_description)
    dp.register_message_handler(process_media,content_types=['photo'] , state=Create_ivent.ivent_media)
    #dp.register_callback_query_handler(callb, text_contains='btn')
    dp.register_message_handler(messages_name, state=Messages.messages_name)
    dp.register_callback_query_handler(get_ivent, text_contains='id')
    dp.register_callback_query_handler(del_ivent, text_contains='delet')
    dp.register_callback_query_handler(new_callb, text_contains='chat')

    dp.register_callback_query_handler(one, text_contains='one')
    dp.register_callback_query_handler(five, text_contains='five')
    dp.register_callback_query_handler(del_yes, text_contains='yes')
    dp.register_callback_query_handler(del_no, text_contains='no')