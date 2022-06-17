import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    USER_ROLE = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN)
    )
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=25, choices=USER_ROLE, default=USER)
    confirmation_code = models.UUIDField(default=uuid.uuid4, editable=False)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
