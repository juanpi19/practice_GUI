import tkinter as tk
import time
from tkinter import *
from tkinter import ttk
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)




conn = sqlite3.connect('expense.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenseTracker
    (amount Int,
     datestamp Datetime,
     reason Text)''')
c.close()
conn.commit()
conn.close()

def savedata():
    conn = sqlite3.connect('expense.db')
    c=conn.cursor()
    c.execute('INSERT INTO expenseTracker(amount, datestamp, reason) VALUES (?, ?, ?)', (entry.get(), entry2.get(), entry3.get()))
    #c.execute('INSERT INTO expenseTracker(datestamp) VALUES (?)', [entry2.get()])
    #c.execute('INSERT INTO expenseTracker(reason) VALUES (?)', [entry3.get()])
    c.close()
    conn.commit()
    conn.close()
    label5['text'] = "Data successfully saved"


def fetchdata():
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    sql = "select * from expenseTracker"
    results = c.execute(sql)
    all_results = results.fetchall()
    c.close()
    conn.close()
    output = ' '
    for x in all_results:
        output = str(output)+str(x[0])+' '+str(x[1])+' '+str(x[2])+'\n'
    return output
    #output = ["\n"]
    #for i in all_results:
        #output = [output]+[i[0]]+[i[1]]+[i[2]
        #output.append(str(i).strip('[]'))
    #return output

def add_record():
    my_tree.insert('', tk.END, values=(entry.get(), entry2.get(), entry3.get()))
    entry.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)




def deletedata():
    x = my_tree.selection()[0]
    my_tree.delete(x)




root = tk.Tk()
root.geometry('700x500')

tab = ttk.Notebook(root)

f1 = Frame(tab, width=500, height=500)
f2 = Frame(tab, width=500, height=500)
f3 = Frame(tab, width=500, height=500)

tab.add(f1, text = 'Expense')
tab.add(f2, text = 'Analysis')
tab.add(f3, text = 'Budget')


tab.pack(fill=BOTH, expand=1)


# ------------ f1 window: where the expenses are added -------------------------
my_tree = ttk.Treeview(f1, column = ('amount', 'datestamp', 'reason'), show='headings')


my_tree.column("#0", width=120, minwidth=25)
my_tree.column("amount", anchor=W ,width=60)
my_tree.column("datestamp", anchor=CENTER  ,width=60)
my_tree.column("reason", anchor=W ,width=60)

my_tree.heading("#0", text = 'Label', anchor=W)
my_tree.heading("#1", text = 'Amount', anchor=W)
my_tree.heading("#2", text = 'Date', anchor=CENTER)
my_tree.heading("#3", text = 'Reason', anchor=W)

my_tree.place(relx = 0.40, rely = 0.19, relheight = 0.70, relwidth = 0.55)

label5 = tk.Label(f1, bg = 'blue')
label5.place(relx = 0.53, rely = 0.87, relheight = 0.08, relwidth = 0.30)

button = tk.Button(f1, bg='blue', text='Save your expense', font='arial', command=savedata)
button.place(relx = 0.07, rely = 0.075, relheight = 0.09, relwidth = 0.25)

my_treeButton = Button(f1, text = 'Display records', command= add_record)
my_treeButton.place(relx = 0.40, rely = 0.075, relheight = 0.09, relwidth = 0.25)

button3 = tk.Button(f1, bg='blue', text='Delete all data', font='arial', command=deletedata)
button3.place(relx = 0.70, rely = 0.075, relheight = 0.09, relwidth = 0.25)

label2 = tk.Label(f1, bg= 'blue', text='Enter amount')
label2.place(relx = 0.1, rely = 0.19, relheight = 0.07, relwidth = 0.20)

entry=tk.StringVar()
entry = tk.Entry(f1, textvariable=entry,  bg = 'white', font = 'Courier')
entry.place(relx = 0.1, rely = 0.29, relheight = 0.08, relwidth = 0.20)

label3 = tk.Label(f1, bg= 'blue', text='Enter date below')
label3.place(relx = 0.1, rely = 0.47, relheight = 0.07, relwidth = 0.20)

entry2=tk.StringVar()
entry2 = tk.Entry(f1, textvariable=entry2, bg = 'white', font = 'Courier')
entry2.place(relx = 0.1, rely = 0.57, relheight = 0.08, relwidth = 0.20)

label4 = tk.Label(f1, bg= 'blue', text='Enter reason')
label4.place(relx = 0.1, rely = 0.77, relheight = 0.07, relwidth = 0.20)

entry3=tk.StringVar()
entry3 = tk.Entry(f1, textvariable=entry3, bg = 'white', font = 'Courier')
entry3.place(relx = 0.1, rely = 0.87, relheight = 0.08, relwidth = 0.20)

# connecting to the data base so it can be permanently displayed
conn = sqlite3.connect('expense.db')
c = conn.cursor()
sql = "select * from expenseTracker"
results = c.execute(sql)
all_results = results.fetchall()
for i in all_results:
    my_tree.insert('', index='end', values=(i[0], i[1], i[2]))
# --------------------- end of f1 window ---------------------

# ------------------- f2 window: some Analysis using pandas are made ----------

# label text for title
ttk.Label(f2, text = "Pick a month to plan budget",
          background = 'green', foreground ="white",
          font = ("Times New Roman", 15)).pack()#grid(row = 0, column = 1)

# label
ttk.Label(f2, text = "Select the Month :",
          font = ("Times New Roman", 10)).pack()#grid(column = 0,
         # row = 5, padx = 10, pady = 25)

# Combobox creation
n = tk.StringVar()
monthchoosen = ttk.Combobox(f2, width = 27, textvariable = n)

# Adding combobox drop down list
monthchoosen['values'] = (' 01',
                          ' 02',
                          ' 03',
                          ' 04',
                          ' 05',
                          ' 06',
                          ' 07',
                          ' 08',
                          ' 09',
                          ' 10',
                          ' 11',
                          ' 12')

monthchoosen.pack()#.grid(column = 1, row = 5)
monthchoosen.current()


def bar_chart():
    figure1 = plt.Figure(figsize=(3,2), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, f2)
    conn = sqlite3.connect("expense.db")
    c = conn.cursor()
    df_expense = pd.read_sql_query('SELECT * FROM expenseTracker', conn)
    df_expenses = pd.DataFrame(df_expense, columns=['amount', 'datestamp', 'reason'])
    #df_expenses.datestamp = pd.to_datetime(df_expenses.datestamp)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df_expenses.datestamp = pd.to_datetime(df_expenses.datestamp)
    df1 = df_expenses.groupby(df_expenses.datestamp.dt.month).sum()
    df1.plot(kind='bar',legend=True, ax=ax1)
    ax1.set_title('Amount per month')

def pie_chart():
    figure2 = plt.Figure(figsize=(3,2), dpi=100)
    ax2 = figure2.add_subplot(111)
    bar2 = FigureCanvasTkAgg(figure2, f2)
    conn = sqlite3.connect("expense.db")
    c = conn.cursor()
    df_expense = pd.read_sql_query('SELECT * FROM expenseTracker', conn)
    df_expenses = pd.DataFrame(df_expense, columns=['amount', 'datestamp', 'reason'])
    #df_expenses.datestamp = pd.to_datetime(df_expenses.datestamp)
    bar2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
    df_expenses.datestamp = pd.to_datetime(df_expenses.datestamp)
    df2 = df_expenses.groupby('reason').size()
    df2.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
    ax2.set_title('Reason of expense')

chartButton = Button(f2, text = 'Display chart', command= lambda: [bar_chart(), pie_chart()])
chartButton.place(relx = 0.72, rely = 0.065, relheight = 0.09, relwidth = 0.25)

# ---------------- f2 window ends -------------------------

# ----------------- f3 window starts -----------------------

# ----------------------------------------------
def clickMe():
    f5label = ttk.Label(f3, text= "In the month" + n.get() + " the amount to spend is: $" + c.get() ).place(relx = 0.49, rely = 0.20, relheight = 0.09, relwidth = 0.55)


#f5label = ttk.Label(f3, text=n.get()).place(relx = 0.6, rely = 0.20, relheight = 0.09, relwidth = 0.15)

buttonBudget = ttk.Button(f3, text='Report', command=clickMe)
buttonBudget.place(relx = 0.6, rely = 0.40, relheight = 0.09, relwidth = 0.15)

# label
ttk.Label(f3, text = "Select the Month :",
          font = ("Times New Roman", 10)).grid(column = 0,
          row = 5, padx = 10, pady = 25)

# Combobox creation
n = tk.StringVar()
monthchoosen = ttk.Combobox(f3, width = 27, textvariable = n)

# Adding combobox drop down list
monthchoosen['values'] = (' 1',
                          ' 2',
                          ' 3',
                          ' 4',
                          ' 5',
                          ' 6',
                          ' 7',
                          ' 8',
                          ' 9',
                          ' 10',
                          ' 11',
                          ' 12')
monthchoosen.grid(column = 1, row = 5)
monthchoosen.current()
# ------------------------------------------------------------------------
# sum up every all the expenses for that especific month and subtracting it
# from the amount set to spend that month

#months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#for i in months:




def amount_spent():
    conn = sqlite3.connect("expense.db")
    conn.cursor()
    df_expense = pd.read_sql_query('SELECT * FROM expenseTracker', conn )
    df_expenses = pd.DataFrame(df_expense, columns=['amount', 'datestamp', 'reason'])
    df_expenses.datestamp = pd.to_datetime(df_expenses.datestamp)
    f6label['text'] = f" You have spent: ${df_expenses[df_expenses.datestamp.dt.month == int(n.get())].amount.sum()}."

f6label = ttk.Label(f3)
f6label.place(relx = 0.50, rely = 0.30, relheight = 0.09, relwidth = 0.4)






#-----------------------------------------------------------------\
# entering the amount to spend this month and displaying it using calculate button
def onclick():
    f4label = ttk.Label(f3, text = '  your amount this month is $' + c.get()).place(relx = 0.03, rely = 0.30, relheight = 0.09, relwidth = 0.4)

f3label = ttk.Label(f3, text = 'Enter amount').place(relx = 0.03, rely = 0.20, relheight = 0.09, relwidth = 0.15)

c = StringVar()
f3entry = ttk.Entry(f3, textvariable = c).place(relx = 0.2, rely = 0.20, relheight = 0.09, relwidth = 0.15)

buttonBudget = ttk.Button(f3, text='calculate', command=onclick).place(relx = 0.1, rely = 0.40, relheight = 0.09, relwidth = 0.15)



buttonBudget = ttk.Button(f3, text='Report', command= lambda : [clickMe(), amount_spent()])
buttonBudget.place(relx = 0.6, rely = 0.40, relheight = 0.09, relwidth = 0.15)





root.mainloop()
