from pprint import pprint
import os

def create_cook_book():
    with open('recipes.txt', encoding='utf-8') as file:
        cook_book = {}
        for line in file:
            recipe = line.rstrip()
            ingredient = []
            quantity = int(file.readline().rstrip())
            for item in range(quantity):
                val = file.readline().split(" | ")
                val_ingr = {}
                val_ingr['ingredient_name'] = val[0]
                val_ingr['quantity'] = int(val[1])
                val_ingr['measure'] = val[2].split()[0]
                ingredient.append(val_ingr)
            file.readline()
            cook_book[recipe] = ingredient
    pprint(cook_book)
    print()
    return cook_book

def get_shop_list_by_dishes(dishes, person_count, cook_book):
    ingredient = {}
    for dishe in dishes:
        if dishe in cook_book:
            for item in cook_book[dishe]:
                list_quantity = {}
                if ingredient.get(item['ingredient_name']) is None:
                    list_quantity['quantity'] = item['quantity'] * person_count
                    list_quantity['measure'] = item['measure']
                    ingredient[item['ingredient_name']] = list_quantity
                else:
                    list_quantity['quantity'] = item['quantity'] * person_count + ingredient[item['ingredient_name']]['quantity']
                    list_quantity['measure'] = item['measure']
                    ingredient[item['ingredient_name']] = list_quantity
    pprint(ingredient)

#Функция создания файла
def create_file(list):
    #Проверить есть ли созданный файл, если есть удалить
    if os.path.exists('SortFile.txt'):
        os.remove('SortFile.txt')
    for count_line, val in sorted(list.items()):
        for item in val:
            for key, lines in item.items():
                with open('SortFile.txt','a',encoding='utf-8') as file_s:
                    file_s.write(f'{key}\n{count_line}\n')
                    for line in lines:
                        file_s.write(f'{line}\n')
    print()
    print('Файл SortFile.txt успешно создан!')

#Функция сортировки файлов. Предусмотрен алгоритм сортировки нескольких файлов
#с возможной ситуацией с файлами одинаковым по количеству строк
def sorted_files():
    full_path = os.path.join(os.getcwd(), 'sorted')
    file_list = os.listdir(full_path)
    list_count_line = {}
    for file_obj in file_list:
        with open(os.path.join(full_path,file_obj), encoding='utf-8') as file:
            list_line = []
            line_count = 0
            for line in file:
                line_count += 1
                list_line.append(line.rstrip())
            dict_file = []
            list_file = {}
            if list_count_line.get(line_count) is None:
                list_file[file_obj] = list_line
                dict_file.append(list_file)
                list_count_line[line_count] = dict_file
            else:
                val_list_count_line = list_count_line.get(line_count)
                list_file[file_obj] = list_line
                val_list_count_line.append(list_file)
                list_count_line[line_count] = val_list_count_line
    create_file(list_count_line)

get_shop_list_by_dishes(['Запеченный картофель','Омлет','Фахитос'], 2, create_cook_book())
sorted_files()