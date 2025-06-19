from itertools import cycle

from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks import serializers
from tasks.models import Task
from tasks.serializers import TaskSerializer
from users.models import Employee


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с задачами
    """

    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        assignee_id = self.request.query_params.get("assignee", None)
        if assignee_id is not None:
            queryset = queryset.filter(assignee_id=assignee_id)
        return queryset

    @action(detail=False, methods=["get"])
    def get_important_tasks_and_employees(self, request):
        # Находим важные задачи, которые:
        # 1. Не назначены
        # 2. Имеют родительские задачи в работе
        important_tasks = Task.objects.filter(
            assignee__isnull=True, parent_task__status=Task.Status.IN_PROGRESS
        ).order_by("deadline")

        # Находим наименее загруженных сотрудников
        employees = list(
            Employee.objects.annotate(
                active_tasks_count=Count(
                    "tasks", filter=Q(tasks__status=Task.Status.IN_PROGRESS)
                )
            ).order_by("active_tasks_count")
        )

        employee_cycle = cycle(employees)  # бесконечный итератор

        result = []
        for task in important_tasks:
            employee = next(employee_cycle)
            result.append(
                {
                    "task": task.title,
                    "deadline": task.deadline,
                    "suggested_employees": [employee.full_name],
                }
            )
        return Response(result)
