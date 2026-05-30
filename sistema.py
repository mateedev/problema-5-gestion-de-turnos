import struct
import os

# Declaracion de constantes — única fuente de verdad

FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)

## ================ MODULO 1 ================ ##


def empaquetar_paciente(dni, apellido, nombre, telefono, prioridad):
      """
      Empaqueta los datos de un paciente en bytes, los codifica en UTF-8 y los trunca si es necesario.
      
      Precondicion: dni es un int32 valido; apellido, nombre, telefono son strings codificados en utf-8 y prioridad es un int (1 a 3)
      
      Postcondicion: Va a devolver un objeto bytes de exactamente TAM_REGISTRO = 75 bytes.
      """
      
      # Codificacion a utf-8 y truncado de cadenas largas
      
      apellido_b = apellido.encode("utf-8")[:30]
      nombre_b = nombre.encode("utf-8")[:24]
      telefono_b = telefono.encode("utf-8")[:16]
      return struct.pack(FORMATO, dni, apellido_b, nombre_b, telefono_b, prioridad)


def desempaquetar_paciente(registro_b):
      """
      Desempaqueta un registro de TAM_REGISTRO (en este caso 75 bytes) y decodifica las cadenas, limpiando los bytes nulos de relleno. Retorna un diccionario.
      
      Precondicion: registro_b es una objeto bytes de longitud TAM_REGISTRO y sigue la estructura binaria definida en FORMATO.
      
      Postcondicion: Devuelve un diccionario con las claves 'dni', 'apellido', 'nombre', 'telefono' y 'prioridad' con los datos decodificados. 
      """
      
      dni, apellido_b, nombre_b, telefono_b, prioridad = struct.unpack(FORMATO, registro_b)
      
      apellido = apellido_b.rstrip(b'\x00').decode('utf-8')  # bytes -> str sin relleno
      nombre = nombre_b.rstrip(b'\x00').decode('utf-8')  # bytes -> str sin relleno
      telefono = telefono_b.rstrip(b'\x00').decode('utf-8')  # bytes -> str sin relleno
      
      return {
        'dni': dni,
        'apellido': apellido,
        'nombre': nombre,
        'telefono': telefono,
        'prioridad': prioridad
      }



def crear_archivo_pacientes(ruta, lista_pacientes):
      """
      Crea un archivo binario y escribe secuencialmente la lista de pacientes.
      
      Precondicion: ruta es un str valido; lista_pacientes es una lista de diccionarios con las claves requeridas para empaquetar_paciente.
      
      Postcondición: escribe los registros empaquetados en el archivo.
      """
      
      with open(ruta, "wb") as archivo:  # wb lo que hace es crear o sobreescribir
            for p in lista_pacientes:
                  registro = empaquetar_paciente(
                        p["dni"],
                        p["apellido"],
                        p["nombre"],
                        p["telefono"],
                        p["prioridad"]
                  )
                  archivo.write(registro)
                  

def leer_paciente(archivo, k):
      """
      Lee y devuelve el paciente ubicado en la posicion k-esima del archivo.
      
      Precondicion: archivo es un objeto de archivo abierto en modo rb o r+b y k es un indice valido (0<=K<=cant_pacientes)
      
      Postcondición: devuelve el diccionario del paciente en la posición k, o None si la posición excede el fin del archivo.
      """
      
      archivo.seek(k * TAM_REGISTRO)
      registro_b = archivo.read(TAM_REGISTRO)
      
      return desempaquetar_paciente(registro_b)


### --- Prueba del Modulo 1 --- ###

# Preparo datos de prueba

pacientes_prueba = [
      {"dni": 44555333, "apellido": "Perez", "nombre": "Juan Martin", "telefono": "1122334466", "prioridad": 3}, {"dni": 44000222, "apellido": "Appio", "nombre": "Mateo", "telefono": "2364682576", "prioridad": 1}
      ]

ruta_archivo = "./semana-12/problema-5-gestion-de-turnos/pacientes_test.bin"


# Ejcuto la funcion para crear el archivo
crear_archivo_pacientes(ruta_archivo, pacientes_prueba)


# Hago la evaluacion que pide el enunciado
cantidad_de_pacientes = len(pacientes_prueba)
tamanio_esperado = cantidad_de_pacientes * TAM_REGISTRO
tamanio_real = os.path.getsize(ruta_archivo)

