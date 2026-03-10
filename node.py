class NodoAST:
    pass


class NodoFuncion(NodoAST):

    def __init__(self, tipo, nombre, parametros, cuerpo):
        self.tipo = tipo
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo

    def traducirPy(self):
        params = ", ".join(p.traducirPy() for p in self.parametros)
        cuerpo = "\n  ".join(c.traducirPy() for c in self.cuerpo)

        return f"def {self.nombre[1]}({params}):\n  {cuerpo}"


class NodoParametro(NodoAST):

    def __init__(self, tipo, nombre):
        self.tipo = tipo
        self.nombre = nombre

    def traducirPy(self):
        return self.nombre[1]


class NodoAsignacion(NodoAST):

    def __init__(self, tipo, nombre, expresion):
        self.tipo = tipo
        self.nombre = nombre
        self.expresion = expresion

    def traducirPy(self):
        return f"{self.nombre[1]} = {self.expresion.traducirPy()}"


class NodoOperacion(NodoAST):

    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

    def traducirPy(self):
        return f"{self.izquierda.traducirPy()} {self.operador[1]} {self.derecha.traducirPy()}"


class NodoRetorno(NodoAST):

    def __init__(self, expresion):
        self.expresion = expresion

    def traducirPy(self):
        return f"return {self.expresion.traducirPy()}"


class NodoIdent(NodoAST):

    def __init__(self, nombre):
        self.nombre = nombre

    def traducirPy(self):
        return self.nombre[1]


class NodoNumero(NodoAST):

    def __init__(self, valor):
        self.valor = valor

    def traducirPy(self):
        return self.valor[1]


class NodoLlamadaFuncion(NodoAST):

    def __init__(self, nombre_funcion, argumentos):
        self.nombre_funcion = nombre_funcion
        self.argumentos = argumentos

    def traducirPy(self):
        args = ", ".join(a.traducirPy() for a in self.argumentos)
        return f"{self.nombre_funcion}({args})"


class NodoPrint(NodoAST):

    def __init__(self, expresion):
        self.expresion = expresion

    def traducirPy(self):
        return f"print({self.expresion.traducirPy()})"


class NodoPrintln(NodoAST):

    def __init__(self, expresion):
        self.expresion = expresion

    def traducirPy(self):
        return f"print({self.expresion.traducirPy()})"


class NodoIf(NodoAST):

    def __init__(self, condicion, cuerpo_if, cuerpo_else=None):
        self.condicion = condicion
        self.cuerpo_if = cuerpo_if
        self.cuerpo_else = cuerpo_else

    def traducirPy(self):

        cuerpo_if = "\n  ".join(c.traducirPy() for c in self.cuerpo_if)

        codigo = f"if {self.condicion.traducirPy()}:\n  {cuerpo_if}"

        if self.cuerpo_else:
            cuerpo_else = "\n  ".join(c.traducirPy() for c in self.cuerpo_else)
            codigo += f"\nelse:\n  {cuerpo_else}"

        return codigo


class NodoWhile(NodoAST):

    def __init__(self, condicion, cuerpo):
        self.condicion = condicion
        self.cuerpo = cuerpo

    def traducirPy(self):

        cuerpo = "\n  ".join(c.traducirPy() for c in self.cuerpo)

        return f"while {self.condicion.traducirPy()}:\n  {cuerpo}"


class NodoFor(NodoAST):

    def __init__(self, inicial, condicion, incremento, cuerpo):
        self.inicial = inicial
        self.condicion = condicion
        self.incremento = incremento
        self.cuerpo = cuerpo

    def traducirPy(self):

        cuerpo = "\n  ".join(c.traducirPy() for c in self.cuerpo)

        return f"{self.inicial.traducirPy()}\nwhile {self.condicion.traducirPy()}:\n  {cuerpo}\n  {self.incremento.traducirPy()}"
