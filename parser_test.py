

def indexing_logs(file_in, file_out):   #filename: DuploServiceLog_test.log


    with open(file_in, encoding='UTF-8') as fd:
        lines = fd.readlines()
    i = 0
    result = ''

    for text in lines:
        i += 1
        # print (text)
        result += f'{i}. {text}'

    print(result)

    with open(file_out, 'w', encoding='UTF-8') as ld:
        ld.write(result)

def test_parser(file_in):


    with open(file_in, encoding='UTF-8') as fd:
        lines = fd.readlines()[::-1]
    
    for text in lines:
    
        if 'longHTTP =' in text:

            print(text)
            print(text.split()[-1])
        
            

    # print(lines)

test_parser('Parser_test.txt')



