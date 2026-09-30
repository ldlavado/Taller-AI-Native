# Documento de evidencias — Taller AI-Native

**Repositorio:** https://github.com/ldlavado/Taller-AI-Native  
**Base:** https://github.com/AndUm423/Taller-AI-Native  
**Fecha:** 30 de septiembre de 2026

Este archivo cubre el texto de las secciones 1–3, 5–7 del documento pedido. Los pantallazos (sección 4) hay que sacarlos en el computador local al ejecutar la app y al pegar los prompts en el chat de IA.

## 1. Análisis inicial

| Problema | Tipo | Impacto | Solución aplicada |
|---|---|---|---|
| `list_tasks(user)` ignoraba el usuario y devolvía toda la lista | Seguridad | Alto | Filtrar por `task["user"] == user` |
| Completar/eliminar usaban esa lista global; un índice tocaba tareas ajenas | Seguridad | Alto | Índice sobre la vista del usuario + dueño comprobado |
| Si `list_tasks` devolvía una copia, `pop` no borraba en `tasks` | Funcional | Alto | `tasks.remove(task)` sobre el dict real |
| `get_index()` hacía `int(...)` fuera del `try`; índice vacío cerraba la app | Funcional | Alto | Validar texto vacío y no numérico con `TaskError` |
| Título vacío se guardaba | Calidad | Medio | Rechazar título en blanco |
| Índice negativo es válido en Python y tocaba la última tarea | Seguridad | Medio | Rechazar `index < 0` |

## 2. Uso de Inteligencia Artificial

- Herramienta: Grok (xAI), usada como apoyo de análisis, corrección y pruebas.
- La IA propuso el filtro por usuario, validaciones y el archivo de tests.
- Decisiones humanas:
  1. No hacer `pop` sobre la lista filtrada; localizar el dict en `tasks` y usar `remove`.
  2. Índice siempre sobre la vista del usuario actual, no sobre la lista global.
  3. Importar Tkinter de forma opcional para que las pruebas corran sin GUI.
  4. Mensajes de negocio con `TaskError`, no excepciones crudas en la interfaz.

## 3. Prompts utilizados

### Prompt de análisis
Ver conversación previa del taller. Se pidió análisis primero, sin código.

### Prompt de generación
Se pidió conservar Tkinter, filtrar por dueño, validar índice y título, y no reescribir la UI.

### Prompt de testing
Se pidió `test_task_manager.py` con unittest, sin abrir la ventana, cubriendo creación, listado, restricción por usuario, completar, eliminar, índice inválido, usuario inexistente, entrada incorrecta y modificación de tarea ajena.

## 4. Evidencias (pendientes en local)

Colocar en `evidencias/`:

- codigo_original.png
- prompt_inicial.png
- respuesta_ia.png
- codigo_corregido.png
- ejecucion_programa.png
- ejecucion_pruebas.png

Comandos locales:

```bash
python task_manager_ai_native.py
python -m unittest test_task_manager.py -v
```

## 5. Código final

https://github.com/ldlavado/Taller-AI-Native

Archivos: `task_manager_ai_native.py`, `test_task_manager.py`.

## 6. Comparación

| Original | Corregido |
|---|---|
| `list_tasks` devolvía `tasks` | Devuelve solo las del usuario |
| `pop(index)` sobre la lista visible | `tasks.remove(task)` del objeto real |
| `int()` fuera del try | Validación + `TaskError` |
| Título vacío permitido | Rechazado |
| Sin pruebas | 18 pruebas unitarias |

## 7. Reflexión

1. El análisis inicial, la decisión de borrar sobre la lista global y la separación Tkinter/pruebas las tomó el estudiante.
2. La primera respuesta de una IA que solo “corrige `list_tasks`” suele dejar el `pop` sobre la copia; hay que revisarla.
3. Hay que validar porque el modelo no ejecuta el programa y puede introducir un bug al arreglar otro.
4. El contexto (requisitos, restricciones y problemas ya vistos) evitó un rediseño innecesario y enfocó el filtro por usuario.
5. Usar la IA como generador entrega un archivo. Usarla en un proceso entrega análisis, código, revisión humana y pruebas que se pueden repetir.
