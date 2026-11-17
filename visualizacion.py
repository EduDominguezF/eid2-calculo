import io
import sys
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from main import ejecutar


class Duplicador(io.TextIOBase):
    def __init__(self, consola):
        self.consola = consola
        self.buffer_texto = io.StringIO()

    def write(self, texto):
        self.consola.write(texto)
        self.buffer_texto.write(texto)
        return len(texto)

    def flush(self):
        self.consola.flush()


def validar_formato(texto):
    limpio = texto.strip()
    if not limpio:
        return "Debe ingresar un RUT."
    permitidos = set("0123456789.-kK ")
    if any(c not in permitidos for c in limpio):
        return "El RUT solo puede contener números, puntos, guion y K."
    if limpio.count("-") > 1:
        return "El RUT solo puede tener un guion."
    return None


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EID N°2 - Protocolo ARQ: Límites, Sucesiones y Series")
        self.geometry("1100x750")
        self.minsize(900, 600)
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.canvases = []
        self.crear_entrada()
        self.crear_pestanas()

    def crear_entrada(self):
        marco = ttk.Frame(self, padding=10)
        marco.pack(fill="x")

        ttk.Label(marco, text="RUT del integrante:", font=("Segoe UI", 11)).pack(side="left")
        self.rut_var = tk.StringVar()
        self.entrada = ttk.Entry(marco, textvariable=self.rut_var, width=20, font=("Segoe UI", 11))
        self.entrada.pack(side="left", padx=8)
        self.entrada.bind("<Return>", lambda e: self.calcular())
        self.entrada.focus()

        ttk.Button(marco, text="Calcular", command=self.calcular).pack(side="left")
        ttk.Button(marco, text="Limpiar", command=self.limpiar).pack(side="left", padx=6)

        self.mensaje = ttk.Label(marco, text="Ejemplo: 24.365.895-K", foreground="gray")
        self.mensaje.pack(side="left", padx=12)

    def crear_pestanas(self):
        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        marco_texto = ttk.Frame(self.pestanas)
        self.texto = tk.Text(marco_texto, font=("Consolas", 10), wrap="none", state="disabled")
        barra_y = ttk.Scrollbar(marco_texto, orient="vertical", command=self.texto.yview)
        barra_x = ttk.Scrollbar(marco_texto, orient="horizontal", command=self.texto.xview)
        self.texto.configure(yscrollcommand=barra_y.set, xscrollcommand=barra_x.set)
        barra_y.pack(side="right", fill="y")
        barra_x.pack(side="bottom", fill="x")
        self.texto.pack(fill="both", expand=True)
        self.pestanas.add(marco_texto, text="Resultados")

        self.marcos_graficos = []
        for caso in ["A", "B", "C"]:
            marco = ttk.Frame(self.pestanas)
            ttk.Label(marco, text="Ingrese un RUT y presione Calcular.", foreground="gray").pack(expand=True)
            self.pestanas.add(marco, text=f"Gráfico caso {caso}")
            self.marcos_graficos.append(marco)

    def mostrar_mensaje(self, texto, color):
        self.mensaje.configure(text=texto, foreground=color)

    def escribir_resultados(self, contenido):
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", contenido)
        self.texto.configure(state="disabled")

    def vaciar_graficos(self, aviso):
        for canvas in self.canvases:
            plt.close(canvas.figure)
        self.canvases = []
        for marco in self.marcos_graficos:
            for hijo in marco.winfo_children():
                hijo.destroy()
            ttk.Label(marco, text=aviso, foreground="gray").pack(expand=True)

    def mostrar_graficos(self, figuras):
        if not figuras:
            self.vaciar_graficos("Gráficos no disponibles todavía.")
            return
        for marco in self.marcos_graficos:
            for hijo in marco.winfo_children():
                hijo.destroy()
        for marco, figura in zip(self.marcos_graficos, figuras):
            canvas = FigureCanvasTkAgg(figura, master=marco)
            NavigationToolbar2Tk(canvas, marco).update()
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            self.canvases.append(canvas)

    def calcular(self):
        texto = self.rut_var.get()
        error = validar_formato(texto)
        if error:
            self.mostrar_mensaje(error, "red")
            messagebox.showerror("RUT inválido", error)
            return

        self.vaciar_graficos("Calculando...")
        duplicador = Duplicador(sys.stdout)
        salida_original = sys.stdout
        sys.stdout = duplicador
        try:
            figuras = ejecutar(texto)
        except ValueError as e:
            sys.stdout = salida_original
            self.mostrar_mensaje(str(e), "red")
            messagebox.showerror("RUT inválido", str(e))
            self.vaciar_graficos("Ingrese un RUT válido.")
            return
        except Exception as e:
            sys.stdout = salida_original
            self.mostrar_mensaje("Ocurrió un error al calcular.", "red")
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")
            return
        finally:
            sys.stdout = salida_original

        self.escribir_resultados(duplicador.buffer_texto.getvalue())
        self.mostrar_graficos(figuras)
        self.mostrar_mensaje("Cálculo realizado correctamente.", "green")
        self.pestanas.select(0)

    def limpiar(self):
        self.rut_var.set("")
        self.escribir_resultados("")
        self.vaciar_graficos("Ingrese un RUT y presione Calcular.")
        self.mostrar_mensaje("Ejemplo: 24.365.895-K", "gray")
        self.entrada.focus()

    def cerrar(self):
        plt.close("all")
        self.destroy()


if __name__ == "__main__":
    Aplicacion().mainloop()
