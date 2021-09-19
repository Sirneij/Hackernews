from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    # def get_absolute_url(self):
    #     return reverse("User_detail", kwargs={"pk": self.pk})

