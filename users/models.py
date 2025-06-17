from django.db import models
class Employee(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    position = models.CharField("Должность", max_length=100)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    def __str__(self):
        return self.full_name