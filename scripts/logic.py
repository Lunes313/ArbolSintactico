from nltk import CFG, ChartParser
import nltk

# Función genérica para realizar una derivación (por izquierda o por derecha)
def GenerarDerivacion(ArbolSintactico, Tipo):
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

def derivacion(expresion, reglas, tipo):
    # Cargar la gramática usando NLTK
    try:
        gramatica = CFG.fromstring(reglas)

        # Expresión a analizar
        entrada = expresion.split()

        # Crear el parser y generar árboles de análisis sintáctico
        parser = ChartParser(gramatica)
        arboles = list(parser.parse(entrada))
        if arboles:
            for arbol in arboles:
                # Generar la derivación según el tipo especificado
                pasos = GenerarDerivacion(arbol, Tipo=tipo)
                return pasos, arbol
        else:
            return False, False
    except ValueError:
        return False, False