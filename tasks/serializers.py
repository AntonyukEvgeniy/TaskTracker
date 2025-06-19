from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "parent_task",
            "assignee",
            "deadline",
            "status",
            "created_at",
            "updated_at",
        ]


class SuggestedEmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    position = serializers.CharField()
    active_tasks_count = serializers.IntegerField()


class ImportantTaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    deadline = serializers.DateTimeField()
    suggested_employees = SuggestedEmployeeSerializer(many=True)
