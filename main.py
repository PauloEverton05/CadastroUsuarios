##############################
#  CRIADO POR PAULO EVERTON  #
##############################

import tkinter as tk
from tkinter import messagebox
import mysql.connector

def create_database():
    cnx = mysql.connector.connect(
        host='######',
        user='#####',
        password='####',
        database='#####'
    )
    return cnx

def create_table():
    cnx = create_database()
    cursor = cnx.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    idade INT NOT NULL
                )''')
    cnx.commit()
    cnx.close()

def insert_client():
    name = entry_name.get()
    age = entry_age.get()
    
    if name and age:
        try:
            cnx = create_database()
            cursor = cnx.cursor()
            sql = 'INSERT INTO clientes (nome, idade) VALUES (%s, %s)'
            val = (name, age)
            cursor.execute(sql, val)
            cnx.commit()
            cnx.close()
            messagebox.showinfo('Sucesso!', 'Cliente inserido com sucesso.')
        except mysql.connector.Error as e:
            messagebox.showerror('Erro!', f'Erro ao inserir cliente: {e}')
    else:
        messagebox.showerror('Erro!', 'Por favor, preencha todos os campos.')

#criar a interface gráfica
root = tk.Tk()
root.title('Sistema cadastro clientes')

#criar os widgets
label_name = tk.Label(root, text='Nome:')
label_name.grid(row=0, column=0, padx=30, pady=30)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=30, pady=30)

label_age = tk.Label(root, text='Idade:')
label_age.grid(row=1, column=0, padx=30, pady=30)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1, padx=30, pady=30)

btn_insert = tk.Button(root, text='ㅤㅤㅤInserirㅤㅤㅤ', command=insert_client)
btn_insert.grid(row=2, column=0, columnspan=2, padx=30, pady=30)
create_table()

#iniciar a interface gráfica
root.mainloop()