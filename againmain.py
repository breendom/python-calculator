from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import math

# =========================
# VARIÁVEIS GLOBAIS
# =========================
expressao = ""
historico = []
tema_atual = "escuro"

# =========================
# TEMAS
# =========================
temas = {
    "escuro": {
        "janela": "#202020",
        "tela": "#202020",
        "texto": "#FFFFFF",
        "botao": "#323232",
        "botao_num": "#3B3B3B",
        "botao_op": "#FFAB40",
        "botao_igual": "#1C8AD3"
    },
    "claro": {
        "janela": "#F3F3F3",
        "tela": "#F3F3F3",
        "texto": "#000000",
        "botao": "#E0E0E0",
        "botao_num": "#FFFFFF",
        "botao_op": "#FFAB40",
        "botao_igual": "#1C8AD3"
    }
}

# =========================
# JANELA
# =========================
janela = Tk()
janela.title("Calculadora Completa")
janela.geometry("360x520")
janela.resizable(False, False)

# =========================
# FUNÇÕES
# =========================
def atualizar_tela():
    if expressao == "":
        valor_texto.set("0")
    else:
        valor_texto.set(expressao)


def adicionar(valor):
    global expressao

    if valor == ",":
        valor = "."

    if valor == "x":
        valor = "*"

    expressao += str(valor)
    atualizar_tela()


def limpar():
    global expressao
    expressao = ""
    atualizar_tela()


def apagar():
    global expressao
    expressao = expressao[:-1]
    atualizar_tela()


def calcular():
    global expressao, historico

    try:
        conta = expressao.replace("÷", "/").replace("x", "*")

        resultado = eval(conta, {"__builtins__": None}, {
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs
        })

        if resultado == int(resultado):
            resultado = int(resultado)

        historico.append(f"{expressao} = {resultado}")
        atualizar_historico()

        expressao = str(resultado)
        atualizar_tela()

    except:
        expressao = ""
        valor_texto.set("Erro")


def porcentagem():
    global expressao

    try:
        expressao += "/100"
        atualizar_tela()
    except:
        valor_texto.set("Erro")


def raiz_quadrada():
    global expressao

    try:
        resultado = math.sqrt(float(eval(expressao)))
        historico.append(f"√{expressao} = {resultado}")
        atualizar_historico()

        if resultado == int(resultado):
            resultado = int(resultado)

        expressao = str(resultado)
        atualizar_tela()

    except:
        expressao = ""
        valor_texto.set("Erro")


def quadrado():
    global expressao

    try:
        resultado = float(eval(expressao)) ** 2
        historico.append(f"{expressao}² = {resultado}")
        atualizar_historico()

        if resultado == int(resultado):
            resultado = int(resultado)

        expressao = str(resultado)
        atualizar_tela()

    except:
        expressao = ""
        valor_texto.set("Erro")


def inverter_sinal():
    global expressao

    try:
        if expressao:
            resultado = float(eval(expressao)) * -1

            if resultado == int(resultado):
                resultado = int(resultado)

            expressao = str(resultado)
            atualizar_tela()
    except:
        valor_texto.set("Erro")


def atualizar_historico():
    lista_historico.delete(0, END)

    for item in historico[-10:]:
        lista_historico.insert(END, item)


def limpar_historico():
    historico.clear()
    atualizar_historico()


def trocar_tema():
    global tema_atual

    if tema_atual == "escuro":
        tema_atual = "claro"
    else:
        tema_atual = "escuro"

    aplicar_tema()


def aplicar_tema():
    tema = temas[tema_atual]

    janela.config(bg=tema["janela"])
    frame_tela.config(bg=tema["tela"])
    frame_botoes.config(bg=tema["janela"])
    frame_historico.config(bg=tema["janela"])

    app_label.config(bg=tema["tela"], fg=tema["texto"])
    titulo_historico.config(bg=tema["janela"], fg=tema["texto"])

    for botao, tipo in botoes:
        if tipo == "num":
            botao.config(bg=tema["botao_num"], fg=tema["texto"])
        elif tipo == "op":
            botao.config(bg=tema["botao_op"], fg="#FFFFFF")
        elif tipo == "igual":
            botao.config(bg=tema["botao_igual"], fg="#FFFFFF")
        else:
            botao.config(bg=tema["botao"], fg=tema["texto"])


