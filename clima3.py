import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import datetime
import io
import locale

# Locale para português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

API_KEY = "4711725945579ad9e2395cc4ad321251"


class OxenteChuvaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OxênteChuva?")
        self.geometry("800x500")
        self.configure(bg="#0A1733")

        self.tela1 = TelaInicial(self)
        self.tela2 = TelaClima(self)

        self.tela1.pack(fill="both", expand=True)

    def mostrar_tela2(self, dados_clima):
        self.tela1.pack_forget()
        self.tela2.atualizar_dados(dados_clima)
        self.tela2.pack(fill="both", expand=True)


class TelaInicial(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#0A1733")
        self.master = master

        tk.Label(self, text="OxênteChuva? ☁️", font=("Tahoma", 22, "bold"), bg="#0A1733", fg="#50C7E0").pack(pady=10)

        tk.Label(self, text="Digite sua cidade:", bg="#0A1733", fg="white", font=("Arial", 12)).pack()
        self.entry_cidade = tk.Entry(self, font=("Arial", 14), bg="#DCEBFB", justify="center")
        self.entry_cidade.pack(pady=5, ipadx=20, ipady=5)

        tk.Label(self, text="Escolha a data:", bg="#0A1733", fg="white", font=("Arial", 12)).pack()
        self.datas_opcoes = obter_datas()
        self.data_var = tk.StringVar(self)
        self.data_var.set(self.datas_opcoes[0][1])
        self.data_menu = ttk.Combobox(self, textvariable=self.data_var,
                                      values=[d[1] for d in self.datas_opcoes], state="readonly")
        self.data_menu.pack(pady=5)

        tk.Button(self, text="Ver Clima", command=self.buscar_tempo,
                  font=("Arial", 12, "bold"), bg="#0094E0", fg="white").pack(pady=20)

    def buscar_tempo(self):
        cidade = self.entry_cidade.get().strip()
        data = self.data_var.get()
        if not cidade:
            tk.messagebox.showerror("Erro", "Digite uma cidade.")
            return

        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&lang=pt_br"
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception("Erro na requisição.")
            dados = resp.json()
            previsao = next((item for item in dados['list'] if item['dt_txt'].startswith(data)), None)

            if not previsao:
                tk.messagebox.showerror("Erro", "Data não encontrada.")
                return

            # Montar dicionário de dados
            clima_dados = {
                "cidade": cidade,
                "temperatura": previsao['main']['temp'] - 273.15,
                "descricao": previsao['weather'][0]['description'].capitalize(),
                "data": data,
                "hora": previsao['dt_txt'].split()[1][:5],
                "icone": previsao['weather'][0]['icon'],
                "chuva": previsao.get('rain', {}).get('3h', 0),
                "umidade": previsao['main']['humidity'],
                "pressao": previsao['main']['pressure'],
                "vento": previsao['wind']['speed'] * 3.6,
                "sensacao": previsao['main'].get('feels_like', 0) - 273.15,
                "direcao_vento": previsao['wind'].get('deg', 0),
                "uv": 0,
                "aqi": 0,
                "umidade_solo": 0
            }

            self.master.mostrar_tela2(clima_dados)

        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao obter dados: {e}")


class TelaClima(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#0D1B3A")
        self.master = master
        self.label_cidade = tk.Label(self, text="", font=("Arial", 20, "bold"), bg="#0D1B3A", fg="#50C7E0")
        self.label_cidade.pack(pady=10)

        self.imagem_clima = tk.Label(self, bg="#0D1B3A")
        self.imagem_clima.pack()

        self.label_temp = tk.Label(self, text="", font=("Arial", 40, "bold"), bg="#0D1B3A", fg="#30C0FF")
        self.label_temp.pack()

        self.label_desc = tk.Label(self, text="", font=("Arial", 16), bg="#0D1B3A", fg="white")
        self.label_desc.pack()

        self.info_extra = tk.Label(self, text="", bg="#0D1B3A", fg="white", font=("Arial", 10), justify="left")
        self.info_extra.pack(pady=10)

        tk.Button(self, text="Voltar", command=self.voltar, bg="#0094E0", fg="white").pack(pady=10)

    def atualizar_dados(self, dados):
        self.label_cidade.config(text=f"{dados['cidade'].upper()}")
        self.label_temp.config(text=f"{dados['temperatura']:.0f}°C")
        self.label_desc.config(text=f"{dados['descricao']}\n{formatar_data(dados['data'])} {dados['hora']}")

        try:
            url_icon = f"https://openweathermap.org/img/wn/{dados['icone']}@2x.png"
            img_data = requests.get(url_icon).content
            img = Image.open(io.BytesIO(img_data)).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            self.imagem_clima.config(image=img_tk)
            self.imagem_clima.image = img_tk
        except:
            self.imagem_clima.config(image='')

        self.info_extra.config(text=f"""
Quantidade de chuva acumulada: {dados['chuva']} mm
Índice de qualidade do ar (AQI): {dados['aqi']}
Umidade do solo: {dados['umidade_solo']}%
Umidade do ar: {dados['umidade']}%
Velocidade do vento: {dados['vento']:.1f} km/h
Direção do vento: {dados['direcao_vento']}°
Índice UV: {dados['uv']}
Sensação térmica: {dados['sensacao']:.0f}°C
Pressão atmosférica: {dados['pressao']} hPa
        """)

    def voltar(self):
        self.pack_forget()
        self.master.tela1.pack(fill="both", expand=True)


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


def formatar_data(data_str):
    dt = datetime.datetime.strptime(data_str, "%Y-%m-%d")
    return dt.strftime("%A").capitalize()


if __name__ == "__main__":
    app = OxenteChuvaApp()
    app.mainloop()