# Printeo los valores

print(f"El tamaño esperado del archivo es: {tamanio_esperado} bytes")
print(f"El tamaño del archivo realmente es: {tamanio_real} bytes")


## ================ MODULO 2 ================ ##

def construir_indices(ruta):
      """
      Construye dos diccionarios. Uno tiene como clave los dni y como valor la posición k
      del paciente en el archivo. El otro tiene como clave los apellidos y como valor el valor k.

      Precondición: ruta es un str valido que apunta al archivo donde estan los pacientes.

      Postcondición: La funcion devuelve los dos diccionarios ya construidos con cada uno de los pacientes. 
      
      """

      indice_por_dni = {}
      indice_por_apellido = {}    # Definó ambos diccionarios vacíos. 

      with open(ruta, "r") as archivo:
            for paciente in archivo:    # Recorro el archivo paciente por paciente y agrego la información a los diccionarios. 
                  dni, apellido = paciente.strip().split(",")
                  bite_actual = archivo.tell()
                  k = bite_actual // TAM_REGISTRO
                  indice_por_dni[dni] = k
                  if apellido not in indice_por_apellido:
                        indice_por_apellido[apellido] = []
                  indice_por_apellido[apellido].append(k)
      return indice_por_dni, indice_por_apellido

def buscar_por_dni(dni, indice_por_dni, ruta):
      """
      Esta función busca el paciente por el dni utilizando el diccionario creado anteriormente, de este modo disminute
      el tiempo de búsqueda. 

      Precondición: El diccionario indice_por_dni debe haber sido construido previamente con la función construir_indices 
      y ruta debe ser un str válido que apunta al archivo de pacientes. 

      Postcondición: Devuelve toda la información del paciente como un string. Si no se encuentra, devuelve
      None. 
      """
      if dni in indice_por_dni:
            k = indice_por_dni[dni]
            with open(ruta, "r") as archivo:
                  archivo.seek(k * TAM_REGISTRO)
            paciente = archivo.readline().strip()
            return paciente
      return None


### --- Prueba del Modulo 2 --- ###

# Los pacientes_prueba y ruta_archivo son los mismos que en el modulo 1, agrego otros datos. 

dni_a_buscar = 44000222

# Ejcuto la función para construir los índices

indice_por_dni, indice_por_apellido = construir_indices(ruta_archivo)

# Busco un paciente por dni utilizando la funcion buscar_por_dni
paciente = buscar_por_dni(dni_a_buscar, indice_por_dni, ruta_archivo)
"""
Si coparamos este método de búsqueda con el metodo secuencial de búsqueda, encontreamos que el gracias a
esta función solo tenemos que ver buscar la key en el diccionario, el cual es el dni, y luego ir a la posición
k en el archivo. Por otro lado, si utilizamos la otra manera, debemos iterar varias veces el archivo hasta 
encontrar el paciente, lo cual es menos eficiente. 
"""

# Printeo los resultados
print(f"El paciente con DNI {dni_a_buscar} es: {paciente}")
print(f"Los diccionarios son los siguientes: {indice_por_dni} y {indice_por_apellido}")

## ================ MODULO 3 ================ ##


def listar_pacientes_ordenados(ruta, criterio):
      """
      La funcion se encarga de listar todos los pacientes de manera ordenada, para ello utiliza la función 
      merge_sort definida luego. 

      Precondición: ruta es un str válido que apunta al archivo de pacientes. 
      Criterio es un str que puede ser "apellido" o "prioridad".

      Postcondición: Devuelve una lista de pacientes ordenados según el criterio especificado.
      """
      pacientes = []
    
      # Leemos el archivo y armamos una lista de diccionarios
      with open(ruta, mode='r', encoding='utf-8') as archivo:
          for fila in archivo:
              paciente = {
                  "dni": fila[0],
                  "apellido": fila[1],
                  "nombre": fila[2],
                  "telefono": fila[3],
                  "prioridad": fila[4]
              }
              pacientes.append(paciente)

      # Lógica de ordenamiento según el criterio
      if criterio == "apellido":
          # Orden simple: solo pasamos la clave 'apellido'
          return merge_sort(pacientes, clave=lambda p: p["apellido"])
        
      elif criterio == "prioridad":
          # ESTRATEGIA DE DOS PASADAS (aprovechando la estabilidad)
        
          # 1ra pasada: Ordenamos por el criterio de desempate (Apellido)
          pacientes_por_apellido = merge_sort(pacientes, clave=lambda p: p["apellido"])
        
          # 2da pasada: Ordenamos por el criterio principal (Prioridad)
          pacientes_final = merge_sort(pacientes_por_apellido, clave=lambda p: p["prioridad"])
        
          return pacientes_final
        

