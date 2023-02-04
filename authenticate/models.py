from django.db import models


class Credential(models.Model):
    code = models.CharField(max_length=128)
    email = models.CharField(max_length=64, null=True)


class Machine(models.Model):
    machine_code = models.CharField(max_length=128)
    os = models.CharField(max_length=16)
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE, null=True)
    activated = models.BooleanField(default=False)
    first_login_time = models.DateTimeField('date published')
    activation_time = models.DateTimeField('date published', null=True)
