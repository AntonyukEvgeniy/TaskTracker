from itertools import cycle

from django.db.models import Count, Q

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from tasks.models import Task
from tasks.serializers import TaskSerializer, ImportantTaskSerializer
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

    @swagger_auto_schema(
        operation_description="Получает список важных задач и предлагаемых исполнителей",
        responses={200: ImportantTaskSerializer(many=True)},
    )
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
        result = []
        for task in important_tasks:
            suggested_employees = [
                {
                    "id": emp.id,
                    "full_name": emp.full_name,
                    "position": emp.position,
                    "active_tasks_count": emp.active_tasks_count
                }
                for emp in employees[:3]  # Берем только 3-х наименее загруженных
            ]

            result.append({
                "title": task.title,
                "deadline": task.deadline,
                "suggested_employees": suggested_employees
            })
        serializer = ImportantTaskSerializer(data=result, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
