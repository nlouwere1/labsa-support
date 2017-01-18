import atexit

from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import ssl
import re
import requests


sslContext = None
sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
sslContext.verify_mode = ssl.CERT_NONE
try:
        service_instance = connect.SmartConnect(host="vmw.nico",user="root",pwd="password",port=443,sslContext=sslContext)
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
            annotation = summary.config.annotation
            State = summary.runtime.powerState
            if summary.guest is not None:
                ip_address = summary.guest.ipAddress
                if ip_address:
                    IP = ip_address
                else:
                    IP = "none"
            print (Moid,Name,Guest,CPU,Mem,State,IP)
            print(child)
except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
