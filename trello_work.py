import requests

"""             1 ---  Либо сохраните свой токен и ключ по адресу '/token.txt'  
                2 ---  Либо в 'auth_params' введите свой токен и ключ в формате:
                                            Первая строка ключ
                                            Вторая строка ваш токен
                                            Третья строка ваш ID Доски, с которой вы собираетесь работать
"""
FILENAME = "token.txt"
# открываем скрытый файл на чтение
fd = open(FILENAME, encoding="UTF-8")
#  сохраняем строки этого файла
text_lines = fd.readlines()
# закрываем файл
fd.close()
key_name = text_lines[0]
token_name = text_lines[1]
board_id = text_lines[2]
if "\n" in key_name:
    key_name = key_name[:-1]
if "\n" in token_name:
    token_name = token_name[:-1]
if "\n" in board_id:
    board_id = board_id[:-1]

"""             Вот ЗДЕСЬ надо переписать токен и ключ, если вы не сохранили их в отдельный файл, так же не забудьте подставить ваш id доски на следующей строке"""
# board_id = Ваш ID Доски!
auth_params = {
    "key": key_name,
    "token": token_name
    }

base_url = "https://api.trello.com/1/{}"

def read():
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + " - " + str(len(task_data)))
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:
            print('\t' + task['name'])


def create_list(column_name):
    # Создает новые колонки
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    column_set = False
    for column in column_data:
        if column_name == column["name"]:
            print("Такая колонка уже есть")
            column_set = True
            break
    if column_set == False:
            requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column_name, **auth_params})


# def delete_list(column_name):
#     column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
#     for column in column_data:
#         if column_name == column["name"]:
#             print(requests.delete(base_url.format('lists') + '/' + column['id'], data={**auth_params}))







def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    name_set = False  
    # Среди всех колонок нужно найти все задачи по имени    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:    
            if task['name'] == name:    
                print("Такая задача уже есть в колонке: " + column['name'])
                name_set = True    
    if name_set == True:
        number_mode = int(input("Все равно создать такую задачу?\n 1 - Да\n 2 - Нет\n"))
        if number_mode == 1:
            for column in column_data:
                if column['name'] == column_name:      
                    # Создадим задачу с именем _name_ в найденной колонке      
                    requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
                    break
        elif number_mode == 2:
            print("Хорошо, не буду записывать")
    if name_set == False:
        for column in column_data:      
            if column['name'] == column_name:      
                # Создадим задачу с именем _name_ в найденной колонке      
                requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
                break


def delete(name, column_name):
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name and column_name == column['name']:
                task_id = task['id']    
                requests.delete(base_url.format('cards') + '/' + task_id, data={**auth_params})            
                break       
        if task_id:
            break


def move(name, column_name_start, column_name_end):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name and column_name_start == column['name']:    
                task_id = task['id']    
                break    
        if task_id:    
            break    
       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name_end:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break  

def mode():
    print("Выберите режим:\n 0 - Посмотреть колонки и задачи\n 1 - Создать новую задачу\n 2 - Перенести существующую задачу\n 3 - Удалить задачу\n 4 - Создать новую колонку для задач")
    number = int(input())
    if number == 1:
        column_name = input("Введите название колонки: ")
        name_a = input("Введите название задачи: ")
        create(name_a, column_name)
    elif number == 2:
        column_name_start = input("Из какой колонки переносим: ")
        name_a = input("Какую задачу переносим: ")
        column_name_end = input("В какую колонку перенести: ")
        move(name_a, column_name_start, column_name_end)
    elif number == 0:
        read()
    elif number == 3:
        column_name = input("Из какой колонки удаляем задачу: ")
        name_a = input("Как называется задача: ")
        delete(name_a, column_name)
    elif number == 4:
        column_name = input("Как будет называться новая колонка: ")
        create_list(column_name)
    else:
        print("Выбран не верный режим")  



if __name__ == "__main__":    
    mode()