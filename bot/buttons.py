from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
import requests

url='https://api-mobilespecs.azharimm.site/v2/brands'

telefonlar=requests.get(url).json()

menu=ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='📱Telefon brendlari'), KeyboardButton(text="❕Ma'lumotnoma")]
  ],
  resize_keyboard=True
)
ortga=ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='🔙ortga')]
  ],
  resize_keyboard=True
)
telefon_brendlari=ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
for i in range(len(telefonlar['data'])):
    telefon_brendlari.insert(telefonlar['data'][i]['brand_name'])
telefon_brendlari.row(KeyboardButton(text='🔙ortga'),KeyboardButton(text='🏠Menu'))

url2=telefonlar['data'][i]['detail']   
malumot=requests.get(url2).json()

telefon_nomlari=ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
for i in range(len(malumot['data']['phones'])):
  # if ==malumot['data']['phones'][i]['phone_name']:
    telefon_nomlari.insert(malumot['data']['phones'][i]['phone_name'])
telefon_nomlari.row(KeyboardButton(text='🔙ortga'),KeyboardButton(text='🏠Menu'))