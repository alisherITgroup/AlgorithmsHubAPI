from django.contrib.auth.models import User
from django.db import models
class CodeSubmission(models.Model):
    STATUS = [
        ("s", "success"),
        ("e", "error"),
        ("p", "pending")
    ]
    LANGUAGES = [
        ("py", "python"),
        ("cpp", "c++"),
        ("c", "c")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGES)
    user_input = models.TextField(null=True, blank=True)
    time = models.CharField(max_length=50, null=True, blank=True)
    output = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    date = models.DateTimeField(auto_now_add=True)
class MathSubmission(models.Model):
    STATUS = [
        ("s", "success"),
        ("e", "error"),
        ("p", "pending")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.TextField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    date = models.DateTimeField(auto_now_add=True)