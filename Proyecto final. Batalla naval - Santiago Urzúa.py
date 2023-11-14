# Introducción a la programación, sección:17
# 14/11/2023
# José Santiago Urzúa Luarca
# Objetivo: crear un juego de Batalla Naval en Python para dos jugadores, donde puedan colocar estratégicamente 
# sus barcos en un tablero y, por turnos, intentar adivinar la ubicación de los barcos del oponente.

# Librería para limpiar consola
import os

# Funcion para limpiar consola
def LimpiarConsola ():
    os.system('cls')

# Funcion para comprobar que el input del usuario es correcto
def ComprobaryTransformarInput(entrada):
    while True:
        Respuesta = input("Ingrese una respuesta correcta\n")
        if entrada == "Orientacion" and (Respuesta == "1" or Respuesta == "2"):
            return Respuesta
        elif entrada == "Coordenada":
            if len(Respuesta) == 2 or (len(Respuesta) == 3 and entrada[1:].isdigit()):
                letra = Respuesta[0].upper()
                numero = Respuesta[1:]
                if letra.isalpha() and letra >= 'A' and letra <= 'J' and numero.isdigit():
                    numero = int(numero)
                    if 1 <= numero <= 10:
                        return letra,numero
                    
class Barco:
    def __init__(self, Casillas, Orientacion, Ubicacion):
        self.Casillas = Casillas
        self.Orientacion = Orientacion
        self.Ubicacion = Ubicacion

class Tablero:
    def __init__(self):
        # Crear matriz 11x11
        self.Mapa = [[' ' for _ in range(11)] for _ in range(11)]

        # Llenar primera fila con letras de la A a la J
        letras = 'ABCDEFGHIJ'
        for i, letra in enumerate(letras):
            if i == 0:
                self.Mapa[0][i] = '  '
                self.Mapa[0][i+1] = letra
            else:
                self.Mapa[0][i+1] = letra

        # Llenar las siguientes filas con números del 1 al 10 en la primera columna
        for i in range(1, 11):
            if i < 10:
                self.Mapa[i][0] = str(i) + ' '
            else:
                self.Mapa[i][0] = str(i)

        # Inicializar lista de barcos (aquí asumimos que ya tienes una clase Barco definida)
        self.Barcos = []
    # Metodos
    # Agrega los barcos al tablero
    def agregar_barco(self, barco):
        self.Barcos.append(barco)
    
    # Muestra el tablero
    def MostrarTablero (self,OcultarBarcos):
        LimpiarConsola()
        for Fila in self.Mapa:
            for Elemento in Fila:
                if Elemento == "o" and OcultarBarcos == False:
                    print(str(Elemento) + "|", end="")  
                elif Elemento == "o" and OcultarBarcos == True:
                    print(str(" ") + "|", end="")
                else:
                    print(str(Elemento) + "|", end="")  
            print("")
    
    # Verificar casillas libres al poner el barco
    def CasillasLibres(self, Orientacion,LongitudBarco,PosicionLetra,PosicionNumero):
            CasillasLibres = False
            if Orientacion == "Vertical" and PosicionNumero <= len(self.Mapa)-LongitudBarco:      
                for i in range (0,LongitudBarco):
                    if self.Mapa[PosicionNumero+i][self.Mapa[0].index(PosicionLetra)] != "o":
                        CasillasLibres=True
                    else:
                        CasillasLibres=False
                        break
            elif Orientacion == "Horizontal" and self.Mapa[0].index(PosicionLetra) <= len(self.Mapa)-LongitudBarco:      
                for i in range (0,LongitudBarco):
                    if self.Mapa[PosicionNumero][self.Mapa[0].index(PosicionLetra)+i] != "o":
                        CasillasLibres=True
                    else:
                        CasillasLibres=False
                        break
            return CasillasLibres
    
    # Colocar los barcos en el tablero
    def ColocarBarco(self,Orientacion,CasillasBarco,PosicionLetra,PosicionNumero):
        if Orientacion == "Vertical":      
            for i in range (0,CasillasBarco):
                self.Mapa[PosicionNumero+i][self.Mapa[0].index(PosicionLetra)] = "o"
        elif Orientacion == "Horizontal":      
            for i in range (0,CasillasBarco):
                self.Mapa[PosicionNumero][self.Mapa[0].index(PosicionLetra)+i] = "o"

    # Arma el tablero que se va a usar durante la partida
    def ArmarTablero (self):
        self.MostrarTablero(False)
        for Barco in self.Barcos:
            # Ciclo para forzar que se coloque correctamente cada uno de los barcos
            BarcoColocado = False
            while BarcoColocado == False:
                # Elegir la orientacion del barco
                print("Presione 1 para colocar el barco verticalmente")
                print("Presione 2 para colocar el barco horizontalmente")
                Orientacion= ComprobaryTransformarInput("Orientacion")
                if Orientacion == "1":
                    Orientacion = "Vertical"
                elif Orientacion == "2":
                    Orientacion = "Horizontal"
                # Recibir la coordenada para la punta del barco
                print("Escriba la coordenada para colocar la punta del barco")
                # Obtener Coordenadas
                Letra, Numero = ComprobaryTransformarInput("Coordenada")
                CasillasDisponibles = self.CasillasLibres(Orientacion,Barco.Casillas,Letra,Numero)
                if CasillasDisponibles == True:
                    if Orientacion == "Vertical" and Numero <= len(self.Mapa)-Barco.Casillas:
                        self.ColocarBarco(Orientacion,Barco.Casillas,Letra,Numero)
                        Barco.Orientacion="Vertical"
                        Barco.Ubicacion = Letra+str(Numero)
                        BarcoColocado = True
                    elif Orientacion == "Horizontal":
                        self.ColocarBarco(Orientacion,Barco.Casillas,Letra,Numero)
                        Barco.Orientacion="Horizontal"
                        Barco.Ubicacion = Letra+str(Numero)
                        BarcoColocado = True
                    input("Barco colocado")
                else:
                    input("No se puede colocar el barco en esa casilla, intente otra casilla")
            self.MostrarTablero(False)
    # Actualizar tablero segun resultados del lanzamiento
    def RealizarLanzamiento(self,PosicionLetra,PosicionNumero):
        AtaqueExitoso = False
        if self.Mapa[PosicionNumero][self.Mapa[0].index(PosicionLetra)] == "o":
            self.Mapa[PosicionNumero][self.Mapa[0].index(PosicionLetra)] = "x"
            self.MostrarTablero(True)
            input("Barco alcanzado")
            AtaqueExitoso = True
        elif self.Mapa[PosicionNumero][self.Mapa[0].index(PosicionLetra)] == "x" or self.Mapa[PosicionNumero][self.Mapa[0].index(PosicionLetra)] == "h":
            self.MostrarTablero(True)
            input("Esta casilla ya fue atacada")
        else:
            self.Mapa[PosicionNumero][self.Mapa[0].index(PosicionLetra)] = "f"
            self.MostrarTablero(True)
            input("Lanzamiento fallido")
        return AtaqueExitoso
    
    # Actulizar tablero si se ha hundido un barco
    def ActualizarHundidos(self):
        Hundido = ""
        for Barco in self.Barcos:
            Letra = Barco.Ubicacion[0]
            Numero = Barco.Ubicacion[1:]
            BarcoHundido = True
            if Barco.Orientacion == "Vertical":      
                for i in range (0,Barco.Casillas):
                    if self.Mapa[int(Numero)+i][self.Mapa[0].index(Letra)] != "x":
                        BarcoHundido=False
                        break
            elif Barco.Orientacion == "Horizontal":      
                for i in range (0,Barco.Casillas):
                    if self.Mapa[int(Numero)][self.Mapa[0].index(Letra)+i] != "x":
                        BarcoHundido=False
                        break
            if BarcoHundido == True:
                if Barco.Orientacion == "Vertical":      
                    for i in range (0,Barco.Casillas):
                        self.Mapa[int(Numero)+i][self.Mapa[0].index(Letra)] = "h"
                elif Barco.Orientacion == "Horizontal":      
                    for i in range (0,Barco.Casillas):
                        self.Mapa[int(Numero)][self.Mapa[0].index(Letra)+i] = "h"
                self.MostrarTablero(True)
                input("Barco hundido")
                # Barcos hundidos
                Hundido = Barco
                break
        if Hundido != "":
            self.Barcos.remove(Hundido)
    

