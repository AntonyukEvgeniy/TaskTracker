from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from tasks.management.commands.populate_db import Command
from tasks.models import Task
from users.models import Employee


class TaskModelTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(full_name="John Doe", position="Dev")
        self.task = Task.objects.create(
            title="My Task", assignee=self.employee, deadline=timezone.now()
        )

    def test_str_representation(self):
        self.assertEqual(str(self.task), "My Task")


class PopulateDBCommandTests(TestCase):
    def setUp(self):
        self.cmd = Command()

    def test_generate_methods(self):
        cmd = Command()
        employees = cmd.generate_employees(2)
        self.assertEqual(len(employees), 2)
        tasks = cmd.generate_tasks(4, employees)
        self.assertEqual(len(tasks), 4)
        self.assertTrue(any(t.parent_task is None for t in tasks))
        self.assertTrue(any(t.parent_task is not None for t in tasks))


class TaskViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.emp1 = Employee.objects.create(full_name="Emp1", position="dev")
        self.emp2 = Employee.objects.create(full_name="Emp2", position="qa")
        self.parent = Task.objects.create(
            title="Parent",
            assignee=self.emp1,
            deadline=timezone.now(),
            status=Task.Status.IN_PROGRESS,
        )
        self.important = Task.objects.create(
            title="Important",
            parent_task=self.parent,
            assignee=None,
            deadline=timezone.now() + timezone.timedelta(days=1),
            status=Task.Status.NEW,
        )
        Task.objects.create(
            title="Another",
            assignee=self.emp1,
            deadline=timezone.now(),
            status=Task.Status.IN_PROGRESS,
        )

    def test_get_important_tasks_and_employees(self):
        url = reverse("task-get-important-tasks-and-employees")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["task"], self.important.title)
        self.assertEqual(data[0]["suggested_employee"], self.emp2.full_name)
