#vms/views.py
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import server, vms
from django.template import loader
from django.http import Http404
import time
import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import ssl
import re
import socket
#from .models import vms


def index(request):
    latest_server_list = server.objects.order_by('server_text')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for server1 in latest_server_list:
    	result = s.connect_ex((server1.IP_addr, 8000))
    	if result == 0: #server is listning
    		server1.up='y'
    	else:
    		server1.up='n'
    	server1.save()
    	s.close
    	
    context = {'latest_server_list': latest_server_list}
    return render(request, 'vms/index.html', context)

def detail(request, server_id):
    server1 = get_object_or_404(server, pk=server_id)
    
    
    vms.objects.filter(server=server1).delete()
    
    sslContext = None
    sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslContext.verify_mode = ssl.CERT_NONE
    try:
        service_instance = connect.SmartConnect(host=server1.IP_addr,user=server1.user,pwd=server1.passwd,port=443,sslContext=sslContext)
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        container = content.rootFolder  # starting point to look into
        viewType = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)

        children = containerView.view
        for child in children:
            summary = child.summary
            Moid = int(re.search(r'\d+', str(child)).group())
            Name = summary.config.name
            Guest = summary.config.guestFullName
            CPU = summary.config.numCpu
            Mem = summary.config.memorySizeMB // 1024
            run = summary.runtime.powerState
            if run == "poweredOn":
                run = "y"
            else:
                run = "n"
            #Uuid = summary.config.instanceUuid
            if summary.guest is not None:
                ip_address = summary.guest.ipAddress
                if ip_address:
                    Ipa = ip_address
                else:
                    Ipa = "none"
            server1.vms_set.create(vm_text=Name,moid=Moid,Guest=Guest,CPU=CPU,Mem=Mem,Ipa=Ipa,run=run)
    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)


    return render(request, 'vms/detail.html', {'server': server1})

def refresh(request, server_id):

    server1 = get_object_or_404(server, pk=server_id)
   
    
    vms.objects.filter(server=server1).delete()
    
    sslContext = None
    sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslContext.verify_mode = ssl.CERT_NONE
    try:
        service_instance = connect.SmartConnect(host=server1.IP_addr,user=server1.user,pwd=server1.passwd,port=443,sslContext=sslContext)
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        container = content.rootFolder  # starting point to look into
        viewType = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)

        children = containerView.view
        for child in children:
            summary = child.summary
            Moid = int(re.search(r'\d+', str(child)).group())
            Name = summary.config.name
            Guest = summary.config.guestFullName
            CPU = summary.config.numCpu
            Mem = summary.config.memorySizeMB // 1024
            run = summary.runtime.powerState
            if run == "poweredOn":
                run = "y"
            else:
                run = "n"
            #Uuid = summary.config.instanceUuid
            if summary.guest is not None:
                ip_address = summary.guest.ipAddress
                if ip_address:
                    Ipa = ip_address
                else:
                    Ipa = "none"
            server1.vms_set.create(vm_text=Name,moid=Moid,Guest=Guest,CPU=CPU,Mem=Mem,Ipa=Ipa,run=run)
    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)





    return HttpResponse("server ip %s. is done" % server1.IP_addr)
    
    

def vote(request, server_id):
    return HttpResponse("You're voting on server %s." % server_id)
# Create your views here.