#Arreglo para definir la cantidad de barcos y su tamaño
LongitudBarcos = [3,3,3,5,5]

# Bienvenida al juego
print ("Batalla Naval")
# Crear Tablero del jugador 1
Tablero1 = Tablero()
Tablero2 = Tablero()
for item in LongitudBarcos:
    PiezaBarco = Barco(item,"","")
    Tablero1.agregar_barco(PiezaBarco)
    Tablero2.agregar_barco(PiezaBarco)

# Armar Tablero de Jugador 1
input("Es el turno del jugador 1 de colocar los barcos")
Tablero1.ArmarTablero()
# Armar Tablero de Jugador 2
input("Es el turno del jugador 2 de colocar los barcos")
Tablero2.ArmarTablero()
input("¡Que empiece la batalla!")

while len(Tablero1.Barcos)!=0 and len(Tablero2.Barcos)!=0:
    if len(Tablero1.Barcos)!=0:
        LimpiarConsola()
        Tablero2.MostrarTablero(True)
        print ("Es el turno del jugador 1")
        print ("Este es el tablero del jugador 2")
        print("Escoja una casilla y ataque")
        Letras,Numero = ComprobaryTransformarInput("Coordenada")
        # Actualizar tablero
        AtaqueExitoso = Tablero2.RealizarLanzamiento(Letras,Numero)
        if AtaqueExitoso == True:
            Tablero2.ActualizarHundidos()
        input ("Quedan " + str(len(Tablero2.Barcos))+" barcos por hundir")
    if len(Tablero2.Barcos)!=0:
        LimpiarConsola()
        Tablero1.MostrarTablero(True)
        print ("Es el turno del jugador 2")
        print ("Este es el tablero del jugador 1")
        print("Escoja una casilla y ataque")
        Letras,Numero = ComprobaryTransformarInput("Coordenada")
        # Actualizar tablero
        AtaqueExitoso = Tablero1.RealizarLanzamiento(Letras,Numero)
        if AtaqueExitoso == True:
            Tablero2.ActualizarHundidos()
        input ("Quedan " + str(len(Tablero1.Barcos))+" barcos por hundir")

# Mostrar al ganador del juego
if len(Tablero1.Barcos)==0:
    LimpiarConsola()
    print("Gana el jugador 2")
elif len(Tablero2.Barcos)==0:
    LimpiarConsola()
    print("Gana el jugador 1")