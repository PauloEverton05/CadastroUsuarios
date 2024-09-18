##############################
#  CRIADO POR PAULO EVERTON  #
##############################

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector
from datetime import datetime

def conectar_db():
    return mysql.connector.connect(
        host='localhost',
        user='######',
        password='#######',
        database='academia'
    )

def add_aluno():
    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    cpf = entry_cpf.get()
    email = entry_email.get()

    if not nome or not data_nascimento or not cpf or not email:
        messagebox.showerror("Erro!", "Preencha todos os campos.")
        return
    
    try:
        data_nascimento_formatada = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("Erro!", "Data de nascimento inválida. Use o formato ano-mês-dia (ex: 1998-08-25).")
        return

    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO alunos (nome, data_nascimento, cpf, email) VALUES (%s, %s, %s, %s)', 
            (nome, data_nascimento_formatada, cpf, email)
        )
        conn.commit()
        messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso")
        entry_nome.delete(0, tk.END)
        entry_data_nascimento.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        listar_alunos()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro!", f"Erro ao adicionar aluno: {err}")
    finally:
        conn.close()

def excluir_aluno():
    id = entry_id.get()

    if not id:
        messagebox.showerror("Erro!", "É necessário o ID para excluir!")
        return

    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM alunos WHERE id = %s', (id,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Aluno deletado com sucesso")
        entry_id.delete(0, tk.END)
        listar_alunos()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro!", f"Erro ao deletar aluno: {err}")
    finally:
        conn.close()

def proc_aluno():
    nome = entry_nome.get()

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alunos WHERE nome LIKE %s', ('%' + nome + '%',))
    resultados = cursor.fetchall()
    conn.close()

    listbox.delete(0, tk.END)
    for resultado in resultados:
        listbox.insert(tk.END, str(resultado))

def listar_alunos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alunos')
    resultados = cursor.fetchall()
    conn.close()

    listbox.delete(0, tk.END)
    for resultado in resultados:
        aluno_info = list(resultado)
        aluno_info[2] = aluno_info[2].strftime("%Y-%m-%d")
        listbox.insert(tk.END, str(tuple(aluno_info)))

app = ctk.CTk()
app.title("Cadastro de Alunos")
app.geometry("430x560")

frame = ctk.CTkFrame(app)
frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

form_layout = ctk.CTkFrame(frame)
form_layout.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

label_nome = ctk.CTkLabel(form_layout, text="Nome")
label_nome.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_nome = ctk.CTkEntry(form_layout)
entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

label_data_nascimento = ctk.CTkLabel(form_layout, text="Data de Nascimento (ano-mês-dia)")
label_data_nascimento.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_data_nascimento = ctk.CTkEntry(form_layout)
entry_data_nascimento.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

label_cpf = ctk.CTkLabel(form_layout, text="CPF (apenas números)")
label_cpf.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_cpf = ctk.CTkEntry(form_layout)
entry_cpf.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

label_email = ctk.CTkLabel(form_layout, text="Email")
label_email.grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_email = ctk.CTkEntry(form_layout)
entry_email.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

btn_frame = ctk.CTkFrame(form_layout)
btn_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

btn_add = ctk.CTkButton(btn_frame, text="Adicionar", command=add_aluno, fg_color="#2c7833")
btn_add.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

btn_proc = ctk.CTkButton(btn_frame, text="Buscar", command=proc_aluno, fg_color="#2c7833")
btn_proc.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

label_id = ctk.CTkLabel(form_layout, text="ID para Deletar")
label_id.grid(row=5, column=0, padx=5, pady=5, sticky="w")
entry_id = ctk.CTkEntry(form_layout)
entry_id.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

btn_del = ctk.CTkButton(form_layout, text="Deletar", command=excluir_aluno, fg_color="#782c2c")
btn_del.grid(row=6, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

listbox = tk.Listbox(frame, height=10)
listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

frame.rowconfigure(1, weight=1)
frame.columnconfigure(0, weight=1)

listar_alunos()
app.mainloop()
