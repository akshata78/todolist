from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name


class ToDo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)

	
	title = models.CharField(max_length=200)
	description = models.TextField()

	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	completed = models.BooleanField(default=False)
	due_date = models.DateField(null=True, blank=True)
	
	def __str__(self):
		return self.title
