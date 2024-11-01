import sqlite3
import json

# Пример JSON-данных
data = [
    {'id_user': '1234',
     '_id': '671cb34a025375dfff7c4e08',
     'createdAt': '2024-10-26T09:15:54+00:00',
     'ticket': {
         'document': {
             'receipt': {
                 'appliedTaxationType': 32,
                 'cashTotalSum': 0,
                 'code': 3,
                 'creditSum': 0,
                 'dateTime': '2024-10-26T12:15:00',
                 'ecashTotalSum': 18000,
                 'fiscalDocumentFormatVer': 4,
                 'fiscalDocumentNumber': 15976,
                 'fiscalDriveNumber': '7380440800992800',
                 'fiscalSign': 161421875,
                 'items': [
                     {
                         'name': 'Гречишный чай 0,3',
                         'nds': 6,
                         'paymentType': 4,
                         'price': 18000,
                         'productType': 1,
                         'quantity': 1,
                         'sum': 18000
                     }
                 ],
                 'kktRegId': '0005027761021217',
                 'ndsNo': 18000,
                 'operationType': 1,
                 'operator': 'Горбова Валерия',
                 'prepaidSum': 0,
                 'provisionSum': 0,
                 'requestNumber': 45,
                 'retailPlace': 'Кофейня',
                 'retailPlaceAddress': '143002,М.О.г.Одинцово,ул.Маршала Неделина,д.6А',
                 'shiftNumber': 57,
                 'taxationType': 32,
                 'totalSum': 18000,
                 'user': 'ЦВЕТКОВ АЛЕКСАНДР ВАЛЕРЬЕВИЧ',
                 'userInn': '772335560450'
             }
         }
     }
     }
]

# Подключаемся к базе данных
conn = sqlite3.connect('receipts.db')
cursor = conn.cursor()

# Создаем таблицы
# cursor.execute('''CREATE TABLE IF NOT EXISTS main_data (
#                     _id TEXT PRIMARY KEY,
#                     createdAt TEXT,
#                     receipt_id INTEGER REFERENCES receipts(receipt_id)
#                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS receipts (
                    receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    _id TEXT PRIMARY KEY,
                    createdAt TEXT,
                    appliedTaxationType INTEGER,
                    cashTotalSum INTEGER,
                    code INTEGER,
                    creditSum INTEGER,
                    dateTime TEXT,
                    ecashTotalSum INTEGER,
                    fiscalDocumentFormatVer INTEGER,
                    fiscalDocumentNumber INTEGER,
                    fiscalDriveNumber TEXT,
                    fiscalSign INTEGER,
                    kktRegId TEXT,
                    ndsNo INTEGER,
                    operationType INTEGER,
                    operator TEXT,
                    prepaidSum INTEGER,
                    provisionSum INTEGER,
                    requestNumber INTEGER,
                    retailPlace TEXT,
                    retailPlaceAddress TEXT,
                    shiftNumber INTEGER,
                    taxationType INTEGER,
                    totalSum INTEGER,
                    user TEXT,
                    userInn TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    receipt_id INTEGER REFERENCES receipts(receipt_id),
                    name TEXT,
                    nds INTEGER,
                    paymentType INTEGER,
                    price INTEGER,
                    productType INTEGER,
                    quantity INTEGER,
                    sum INTEGER
                )''')

# Записываем данные
for record in data:
    receipt_data = record['ticket']['document']['receipt']

    # Вставляем данные в таблицу receipts
    cursor.execute('''INSERT INTO receipts (appliedTaxationType, cashTotalSum, code, creditSum, dateTime, ecashTotalSum,
                                            fiscalDocumentFormatVer, fiscalDocumentNumber, fiscalDriveNumber, fiscalSign,
                                            kktRegId, ndsNo, operationType, operator, prepaidSum, provisionSum,
                                            requestNumber, retailPlace, retailPlaceAddress, shiftNumber, taxationType,
                                            totalSum, user, userInn)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (receipt_data['appliedTaxationType'], receipt_data['cashTotalSum'], receipt_data['code'],
                    receipt_data['creditSum'], receipt_data['dateTime'], receipt_data['ecashTotalSum'],
                    receipt_data['fiscalDocumentFormatVer'], receipt_data['fiscalDocumentNumber'],
                    receipt_data['fiscalDriveNumber'], receipt_data['fiscalSign'], receipt_data['kktRegId'],
                    receipt_data['ndsNo'], receipt_data['operationType'], receipt_data['operator'],
                    receipt_data['prepaidSum'], receipt_data['provisionSum'], receipt_data['requestNumber'],
                    receipt_data['retailPlace'], receipt_data['retailPlaceAddress'], receipt_data['shiftNumber'],
                    receipt_data['taxationType'], receipt_data['totalSum'], receipt_data['user'],
                    receipt_data['userInn']))

    # Получаем id вставленной строки для связи
    receipt_id = cursor.lastrowid

    # Вставляем данные в таблицу main_data
    cursor.execute('''INSERT INTO main_data (_id, createdAt, receipt_id) VALUES (?, ?, ?)''',
                   (record['_id'], record['createdAt'], receipt_id))

    # Вставляем данные товаров в таблицу items
    for item in receipt_data['items']:
        cursor.execute('''INSERT INTO items (receipt_id, name, nds, paymentType, price, productType, quantity, sum)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (receipt_id, item['name'], item['nds'], item['paymentType'], item['price'],
                        item['productType'], item['quantity'], item['sum']))

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
