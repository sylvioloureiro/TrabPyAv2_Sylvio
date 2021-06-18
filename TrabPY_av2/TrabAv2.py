import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb
from tkinter import *
import sqlite3

root = Tk()
root.title("CONTROLE DE NOTAS")
width = 800
height = 400
sc_width = root.winfo_screenwidth()
sc_height = root.winfo_screenheight()
x = (sc_width/2) - (width/2)
y = (sc_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#6666ff")

# VARIAVEIS 
materia= StringVar()
nomeAluno = StringVar()
notaav1 = StringVar()
notaav2 = StringVar()
notaav3 = StringVar()
notaavd = StringVar()
notaavds = StringVar()
updateWindow = None
id = None
newWindow = None
notas = [0, 0, 0, 0, 0]  #indice 0 = av1, indice 1 = av2, indice 2 = av3, indice 3 = avd, indice 4 = avds

# METODOS 
def database():

    conn = sqlite3.connect("Alunos.db")
    cursor = conn.cursor()
    query = """ CREATE TABLE IF NOT EXISTS 'Notas' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, materia TEXT,
                nomeAluno TEXT, notaav1 TEXT, notaav2 TEXT, notaav3 TEXT, notaavd TEXT, notaavds TEXT) """
    cursor.execute(query)
    cursor.execute('SELECT * FROM Notas ORDER BY nomeAluno')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def submitData():
    global notas, notaav1, notaav2, notaav3, notaavd, notaavds

    notas[0] = float(notaav1.get())
    notas[1] = float(notaav2.get())
    notas[2] = float(notaav3.get())
    notas[3] = float(notaavd.get())
    notas[4] = float(notaavds.get())

    if materia.get() == "" or nomeAluno.get() == "" or notaav1.get() == "" or notaav2.get() == "" or notaav3.get() == "" or notaav3.get() == "" or notaavd.get() == "" or notaavds.get() == "":
        resultado = msb.showwarning("", "PREENCHA TODOS OS CAMPOS.", icon="warning")
    else:
        
        reprovado = False
        if (notas[0]+notas[1]+notas[3]) / 3 < 6:
            menor_nota = 10
            for nota in [notas[0], notas[1], notas[3]]:
                if nota < menor_nota:
                    menor_nota = nota
            
            menor_nota_index = notas.index(menor_nota)
            prova = ''
            prova_reprovada = ""
            
            if menor_nota_index in [0, 1]:
                prova = "v3"

                if menor_nota_index == 0:
                    prova_reprovada = "v1"
                elif menor_nota_index == 1:
                    prova_reprovada = "v2"
            elif menor_nota_index == 3:
                prova = "vds"

            if prova == "v3":
                if prova_reprovada == "v1":
                    notas[0] = notas[2]
                elif prova_reprovada == "v2":
                    notas[1] = notas[2]
            elif prova == "vds":
                notas[3] = notas[4]
            
            if (notas[0]+notas[1]+notas[3]) / 3 < 6:
                reprovado = True
        print(reprovado)
        
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("Alunos.db")
        cursor = conn.cursor()
        query = """ INSERT INTO 'Notas' (materia, nomeAluno, notaav1, notaav2, notaav3, notaavd, notaavds) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, (str(materia.get()), str(nomeAluno.get()), str(notaav1.get()), 
                        str(notaav2.get()), str(notaav3.get()), str(notaavd.get()), str(notaavds.get())))
        conn.commit()
        cursor.execute('SELECT * FROM Notas ORDER BY nomeAluno')
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data)) 
        cursor.close()
        conn.close()
        materia.set("")
        nomeAluno.set("")
        notaav1.set("")
        notaav2.set("")
        notaav3.set("")
        notaavd.set("")
        notaavds.set("")

def updateData():

    tree.delete(*tree.get_children())
    conn = sqlite3.connect("Alunos.db")
    cursor = conn.cursor()
    query = """ UPDATE 'Notas' SET materia = ?,nomeAluno = ?, notaav1 = ?, notaav2 = ?, notaav3 = ?, notaavd = ?, notaavds = ? WHERE id = ?"""
    cursor.execute(query, (str (materia.get()), str(nomeAluno.get()), str(notaav1.get()),
                           str(notaav2.get()), str(notaav3.get()), str(notaavd.get()), str(notaavds()), int(id)))
    conn.commit()
    cursor.execute('SELECT * FROM Notas ORDER BY nomeAluno')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

    materia.set("")
    nomeAluno.set("")
    notaav1.set("")
    notaav2.set("")
    notaav3.set("")
    notaavd.set("")
    notaavds.set("")
    updateWindow.destroy()

def onSelect(event):

    global id, updateWindow
    selectItem = tree.focus()
    conteudo = (tree.item(selectItem))
    selectedItem = conteudo["values"]
    id = selectedItem[0]

    materia.set("")
    nomeAluno.set("")
    notaav1.set("")
    notaav2.set("")
    notaav3.set("")
    notaavd.set("")
    notaavds.set("")

    materia.set(selectedItem[1])
    nomeAluno.set(selectedItem[2])
    notaav1.set(selectedItem[3])
    notaav2.set(selectedItem[4])
    notaav3.set(selectedItem[5])
    notaavd.set(selectedItem[6])
    notaavds.set(selectedItem[7])

    # CRIANDO JANELA UPDATE 
    updateWindow = Toplevel()
    updateWindow.title("NOTAS")
    width = 480
    heigth = 200
    sc_width = updateWindow.winfo_screenwidth()
    sc_height = updateWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    updateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateWindow.resizable(0, 0)

    # FRAME DO ATUALIZAR
    formTitle = Frame(updateWindow)
    formTitle.pack(side=TOP)
    formContact = Frame(updateWindow)
    formContact.pack(side = TOP, pady = 10)

    # LABEL DO ATUALIZAR
    lbl_title = Label(formTitle, text="ATUALIZANDO DADOS", font=('arial', 14), bg='OliveDrab1', width=300)
    lbl_title.pack(fill=X)

    lbl_materia = Label(formContact, text="MATERIA", font=('arial', 10))
    lbl_materia.grid(row=0, sticky=W)
    lbl_nomeAluno = Label(formContact, text="ALUNO", font=('arial', 10))
    lbl_nomeAluno.grid(row=1, sticky=W)
    lbl_notaav1 = Label(formContact, text="AV1", font=('arial', 10))
    lbl_notaav1.grid(row=2, sticky=W)
    lbl_notaav2 = Label(formContact, text="AV2", font=('arial', 10))
    lbl_notaav2.grid(row=3, sticky=W)
    lbl_notaav3 = Label(formContact, text="AV3", font=('arial', 10))
    lbl_notaav3.grid(row=4, sticky=W)
    lbl_notaavd = Label(formContact, text="AVD", font=('arial', 10))
    lbl_notaavd.grid(row=5, sticky=W)
    lbl_notaavds = Label(formContact, text="AVDS", font=('arial', 10))
    lbl_notaavds.grid(row=6, sticky=W)
  

    # ENTRY DO ATUALIZAR 
    materiaEntry = Entry(formContact, textvariable=materia, font=('arial', 8))
    materiaEntry.grid(row=0, column=1)
    nomeAlunoEntry = Entry(formContact, textvariable=nomeAluno, font=('arial', 8))
    nomeAlunoEntry.grid(row=1, column=1)
    notaav1Entry = Entry(formContact, textvariable=notaav1, font=('arial', 8))
    notaav1Entry.grid(row=2, column=1)
    notaav2Entry = Entry(formContact, textvariable=notaav2, font=('arial', 8))
    notaav2Entry.grid(row=3, column=1)
    notaav3Entry = Entry(formContact, textvariable=notaav3, font=('arial', 8))
    notaav3Entry.grid(row=4, column=1)
    notaavdEntry = Entry(formContact, textvariable=notaavd, font=('arial', 8))
    notaavdEntry.grid(row=5, column=1)
    notaavdsEntry = Entry(formContact, textvariable=notaavds, font=('arial', 8))
    notaavdsEntry.grid(row=6, column=1)
    
    # BUTTON DO ATUALIZAR
    bttn_update = Button(formContact, text="ATUALIZAR", width=50, command=updateData)
    bttn_update.grid(row=7, columnspan=2, pady=10)

def deletarData():

    if not tree.selection():
        resultado = msb.showwarning("", "POR FAVOR, SELECIONE UMA LINHA.", icon="warning")
    else:
        resultado = msb.askquestion("", "DESEJA DELETAR?")
        if resultado == 'yes':
            selectItem = tree.focus()
            conteudo = (tree.item(selectItem))
            selectedItem = conteudo['values']
            tree.delete(selectItem)
            conn = sqlite3.connect("Alunos.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM 'Notas' WHERE id = %d" % selectedItem[0])
            conn.commit()
            cursor.close()
            conn.close()

def inserirData():

    global newWindow
    materia.set("")
    nomeAluno.set("")
    notaav1.set("")
    notaav2.set("")
    notaav3.set("")
    notaavd.set("")
    notaavds.set("")

    # CRIANDO JANELA INCLUDE 
    newWindow = Toplevel()
    newWindow.title("NOVO CADASTRO")
    width = 480
    heigth = 200
    sc_width = newWindow.winfo_screenwidth()
    sc_height = newWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    newWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    newWindow.resizable(0, 0)

    # FRAME DO INCLUDE
    formTitle = Frame(newWindow)
    formTitle.pack(side=TOP)
    formContact = Frame(newWindow)
    formContact.pack(side=TOP, pady=10)

    # LABEL DO INCLUDE 
    lbl_title = Label(formTitle, text="NOVO CADASTRO DE NOTAS",
                      font=('arial', 18), bg='gray', width=300)
    lbl_title.pack(fill=X)
    lbl_materia = Label(formContact, text="MATERIA", font=('arial', 10))
    lbl_materia.grid(row=0, sticky=W)
    lbl_nomeAluno = Label(formContact, text="ALUNO", font=('arial', 10))
    lbl_nomeAluno.grid(row=1, sticky=W)
    lbl_notaav1 = Label(formContact, text="AV1", font=('arial', 10))
    lbl_notaav1.grid(row=2, sticky=W)
    lbl_notaav2 = Label(formContact, text="AV2", font=('arial', 10))
    lbl_notaav2.grid(row=3, sticky=W)
    lbl_notaav3 = Label(formContact, text="AV3", font=('arial', 10))
    lbl_notaav3.grid(row=4, sticky=W)
    lbl_notaavd = Label(formContact, text="AVD", font=('arial', 10))
    lbl_notaavd.grid(row=5, sticky=W)
    lbl_notaavds = Label(formContact, text="AVDS", font=('arial', 10))
    lbl_notaavds.grid(row=6, sticky=W)

    # ENTRY DO INCLUDE 
    materiaEntry = Entry(formContact, textvariable=materia, font=('arial', 10))
    materiaEntry.grid(row=0, column=1)
    nomeAlunoEntry = Entry(formContact, textvariable=nomeAluno, font=('arial', 10))
    nomeAlunoEntry.grid(row=1, column=1)
    notaav1Entry = Entry(formContact, textvariable=notaav1, font=('arial', 10))
    notaav1Entry.grid(row=2, column=1)
    notaav2Entry = Entry(formContact, textvariable=notaav2, font=('arial', 10))
    notaav2Entry.grid(row=3, column=1)
    notaav3Entry = Entry(formContact, textvariable=notaav3, font=('arial', 10))
    notaav3Entry.grid(row=4, column=1)
    notaavdEntry = Entry(formContact, textvariable=notaavd, font=('arial', 10))
    notaavdEntry.grid(row=5, column=1)
    notaavdsEntry = Entry(formContact, textvariable=notaavds, font=('arial', 10))
    notaavdsEntry.grid(row=6, column=1)

    # BUTTON DO INCLUDE 
    bttn_inserir = Button(formContact, text="CADASTRAR",
                        width=50, command=submitData)
    bttn_inserir.grid(row=7, columnspan=2, pady=10)

def sobreApp():
    pass

# FRAMES TELA PRINCIPAL
top = Frame(root, width=500, bd=1,relief=SOLID)
top.pack(side=TOP)
mid = Frame(root, width=500, bg="#6666ff")
mid.pack(side=TOP)
midLeft = Frame(mid, width=100)
midLeft.pack(side=LEFT)
midLeftPadding = Frame(mid, width=350, bg="#6666ff")
midLeftPadding.pack(side=LEFT)
midRight = Frame(mid, width=100)
midRight.pack(side=RIGHT)
bottom = Frame(root, width=200)
bottom.pack(side=BOTTOM)
tableMargim = Frame(root, width=500)
tableMargim.pack(side=TOP)


# LABELS TELA PRINCIPAL 
lbl_title = Label(top, text="GERENCIAMENTO DE NOTAS - ESTÁCIO", font=('arial', 13), width=500)
lbl_title.pack(fill=X)

lbl_alt = Label(bottom, text="PARA EDITAR CLIQUE DUAS VEZES SOBRE O CADASTRO.", font=('arial', 10), width=200)
lbl_alt.pack(fill=X)

# BUTTONS TELA PRINCIPAL 
bttn_add = Button(midLeft, text="INSERIR", bg="OliveDrab1", command=inserirData)
bttn_add.pack()
bttn_del = Button(midRight, text="APAGAR",
                 bg="orange red", command=deletarData)
bttn_del.pack(side=RIGHT)

# TREEVIEW TELA PRINCIPAL
scrollbarX = Scrollbar(tableMargim, orient=HORIZONTAL)
scrollbarY = Scrollbar(tableMargim, orient=VERTICAL)

tree = ttk.Treeview(tableMargim, columns=("ID", "Materia", "Nome do Aluno", "Nota AV1", "Nota AV2", "Nota AV3", "Nota AVD", "Nota AVDS"), height=400, 
                    selectmode="extended", yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
scrollbarY.config(command=tree.yview)
scrollbarY.pack(side=RIGHT, fill=Y)
scrollbarX.config(command=tree.xview)
scrollbarX.pack(side=BOTTOM, fill=X)

tree.heading("ID", text="ID", anchor=W)
tree.heading("Materia", text="MATÉRIA", anchor=W)
tree.heading("Nome do Aluno", text="ALUNO", anchor=W)
tree.heading("Nota AV1", text="AV1", anchor=W)
tree.heading("Nota AV2", text="AV2", anchor=W)
tree.heading("Nota AV3", text="AV3", anchor=W)
tree.heading("Nota AVD", text="AVD", anchor=W)
tree.heading("Nota AVDS", text="AVDS", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=60)
tree.column('#1', stretch=NO, minwidth=0, width=60)
tree.column('#2', stretch=NO, minwidth=0, width=60)
tree.column('#3', stretch=NO, minwidth=0, width=60)
tree.column('#4', stretch=NO, minwidth=0, width=60)
tree.column('#5', stretch=NO, minwidth=0, width=60)
tree.column('#6', stretch=NO, minwidth=0, width=60)
tree.column('#7', stretch=NO, minwidth=0, width=60)

tree.pack()
tree.bind('<Double-Button-1>', onSelect)

# CRIANDO MENU 
menu_bar = Menu(root)
root.config(menu=menu_bar)

# MENU
fileMenu = Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label="MENU", menu=fileMenu)
fileMenu.add_command(label="NOVO CADASTRO", command=inserirData)
fileMenu.add_separator()
fileMenu.add_command(label="SAIR", command=root.destroy)

# INICIANDO
if __name__ == '__main__':
    database()
    root.mainloop()
