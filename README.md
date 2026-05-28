# Problema 5: Sistema de turnos de un consultorio médico

Sistema de gestión de turnos para un consultorio médico. El sistema persiste los datos en un archivo binario de registros de longitud fija,mantiene índices en memoria mediante diccionarios, produce reportes ordenados, resuelve búsquedas eficientes por distintos criterios, y asigna turnos a una agenda diaria mediante backtracking. El problema se descompone en cuatro módulos

## Módulo 1 — Persistencia binaria de pacientes

Diseñar el registro de paciente de longitud fija y sus operaciones de lectura y escritura. El registro tiene la siguiente estructura:

| Campo     | Tipo struct | Tamaño   |
| --------- | ----------- | -------- |
| dni       | i (int32)   | 4 bytes  |
| apellido  | 30s         | 30 bytes |
| nombre    | 24s         | 24 bytes |
| telefono  | 16s         | 16 bytes |
| prioridad | B (uint8)   | 1 byte   |

### Constantes globales:

`FORMATO = "<i30s24s16sB"`
`TAM_REGISTRO = struct.calcsize(FORMATO)`

Implementar `empaquetar_paciente` y `desempaquetar_paciente`, con codificación UTF-8, truncado de cadenas largas y removido del relleno de ceros al desempaquetar. El campo prioridad es un entero de 1 (alta) a 3 (baja).

Implementar `crear_archivo_pacientes(ruta, lista_pacientes)` y `leer_paciente(archivo, k)` con acceso directo por offset(seek(k \* TAM_REGISTRO)). Usar el context manager with en todo acceso a archivo.

## Módulo 2 — Índices en memoria

Implementar `construir_indices(ruta)` que recorra una sola vez el archivo binario y devuelva dos diccionarios: `indice_por_dni` (clave: DNI, valor: posición k del registro en el archivo) e `indice_por_apellido` (clave: apellido, valor: lista de posiciones, porque puede haber apellidos repetidos).

Implementar `buscar_por_dni(archivo, indice_por_dni, dni)` que resuelva la búsqueda en O(1) promedio consultando el diccionario y leyendo un único registro. Comparar conceptualmente, en la docstring, con el costo de una búsqueda secuencial O(n) sobre el archivo sin índice.

## Módulo 3 — Reportes ordenados

Implementar `listar_pacientes_ordenados(ruta, criterio)` que lea todos los pacientes del archivo y devuelva la lista ordenada según el criterio indicado: "apellido" (alfabético) o "prioridad" (de 1 a 3, y dentro de cada prioridad, por apellido). Reutilizar la implementación de merge_sort del Problema 1 —que es estable— para el ordenamiento por prioridad con desempate por apellido.

Justificar por escrito por qué la estabilidad del algoritmo de ordenamiento es relevant para el criterio "prioridad": describir el procedimiento de dos pasadas (ordenar por apellido luego por prioridad) y explicar qué se rompería si el segundo ordenamiento no fuera estable.

## Módulo 4 — Asignación de la agenda diaria por backtracking

El consultorio tiene una agenda de franjas horarias (por ejemplo, 8 franjas de 30 minutos).
Algunos pacientes tienen restricciones de disponibilidad: una lista de las franjas en las que cada uno puede asistir. El problema es asignar cada paciente de una lista del día a una franja, respetando que (1) cada franja recibe a lo sumo un paciente y (2) cada paciente queda en una franja compatible con su disponibilidad.

Implementar `asignar_agenda(pacientes_del_dia, franjas, disponibilidad)` mediante backtracking. El estado parcial es la asignación construida hasta el momento (un diccionario franja → paciente, o paciente → franja). La poda descarta asignar un paciente a una franja ya ocupada o no disponible para él. La función devuelve una asignación válida, o None si no existe ninguna.

Probar con un caso que tenga solución y con un caso sobre-restringido que no la tenga
(más pacientes que franjas compatibles). Para el caso con solución, verificar que la
asignación devuelta respeta todas las restricciones. Discutir: ¿cuántas asignaciones posibles
habría que revisar por fuerza bruta, y cuántas evita la poda?
