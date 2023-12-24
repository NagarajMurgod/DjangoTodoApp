from django.db import models
from todo.choices import StatusChoices
from django.contrib.auth import get_user_model


User = get_user_model()

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length = 255)
    description = models.TextField(default="")
    status = models.CharField(choices=StatusChoices.CHOICE_LIST, max_length=16)
    due_date = models.DateField(blank = True,null=True)
    due_time = models.TimeField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


