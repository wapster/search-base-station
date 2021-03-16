import sqlite3
from tkinter import *
import tkinter.messagebox as box

from datetime import datetime

window = Tk()
window.title("Поиск БС")
window.resizable(0, 0)

# window.iconbitmap('@bs.xbm')
def clear():
	entry.delete(0, END)

def clearTextArea():
	text.delete(1.0, END)
	
	
# всплывающее окошко
def dialog():
	box.showinfo( 'Поиск БС', lac_entry.get() + "-" + cid_entry.get() + "\n" + "ничего не найдено")
	# box.showinfo( 'Адрес БС', 'CID: ' + opsos.get() )

# срабатывание при нажати Enter
def getInfoReturn(e):
    getInfo()
window.bind('<Return>', getInfoReturn)


def getInfo():
	# работа с БД
	connection = sqlite3.connect("all_bs.db")
	cursor = connection.cursor()

	counter = cursor.execute("SELECT COUNT(*) FROM `bs` WHERE Lac = '" + lac_entry.get() + "' AND Cellid = '" + cid_entry.get() + "' AND `EndTime` > datetime('now')").fetchone()
	
	# если нашли то, что искали
	if (counter[0] > 0):
		row = cursor.execute("SELECT `EndTime`, `Address`, `Lac`, `Cellid`, `Azimut`, `BSFrequency` FROM `bs` WHERE Lac = '" + lac_entry.get() + "' AND Cellid = '" + cid_entry.get() + "' AND `EndTime` > datetime('now')").fetchone()
		text.insert( '1.0', '---------------------------------------------------------' )
		text.insert( '1.0', '\n\n')
		text.insert( '1.0', row[5] )
		text.insert( '1.0', 'частота: ' )
		text.insert( '1.0', '\n')
		text.insert( '1.0', row[4] )
		text.insert( '1.0', 'азимут: ' )
		text.insert( '1.0', '\n')
		text.insert( '1.0', row[1])
		text.insert( '1.0', '\n')
		text.insert( '1.0', row[3] )
		text.insert( '1.0', '-' )
		text.insert( '1.0', row[2])
		text.insert( '1.0', '\n* ')
	
	# если не нашли то, что искали
	if (counter[0] == 0):
		dialog()

	



# поле для ввода LACa
lac_entry = Entry( window, width = 11 )

# поле для ввода CIDa
cid_entry = Entry( window, width = 11 )

# область для вывода ответов на запросы к БД
text = Text(width = 51, height = 26, bg = "white", fg = 'black', wrap = WORD, font=("Verdana", 10) )
text.place( x = 8, y = 65 )


label_lac = Label( window, text = 'LAC: ' )
label_cid = Label( window, text = 'CID: ' )
btn = Button( window, text = 'Поиск', command = getInfo )
btn_clear = Button( window, text = 'Очистить', command = clearTextArea)


# расположение элементов в окне
label_lac.place( x = 5, y = 20 )
label_cid.place( x = 120, y = 20 )

lac_entry.place( x = 40, y = 20 )
cid_entry.place( x = 150, y = 20 )

btn.place( x = 250, y = 18 )
btn_clear.place( x = 360, y = 18)


# размеры окна
window_height = 500
window_width = 430

# показываем окно по центру
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

window.mainloop()