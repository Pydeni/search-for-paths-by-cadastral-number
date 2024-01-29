import datetime
import time
import os
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import webbrowser
import re



path = r'\\10.50.141.210\plans'
kolvo_zapisan_adressov = 0

# Проходимся по всем папкам и файлам и записываем их(в т.ч. пути) в текстовик baza_path.txt
def create_baza_plans(path):
    global kolvo_zapisan_adressov
    print("Индексация и запись начата", datetime.now())
    baza = os.walk(path)
    with open("baza_path.txt", "w", encoding="utf-8") as baza_path:
        for i in baza:
            if type(i[1]) == list and len(i[1]) == 0:
                baza_path.write(str(i)+"\n")
                kolvo_zapisan_adressov += 1
                print(datetime.now(), f'Записан {i}')

        print("Индексация и запись окончена", datetime.now())
        onInfo()




# Уведомление о завершении обновления базы
def onInfo():
    mb.showinfo("Информация", "Обновление завершено")




# Функция обновления базы путей plans
def update_base():
    answer = mb.askyesno(title="Вопрос",
                         message="ВНИМАНИЕ! Обновление базы путей занимает, примерно, 13 часов. Обновить данные?")
    if answer:
        create_baza_plans(path)

# Функция вывода результатов списком
def res(result):
    text.insert(1.0,"Путь до папки: "+result +'\n')

def res_1(number):
    text.insert(2.0, "Кадастровый номер: " + number[0]+'\n')
    text.insert(3.0, "Инвентарный номер: " + number[1] + '\n')
    text.insert(4.0, "Условный номер: " + number[2]+'\n')

# Ивент для удаления инфы из окна
def delete_text():
    text.delete("1.0", END)

# Ивент для ввода номера
def slovo():
    s = entry.get()
    # Если инвентарный номер ввели
    if s.count(":") <= 2:
        poisk_kad(s)
        s = s.replace(":","_").replace("/", "_")
        poisk(s)
    # Если ввели кадастровый
    else:
        inven = poisk_kad(s)[1]
        inven = inven.replace(":","_").replace("/", "_")
        poisk(inven)



# Функция поиска по базе с путями
def poisk(invent_number):
    with open('baza_path.txt', encoding="utf-8") as baza_path:
        in_numbr = sorted(re.split("[_/-]", invent_number))
        for i in baza_path:
            # Убираем из пути лишние символы
            x = i.split(',')[0].strip("'").lstrip('(').lstrip("'")
            # Создаем список и берем последний инв. номер для сравнения с вводимым
            x_1 = x.split('\\')
            last = sorted(re.split("[_/-]", x_1[-1]))
            if in_numbr == last:
                absol = os.path.abspath(x)
                result = '\\' + absol
                res(result)

            # if  invent_number in i:
            #
            #     # x = i.split(',')[0].strip("'").lstrip('(').lstrip("'")
            #
            #     if invent_number == x_1[-1]:



# Функция поиска по файлу с кад,инв, усл. номерами
def poisk_kad(invent_number):
    with open('инв,усл,кад.csv') as csvfile:
        # Если введен номер без ":"
        if invent_number.count(":") <= 2:
            # in_numbr = invent_number.replace("_", ":")
            for i in csvfile:
                 in_numbr = re.split("[:_/-]",invent_number)
                 sp_num = i.split(';')[:3]
                 for k_n in sp_num[:1]:
                     kad_n = re.split("[:_/-]", k_n)
                 for i_n in sp_num[1:2]:
                     inv_n = re.split("[:_/-]", i_n)
                 x1 = sorted(in_numbr)
                 x2 = sorted(kad_n)
                 y1 = sorted(inv_n)
                 if x1 == x2:
                     res_1(sp_num)
                     return sp_num
                 if x1 == y1:
                     res_1(sp_num)
                     return sp_num
                 # if in_numbr in i:
                 #    print(f"Возможные строки {i}")
                 #    stroka_path = i.split(";")
                 #    if in_numbr == stroka_path[1]:
                 #        res_1(stroka_path)
                 #        return stroka_path

        # Если введен номер с ":"
        else:
            for i in csvfile:
                if invent_number in i:
                    number = i.split(";")
                    if invent_number == number[1] or invent_number == number[0]:
                        res_1(number)
                        return number


"""Программа"""

root = Tk()  # создаем корневой объект - окно
root.title("Поиск по plans")  # устанавливаем заголовок окна
root.geometry("1000x500")  # устанавливаем размеры окна

# Текст, который выводится
label = Label(text='Кад или Инв номер')  # создаем текстовую метку
label.pack(anchor=NW, padx=6, pady=5)  # размещаем метку в окне

# Поле для ввода  номеров
entry = ttk.Entry()
entry.place(x=6,y=30)





"""Кнопки"""
# Кнопка поиска по папке plans
btn = Button(text="Начать поиск", command=slovo)
# btn.bind('<Button-1>', slovo)
btn.pack(padx=6,pady=25)

# Кнопка обновления базы путей plans
button_path = Button(text="Обновление базы путей plans",command=update_base)
button_path.place(x=800,y=25)

# Кнопка очистки текста
button = ttk.Button(text="Очистить окно", command=delete_text)
button.pack(side=BOTTOM)



# Виджет большого окна текста
text = Text(width=120, height=500)
text.pack(side=LEFT)

# Создаем скороллер
scroll = Scrollbar(command=text.yview)
scroll.pack(side=LEFT, fill=Y)
# Привязываем скроллер к виджету текст
text.config(yscrollcommand=scroll.set)

# горизонтальный Progressbar








root.mainloop()


