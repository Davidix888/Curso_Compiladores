from node import *
from lexico import *
import json

# Analizador sintactico 
class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.pos = 0

  def obtener_token(self):
    return self.tokens[self.pos] if self.pos < len(self.tokens) else None

  def coincidir(self, tipo_esperado):
    token_actual = self.obtener_token()
    if token_actual and token_actual[0] == tipo_esperado:
      self.pos += 1
      return token_actual
    else:
      raise SyntaxError(f"Error sintáctico: Se esperaba {tipo_esperado} pero se encontró: {token_actual}")

  def parsear(self):
    #Punto de entrada: se espera una función
    return self.funcion()

  def funcion(self):
    #Gramatica para una función: int IDENTIFIER (ind IDENTIFIER) {Cuerpo}
    tipo_retorno = self.coincidir('KEYWORD') # Retorna int
    nombre_funcion = self.coincidir('IDENTIFIER')
    self.coincidir('DELIMITER')
    parametros = self.parametros()
    self.coincidir('DELIMITER')
    self.coincidir('DELIMITER')
    cuerpo = self.cuerpo()
    self.coincidir('DELIMITER')
    return NodoFuncion(tipo_retorno, nombre_funcion, parametros, cuerpo)

  def parametros(self):
    lista_parametros = []

    tipo = self.coincidir("KEYWORD")
    nombre = self.coincidir('IDENTIFIER')

    lista_parametros.append(NodoParametro(tipo, nombre))

    while self.obtener_token() and self.obtener_token()[1] == ',':
        self.coincidir("DELIMITER")
        tipo = self.coincidir("KEYWORD")
        nombre = self.coincidir('IDENTIFIER')
        lista_parametros.append(NodoParametro(tipo, nombre))

    return lista_parametros

  def cuerpo(self):

    instrucciones = []

    while self.obtener_token() and self.obtener_token()[1] != '}':

        token = self.obtener_token()

        if token[1] == 'return':
            instrucciones.append(self.retorno())

        elif token[1] == 'print':
            instrucciones.append(self.sentencia_print())

        elif token[1] == 'println':
            instrucciones.append(self.sentencia_print())

        elif token[1] == 'if':
            instrucciones.append(self.sentencia_if())

        elif token[1] == 'while':
            instrucciones.append(self.sentencia_while())

        elif token[1] == 'for':
            instrucciones.append(self.sentencia_for())

        else:
            instrucciones.append(self.asignacion())

    return instrucciones
  def asignacion(self):
    #Gramática pra la estructura de asignación
    tipo = self.coincidir('KEYWORD') #Se espera un tipo
    nombre = self.coincidir('IDENTIFIER')
    operador = self.coincidir('OPERATOR') #Se espera un operador =
    expresion = self.expresion()
    self.coincidir('DELIMITER')
    return NodoAsignacion(tipo, nombre, expresion)

  def retorno(self):
    self.coincidir('KEYWORD')
    expresion = self.expresion()
    self.coincidir('DELIMITER')
    return NodoRetorno(expresion)

  def expresion(self):
    izquierda = self.termino()
    while self.obtener_token() and self.obtener_token()[0] == "OPERATOR":
      operador = self.coincidir("OPERATOR")
      derecha = self.termino()
      izquierda = NodoOperacion(izquierda, operador, derecha)
    return izquierda

  def termino(self):
    token = self.obtener_token()
    if token and token[0] == "NUMBER":
      return NodoNumero(self.coincidir("NUMBER"))
    elif token and token[0] == "IDENTIFIER":
      identificador = self.coincidir("IDENTIFIER")
      if self.obtener_token() and self.obtener_token()[1] == "(":
        self.coincidir("DELIMITER")
        argumentos = self.llamadaFuncion()
        self.coincidir("DELIMITER")
        return NodoLlamadaFuncion(identificador[1], argumentos)
      else:
        return NodoIdent(identificador)
    else:
      raise SyntaxError(f"Expresión no válida: {token}")

  def llamadaFuncion(self):
    argumentos = []
    # Reglas para argumentos: (,IDENTIFIER | NUMBER)*
    sigue = True
    token = self.obtener_token()
    while sigue:
      sigue = False
      if token[0] == "NUMBER":
        argumento = NodoNumero(self.coincidir("NUMBER"))
      elif token[0] == "IDENTIFIER":
        argumento = NodoIdent(self.coincidir("IDENTIFIER"))
      else:
        raise SyntaxError(f"Error de sintaxis, se esperaba un IDENTIFICADOR|NUMERO pero se encontró: {token}")
      argumentos.append(argumento)
      if self.obtener_token() and self.obtener_token()[1] == ",":
        self.coincidir("DELIMITER") # Se espera una coma
        token = self.obtener_token()
        sigue = True
    return argumentos
 
  def sentencia_print(self):
    self.coincidir('IDENTIFIER') # Se espera print
    self.coincidir('DELIMITER') # Se espera (
    expresion = self.expresion()
    self.coincidir('DELIMITER') # Se espera )
    self.coincidir('DELIMITER') # Se espera ;
    return NodoPrint(expresion)

def imprimir_ast(nodo):
    if isinstance(nodo, NodoFuncion):
      return { "Funcion" : nodo.nombre,
               "Parametros" : [imprimir_ast(p) for p in nodo.parametros],
               "Cuerpo" : [imprimir_ast(c) for c in nodo.cuerpo]}
    elif(isinstance(nodo, NodoParametro)):
      return {"Parametro" : nodo.nombre, "Tipo" : nodo.tipo}
    elif(isinstance(nodo, NodoAsignacion)):
      return {"Asignación" : nodo.nombre, "Expresion" : imprimir_ast(nodo.expresion)}
    elif isinstance(nodo, NodoOperacion):
      return {"Operacion" : nodo.operador,
              "Izquierda" : imprimir_ast(nodo.izquierda),
              "Derecha" : imprimir_ast(nodo.derecha)}
    elif isinstance(nodo, NodoRetorno):
      return {"Retorno" : imprimir_ast(nodo.expresion)}
    elif isinstance(nodo, NodoIdent):
      return {"Identificador" : nodo.nombre}
    elif isinstance(nodo, NodoNumero):
      return {"Numero" : nodo.valor}
    elif isinstance(nodo, NodoPrint):
      return {"Print" : imprimir_ast(nodo.expresion)}
    return {}






