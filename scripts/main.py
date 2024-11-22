from interface import interfaz
from nltk import CFG, ChartParser
from PyQt5 import QtWidgets
import nltk
import sys

# Función genérica para realizar una derivación (por izquierda o por derecha)
def GenerarDerivacion(ArbolSintactico, Tipo="izquierda"):
    pasos = []  # Almacena los pasos de la derivación
    derivacionActual = [ArbolSintactico.label()]  # Comienza con el símbolo inicial

    # Función recursiva para procesar cada nodo del árbol
    def ProcesarNodo(Nodo):
        nonlocal derivacionActual  # Modifica directamente la derivación actual
        if isinstance(Nodo, str):  # Si es un terminal, no se expande
            return

        # Obtener etiqueta del nodo (no terminal) y sus hijos (producciones)
        NoTerminal = Nodo.label()
        HijosDelNodo = [hijo.label() if type(hijo) is nltk.Tree else hijo for hijo in Nodo]

        # Reemplazar el no terminal en la derivación actual por sus hijos
        if Tipo == "izquierda":
            posicion = derivacionActual.index(NoTerminal)  # Primera aparición del no terminal
        else:  # Por derecha
            posicion = len(derivacionActual) - 1 - derivacionActual[::-1].index(NoTerminal)

        derivacionActual = (
            derivacionActual[:posicion] + HijosDelNodo + derivacionActual[posicion + 1:]
        )
        pasos.append(" ".join(derivacionActual))  # Guardar el estado actual de la derivación

        # Expandir hijos (en orden específico según el tipo de derivación)
        Hijos = Nodo if Tipo == "izquierda" else reversed(Nodo)
        for hijo in Hijos:
            ProcesarNodo(hijo)

    # Iniciar la derivación desde la raíz
    pasos.append(" ".join(derivacionActual))  # Estado inicial
    ProcesarNodo(ArbolSintactico)
    return pasos


# Leer la gramática desde un archivo
try:
    with open("../grammar/reglas.txt", "r") as archivo:
        reglas_gramatica = archivo.read()

    # Cargar la gramática usando NLTK
    gramatica = CFG.fromstring(reglas_gramatica)

    # Expresión a analizar
    expresion_entrada = "( 4 - a )".split()

    # Crear el parser y generar árboles de análisis sintáctico
    parser = ChartParser(gramatica)
    arboles = list(parser.parse(expresion_entrada))

    if arboles:
        for arbol in arboles:
            print("\nÁrbol generado:")
            print(arbol)

            # Derivación por izquierda
            print("\nDerivación por izquierda:")
            pasos_izquierda = GenerarDerivacion(arbol, Tipo="izquierda")
            for paso in pasos_izquierda:
                print(paso)

            # Derivación por derecha
            print("\nDerivación por derecha:")
            pasos_derecha = GenerarDerivacion(arbol, Tipo="derecha")
            for paso in pasos_derecha:
                print(paso)
    else:
        print("No se encontró una derivación válida para la expresión.")
except FileNotFoundError:
    print("Error: El archivo 'reglas.txt' no fue encontrado.")
except Exception as e:
    print(f"Error: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = interfaz()
    window.show()
    sys.exit(app.exec_())