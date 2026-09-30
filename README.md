# Taller AI-Native — Entrega

**Estudiante:** Luis Daniel Lavado Carreño (`ldlavado`)  
**Repositorio:** https://github.com/ldlavado/Taller-AI-Native  
**Base del taller:** https://github.com/AndUm423/Taller-AI-Native  
**Fecha:** 30 de septiembre de 2026

Este README es la entrega. El enunciado original se conserva como referencia al final.

---

## Qué se entregó

| Archivo | Qué es |
|---|---|
| [`task_manager_ai_native.py`](task_manager_ai_native.py) | Programa corregido (Tkinter + lógica de negocio) |
| [`test_task_manager.py`](test_task_manager.py) | 18 pruebas unitarias (`unittest`) |
| [`docs/documento_evidencias.md`](docs/documento_evidencias.md) | Copia del proceso y la reflexión |

Flujo aplicado:

```text
comprende → proporciona contexto → solicita → verifica → prueba → corrige → documenta
```

---

## Cómo ejecutar

Aplicación (requiere Tkinter):

```bash
python task_manager_ai_native.py
```

Pruebas (no abren la ventana):

```bash
python -m unittest test_task_manager.py -v
```

Resultado esperado: **18 tests OK**.

Usuarios de la interfaz: `ana`, `jorge`, `jojo`. Cada uno solo ve y modifica sus propias tareas.

---

## Solución

El programa original permitía crear, listar, completar y eliminar tareas, pero no respetaba al dueño de cada tarea y se caía con entradas inválidas.

### Comportamiento corregido

1. Cada tarea pertenece a un usuario.
2. `list_tasks(user)` solo devuelve las tareas de ese usuario.
3. Completar y eliminar usan el **índice visible del usuario**, no el índice de la lista global.
4. Un usuario no puede completar ni eliminar una tarea ajena.
5. Título vacío, índice vacío, índice no numérico e índice negativo no cierran el programa: muestran un mensaje.
6. Tkinter se importa de forma opcional para que las pruebas corran sin interfaz.

### Decisión humana (obligatoria en el taller)

Corregir solo `list_tasks` no bastaba. Si esa función devuelve una lista filtrada nueva, `pop(index)` borra la copia y **no** actualiza `tasks`.

La corrección opera sobre el diccionario real:

```python
def _resolve_owned_task(index, user):
    """DECISIÓN DEL DESARROLLADOR:
    El índice es de la lista filtrada del usuario, no de la lista global.
    complete/delete no hacen pop sobre la copia filtrada: esa lista es
    solo una vista y no actualizaría `tasks`. Se localiza el mismo dict
    en la lista global y se opera sobre él.
    """
    ...
    return owned[index]


def delete_task(index, user):
    task = _resolve_owned_task(index, user)
    tasks.remove(task)
    return "Tarea eliminada"
```

### Funciones de negocio

```python
def add_task(title, user):
    # valida título y usuario; guarda title, user, completed=False

def list_tasks(user):
    # solo tareas de ese usuario

def complete_task(index, user):
    # marca completed=True si la tarea es del usuario

def delete_task(index, user):
    # elimina el objeto en la lista global tasks
```

Los errores de negocio se lanzan como `TaskError` (subclase de `ValueError`) y la interfaz los muestra con `messagebox`, sin trazar una excepción cruda al usuario.

---

## 1. Análisis inicial

Hecho **antes** de pedirle a la IA que reescribiera el archivo.

| Problema | Tipo | Impacto | Solución aplicada |
|---|---|---|---|
| `list_tasks(user)` ignoraba `user` y devolvía toda la lista `tasks` | Seguridad | Alto | Filtrar por `task["user"] == user` |
| Completar/eliminar usaban esa lista; un índice tocaba tareas ajenas | Seguridad | Alto | Índice sobre la vista del usuario y comprobación de dueño |
| Si `list_tasks` devolvía una copia, `pop` no borraba en `tasks` | Funcional | Alto | `tasks.remove(task)` sobre el dict real |
| `get_index()` hacía `int(...)` fuera del `try`; índice vacío cerraba la app | Funcional | Alto | Validar texto vacío y no numérico con `TaskError` |
| Título vacío se guardaba | Calidad | Medio | Rechazar título en blanco |
| Índice negativo es válido en Python y tocaba la última tarea | Seguridad | Medio | Rechazar `index < 0` |

El propio código original marcaba el filtro de `list_tasks` como problema intencional del taller.

---

## 2. Uso de Inteligencia Artificial

- **Herramienta:** Grok (xAI).
- **Qué hizo la IA:** análisis del código base, propuesta de validaciones, versión corregida y archivo de pruebas.
- **Qué decidió el estudiante:**
  1. No aceptar `pop` sobre la lista filtrada.
  2. Tratar el índice como posición en la vista del usuario, no en `tasks`.
  3. Importar Tkinter solo si está disponible, para poder probar sin GUI.
  4. Usar `TaskError` con mensajes de negocio en lugar de `IndexError` / `ValueError` crudos.

La IA no se usó como “haz el programa y listo”. Primero se pidió análisis, después código, después pruebas, y cada salida se revisó.

---

## 3. Prompts utilizados

### Prompt de análisis

