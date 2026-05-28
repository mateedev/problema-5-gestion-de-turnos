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


## ================ MODULO 3 ================ ##


## ================ MODULO 4 ================ ##