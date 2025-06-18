from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        COMPLETED = "completed", "Завершена"
        CANCELED = "canceled", "Отменена"

    title = models.CharField("Наименование", max_length=255)
    parent_task = models.ForeignKey(
        "self",
        verbose_name="Родительская задача",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subtasks",
    )
    assignee = models.ForeignKey(
        "users.Employee",
        verbose_name="Исполнитель",
        on_delete=models.PROTECT,
        related_name="tasks",
    )
    deadline = models.DateTimeField("Срок выполнения")
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        indexes = [
            models.Index(fields=['status', 'assignee']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title
