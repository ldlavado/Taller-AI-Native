import unittest

import task_manager_ai_native as tm


class TaskManagerTestCase(unittest.TestCase):
    def setUp(self):
        tm.tasks.clear()

    def tearDown(self):
        tm.tasks.clear()


class TestCreacion(TaskManagerTestCase):
    def test_crear_tarea(self):
        task = tm.add_task("Revisar informe", "ana")
        self.assertEqual(task["title"], "Revisar informe")
        self.assertEqual(task["user"], "ana")
        self.assertFalse(task["completed"])
        self.assertEqual(len(tm.tasks), 1)

    def test_titulo_se_normaliza(self):
        task = tm.add_task("  Comprar insumos  ", "Ana")
        self.assertEqual(task["title"], "Comprar insumos")
        self.assertEqual(task["user"], "ana")


class TestListadoYRestriccion(TaskManagerTestCase):
    def test_listado_solo_tareas_del_usuario(self):
        tm.add_task("Tarea de Ana", "ana")
        tm.add_task("Tarea de Jorge", "jorge")
        tm.add_task("Otra de Ana", "ana")

        de_ana = tm.list_tasks("ana")
        de_jorge = tm.list_tasks("jorge")

        self.assertEqual([t["title"] for t in de_ana], ["Tarea de Ana", "Otra de Ana"])
        self.assertEqual([t["title"] for t in de_jorge], ["Tarea de Jorge"])

    def test_usuario_sin_tareas_devuelve_lista_vacia(self):
        tm.add_task("Solo Ana", "ana")
        self.assertEqual(tm.list_tasks("jojo"), [])

    def test_usuario_inexistente_puede_listar_vacio(self):
        tm.add_task("Solo Ana", "ana")
        self.assertEqual(tm.list_tasks("carlos"), [])


class TestCompletarYEliminar(TaskManagerTestCase):
    def test_completar_tarea_propia(self):
        tm.add_task("Primera", "ana")
        tm.add_task("Segunda", "ana")
        mensaje = tm.complete_task(1, "ana")
        self.assertEqual(mensaje, "Tarea completada")
        self.assertTrue(tm.list_tasks("ana")[1]["completed"])
        self.assertFalse(tm.list_tasks("ana")[0]["completed"])

    def test_eliminar_tarea_propia(self):
        tm.add_task("A", "ana")
        tm.add_task("B", "ana")
        mensaje = tm.delete_task(0, "ana")
        self.assertEqual(mensaje, "Tarea eliminada")
        restantes = tm.list_tasks("ana")
        self.assertEqual(len(restantes), 1)
        self.assertEqual(restantes[0]["title"], "B")
        self.assertEqual(len(tm.tasks), 1)

    def test_eliminar_no_afecta_tareas_de_otro_usuario(self):
        tm.add_task("De Ana", "ana")
        tm.add_task("De Jorge", "jorge")
        tm.delete_task(0, "ana")
        self.assertEqual(len(tm.list_tasks("jorge")), 1)
        self.assertEqual(tm.list_tasks("jorge")[0]["title"], "De Jorge")


class TestIndiceInvalido(TaskManagerTestCase):
    def test_indice_inexistente(self):
        tm.add_task("Una", "ana")
        with self.assertRaises(tm.TaskError) as ctx:
            tm.complete_task(5, "ana")
        self.assertIn("índice", str(ctx.exception).lower())

    def test_indice_negativo(self):
        tm.add_task("Una", "ana")
        with self.assertRaises(tm.TaskError):
            tm.delete_task(-1, "ana")

    def test_indice_no_entero(self):
        tm.add_task("Una", "ana")
        with self.assertRaises(tm.TaskError):
            tm.complete_task("0", "ana")


class TestUsuarioEIngresoIncorrecto(TaskManagerTestCase):
    def test_usuario_vacio(self):
        with self.assertRaises(tm.TaskError):
            tm.add_task("Algo", "   ")

    def test_usuario_inexistente_sin_tareas_al_completar(self):
        tm.add_task("De Ana", "ana")
        with self.assertRaises(tm.TaskError) as ctx:
            tm.complete_task(0, "carlos")
        self.assertIn("no tiene tareas", str(ctx.exception))

    def test_titulo_vacio(self):
        with self.assertRaises(tm.TaskError):
            tm.add_task("   ", "ana")

    def test_titulo_nulo(self):
        with self.assertRaises(tm.TaskError):
            tm.add_task(None, "ana")


class TestModificarTareaAjena(TaskManagerTestCase):
    def test_no_completar_tarea_de_otro_usuario(self):
        tm.add_task("De Jorge", "jorge")
        with self.assertRaises(tm.TaskError):
            tm.complete_task(0, "ana")
        self.assertFalse(tm.tasks[0]["completed"])

    def test_indice_visible_no_apunta_a_tarea_ajena(self):
        tm.add_task("De Jorge primero", "jorge")
        tm.add_task("De Ana", "ana")
        tm.complete_task(0, "ana")
        self.assertTrue(tm.list_tasks("ana")[0]["completed"])
        self.assertFalse(tm.list_tasks("jorge")[0]["completed"])

    def test_no_eliminar_tarea_de_otro_usuario(self):
        tm.add_task("De Jorge", "jorge")
        with self.assertRaises(tm.TaskError):
            tm.delete_task(0, "ana")
        self.assertEqual(len(tm.tasks), 1)


if __name__ == "__main__":
    unittest.main()
