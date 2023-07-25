import sqlite3 as sq

from create_bot import dp, bot

'''
Эта база встроена в Пайтон , реалтизована в виде одного файла и не требует кл действий по ее установки
'''
base = None
cur = None


def sql_start():
    """
Здесь подключается имеющаяся БД или создается вновь. Для этого обьявляется две переменные-объекта -  base – это собственно подключение базы с нашим именем  и cur – это указатель, который определяет текущее место в базе.
Далее - base.execute – создание в БД таблицы (если ее нет) в которой хранятся наши блюда
base.commit() -  внесение изменений в БД и Таблицу
    """
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected, OK!')
        print(str(base))
    base.execute("CREATE TABLE IF NOT EXISTS menu(photo, name PRIMARY KEY, description, price)")
    # base.execute("CREATE TABLE IF NOT EXISTS menu(photo TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)")
    base.commit()


async def sql_add_command(state):
    """
    Она записывает изменения, которые вносит модератор в БД
Принимает на входе Состояние Машины Состояний – в котором уже имеется все данные для Таблицы бД.
Открываем Мемори сторидж – как наше имя дата. Выполняем команду в месте текущего положения курсора в БД
– ВСТАВЛЯЕМ в таблицу ЗНАЧЕНИЯ – из входного STATE. ???? – это безопасное подставление данных
Данные сначала приводятся к кортрежу -  потому, что так они хранятся в скулайт - tuple(data.values()
         base.commit() – коммент – сохранение изменений
    """
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    """
    fetchall - этот метод БД выгружает все из таблицы menu БД в виде ret - списка из строк-
    все что после  await - это очередная строка таблицы, которая разбирается
    ret[0] - фото , ret[1] - Описание  и тд
    bot.send_photo(.... - отправляет каждую строку таблицы , разобранную по элементам
    \n - оператор перевода на новую строку
    """
    for ret in cur.execute("SELECT * FROM menu").fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')

# выбор всех записей БД
async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

# удаление записи по названию: name == data
async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()