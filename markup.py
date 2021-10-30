from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.sql.expression import text

# main menu
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Каталог", "Добавить событие  📌"]
keyboard.add(*buttons)

#cancel button for FSM Create_ivent class
cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = "❌ Отменить операцию"
cancel_keyboard.add(cancel_button)

# feedback button
def feedback(callback_data):
    fb_keyb = InlineKeyboardMarkup()
    inline_feedback = InlineKeyboardButton(text='Связатся', callback_data=callback_data)
    fb_keyb.add(inline_feedback)
    return fb_keyb

# delete button
#def keybdel(id):
#    delet = InlineKeyboardMarkup()
#    inline_kb = InlineKeyboardButton(text='Удалить', callback_data=id)
#    delet.add(inline_kb)
#    return delet

# menu for chat
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True)
buttons2 = "❌Выйти из чата"
keyboard2.add(buttons2)

# feedback
#def keyboard3(ar, chat):
#    ky3 = InlineKeyboardMarkup()
#    inline_kb3 = InlineKeyboardButton(text='показать событие', callback_data=ar)
#    inline_kb31 = InlineKeyboardButton(text='войти в чат', callback_data=chat)
#    ky3.add(inline_kb3, inline_kb31)
#    return ky3

# pagination
def pagin(num1, num5):
    ikm = InlineKeyboardMarkup()
    i_kb3 = InlineKeyboardButton(text='+1', callback_data=num1)
    i_kb31 = InlineKeyboardButton(text='+5', callback_data=num5)
    ikm.add(i_kb3, i_kb31)
    return ikm

# if user really want delete event
def delete_ivent(arg, arg2):
    yn = InlineKeyboardMarkup()
    yes = InlineKeyboardButton(text='yes', callback_data=arg)
    no = InlineKeyboardButton(text='no', callback_data=arg2)
    yn.add(yes, no)
    return yn

#server bot keyboard
def serv_keyboard(user_full_name, ivent_name, ivent_id, chat_id):
    serv_keyboard = InlineKeyboardMarkup()
    ser_in = InlineKeyboardButton(text=f'Ответить {user_full_name}', callback_data=f'Ответить,{user_full_name},{chat_id},{ivent_name},{ivent_id}')
    ser_inl = InlineKeyboardButton(text=f'Посмотреть событие {ivent_name}', callback_data=f'Посмотреть событие,{ivent_name},{ivent_id}')
    serv_keyboard.add(ser_in, ser_inl)
    return serv_keyboard

def nnn(chat, id, own_id, user_id):
    new = InlineKeyboardMarkup()
    cal = InlineKeyboardButton(text='Связатся', callback_data=chat)
    cal2 = InlineKeyboardButton(text='Удалить', callback_data=id)
    new.add(cal)
    if own_id == user_id:
        new.add(cal2)
    return new