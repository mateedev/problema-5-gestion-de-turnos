import struct
import os

# Declaracion de constantes — única fuente de verdad

FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)


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
      
      Postcondición: escribe los registros empaquetados en el archivo. Y crea o sobrescribe un archivo.
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
                  
