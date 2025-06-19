import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task
from users.models import Employee


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными"

    def generate_employees(self, count):
        positions = [
            "Разработчик",
            "Тестировщик",
            "Менеджер проекта",
            "Аналитик",
            "Дизайнер",
            "DevOps инженер",
            "Системный администратор",
        ]

        employees = []
        for i in range(count):
            employee = Employee.objects.create(
                full_name=f"Сотрудник {i + 1}", position=random.choice(positions)
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
                status=random.choice(statuses),
            )
            tasks.append(task)

        # Создаем подзадачи (30% от общего количества)
        subtasks_count = count - root_tasks_count
        for i in range(subtasks_count):
            deadline = timezone.now() + timedelta(days=random.randint(1, 60))
            task = Task.objects.create(
                title=f"Подзадача {i + 1}",
                parent_task=random.choice(tasks),
                assignee=random.choice(employees),
                deadline=deadline,
                status=random.choice(statuses),
            )
            tasks.append(task)

        return tasks

    def generate_important_tasks(self, count):
        """
        Создает специальные подзадачи с assignee=None и parent_task в статусе IN_PROGRESS
        """
        # Найти родительские задачи в статусе IN_PROGRESS
        in_progress_parents = Task.objects.filter(
            parent_task__isnull=True, status=Task.Status.IN_PROGRESS
        )

        if not in_progress_parents.exists():
            # Если таких нет, создадим одну родительскую задачу вручную
            parent = Task.objects.create(
                title="Родительская задача для важных задач",
                status=Task.Status.IN_PROGRESS,
                deadline=timezone.now() + timedelta(days=30),
                assignee=None,
            )
            in_progress_parents = [parent]
        tasks = []
        for i in range(count):
            task = Task.objects.create(
                title=f"Важная подзадача {i + 1}",
                parent_task=random.choice(in_progress_parents),
                assignee=None,
                deadline=timezone.now() + timedelta(days=random.randint(1, 30)),
                status=Task.Status.NEW,
            )
            tasks.append(task)
        return tasks

    def handle(self, *args, **options):
        """
        Заполняет базу данных тестовыми данными:
        - 1000 сотрудников
        - 10000 задач
        - 50 важных подзадач
        """
        employees = self.generate_employees(1000)
        self.generate_tasks(10000, employees)
        self.generate_important_tasks(50)
        self.stdout.write(
            self.style.SUCCESS("База данных успешно заполнена тестовыми данными")
        )
