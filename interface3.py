import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import datetime

API_KEY = "4711725945579ad9e2395cc4ad321251"


def obter_datas():
    hoje = datetime.date.today()
    datas = [(hoje + datetime.timedelta(days=i)) for i in range(6)]
    return [
        ("hoje", datas[0].strftime("%Y-%m-%d")),
        ("Amanhã", datas[1].strftime("%Y-%m-%d")),
        (datas[2].strftime("%A, %d %B"), datas[2].strftime("%Y-%m-%d")),
        (datas[3].strftime("%A, %d %B"), datas[3].strftime("%Y-%m-%d")),
        (datas[4].strftime("%A, %d %B"), datas[4].strftime("%Y-%m-%d")),
        (datas[5].strftime("%A, %d %B"), datas[5].strftime("%Y-%m-%d"))
    ]


def buscar_tempo():
    cidade = entry.get()
    data = data_var.get()

    link = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&lang=pt_br"
    requisicao = requests.get(link)
    if requisicao.status_code == 200:
        requisicao_dic = requisicao.json()
        previsao = None

        for item in requisicao_dic['list']:
            if data in item['dt_txt']:
                previsao = item
                break

        if previsao:
            descricao = previsao['weather'][0]['description']
            temperatura = previsao['main']['temp'] - 273.15
            resultado_label.config(text=f"{descricao}, {temperatura:.2f}°C")
            exibir_imagem(descricao)
        else:
            messagebox.showerror("Erro", "Data não encontrada na previsão.")
    else:
        messagebox.showerror("Erro", "Não foi possível obter os dados do clima.")


def exibir_imagem(descricao):
    if "nublado" in descricao:
        img = Image.open("nublado.png")
    elif "chuva leve" in descricao:
        img = Image.open("chuva.png")
    elif "chuva moderada" in descricao:
        img = Image.open("trovoada.png")
    elif "nuvens dispersas" in descricao:
        img = Image.open("parcialmente-nublado.png")
    elif "algumas nuvens" in descricao:
        img = Image.open("nebuloso.png")
    elif "sol" in descricao or "céu" in descricao:
        img = Image.open("sol.png")
    else:
        img = Image.open("default.png")

    img = img.resize((50, 50))
    img = ImageTk.PhotoImage(img)
    img_label.config(image=img)
    img_label.image = img


# Criar a janela principal
root = tk.Tk()
root.title("Consulta de Clima")
root.geometry("350x300")

# Criar um rótulo
label = tk.Label(root, text="Digite a cidade:")
label.pack(pady=5)

# Criar um campo de entrada
entry = tk.Entry(root)
entry.pack(pady=5)

# Criar um rótulo para seleção de data
label_data = tk.Label(root, text="Selecione a data:")
label_data.pack(pady=5)

# Criar um menu suspenso para selecionar a data
datas_opcoes = obter_datas()
data_var = tk.StringVar(root)
data_var.set(datas_opcoes[0][1])  # Define a data de hoje como padrão
data_menu = ttk.Combobox(root, textvariable=data_var, values=[opcao[1] for opcao in datas_opcoes])
data_menu.pack(pady=5)

# Criar um botão
button = tk.Button(root, text="Buscar Clima", command=buscar_tempo)
button.pack(pady=10)

# Criar um rótulo para exibir o resultado
resultado_label = tk.Label(root, text="")
resultado_label.pack(pady=10)

# Criar um rótulo para exibir a imagem do clima
img_label = tk.Label(root)
img_label.pack(pady=10)

# Iniciar o loop da interface gráfica
root.mainloop()
