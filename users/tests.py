from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from tasks.models import Task
from users.models import Employee


class EmployeeModelTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            full_name="Антонюк Евгений", position="QA"
        )

    def test_str_representation(self):
        employee = Employee.objects.create(full_name="Антонюк Евгений", position="QA")
        self.assertEqual(str(employee), "Антонюк Евгений")


class EmployeeViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.emp1 = Employee.objects.create(full_name="Emp1", position="dev")
        self.emp2 = Employee.objects.create(full_name="Emp2", position="qa")
        Task.objects.create(
            title="T1",
            assignee=self.emp1,
            deadline=timezone.now(),
            status=Task.Status.IN_PROGRESS,
        )
        Task.objects.create(
            title="T2",
            assignee=self.emp1,
            deadline=timezone.now(),
            status=Task.Status.NEW,
        )
        Task.objects.create(
            title="T3",
            assignee=self.emp2,
            deadline=timezone.now(),
            status=Task.Status.COMPLETED,
        )

    def test_busy_action(self):
        url = reverse("employee-busy")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], self.emp1.id)
        self.assertEqual(data[0]["active_tasks_count"], 2)
        self.assertEqual(len(data[0]["active_tasks"]), 2)
