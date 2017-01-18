#!/bin/bash
clear
cd /nfs/vmware
python3 manage.py runserver 0.0.0.0:80
# you can check with fg
