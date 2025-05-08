import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3
import csv
from datetime import datetime
import matplotlib.pyplot as plt

# connect to the SQLite database
conn = sqlite3.connect('expense.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses  
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT,
    date TEXT, 
    amount REAL, 
    category TEXT
    )
''')

# Categories 
category_options = [
    'Food', 'Transport', 'Utilities', 'Entertainment', 'Shopping',
      'Healthcare', 'Rent', 'Education', 'Other'
      ]

# function to add an expense
def add_expense():
    date = entry_date.get()
    category = combo_category.get()
    name = entry_name.get()
   
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter a valid amount')
        return
    
    if name and date and amount and category:
            cursor.execute('''INSERT INTO expenses (name, date, amount, category) VALUES (?, ?, ?, ?)''', 
                           (name, date, amount, category))
            conn.commit()
            messagebox.showinfo('Success', 'Expense added successfully')
            entry_name.delete(0, tk.END)
            entry_date.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            combo_category.set('')     
    else:
        messagebox.showerror('Error', 'Please fill all fields')

# function to export expenses to a CSV file
def export_to_csv():
    cursor.execute('''SELECT * FROM expenses''')
    data = cursor.fetchall()

    with open('expenses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Date', 'Amount', 'Category'])
        writer.writerows(data)

    messagebox.showinfo('Success', 'Expenses exported to expenses.csv')

# function to show a bar chart of expenses by category
def show_graph():
    cursor.execute('''SELECT category, SUM(amount) FROM expenses GROUP BY category''')
    data = cursor.fetchall()

    if data:
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.figure(figsize=(10, 5))
        plt.bar(categories, amounts, color=['skyblue','lightgreen','yellow','red','purple','orange','pink','brown','gray','black','white'])
        plt.xlabel('Category')
        plt.ylabel('Amount spent')
        plt.title('Expenses distribution')
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror('Error', 'No data to display')

# function to filter and show monthly summary
def show_monthly_summary():
    month = combo_month.get()
    year = combo_year.get()
    if not(month and year):
        messagebox.showerror('Error', 'Please select both month and year')
        return
    
    month_number = datetime.strptime(month, "%B").month
    pattern = f"%02d-%02d-%%y" %(1, month_number)

    cursor.execute('''
                   SELECT SUM(amount) FROM expenses 
                   WHERE strftime('%Y-%m', date) = ?''', 
                   (f"{month_number:02d}",year))
    
    results = cursor.fetchone()
    total = sum([r[0] for r in results]) if results else 0
    label_summary.config(text=f"Total expenses for {month} {year}: ${total:.2f}")

    
# create the main window
root = tk.Tk()
root.title('Expense Tracker')
root.geometry('700x700')

# UI Widgets
tk.Label(root, text='Expense Name:').pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text='Date (dd-mm-yyyy):').pack()
entry_date = DateEntry(root, date_pattern='dd-mm-yyyy')
entry_date.pack()

tk.Label(root, text='Amount:').pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

# Button Widgets
tk.Label(root, text='Category:').pack()
combo_category = ttk.Combobox(root, values=category_options, state='readonly')
combo_category.pack()

tk.Button(root, text='Add Expense', command=add_expense).pack()
tk.Button(root, text='Export to CSV', command=export_to_csv).pack()
tk.Button(root, text='Show Graph', command=show_graph).pack()

# monthly filtter
tk.Label(root, text='--- Monthly Summary ---').pack(pady=10)
months = [datetime(2000, m, 1).strftime('%B') for m in range(1, 13)]
year = [str(y) for y in range(2020, datetime.now().year +1)]

combo_month = ttk.Combobox(root, values=months, state='readonly')
combo_month.set('Select Month')
combo_month.pack()

combo_year = ttk.Combobox(root, values=year, state='readonly')
combo_year.set('Select Year')
combo_year.pack()

tk.Button(root, text='Show Summary', command=show_monthly_summary).pack()
label_summary = tk.Label(root, text='')
label_summary.pack()

# Handle closing DB connection on app close
def on_closing():
    conn.close()
    root.destroy()

root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()
