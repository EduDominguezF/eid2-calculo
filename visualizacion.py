import io
import re
import sys

import matplotlib
matplotlib.use("qtagg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget, QHeaderView,
)


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
    if not re.fullmatch(r"\d{8}(?:-?[\dkK])?", limpio.replace(".", "").replace(" ", "")):
        return "Ingrese exactamente 8 dígitos, opcionalmente seguidos por guion y dígito verificador (ej: 24.365.895-K)."
    return None


class Aplicacion(QMainWindow):
    def __init__(self, funcion_ejecutar=None):
        super().__init__()
        if funcion_ejecutar is None:
            from main import ejecutar as funcion_ejecutar
        self.ejecutar = funcion_ejecutar
        self.lienzos = []
        self.setWindowTitle("EID N°2 · Protocolo ARQ")
        self.resize(1180, 820)
        self.setMinimumSize(900, 620)
        self.setStyleSheet("""
            QWidget { background: #101827; color: #e5edf8; font-family: 'Segoe UI'; font-size: 10pt; }
            QLabel { background: transparent; }
            QFrame#header { background: #14243d; border: 1px solid #263a58; border-radius: 16px; }
            QLabel#eyebrow { color: #83b5ff; font-size: 9pt; font-weight: 700; letter-spacing: 1px; }
            QLabel#title { color: white; font-size: 22pt; font-weight: 700; }
            QLabel#subtitle { color: #bac9dd; font-size: 10pt; }
            QFrame#panel { background: #1b2739; border: 1px solid #2d3b50; border-radius: 14px; }
            QLineEdit { background: #111c2e; color: #e5edf8; border: 1px solid #3a4b63; border-radius: 8px; padding: 10px 12px; min-width: 210px; }
            QLineEdit:focus { border: 2px solid #3978d4; }
            QPushButton { border: 0; border-radius: 8px; padding: 10px 18px; font-weight: 600; }
            QPushButton#primary { background: #3478d4; color: white; }
            QPushButton#primary:hover { background: #1f56a8; }
            QPushButton#secondary { background: #2b3a50; color: #e5edf8; }
            QPushButton#secondary:hover { background: #394b64; }
            QTabWidget::pane { background: #1b2739; border: 1px solid #2d3b50; border-radius: 10px; top: -1px; }
            QTabBar::tab { background: #26344a; color: #b9c8dc; padding: 11px 20px; margin-right: 4px; border-top-left-radius: 8px; border-top-right-radius: 8px; }
            QTabBar::tab:hover { background: #30435f; color: white; }
            QTabBar::tab:selected { background: #2868c7; color: white; }
            QTextEdit { background: #151f30; color: #e5edf8; border: 0; padding: 14px; selection-background-color: #3478d4; }
            QScrollBar:vertical { background: #151f30; width: 12px; margin: 2px; }
            QScrollBar::handle:vertical { background: #40536d; min-height: 28px; border-radius: 5px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)
        self._crear_interfaz()

    def _crear_interfaz(self):
        central = QWidget()
        self.setCentralWidget(central)
        raiz = QVBoxLayout(central)
        raiz.setContentsMargins(24, 22, 24, 18)
        raiz.setSpacing(16)

        encabezado = QFrame(objectName="header")
        disposicion_encabezado = QVBoxLayout(encabezado)
        disposicion_encabezado.setContentsMargins(26, 20, 26, 22)
        disposicion_encabezado.setSpacing(5)
        antetitulo = QLabel("EID N°2  /  CÁLCULO", objectName="eyebrow")
        disposicion_encabezado.addWidget(antetitulo)
        titulo = QLabel("Análisis de series · Protocolo ARQ", objectName="title")
        titulo.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        subtitulo = QLabel("Límites, sucesiones y evaluación de viabilidad", objectName="subtitle")
        disposicion_encabezado.addWidget(titulo)
        disposicion_encabezado.addWidget(subtitulo)
        raiz.addWidget(encabezado)

        panel = QFrame(objectName="panel")
        fila = QHBoxLayout(panel)
        fila.setContentsMargins(18, 14, 18, 14)
        etiqueta = QLabel("RUT del integrante")
        etiqueta.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        fila.addWidget(etiqueta)
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ejemplo: 24.365.895-K")
        self.entrada.returnPressed.connect(self.calcular)
        fila.addWidget(self.entrada)
        calcular = QPushButton("Calcular", objectName="primary")
        calcular.clicked.connect(self.calcular)
        fila.addWidget(calcular)
        limpiar = QPushButton("Limpiar", objectName="secondary")
        limpiar.clicked.connect(self.limpiar)
        fila.addWidget(limpiar)
        self.mensaje = QLabel("Ingresa tu RUT para generar el análisis.")
        self.mensaje.setStyleSheet("color:#aab8cc; padding-left:8px")
        fila.addWidget(self.mensaje, 1)
        raiz.addWidget(panel)

        self.pestanas = QTabWidget()
        self.resumen = QWidget()
        self.resumen_disposicion = QVBoxLayout(self.resumen)
        self.resumen_disposicion.setContentsMargins(18, 18, 18, 18)
        self.resumen_disposicion.setSpacing(14)
        self.resumen_aviso = QLabel("Calcula con un RUT para ver el resumen.")
        self.resumen_disposicion.addWidget(self.resumen_aviso)
        self.pestanas.addTab(self.resumen, "Resumen")

        self.tabla = self._nueva_tabla()
        self.pestanas.addTab(self.tabla, "Sumas parciales")
        self.tabla_conv = self._nueva_tabla()
        self.pestanas.addTab(self.tabla_conv, "Convergencia y viabilidad")

        self.texto = QTextEdit()
        self.texto.setReadOnly(True)
        self.texto.setFont(QFont("Consolas", 10))
        self.texto.setPlaceholderText("Los resultados, tablas y conclusiones aparecerán aquí.")
        self.pestanas.addTab(self.texto, "Desarrollo completo")
        self.marcos_graficos = []
        for caso in "ABC":
            marco = QWidget()
            disposicion = QVBoxLayout(marco)
            aviso = QLabel("Calcula con un RUT para visualizar este gráfico.")
            aviso.setAlignment(Qt.AlignmentFlag.AlignCenter)
            aviso.setStyleSheet("color:#aab8cc")
            disposicion.addWidget(aviso)
            self.marcos_graficos.append(marco)
            self.pestanas.addTab(marco, f"Caso {caso}")
        raiz.addWidget(self.pestanas, 1)
        pie = QLabel("EID N°2  ·  Cálculo aplicado a la confiabilidad de redes")
        pie.setStyleSheet("color:#8293aa; padding-left:4px")
        raiz.addWidget(pie)
        self.entrada.setFocus()

    def _nueva_tabla(self):
        tabla = QTableWidget()
        tabla.setAlternatingRowColors(True)
        tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tabla.setStyleSheet("QTableWidget { background:#151f30; alternate-background-color:#1b293d; gridline-color:#34445b; border:0; } QHeaderView::section { background:#263a55; color:#e5edf8; padding:7px; border:0; font-weight:600; }")
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return tabla

    @staticmethod
    def _celda(tabla, fila, columna, valor):
        elemento = QTableWidgetItem(str(valor))
        elemento.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        tabla.setItem(fila, columna, elemento)

    def _mostrar_datos(self, datos):
        probs, conv, viable = datos["probs"], datos["convergencia"], datos["viabilidad"]
        while self.resumen_disposicion.count() > 1:
            elemento = self.resumen_disposicion.takeAt(1)
            if elemento.widget(): elemento.widget().deleteLater()
        aviso_resumen = self.resumen_aviso
        aviso_resumen.setText(f"RUT {datos['rut']}  ·  Umbral de costo Cₘáx = {datos['c_max']:g}")
        tarjetas = QHBoxLayout()
        for nombre, p in probs.items():
            tarjeta = QFrame(objectName="panel")
            disposicion_tarjeta = QVBoxLayout(tarjeta)
            disposicion_tarjeta.addWidget(QLabel(nombre.upper()))
            valor = QLabel(f"{p:.2f}")
            valor.setStyleSheet("font-size:22pt; font-weight:700; color:#83b5ff")
            disposicion_tarjeta.addWidget(valor)
            tarjetas.addWidget(tarjeta)
        self.resumen_disposicion.addLayout(tarjetas)
        caso, nombre = datos["recomendacion"] if datos["recomendacion"] else (None, None)
        if caso:
            d = conv[caso][nombre]
            recomendacion = QLabel(f"RECOMENDACIÓN   Caso {caso} · {nombre} = {d['p']:.2f}     |     Costo esperado {d['limite']:.4f}     |     Margen {datos['c_max']-d['limite']:.4f}")
            recomendacion.setWordWrap(True)
            recomendacion.setStyleSheet("background:#183a39; color:#8ce3bd; border:1px solid #28665a; border-radius:10px; padding:16px; font-size:12pt; font-weight:700")
            self.resumen_disposicion.addWidget(recomendacion)
        else:
            self.resumen_disposicion.addWidget(QLabel("Ninguna combinación cumple el umbral de costo."))
        self.resumen_disposicion.addWidget(QLabel("El método del cociente confirma convergencia para 0 < p < 1. El error reportado compara la suma truncada con el límite teórico."))

        nombres = list(probs)
        casos = list(datos["resultados"])
        n_filas = len(next(iter(datos["resultados"][casos[0]].values())))
        self.tabla.setRowCount(n_filas * len(casos)); self.tabla.setColumnCount(1 + len(nombres))
        self.tabla.setHorizontalHeaderLabels(["Caso / k"] + [f"{n} (p={probs[n]:.2f})" for n in nombres])
        fila_actual = 0
        for c in casos:
            for k in range(n_filas):
                self._celda(self.tabla,fila_actual,0,f"{c} / S{k+1}")
                for j,n in enumerate(nombres,1): self._celda(self.tabla,fila_actual,j,f"{datos['resultados'][c][n][k]:.6f}")
                fila_actual += 1
        filas_conv = [(c,n,d) for c,por_p in conv.items() for n,d in por_p.items()]
        encabezados = ["Caso", "Probabilidad", "Límite teórico", "Límite empírico", "Error absoluto", "k estable", "Viabilidad"]
        self.tabla_conv.setColumnCount(len(encabezados)); self.tabla_conv.setRowCount(len(filas_conv)); self.tabla_conv.setHorizontalHeaderLabels(encabezados)
        for i,(c,n,d) in enumerate(filas_conv):
            valores = [c, f"{d['p']:.2f}", f"{d['teorico']:.8f}", f"{d['limite']:.8f}", f"{d['error']:.2e}", d['k_estable'], "CUMPLE" if viable[c][n] else "NO CUMPLE"]
            for j,v in enumerate(valores): self._celda(self.tabla_conv,i,j,v)

    def mostrar_mensaje(self, texto, color="#64748b"):
        self.mensaje.setText(texto)
        self.mensaje.setStyleSheet(f"color:{color}; padding-left:8px; background:transparent")

    def _limpiar_graficos(self, aviso):
        for lienzo in self.lienzos:
            plt.close(lienzo.figure)
        self.lienzos.clear()
        for marco in self.marcos_graficos:
            while marco.layout().count():
                elemento = marco.layout().takeAt(0)
                componente = elemento.widget()
                if componente:
                    componente.deleteLater()
            etiqueta = QLabel(aviso)
            etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)
            etiqueta.setStyleSheet("color:#aab8cc")
            marco.layout().addWidget(etiqueta)

    def mostrar_graficos(self, figuras):
        self._limpiar_graficos("Gráfico no disponible.")
        for marco, figura in zip(self.marcos_graficos, figuras):
            while marco.layout().count():
                elemento = marco.layout().takeAt(0)
                if elemento.widget():
                    elemento.widget().deleteLater()
            lienzo = FigureCanvasQTAgg(figura)
            barra = NavigationToolbar2QT(lienzo, marco)
            barra.setStyleSheet("QToolBar { background:#1b2739; border:0; spacing:5px; } QToolButton { color:#dce7f5; background:transparent; padding:4px; } QToolButton:hover { background:#30435f; border-radius:4px; }")
            marco.layout().addWidget(barra)
            marco.layout().addWidget(lienzo)
            lienzo.draw()
            self.lienzos.append(lienzo)

    def calcular(self):
        texto = self.entrada.text()
        error = validar_formato(texto)
        if error:
            self.mostrar_mensaje(error, "#c0392b")
            QMessageBox.warning(self, "RUT inválido", error)
            return
        duplicador = Duplicador(sys.stdout)
        salida_original = sys.stdout
        sys.stdout = duplicador
        try:
            datos = self.ejecutar(texto)
        except ValueError as e:
            self.mostrar_mensaje(str(e), "#c0392b")
            QMessageBox.warning(self, "RUT inválido", str(e))
            self._limpiar_graficos("Ingresa un RUT válido.")
            return
        except Exception as e:
            self.mostrar_mensaje("Ocurrió un error al calcular.", "#c0392b")
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado:\n{e}")
            self._limpiar_graficos("Gráficos no disponibles.")
            return
        finally:
            sys.stdout = salida_original
        self.texto.setPlainText(duplicador.buffer_texto.getvalue())
        if isinstance(datos, dict):
            self._mostrar_datos(datos)
            self.mostrar_graficos(datos["figuras"])
        else:
            self.mostrar_graficos(datos)
        self.mostrar_mensaje("Análisis calculado correctamente.", "#16804a")
        self.pestanas.setCurrentIndex(0)

    def limpiar(self):
        self.entrada.clear()
        self.texto.clear()
        self._limpiar_graficos("Calcula con un RUT para visualizar este gráfico.")
        self.mostrar_mensaje("Ingresa tu RUT para generar el análisis.")
        self.entrada.setFocus()

    def closeEvent(self, evento):
        plt.close("all")
        evento.accept()


if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = Aplicacion()
    ventana.show()
    sys.exit(aplicacion.exec())