def abrir_configuracoes():
    config = Toplevel(janela)
    config.title("Configurações")
    config.geometry("260x180")
    config.resizable(False, False)

    Label(config, text="Configurações da Calculadora", font=("Arial", 12, "bold")).pack(pady=15)

    Button(config, text="Trocar tema claro/escuro", command=trocar_tema, width=25).pack(pady=5)
    Button(config, text="Limpar histórico", command=limpar_historico, width=25).pack(pady=5)
    Button(config, text="Sobre", command=lambda: messagebox.showinfo(
        "Sobre",
        "Calculadora em Python com Tkinter\nCriada para estudo."
    ), width=25).pack(pady=5)


def tecla_pressionada(event):
    tecla = event.char

    if tecla in "0123456789+-*/.":
        adicionar(tecla)
    elif tecla == ",":
        adicionar(".")
    elif event.keysym == "Return":
        calcular()
    elif event.keysym == "BackSpace":
        apagar()
    elif event.keysym == "Escape":
        limpar()


# =========================
# MENU
# =========================
menu = Menu(janela)
janela.config(menu=menu)

menu_arquivo = Menu(menu, tearoff=0)
menu.add_cascade(label="Menu", menu=menu_arquivo)
menu_arquivo.add_command(label="Configurações", command=abrir_configuracoes)
menu_arquivo.add_command(label="Limpar", command=limpar)
menu_arquivo.add_command(label="Sair", command=janela.quit)

# =========================
# TELA
# =========================
valor_texto = StringVar()
valor_texto.set("0")

frame_tela = Frame(janela, height=100)
frame_tela.pack(fill=X)

app_label = Label(
    frame_tela,
    textvariable=valor_texto,
    font=("Arial", 32),
    anchor="e",
    padx=15,
    pady=20
)
app_label.pack(fill=BOTH, expand=True)

# =========================
# BOTÕES
# =========================
frame_botoes = Frame(janela)
frame_botoes.pack()

botoes = []

def criar_botao(texto, linha, coluna, comando, tipo="num", largura=8, altura=2):
    botao = Button(
        frame_botoes,
        text=texto,
        width=largura,
        height=altura,
        font=("Arial", 13, "bold"),
        relief=FLAT,
        command=comando
    )
    botao.grid(row=linha, column=coluna, padx=2, pady=2)
    botoes.append((botao, tipo))
    return botao


criar_botao("C", 0, 0, limpar, "extra")
criar_botao("⌫", 0, 1, apagar, "extra")
criar_botao("%", 0, 2, porcentagem, "extra")
criar_botao("÷", 0, 3, lambda: adicionar("/"), "op")

criar_botao("x²", 1, 0, quadrado, "extra")
criar_botao("√", 1, 1, raiz_quadrada, "extra")
criar_botao("+/-", 1, 2, inverter_sinal, "extra")
criar_botao("x", 1, 3, lambda: adicionar("*"), "op")

criar_botao("7", 2, 0, lambda: adicionar("7"))
criar_botao("8", 2, 1, lambda: adicionar("8"))
criar_botao("9", 2, 2, lambda: adicionar("9"))
criar_botao("-", 2, 3, lambda: adicionar("-"), "op")

criar_botao("4", 3, 0, lambda: adicionar("4"))
criar_botao("5", 3, 1, lambda: adicionar("5"))
criar_botao("6", 3, 2, lambda: adicionar("6"))
criar_botao("+", 3, 3, lambda: adicionar("+"), "op")

criar_botao("1", 4, 0, lambda: adicionar("1"))
criar_botao("2", 4, 1, lambda: adicionar("2"))
criar_botao("3", 4, 2, lambda: adicionar("3"))
criar_botao("=", 4, 3, calcular, "igual")

criar_botao("0", 5, 0, lambda: adicionar("0"), "num")
criar_botao(",", 5, 1, lambda: adicionar("."))
criar_botao("(", 5, 2, lambda: adicionar("("), "extra")
criar_botao(")", 5, 3, lambda: adicionar(")"), "extra")

# =========================
# HISTÓRICO
# =========================
frame_historico = Frame(janela)
frame_historico.pack(fill=BOTH, expand=True, pady=5)

titulo_historico = Label(frame_historico, text="Histórico", font=("Arial", 12, "bold"))
titulo_historico.pack()

lista_historico = Listbox(frame_historico, height=5, font=("Arial", 10))
lista_historico.pack(fill=BOTH, expand=True, padx=10, pady=5)

# =========================
# TECLADO
# =========================
janela.bind("<Key>", tecla_pressionada)

# =========================
# INICIAR
# =========================
aplicar_tema()
janela.mainloop()