def merge_sort(lista):
      """
      Funcion de ordenamiento eficiente, vista en la semana 6.
      """
      if len(lista) <= 1:
            return lista

      medio = len(lista) // 2
      izquierda = lista[:medio]
      derecha = lista[medio:]


      izquierda_ordenada = merge_sort(izquierda)
      derecha_ordenada = merge_sort(derecha)


      return merge(izquierda_ordenada, derecha_ordenada)


def merge(izquierda, derecha):
      """
      Función auxiliar para merge_sort, también vista en la semana 6.
      """

      resultado = []
      i = 0  # Índice para recorrer la lista 'izquierda'
      j = 0  # Índice para recorrer la lista 'derecha'

      #
      while i < len(izquierda) and j < len(derecha):
            if izquierda[i] <= derecha[j]:
                  resultado.append(izquierda[i])
                  i += 1  
            else:
                  resultado.append(derecha[j])
                  j += 1  

      resultado.extend(izquierda[i:])
      resultado.extend(derecha[j:])

      return resultado

### --- Prueba del Modulo 3 --- ###

#Los datos son los mismos que en los modulos anteriores. 

# Ejcuto la función para listar los pacientes ordenados por apellido
pacientes_ordenados_apellido = listar_pacientes_ordenados(ruta_archivo, "apellido")
pacientes_ordenados_prioridad = listar_pacientes_ordenados(ruta_archivo, "prioridad")

# Printeo los resultados
print(f"Los pacientes ordenados por apellido son: {pacientes_ordenados_apellido}")
print(f"Los pacientes ordenados por prioridad son: {pacientes_ordenados_prioridad}")

#Justificacion de la estabilidad de la funcion.
"""
La función es estable, ya que en la primera pasada ordenamos el archivo según los apellidos de los pacientes, 
y luego, en la segunda pasada, ordenamos por prioridad. Esto es importante, ya que si no fuese así, cuando
se ordene por prioridad, solo sería ordenado por prioridad y no también por apellido. Por eso, se divide en 
pasadas para aprovechar la estabilidad del algoritmo de ordenamiento.
"""

## ================ MODULO 4 ================ ##

def asignar_agenda(pacientes_del_dia, franjas, disponibilidad):
      """
      Asigna pacientes a franjas horarias utilizando backtracking.

      Precondicion: pacientes_del_dia es una lista de pacientes, franjas es una lista
      de franjas horarias y disponibilidad es un diccionario que asocia cada paciente
      con las franjas en las que puede asistir.

      Postcondicion: Devuelve un diccionario paciente -> franja con una asignación
      válida o None si no existe ninguna solucion
      """

      asignacion = {}

      def backtracking(indice):

            if indice == len(pacientes_del_dia):
                  return True

            paciente = pacientes_del_dia[indice]

            for franja in franjas:

                  # Poda: la franja ya está ocupada
                  if franja in asignacion.values():
                        continue

                  # Poda: la franja no está disponible para el paciente
                  if franja not in disponibilidad[paciente]:
                        continue

                  asignacion[paciente] = franja

                  if backtracking(indice + 1):
                        return True

                  del asignacion[paciente]

            return False

      if backtracking(0):
            return asignacion

      return None


### --- Prueba del Modulo 4 --- ###

# Caso con solucion

pacientes_del_dia = ["Juan", "Mateo", "Ana"]

franjas = ["08:00", "08:30", "09:00"]

disponibilidad = {
      "Juan": ["08:00", "08:30"],
      "Mateo": ["08:30", "09:00"],
      "Ana": ["09:00"]
}

agenda = asignar_agenda(
      pacientes_del_dia,
      franjas,
      disponibilidad
)

print("Caso con solucion:")
print(agenda)

