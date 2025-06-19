from rest_framework import serializers
from users.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "position", "created_at", "updated_at"]


class EmployeeWithTasksSerializer(serializers.ModelSerializer):
    active_tasks_count = serializers.IntegerField()
    active_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "full_name", "position", "active_tasks_count", "active_tasks"]

    def get_active_tasks(self, obj):
        return [
            {"id": task.id, "title": task.title, "status": task.status}
            for task in getattr(obj, "prefetched_active_tasks", [])
        ]