```text
Actúa como ingeniero de software senior en Python.

Sistema: gestor de tareas de escritorio (Tkinter) para ana, jorge y jojo.
Archivo: task_manager_ai_native.py. Estado en memoria, lista global tasks.

Restricciones:
- Seguir en Python y Tkinter.
- Sin base de datos ni frameworks nuevos.
- No reescribir la interfaz si no hace falta.
- No des todavía el código corregido.

Requisitos:
1. Cada tarea pertenece a un usuario.
2. Un usuario solo ve y modifica las suyas.
3. Índice inválido, negativo o no numérico no tumba el programa.
4. Título vacío no se guarda.
5. Mensajes de error entendibles.

Problemas que ya encontré:
- list_tasks ignora el usuario.
- complete_task y delete_task usan esa lista y permiten tocar tareas ajenas.
- get_index() está fuera del try y un índice vacío cierra la app.
- Si list_tasks filtra a una lista nueva, delete_task con pop no borra el original.

Analiza el código. Para cada problema: explicación, prioridad y recomendación.
No generes la solución final.
```

### Prompt de generación

```text
Con el análisis anterior, entrega task_manager_ai_native.py corregido.

Exigencias:
- Mantener crear, listar, completar y eliminar.
- Conservar Tkinter y la estructura de la ventana.
- Un usuario solo ve y modifica sus tareas.
- Validar título e índice.
- El programa no debe cerrarse ante entradas incorrectas.
- No hacer pop sobre una lista filtrada: operar sobre el objeto real en tasks.
- Marcar en un comentario al menos una decisión del desarrollador.
```

### Prompt de testing

```text
Crea test_task_manager.py con unittest.
No abras Tkinter.
Limpia la lista tasks en setUp.

Cubre como mínimo:
- creación de una tarea
- listado
- restricción por usuario
- completar
- eliminar
- índice inválido
- usuario inexistente
- entrada incorrecta (título vacío, índice no entero)
- intento de modificar una tarea de otro usuario
```

---

## 4. Comparación original vs final

| Original | Corregido |
|---|---|
| `list_tasks` devolvía `tasks` completa | Devuelve solo las del usuario |
| Completar/eliminar por índice global | Índice de la vista del usuario + dueño |
| `pop(index)` sobre la lista visible | `tasks.remove(task)` del objeto real |
| `int()` fuera del `try` | Validación previa + `TaskError` |
| Título vacío permitido | Rechazado |
| Sin pruebas | 18 pruebas unitarias |
| Mezcla total GUI / lógica | Lógica reusable por los tests; GUI opcional |

---

## 5. Pruebas

Archivo: [`test_task_manager.py`](test_task_manager.py)

| Grupo | Qué comprueba |
|---|---|
| Creación | Alta de tarea y normalización de título/usuario |
| Listado y restricción | Ana no ve las de Jorge; usuario sin tareas → lista vacía |
| Completar y eliminar | Operan sobre la propia lista y no tocan al otro usuario |
| Índice inválido | Fuera de rango, negativo y no entero |
| Entrada incorrecta | Usuario vacío, título vacío, usuario sin tareas |
| Tarea ajena | No completar ni eliminar la de otro; el índice 0 de Ana no es la de Jorge |

---

## 6. Revisión humana

1. ¿La IA corrigió los problemas identificados? Sí, con el ajuste humano del `remove`.
2. ¿Introdujo problemas nuevos? El riesgo era borrar sobre la copia filtrada; se evitó.
3. ¿La solución es entendible? Sí: validadores, `_resolve_owned_task` y la GUI casi igual.
4. ¿Se mantienen las funcionalidades? Crear, listar, completar, eliminar y cambio de usuario.
5. ¿Quedan huecos de seguridad? Un usuario de la GUI ya no ve ni modifica tareas ajenas.
6. ¿Qué parte modificó el estudiante? El criterio de borrado, el índice visible y la importación opcional de Tkinter.

---

## 7. Reflexión

1. **Qué hizo el estudiante.** El análisis inicial, la tabla de problemas, la decisión de no usar `pop` sobre la vista filtrada, la separación pruebas/GUI y la revisión del código generado.
2. **¿La primera respuesta de la IA fue correcta?** En lo grueso sí (filtrar por usuario). En el detalle no: una corrección ingenua de `list_tasks` deja `delete_task` inútil porque `pop` actúa sobre una copia.
3. **¿Por qué validar el código de una IA?** El modelo no ejecuta el programa. Puede arreglar un defecto y crear otro. Las pruebas son la evidencia, no la afirmación de la IA.
4. **¿Qué aportó el contexto?** Evitó un rediseño con base de datos o frameworks. El modelo trabajó sobre los problemas ya encontrados y sobre las restricciones del enunciado.
5. **Generador vs proceso de ingeniería.** Pedir “corrige este código” entrega un archivo. El flujo AI-Native entrega análisis, restricciones, código, una decisión humana trazable y pruebas que se pueden repetir.

---

## Estructura del repositorio

```text
Taller-AI-Native/
├── README.md                      ← este documento (entrega)
├── task_manager_ai_native.py      ← solución
├── test_task_manager.py           ← pruebas
└── docs/
    └── documento_evidencias.md
```

Commit de la solución: https://github.com/ldlavado/Taller-AI-Native/commit/70a03a40d4787f8d423b3a6ef66276deada15f67

---

## Enunciado original del taller

El README del repositorio base describe el propósito, las seis actividades, las reglas (IA permitida, proceso obligatorio, verificación real, intervención humana) y las preguntas de reflexión.

Repositorio base: https://github.com/AndUm423/Taller-AI-Native
