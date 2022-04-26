

file_log = './logs/DuploServiceLog.log'     # DuploServiceLog.log
log_encoding = 'UTF-8'                # UTF-8
clear_phrase = 'longHTTP ='        # longHTTP =
value_offset = -1              # -1


def parser(dirty_text):
    phrases = []
    phrases.append(dirty_text.split())
    return phrases

with open(file_log, encoding=log_encoding) as fd:
    lines = fd.readlines()

status_count = 0    
error_count = 0
count = 0
error_log = ''
error_dict = {}
last_date_flag = 1
last_report = []

for text in lines[::-1]:


    count += 1
    if clear_phrase in text:
        print(text)
        if last_date_flag:
            last_report = f'последний раз {clear_phrase} {text.split()[value_offset]} зафиксирована {text.split()[0]} в {text.split()[1]}\n'
            last_date_flag = 0
        status_count += 1
        # print(text[0])
        if text.split()[value_offset] != '200':
            error_code = text.split()[value_offset]
            error_count += 1
            if error_dict.get(error_code, False):
                error_dict[error_code] += 1
            else:
                error_dict[error_code] = 1
            error_log += f'Ошибка {text.split()[value_offset]} зафиксирована {text.split()[0]} в {text.split()[1]}\n'
            # print(parser(text)[0][0])
            # print(parser(text)[0][1])
            # print(parser(text)[0][-1])

    # нужно реализовать запись кода ошибочных longHTTP = и их количества. Далее вывода самой большой ошибки если допустим ошибочных больше 25%
    # То есть когда ошибок менее 25% выводится "longHTTP = 200",  а если более 25% то самая распространенная ошибка "longHTTP = ххх"
    # Далее прикрутить второй строкой под параметром типа last_log = дату и время последней записи "longHTTP ="
    # Далее прикрутить судя исполнение моего SQL запроса- и запись его результата под параметров типа "custom_SQL ="
    # Все это перезаписывать в выходной файл и придумать как этот файл будет выполняться каждые 3 минуты.  

    if status_count == 100:
        break

if error_count/status_count < 0.25:
    print(error_log)
    print(error_dict)
    print(max(error_dict, key=error_dict.get))
    print(last_report)