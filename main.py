import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from prophet import Prophet
from datetime import datetime, timedelta
from tkinter import Tk, Label, PhotoImage
# Örnek veri
products = ['Ürün 1', 'Ürün 2', 'Ürün 3', 'Ürün 4', 'Ürün 5',
           'Ürün 6', 'Ürün 7', 'Ürün 8', 'Ürün 9', 'Ürün 10',
           'Ürün 11', 'Ürün 12', 'Ürün 13', 'Ürün 14', 'Ürün 15',
           'Ürün 16', 'Ürün 17', 'Ürün 18', 'Ürün 19', 'Ürün 20',
           'Ürün 21', 'Ürün 22', 'Ürün 23', 'Ürün 24', 'Ürün 25',
           'Ürün 26', 'Ürün 27', 'Ürün 28', 'Ürün 29', 'Ürün 30',
           'Ürün 31', 'Ürün 32', 'Ürün 33', 'Ürün 34', 'Ürün 35',
           'Ürün 36', 'Ürün 37', 'Ürün 38', 'Ürün 39', 'Ürün 40',
           'Ürün 41', 'Ürün 42', 'Ürün 43', 'Ürün 44', 'Ürün 45',
           'Ürün 46', 'Ürün 47', 'Ürün 48', 'Ürün 49', 'Ürün 50']

# Örnek satış verileri (yıllara göre)
sales_data = pd.DataFrame({
    'Yıl': [2020, 2021, 2022, 2023],
    'Ürün 1': [100, 120, 150, 180],
    'Ürün 2': [80, 90, 100, 110],
    'Ürün 3': [60, 70, 80, 90],
    # Diğer ürünlerin verileri...
})

