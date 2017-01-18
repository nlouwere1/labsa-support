from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class server(models.Model):
    server_text = models.CharField(max_length=20)
    IP_addr = models.CharField(max_length=20)
    user = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    up = models.CharField(max_length=2)
    def __str__(self):
        return self.server_text

class vms(models.Model):
    server = models.ForeignKey(server, blank=True, null=True, on_delete=models.CASCADE)
    vm_text = models.CharField(max_length=200)
    moid = models.IntegerField(default=0)
    run = models.CharField(max_length=2,default="n")
    Guest = models.CharField(max_length=200,default="none")
    CPU = models.IntegerField(default=0)
    Mem = models.IntegerField(default=0)
    Ipa = models.CharField(max_length=200,default="none")
    def __str__(self):
        return self.vm_text



