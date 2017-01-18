#vms/views.py
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import server, vms
from django.template import loader
from django.http import Http404
import time
from pexpect import pxssh
import re
#from .models import vms


def index(request):
    latest_server_list = server.objects.order_by('server_text')
    context = {'latest_server_list': latest_server_list}
    return render(request, 'vms/index.html', context)

def detail(request, server_id):
    server1 = get_object_or_404(server, pk=server_id)
    return render(request, 'vms/detail.html', {'server': server1})

def refresh(request, server_id):

    server1 = get_object_or_404(server, pk=server_id)
    s = pxssh.pxssh()
    entry_list = list(server1.vms_set.all())
    for e in server1.vms_set.all()
    	e.delete()
    if not s.login (server1.IP_addr, server1.user, server1.passwd):
       return render(request, 'vms/death.html', {'server': server1})
    else:
        s.sendline ('vim-cmd vmsvc/getallvms')
        s.prompt()         # match the prompt
        allvmss=s.before.decode('utf-8')     # print everything before the prompt.
        s.logout()
        x=0
        xs=re.sub(' +',' ',allvmss)
        xs1 = re.split("[\r\n]", xs)
        for c in xs1:
           vm=xs1[x].split(" ")
           if vm[0].isdigit():
             server1.vms_set.create(vm_text=vm[1],moid=vm[0])
           x=x+1





    return HttpResponse("server ip%s. is aan het einde" % server1.IP_addr)
    
    

def vote(request, server_id):
    return HttpResponse("You're voting on server %s." % server_id)
# Create your views here.