def first():  # giriş formu
    name = "Ali Demir"
    pword = "asd"
    windowKayit = tk.Tk()
    windowKayit.title("Ürün Satış Takip Sistemi")

    window_width = 400
    window_height = 200
    screen_width = windowKayit.winfo_screenwidth()
    screen_height = windowKayit.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    windowKayit.geometry(f"{window_width}x{window_height}+{x}+{y}")
    bg_image = PhotoImage(file="p.png")

    # Resmi göstermek için bir Label oluştur
    background_label = Label(windowKayit, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Başlığı ortalama
    greet = tk.Label(windowKayit, text="Merhaba")
    greet.place(relx=0.5, rely=0.1, anchor="center")

    # Kullanıcı adı ve parola alanlarını ortalama
    label_username = tk.Label(windowKayit, text="Kullanıcı adı: ")
    label_username.place(relx=0.3, rely=0.3, anchor="e")

    entry_username = tk.Entry(windowKayit)
    entry_username.place(relx=0.5, rely=0.3, anchor="w")

    label_pword = tk.Label(windowKayit, text="Parola: ")
    label_pword.place(relx=0.3, rely=0.5, anchor="e")

    entry_pword = tk.Entry(windowKayit, show="*")
    entry_pword.place(relx=0.5, rely=0.5, anchor="w")

    def compare(): # login fonksiyonu
        entered_username = entry_username.get()
        entered_pword = entry_pword.get()
        if entered_username == name and entered_pword == pword:
            windowKayit.destroy()
            second()
            return True
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")
            return False

    login = tk.Button(windowKayit, text="Giriş Yap", command=compare)
    login.place(relx=0.5, rely=0.7, anchor="center")

    windowKayit.mainloop()

def second():  # grafikler, tahmin vs. 2.form
    # Pencere oluşturma
    window = tk.Tk()
    window.title("Ürün Satış Takip Sistemi")
    window.geometry("1000x800")
    bg_image = PhotoImage(file="pexels-vlado-paunovic-1567547-3038740.png")

    # Resmi göstermek için bir Label oluştur
    background_label = Label(window, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Ürün seçme dropdown menüsü
    selected_product = tk.StringVar()
    product_dropdown = ttk.Combobox(window, textvariable=selected_product, values=products)
    product_dropdown.pack(pady=20)

    def show_sales_data():  # satış verilerini gösterme
        selected = selected_product.get()
        sales_data = aggregate_sales_data()

        # Seçilen ürünün satış verilerini filtreleme
        product_sales = [item for item in sales_data if item['item'] == products.index(selected) + 1]

        # Yılları artan sırada sıralama
        product_sales = sorted(product_sales, key=lambda x: x['date'])

        # Grafiği oluştur
        fig = go.Figure()
        trace = go.Scatter(x=[item['date'] for item in product_sales], y=[item['sales'] for item in product_sales])
        trace.update(mode='lines+markers')
        trace.update(hovertemplate='Yıl: %{x}<br>Satış: %{y}K')
        fig.add_trace(trace)
        fig.update_layout(
            title=f"{selected} Satış Verileri",
            xaxis_title="Yıl",
            yaxis_title="Satış",
            width=800,
            height=600
        )
        fig.show()

    show_data_button = ttk.Button(window, text="      Veri Yükle ve \nSatış Verilerini Göster", command=show_sales_data)
    show_data_button.pack(pady=10)

    def load_data():
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV Dosyaları", "*.csv")])
            if file_path:
                with open(file_path, 'r') as file:
                    data = file.read().strip().split('\n')
                # Verileri DataFrame'e dönüştürme
                df = pd.DataFrame([row.split(',') for row in data], columns=['date', 'item', 'sales'])

                # Verileri dönüştürme
                df['date'] = df['date'].astype(int)
                df['item'] = df['item'].astype(int)
                df['sales'] = df['sales'].astype(int)

                # Verileri döndürme
                return df['date'], df['item'], df['sales']
            else:
                messagebox.showerror("Hata", "Lütfen bir dosya seçin.")
                return None, None, None
        except Exception as e:
            messagebox.showerror("Hata", f"Veri yüklenirken bir hata oluştu: {str(e)}")
            return None, None, None

    def aggregate_sales_data():
        date_data, item_data, sales_data = load_data()

        result = {}
        for i in range(len(date_data)):
            year = date_data[i]
            product = item_data[i]
            sales = sales_data[i]

            if year not in result:
                result[year] = {}

            if product not in result[year]:
                result[year][product] = {'date': year, 'item': product, 'sales': 0}

            result[year][product]['sales'] += sales

        output = []
        for year, products in result.items():
            output.extend(list(products.values()))

        return output

    def predict():
        selected = selected_product.get()
        sales_data = aggregate_sales_data()

        # Seçilen ürünün satış verilerini filtreleme
        product_sales = [item for item in sales_data if item['item'] == products.index(selected) + 1]

        # Verileri DataFrame'e dönüştürme
        df = pd.DataFrame(product_sales)
        df['date'] = pd.to_datetime(df['date'], format='%Y')
        df = df.rename(columns={'date': 'ds', 'sales': 'y'})

        # Prophet modelini oluşturma ve eğitme
        model = Prophet()
        model.fit(df)

        # Önümüzdeki 3 ay için tahmin
        future = model.make_future_dataframe(periods=3, freq='M')
        forecast = model.predict(future)

        # Tahminleri bin cinsine dönüştürme
        forecast['yhat'] = forecast['yhat'] / 1000

        # Grafiği görüntüleme
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast['ds'][-3:], y=forecast['yhat'][-3:],
                                 mode='lines+markers',
                                 name='Tahmini Satış'))
        fig.update_layout(
            title=f"{selected} İçin Satış Tahmini",
            xaxis_title="Tarih",
            yaxis_title="Tahmini Satış",
            xaxis_ticktext=['Ocak', 'Şubat', 'Mart'],
            xaxis_tickvals=forecast['ds'][-3:]
        )
        fig.show()

    tahmin_buton = ttk.Button(window, text="      Veri Yükle ve \nSatış Tahminlerini Göster", command=predict)
    tahmin_buton.pack(pady=10)
    window.mainloop()

first()