"""
Verificación manual:

La asignacion obtenida fue:

{'Juan': '08:00', 'Mateo': '08:30', 'Ana': '09:00'}

Disponibilidad:
- Juan puede asistir a 08:00 o 08:30, por lo tanto cumple.
- Mateo puede asistir a 08:30 o 09:00, por lo tanto cumple.
- Ana puede asistir a 09:00, por lo tanto cumple.

Unicidad de franjas:
- 08:00 aparece una sola vez.
- 08:30 aparece una sola vez.
- 09:00 aparece una sola vez.

Por lo tanto, la asignacion respeta todas las restricciones.
"""


# Caso sin solucion

pacientes_del_dia_2 = ["Juan", "Mateo", "Ana"]

franjas_2 = ["08:00", "08:30"]

disponibilidad_2 = {
      "Juan": ["08:00"],
      "Mateo": ["08:00"],
      "Ana": ["08:00"]
}

agenda_sin_solucion = asignar_agenda(
      pacientes_del_dia_2,
      franjas_2,
      disponibilidad_2
)

print("Caso sin solucion:")
print(agenda_sin_solucion)

"""
Como los tres pacientes solamente pueden asistir a la franja 08:00
y una franja puede recibir a lo sumo un paciente, no existe ninguna
asignacion valida.

Por lo tanto, la función devuelve None.
"""


# Discusión

"""
En el caso con solucion hay 3 pacientes y 3 franjas.

Si utilizamos fuerza bruta, cada paciente podría intentar ubicarse
en cualquiera de las 3 franjas, por lo que habría hasta 3³ = 27
asignaciones posibles para revisar.

El algoritmo de backtracking evita revisar muchas de ellas gracias
a las podas. Cuando una franja ya está ocupada o cuando una franja
no pertenece a la disponibilidad del paciente, esa rama se descarta
inmediatamente.

Por lo tanto, se exploran menos estados que en una busqueda por
fuerza bruta, ya que muchas combinaciones invalidas nunca llegan a
completarse.
"""

## ================ PROGRAMA PRINCIPAL ================ ##

def main():
      """
      Coordina los cuatro modulos del sistema.

      Precondicion: Las funciones de los modulos 1, 2, 3 y 4 deben estar definidas.

      Postcondicion: Permite crear el archivo, construir indices,
      realizar consultas y resolver la agenda del dia.
      """

      pacientes = [
            {
                  "dni": 44555333,
                  "apellido": "Saliani",
                  "nombre": "Pedro",
                  "telefono": "1122334466",
                  "prioridad": 3
            },
            {
                  "dni": 44000222,
                  "apellido": "Appio",
                  "nombre": "Mateo",
                  "telefono": "2364682576",
                  "prioridad": 1
            }
      ]

      ruta = "./semana-12/problema-5-gestion-de-turnos/pacientes.bin"

      # Modulo 1
      crear_archivo_pacientes(ruta, pacientes)

      # Modulo 2
      indice_por_dni, indice_por_apellido = construir_indices(ruta)

      opcion = ""

      while opcion != "4":

            print("\n=== MENU ===")
            print("1. Buscar paciente por DNI")
            print("2. Listar pacientes por apellido")
            print("3. Listar pacientes por prioridad")
            print("4. Resolver agenda del dia y salir")

            opcion = input("Seleccione una opcion: ")

            if opcion == "1":

                  dni = int(input("Ingrese DNI: "))

                  paciente = buscar_por_dni(
                        dni,
                        indice_por_dni,
                        ruta
                  )

                  print(paciente)

            elif opcion == "2":

                  pacientes_ordenados = listar_pacientes_ordenados(
                        ruta,
                        "apellido"
                  )

                  print(pacientes_ordenados)

            elif opcion == "3":

                  pacientes_ordenados = listar_pacientes_ordenados(
                        ruta,
                        "prioridad"
                  )

                  print(pacientes_ordenados)

            elif opcion == "4":

                  pacientes_del_dia = ["Pedro", "Mateo", "Ana"]

                  franjas = ["08:00", "08:30", "09:00"]

                  disponibilidad = {
                        "Pedro": ["08:00", "08:30"],
                        "Mateo": ["08:30", "09:00"],
                        "Ana": ["09:00"]
                  }

                  agenda = asignar_agenda(
                        pacientes_del_dia,
                        franjas,
                        disponibilidad
                  )

                  print("Agenda del dia:")
                  print(agenda)

            else:
                  print("Opcion invalida")


if __name__ == "__main__":
      main()