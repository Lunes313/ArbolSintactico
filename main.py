from nltk import CFG, ChartParser

# Definir la gramática
gramatica = CFG.fromstring("""
    E -> E '+' T | E '-' T | T
    T -> T '*' F | T '/' F | F
    F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
""")

# Define la expresión que deseas analizar
expresion_objetivo = "4 + ( a - b ) * x".split()

# Crear un parser usando la gramática
parser = ChartParser(gramatica)

# Generar el árbol de derivación y mostrarlo en una ventana
for tree in parser.parse(expresion_objetivo):
    print("Árbol de derivación:")
    tree.pretty_print()# Muestra el árbol en la consola
    tree.draw()  # Abre una ventana con el árbol sintáctico