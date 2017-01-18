from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class server(models.Model):
    server_text = models.CharField(max_length=20)
    IP_addr = models.CharField(max_length=20)
    user = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    def __str__(self):
        return self.server_text

class vms(models.Model):
    server = models.ForeignKey(server, on_delete=models.CASCADE)
    vm_text = models.CharField(max_length=200)
    moid = models.IntegerField(default=0)
    def __str__(self):
        return self.vm_text