import requests
from main import msg

url='https://api-mobilespecs.azharimm.site/v2/brands'

telefonlar=requests.get(url).json()

print('ID - Telefon nomi')


for i in range(len(telefonlar['data'])):
    print(telefonlar['data'][i]['brand_id'],'-', telefonlar['data'][i]['brand_name'])

telefon_id=input('Brendlarning Id raqamini yoki nomini kiriting: ')



for i in range(len(telefonlar['data'])):
    if telefon_id==str(telefonlar['data'][i]['brand_id']) or telefon_id==(telefonlar['data'][i]['brand_name']).lower() or telefon_id==(telefonlar['data'][i]['brand_name']).upper() or telefon_id==(telefonlar['data'][i]['brand_name']):
        print('Brend nomi: ',telefonlar['data'][i]['brand_name'],'\n')
        url2=telefonlar['data'][i]['detail']
        
malumot=requests.get(url2).json()

print('Brend nomi:',malumot['data']['phones'][0]['brand'])
for i in range(len(malumot['data']['phones'])):
    print('Telefon nomi:',malumot['data']['phones'][i]['phone_name'])

telefon_id2=input("Telefon nomini kiriting: ")
for i in range(len(malumot['data']['phones'])):
    if telefon_id2==str(malumot['data']['phones'][i]['phone_name']).lower() or str(malumot['data']['phones'][i]['phone_name'])==telefon_id2:
        print(malumot['data']['phones'][i]['phone_name'])
        url3=malumot['data']['phones'][i]['detail']

qoshimcha=requests.get(url3).json()
print('Tayyorlangan vaqti: ',qoshimcha['data']['release_date'],'\n','Dasturiy ta`minoti: ',qoshimcha['data']['os'],'\n','Xotirasi: ',qoshimcha['data']['storage'])
for i in range(len(qoshimcha['data']['specifications'])):
     print('\n',qoshimcha['data']['specifications'][i]['title'],'\n')
     for l in range(len(qoshimcha['data']['specifications'][i]['specs'])):
         print(qoshimcha['data']['specifications'][i]['specs'][l]['key'],'-',str(qoshimcha['data']['specifications'][i]['specs'][l]['val'][0]))

