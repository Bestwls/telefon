from pkgutil import get_data
from aiogram import Dispatcher, types, Bot,executor
import logging
import requests
from config import tok
from states import tel
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



logging.basicConfig(level=logging.INFO)
bot=Bot(token=tok)
dp=Dispatcher(bot, storage=MemoryStorage())



url='https://api-mobilespecs.azharimm.site/v2/brands'
telefonlar=requests.get(url).json()



#Buttons menu_______________________________________________________
menu=ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='📱Telefon brendlari'), KeyboardButton(text="❕Ma'lumotnoma")]
  ],
  resize_keyboard=True
)
#___________________________________________________________________
@dp.message_handler(commands=['start'])
async def do_start(message: types.Message):
  user=message.from_user.first_name
  await message.answer(f"Salom {user}", reply_markup=menu)
  



@dp.message_handler(text="❕Ma'lumotnoma")
async def do_help(message: types.Message):
  ortga=ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='🔙ortga')]
  ],
  resize_keyboard=True
)
  await message.answer(f"Men sizga telefon brendlari haqida ma'lumot beraman",reply_markup=ortga)
  



@dp.message_handler(text='🔙ortga',state=tel.brendlar)
async def do_back(message: types.Message):
  await message.answer('Ortga qaytdingiz', reply_markup=menu)
@dp.message_handler(text='🔙ortga',state=tel.brendlar)
async def do_back(message: types.Message):
  await message.answer('Ortga qaytdingiz', reply_markup=menu)




@dp.message_handler(text=['📱Telefon brendlari'])   
async def do_back(message: types.Message):
  telefon_brendlari=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
  for i in range(len(telefonlar['data'])):
    telefon_brendlari.insert(telefonlar['data'][i]['brand_name'])
  telefon_brendlari.row(KeyboardButton(text='🔙ortga'),KeyboardButton(text='🏠Menu'))
  await message.answer('Telefon brendlaridan keragini tanlang', reply_markup=telefon_brendlari)
  await tel.brendlar.set()




@dp.message_handler(state=tel.brendlar)
async def telefon1(message: types.Message, state:FSMContext):
  msg=message.text
  
  for l in range(len(telefonlar['data'])):
    if str(msg)==str(telefonlar['data'][l]['brand_name']):
      url2=telefonlar['data'][l]['detail']
      await state.update_data(
        {'url': url2}
      )
  malumot=requests.get(url2).json()

  telefon_nomlari=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
  for i in range(len(malumot['data']['phones'])):
    telefon_nomlari.insert(malumot['data']['phones'][i]['phone_name'])
  telefon_nomlari.row(KeyboardButton(text='🔙ortga'),KeyboardButton(text='🏠Menu'))

  await message.answer(f'Telefonlardan keragini tanlang ', reply_markup=telefon_nomlari)
  
  
  await tel.next()




@dp.message_handler(state=tel.telefonlar)
async def malumotlar(message: types.Message, state:FSMContext):
  data=await state.get_data()
  url3 = data.get('url')
  malumot=requests.get(url3).json()
  msg=message.text
  for i in range(len(malumot['data']['phones'])):
    if msg==malumot['data']['phones'][i]['phone_name']:
      url3=malumot['data']['phones'][i]['detail']
      qoshimcha=requests.get(url3).json()
      photo1=data_make=qoshimcha['data']['phone_images'][0]
      photo2=data_make=qoshimcha['data']['phone_images'][1]
      data_make=qoshimcha['data']['release_date']
      os=qoshimcha['data']['os']

  for l in range(len(qoshimcha['data']['specifications'])):
    for i in range(len(qoshimcha['data']['specifications'][l]['specs'])):
        if qoshimcha['data']['specifications'][l]['specs'][i]['key']=='CPU':
           cpu=qoshimcha['data']['specifications'][l]['specs'][i]['val']
        if qoshimcha['data']['specifications'][l]['specs'][i]['key'] =="Internal":
            Ram_and_rom=qoshimcha['data']['specifications'][l]['specs'][i]['val']
        if qoshimcha['data']['specifications'][l]['specs'][i]['key']=='Single' or qoshimcha['data']['specifications'][l]['specs'][i]['key']=='Dual':
          camera=qoshimcha['data']['specifications'][l]['specs'][i]['val']
        if qoshimcha['data']['specifications'][l]['specs'][i]['key']=='USB':
          usb=qoshimcha['data']['specifications'][l]['specs'][i]['val']
        if qoshimcha['data']['specifications'][l]['specs'][i]['key']=='Battery' or qoshimcha['data']['specifications'][l]['title']=='Battery':
          battary=qoshimcha['data']['specifications'][l]['specs'][i]['val']
        if qoshimcha['data']['specifications'][l]['specs'][i]['key']=='Price':
          price=qoshimcha['data']['specifications'][l]['specs'][i]['val']
  await message.answer_photo(photo1)
  await message.answer_photo(photo2)
  await message.answer(f'Chiqarilgan sanasi: {data_make}\n\nTizim: {os}\n\nCPU: {cpu}\n\nXotira, tezkor xotira: {Ram_and_rom}\n\nKamera: {camera}\n\nUSB: {usb}\n\nQuvvat: {battary}\n\nNarx: {price}')
  await tel.next()
if __name__=='__main__':
  executor.start_polling(dp,skip_updates=True)