import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import datetime
import io
import locale

API_KEY = "4711725945579ad9e2395cc4ad321251"

# Configurar o locale para português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


def obter_datas():
    hoje = datetime.date.today()
    datas = [(hoje + datetime.timedelta(days=i)) for i in range(6)]
    return [
        ("Hoje", datas[0].strftime("%Y-%m-%d")),
        ("Amanhã", datas[1].strftime("%Y-%m-%d")),
        (datas[2].strftime("%A, %d de %B"), datas[2].strftime("%Y-%m-%d")),
        (datas[3].strftime("%A, %d de %B"), datas[3].strftime("%Y-%m-%d")),
        (datas[4].strftime("%A, %d de %B"), datas[4].strftime("%Y-%m-%d")),
        (datas[5].strftime("%A, %d de %B"), datas[5].strftime("%Y-%m-%d"))
    ]


def buscar_tempo():
    cidade = entry.get().strip()
    data = data_var.get()
    if not cidade:
        messagebox.showerror("Erro", "Por favor, insira o nome da cidade.")
        return

    link = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&lang=pt_br"
    requisicao = requests.get(link)

    if requisicao.status_code == 200:
        requisicao_dic = requisicao.json()
        previsao = None
        for item in requisicao_dic['list']:
            if item['dt_txt'].startswith(data):
                previsao = item
                break

        if previsao:
            descricao = previsao['weather'][0]['description'].capitalize()
            temperatura = previsao['main']['temp'] - 273.15
            umidade = previsao['main']['humidity']
            pressao = previsao['main']['pressure']
            vento_vel = previsao['wind']['speed'] * 3.6  # Convertendo para km/h
            chuva = previsao.get('rain', {}).get('3h', 0)
            resultado_label.config(
                text=f"{descricao}\n{temperatura:.2f}°C\nUmidade: {umidade}%\nPressão: {pressao} hPa\nVento: {vento_vel:.2f} km/h\nChuva: {chuva} mm")
            exibir_imagem(previsao['weather'][0]['icon'])
        else:
            messagebox.showerror("Erro", "Data não encontrada na previsão.")
    else:
        messagebox.showerror("Erro", "Não foi possível obter os dados do clima. Verifique o nome da cidade.")


def exibir_imagem(codigo_icone):
    try:
        url = f"https://openweathermap.org/img/wn/{codigo_icone}@2x.png"
        img_data = requests.get(url).content
        img = Image.open(io.BytesIO(img_data)).resize((80, 80))
        img = ImageTk.PhotoImage(img)
        img_label.config(image=img)
        img_label.image = img
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        img_label.config(image='')


# Criar a janela principal
root = tk.Tk()
root.title("OxênteChuva?")
root.geometry("400x500")
root.configure(bg="#0A1733")

# Título
titulo_label = tk.Label(root, text="OxênteChuva? ☁️", font=("Tahoma", 18, "bold"), bg="#0A1733", fg="#50C7E0")
titulo_label.pack(pady=10)

# Entrada de cidade
frame_entry = tk.Frame(root, bg="#0A1733")
frame_entry.pack()

label = tk.Label(frame_entry, text="Digite aqui sua cidade: ☁️", bg="#0A1733", fg="white", font=("Arial", 10, "bold"))
label.pack()

entry = tk.Entry(frame_entry, font=("Arial", 12), bg="#DCEBFB", fg="black", bd=0, justify="center")
entry.pack(pady=5, ipady=5, ipadx=30)

# Seleção de data
label_data = tk.Label(root, text="Data estimada", bg="#0A1733", fg="white", font=("Arial", 10, "bold"))
label_data.pack()

datas_opcoes = obter_datas()
data_var = tk.StringVar(root)
data_var.set(datas_opcoes[0][1])
data_menu = ttk.Combobox(root, textvariable=data_var, values=[opcao[1] for opcao in datas_opcoes], state="readonly",
                         justify="center")
data_menu.pack(pady=5)

# Botão de pesquisa
button = tk.Button(root, text="Pesquisar", command=buscar_tempo, bg="#0094E0", fg="white", font=("Arial", 12, "bold"),
                   bd=0, relief="flat")
button.pack(pady=10, ipadx=40, ipady=5)

# Exibição dos dados
img_label = tk.Label(root, bg="#0A1733")
img_label.pack(pady=5)
resultado_label = tk.Label(root, text="", font=("Arial", 12), bg="#0A1733", fg="white")
resultado_label.pack(pady=10)

# Iniciar interface gráfica
root.mainloop()