import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from projects.models import Project

User = get_user_model()


class Issue(models.Model):

    PRIORITY_CHOICES = (
        (1, "Trivial"),
        (2, "Minor"),
        (3, "Major"),
        (4, "Critical"),
        (5, "Blocker"),
    )
    TYPE_CHOICES = (
        (1, "Bug"),
        (2, "Enhancement"),
        (3, "Request"),
        (4, "Task"),
    )
    STATUS_CHOICES = (
        (1, "Open"),
        (2, "Development"),
        (3, "QA"),
        (4, "Closed"),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    type = models.IntegerField(choices=TYPE_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item-detail", kwargs={"pk": self.pk})

    def count_for_user(self, user):
        return self.objects.filter(user=user).count()
