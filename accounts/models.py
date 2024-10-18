from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(Role, related_name="users", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_role(self, role_name):
        """
        Check if the user has a specific role.
        """
        return self.roles.filter(name=role_name).exists()

    def assign_role(self, role_name):
        """
        Dynamically assign a role to the user.
        """
        role, created = Role.objects.get_or_create(name=role_name)
        self.roles.add(role)

    def remove_role(self, role_name):
        """
        Remove a role from the user.
        """
        role = Role.objects.filter(name=role_name).first()
        if role:
            self.roles.remove(role)




'''
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    """
    Role model to represent user roles dynamically (e.g., Moderator, Data Collector).
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """
    Custom User model with dynamic roles.
    """
    roles = models.ManyToManyField(Role, related_name="users")  # Many-to-many relationship with roles

    def has_role(self, role_name):
        """
        Check if the user has a specific role.
        """
        return self.roles.filter(name=role_name).exists()

    def assign_role(self, role_name):
        """
        Dynamically assign a role to the user.
        """
        role, created = Role.objects.get_or_create(name=role_name)
        self.roles.add(role)

    def remove_role(self, role_name):
        """
        Remove a role from the user.
        """
        role = Role.objects.filter(name=role_name).first()
        if role:
            self.roles.remove(role)

'''
