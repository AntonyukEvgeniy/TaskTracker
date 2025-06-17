import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task
from users.models import Employee


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def generate_employees(self, count):
        positions = [
            "Разработчик", "Тестировщик", "Менеджер проекта", "Аналитик",
            "Дизайнер", "DevOps инженер", "Системный администратор"
        ]

        employees = []
        for i in range(count):
            employee = Employee.objects.create(
                full_name=f"Сотрудник {i + 1}",
                position=random.choice(positions)
            )
            employees.append(employee)
        return employees

    def generate_tasks(self, count, employees):
        tasks = []
        statuses = [status[0] for status in Task.Status.choices]

        # Создаем задачи без родителей (70% от общего количества)
        root_tasks_count = int(count * 0.7)
        for i in range(root_tasks_count):
            deadline = timezone.now() + timedelta(days=random.randint(1, 60))
            task = Task.objects.create(
                title=f"Задача {i + 1}",
                assignee=random.choice(employees),
                deadline=deadline,
                status=random.choice(statuses)
            )
            tasks.append(task)
        # Создаем подзадачи (30% от общего количества)
        subtasks_count = count - root_tasks_count
        for i in range(subtasks_count):
            deadline = timezone.now() + timedelta(days=random.randint(1, 60))
            task = Task.objects.create(
                title=f"Подзадача {i + 1}",
                parent_task=random.choice(tasks),  # Выбираем случайную родительскую задачу
                assignee=random.choice(employees),
                deadline=deadline,
                status=random.choice(statuses)
            )
            tasks.append(task)
        return tasks

    def handle(self, *args, **options):
        # Создаем сотрудников
        self.stdout.write('Создание сотрудников...')
        employees = self.generate_employees(1000)
        self.stdout.write(f'Создано {len(employees)} сотрудников')
        # Создаем задачи
        self.stdout.write('Создание задач...')
        tasks = self.generate_tasks(10000, employees)
        self.stdout.write(f'Создано {len(tasks)} задач')