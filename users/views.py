from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks import models
from tasks.models import Task
from users.models import Employee
from users.serializers import EmployeeWithTasksSerializer, EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    @action(detail=False, methods=["get"])
    def busy(self, request):
        queryset = Employee.objects.prefetch_related(
            models.Prefetch(
                'tasks',
                queryset=Task.objects.filter(
                    status__in=['new', 'in_progress']
                ).only('id', 'title', 'status'),
                to_attr='prefetched_active_tasks'
            )
        ).annotate(
            active_tasks_count=Count(
                "tasks", filter=Q(tasks__status__in=["new", "in_progress"])
            )
        ).order_by("-active_tasks_count")
        serializer = EmployeeWithTasksSerializer(queryset, many=True)
        return Response(serializer.data)
