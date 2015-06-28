#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import tkinter
from tkinter import messagebox
import tkinter.font
import tkinter.filedialog
import urllib.request
from urllib.request import URLError, HTTPError
import subprocess
import filecmp

def test_program(event):
    test_number = 1
    while True:
        try:
            test_url = test_url_const + str(test_number)
            answer_url = test_url + ".a"
            test = urllib.request.urlopen(test_url).read()
            test = test.decode()
            answer = urllib.request.urlopen(answer_url).read()
            answer = answer.decode()
        except HTTPError:
            messagebox.showinfo("Test", "Все тесты пройдены!")
            break
        except URLError:
            messagebox.showinfo("Test", "Все тесты пройдены!")
            break

        test_file = open("test.txt", "w")
        answer_file = open("answer.txt","w")
        test_file.write(test)
        answer_file.write(answer)
        test_file.close()
        answer_file.close()

        command = "timeout 3s valgrind -q ./a.out <test.txt"
        process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()
        if error != "":
            messagebox.showerror("Test", "valgrind показывает ошибки в тесте" + str(test_number))
            print(error)
        output_file = open("output.txt", "w")
        output_file.write(output)
        output_file.close()
        if filecmp.cmp("answer.txt","output.txt") == False:
            messagebox.showerror("Test", "Неправильный ответ для теста №" + str(test_number))
            break
        test_number +=1


def compile_program(event):
    process = subprocess.Popen(compile_string.get(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    output, error = process.communicate()
    error = error.decode()
    if error == "":
        messagebox.showinfo("Compile", "Компиляция прошла удачно!")
    else:
        messagebox.showerror("Compile", "Компиляция не была проведена. Возникла ошибка")
        print(error)


def choose_directory():
    directory_path = tkinter.filedialog.askopenfilename(initialdir="/home/great",title="Выберите файл для компиляции")
    file_path.set(directory_path)
    return None

def create_choose_language(list,v):
    buttons=[]
    for text,value in list:
        buttons.append(tkinter.Radiobutton(frame1,text=text,value=value,variable=v))
    return buttons

test_url_const = "http://195.19.40.181:3386/tasks/iu9/algorithms_and_data_structures.3/clang/polynom/tests/"

wnd = tkinter.Tk()
wnd.geometry("600x250")
wnd.title("T-bmstu tester")
t_bmstu_ip=tkinter.StringVar()
t_bmstu_ip.set("http://195.19.40.181:3386")
file_path=tkinter.StringVar()
file_path.set(str(os.getcwd()))
frame1=tkinter.Frame(wnd)
frame1.pack(fill="both",expand="Yes")
test_url=tkinter.StringVar()
info_label=tkinter.Label(frame1,text="Автоматический тестер решения задач в системе тестирования T-bmstu")
t_bmstu_label=tkinter.Label(frame1,text="Сайт t-bmstu(изменен с 2015 г.):",width=30)
t_bmstu_entry=tkinter.Entry(frame1,width=40,textvariable=t_bmstu_ip)
file_label=tkinter.Label(frame1,text="Укажите путь к файлу")
file_entry=tkinter.Entry(frame1,width=40,textvariable=file_path)
file_button=tkinter.Button(frame1,text="Выбери директорию",command=choose_directory)
language_label=tkinter.Label(frame1,text="Выберите один из языков программирования")
language_list=[("C",0),("C++",1),("Java",2),("Python",3),("Scheme",4),("Ruby",5),("Pascal",6)]
test_url_label=tkinter.Label(frame1,text="Введите ссылку на тесты\n (если возникнет неизвестная ошибка)")
compile_button=tkinter.Button(frame1,text="Compile")
compile_label = tkinter.Label(frame1,text="Строка компиляции для bash")
language_string = tkinter.StringVar()
language_string.set("gcc " + str(os.getcwd()) + " ")
compile_string = tkinter.Entry(frame1,width=40,textvariable=language_string)
compile_button.bind("<Button-1>",compile_program)
test_button=tkinter.Button(frame1,text="Test!")
test_button.bind("<Button-1>",test_program)
test_url_entry=tkinter.Entry(frame1,textvariable=test_url,width=40)
author_name=tkinter.Label(frame1,text="by George Great")
language_choose=tkinter.IntVar()
buttons = create_choose_language(language_list,language_choose)
info_label.grid(row=1,column=1,columnspan=4)
t_bmstu_label.grid(row=2,column=1)
t_bmstu_entry.grid(row=2,column=2,columnspan=3)
file_label.grid(row=3,column=1)
file_entry.grid(row=3,column=2,columnspan=3)
file_button.grid(row=4,column=2,columnspan=3)
language_label.grid(row=5,column=1)
column_number = 2
flag=False
for button in buttons:
    if column_number == 5:
        row = 6
        column_number=1
        flag=True
    elif flag == False:
        row = 5
    button.grid(row=row,column=column_number)
    column_number+=1
test_url_label.grid(row=7,column=1)
test_url_entry.grid(row=7,column=2,columnspan=3)
compile_label.grid(row=8,column=1)
compile_string.grid(row=8,column=2,columnspan=3)
test_button.grid(row=9,column=2)
compile_button.grid(row=9,column=3)
author_name.grid(row=10,column=1,columnspan=4)
wnd.mainloop()
