import sqlite3
from tkinter import *
import tkinter.messagebox as box

from datetime import datetime

window = Tk()
window.title("Поиск БС")
window.resizable(0, 0)

window.iconbitmap('@bs.xbm')

# c = Canvas(window)
# c.pack()
# c.create_line( 0, 60, 450, 60 ) # рисуем черную прямую линию

# всплывающее окошко
def dialog():
	# box.showinfo( 'Адрес БС', 'CID: ' + entry.get() )
	box.showinfo( 'Адрес БС', 'CID: ' + opsos.get() )

# срабатывание при нажати Enter
def getInfoReturn(e):
    getInfo()
window.bind('<Return>', getInfoReturn)


def getInfo():
	
	operator = opsos.get()

	# работа с БД
	connection = sqlite3.connect("bs")
	cursor = connection.cursor()

	if (operator == 'Motiv'):
		rows = cursor.execute("SELECT lac, cid, azimut, adress_bs, end_of_action FROM motiv WHERE (cid = " + entry.get() + ") ORDER BY end_of_action").fetchall()
	if (operator == 'Tele2'):
		rows = cursor.execute("SELECT lac, cid, azimut, adress_bs, end_of_action FROM tele2 WHERE (cid = " + entry.get() + ") ORDER BY end_of_action").fetchall()
	if (operator == 'МТС'):
		rows = cursor.execute("SELECT lac, cid, azimut, adress_bs, end_of_action FROM `МТС` WHERE (cid = " + entry.get() + ") ORDER BY end_of_action").fetchall()
	if (operator == 'Мегафон'):
		rows = cursor.execute("SELECT lac, cid, azimut, adress_bs, end_of_action FROM `Мегафон` WHERE (cid = " + entry.get() + ") ORDER BY end_of_action").fetchall()
	if (operator == 'Билайн'):
		rows = cursor.execute("SELECT lac, cid, azimut, adress_bs, end_of_action FROM `Билайн` WHERE (cid = " + entry.get() + ") ORDER BY end_of_action").fetchall()

	# rows = cursor.execute("SELECT lac, cid, azimut, adress_bs FROM " + operator + " WHERE (cid = " + entry.get() + ") ORDER BY end_of_action LIMIT 1").fetchall()
	# text.insert('1.0', len(rows) )
	# text.insert( '1.0', '-----------------------------------------' )
	# text.insert( '1.0', '-----------------------------------------' )

	# получаем текущее время
	current_time = datetime.timestamp(datetime.now())

	text.insert( '1.0', '---------------------------------------------------------------------------------------------' )
	for row in rows:
		# время окончания работы вышки
		end_time = datetime.strptime(row[4], '%d.%m.%Y %H:%M').timestamp()
		
		# если время окончания действия вышки больше текущего - отображаем результат
		# т.е. вышка активна
		if (end_time > current_time):
			# вставляем полученный результат
			text.insert( '1.0', '\n\n')
			text.insert( '1.0', row[4] )
			text.insert( '1.0', '\n')
			text.insert( '1.0', row[3] )
			text.insert( '1.0', '\n')
			text.insert( '1.0', row[2])
			text.insert( '1.0', ', азимут: ' )
			text.insert( '1.0', row[1] )
			text.insert( '1.0', '-' )
			text.insert( '1.0', row[0])
			text.insert( '1.0', '\n* ')

# поле для ввода CIDa
entry = Entry( window, width = 11 )

# область для вывода ответов на запросы к БД
text = Text(width = 58, height = 37, bg = "white", fg = 'black', wrap = WORD, font=("Verdana", 8) )
text.place( x = 8, y = 65 )


label_lac = Label( window, text = 'LAC: ' )
label_cid = Label( window, text = 'CID: ' )
btn = Button( window, text = 'Поиск', command = getInfo )


#куда сохранять выбор оператора
opsos = StringVar()
OPTIONS = ["Билайн", "Мегафон", "МТС", "Tele2", "Motiv"]
opsos.set(OPTIONS[4]) # значение по-умолчанию
operator_list = OptionMenu(window, opsos, *OPTIONS)




# расположение элементов в окне
label_lac.place( x = 5, y = 20 )
operator_list.place( x = 50, y = 15 )
label_cid.place( x = 165, y = 20 )
entry.place( x = 215, y = 20 )
btn.place( x = 340, y = 15 )


# размеры окна
window_height = 600
window_width = 430

# показываем окно по центру
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

window.mainloop()