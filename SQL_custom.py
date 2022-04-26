import sqlite3

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
conn = sqlite3.connect('Chinook_Sqlite.sqlite')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ
# КОД ДАЛЬНЕЙШИХ ПРИМЕРОВ ВСТАВЛЯТЬ В ЭТО МЕСТО
# Делаем SELECT запрос к базе данных, используя обычный SQL-синтаксис
cursor.execute("""
SELECT COUNT(Sub.passenger) AS zero_count
FROM 
(SELECT id, passenger FROM Pass_in_trip WHERE passenger LIKE "1"
ORDER BY id DESC LIMIT 5) AS Sub;
""")

# Получаем результат сделанного запроса
results = cursor.fetchall()
results2 =  cursor.fetchall()

print(results)   # [('A Cor Do Som',), ('Aaron Copland & London Symphony Orchestra',), ('Aaron Goldberg',)]
print(results2)  # []

# Не забываем закрыть соединение с базой данных
conn.close()