from django.db.models import Count, Prefetch, Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks.models import Task
from users.models import Employee
from users.serializers import EmployeeSerializer, EmployeeWithTasksSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @swagger_auto_schema(
        operation_description="Получает список сотрудников, отсортированный по количеству активных задач",
        responses={200: EmployeeWithTasksSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def busy(self, request):
        active_statuses = ["new", "in_progress"]
        queryset = (
            Employee.objects.annotate(
                active_tasks_count=Count(
                    "tasks", filter=Q(tasks__status__in=active_statuses)
                )
            )
            .prefetch_related(
                Prefetch(
                    "tasks",
                    queryset=Task.objects.filter(status__in=active_statuses)
                    .only("id", "title", "status", "assignee_id"),
                    to_attr="prefetched_active_tasks",
                )
            )
            .order_by("-active_tasks_count")
        )
        serializer = EmployeeWithTasksSerializer(queryset, many=True)
        return Response(serializer.data)
