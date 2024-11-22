from PyQt5 import QtWidgets, uic, QtGui, QtCore
from nltk import Tree
import logic

class interfaz(QtWidgets.QMainWindow):
    def __init__(self):
        super(interfaz, self).__init__()
        uic.loadUi("../design/interface.ui", self)
        self.setWindowTitle("   Gramatica y Arboles Sintacticos  ")

        self.btnSalir.clicked.connect(self.close)
        self.btnDerivacion.clicked.connect(self.generarDerivacion)

        self.sceneArbolSintactico = QtWidgets.QGraphicsScene(self)
        self.sceneArbolAbstracto = QtWidgets.QGraphicsScene(self)
        self.arbolSintactico.setScene(self.sceneArbolSintactico)
        self.arbolAbstracto.setScene(self.sceneArbolAbstracto)

    def generar_ast(self, tree):

        if not isinstance(tree, Tree):
            return tree

        if len(tree) == 1 and not isinstance(tree[0], Tree):
            return tree[0]

        # Procesar los hijos
        hijos_procesados = []
        operador = None

        for hijo in tree:
            if isinstance(hijo, Tree):
                resultado = self.generar_ast(hijo)
                if resultado is not None:
                    if isinstance(resultado, str) and resultado in {'+', '-', '*', '/', '^'}:
                        operador = resultado
                    else:
                        hijos_procesados.append(resultado)
            else:
                if hijo in {'+', '-', '*', '/', '^'}:
                    operador = hijo
                else:
                    hijos_procesados.append(hijo)

        if operador and len(hijos_procesados) > 0:
            return Tree(operador, hijos_procesados)
        elif len(hijos_procesados) == 1:
            return hijos_procesados[0]
        elif len(hijos_procesados) > 1:
            return hijos_procesados[1] # se imprime el segundo hijo para evitar los parentesis

        return None

    def dibujar_arboles(self, tree_str):
        if isinstance(tree_str, str):
            tree = Tree.fromstring(tree_str)
        else:
            tree = tree_str

        self.sceneArbolSintactico.clear()
        self.sceneArbolAbstracto.clear()

        ast = self.generar_ast(tree)
        if not isinstance(ast, Tree) and ast is not None:
            ast = Tree('expr', [ast])

        espaciadoVertical = 60
        espaciadoHorizontal = 50
        radio = 20

        def calcular_ancho(subtree):
            if not isinstance(subtree, Tree):
                return 1
            if not subtree:
                return 1
            return max(sum(calcular_ancho(child) for child in subtree), 1)

        def calcular_posiciones(subtree, nivel=0, offset=0, camino=[]):
            ancho = calcular_ancho(subtree)
            x = offset * espaciadoHorizontal + (ancho * espaciadoHorizontal) / 2
            y = nivel * espaciadoVertical

            posiciones = {tuple(camino): (x, y)}

            if isinstance(subtree, Tree):
                pos_actual = offset
                for idx, hijo in enumerate(subtree):
                    ancho_hijo = calcular_ancho(hijo)
                    pos_hijos = calcular_posiciones(hijo, nivel + 1, pos_actual, camino + [idx])
                    posiciones.update(pos_hijos)
                    pos_actual += ancho_hijo

            return posiciones

        # Calcular posiciones para ambos árboles
        posiciones_sintactico = calcular_posiciones(tree)
        if ast is not None:
            posiciones_ast = calcular_posiciones(ast)

        def dibujar_nodo(x, y, texto, scene, esHoja=False):
            color = QtGui.QColor("lightgreen") if esHoja else QtGui.QColor("lightblue")

            ellipse = QtWidgets.QGraphicsEllipseItem(x - radio, y - radio, 2 * radio, 2 * radio)
            ellipse.setBrush(QtGui.QBrush(color))
            ellipse.setPen(QtGui.QPen(QtCore.Qt.black))
            scene.addItem(ellipse)

            text = QtWidgets.QGraphicsTextItem(str(texto))
            text.setDefaultTextColor(QtCore.Qt.black)
            text_width = text.boundingRect().width()
            text_height = text.boundingRect().height()
            text.setPos(x - text_width / 2, y - text_height / 2)
            scene.addItem(text)

        def dibujar_recursivo(subtree, posiciones, scene, camino=[]):
            if subtree is None:
                return

            x, y = posiciones[tuple(camino)]

            if isinstance(subtree, Tree):
                # Los operadores se muestran en azul
                dibujar_nodo(x, y, subtree.label(), scene, False)

                for idx, hijo in enumerate(subtree):
                    hijo_x, hijo_y = posiciones[tuple(camino + [idx])]

                    linea = QtWidgets.QGraphicsLineItem(
                        x, y + radio,
                        hijo_x, hijo_y - radio
                    )
                    linea.setPen(QtGui.QPen(QtCore.Qt.black))
                    scene.addItem(linea)

                    dibujar_recursivo(hijo, posiciones, scene, camino + [idx])
            else:
                # Los operandos se muestran en verde
                dibujar_nodo(x, y, subtree, scene, True)

        # Dibujar árbol sintáctico
        dibujar_recursivo(tree, posiciones_sintactico, self.sceneArbolSintactico)

        # Dibujar AST
        if ast is not None:
            dibujar_recursivo(ast, posiciones_ast, self.sceneArbolAbstracto)

        # Ajustar las vistas
        self.sceneArbolSintactico.setSceneRect(self.sceneArbolSintactico.itemsBoundingRect())
        self.arbolSintactico.fitInView(self.sceneArbolSintactico.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.arbolSintactico.centerOn(0, 0)

        self.sceneArbolAbstracto.setSceneRect(self.sceneArbolAbstracto.itemsBoundingRect())
        self.arbolAbstracto.fitInView(self.sceneArbolAbstracto.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.arbolAbstracto.centerOn(0, 0)

    def generarDerivacion(self):
        gramatica = self.textGramatica.toPlainText()
        expresion = self.textExpresion.toPlainText()
        expresion = " ".join(expresion)
        tipo = "izquierda" if self.radioButtonIzquierda.isChecked() else "derecha"
        pasos, arbol = logic.derivacion(expresion, gramatica, tipo)
        if pasos:
            texto = pasos[0] + " -> " + "\n   -> ".join(pasos[1:])
            self.textDerivacion.setPlainText(texto)

            self.dibujar_arboles(arbol)
        else:
            self.textDerivacion.setPlainText("No se pudo realizar la derivación")