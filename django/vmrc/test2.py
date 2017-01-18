import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = s.connect_ex((127.0.0.1, 8000))

if result == 0:
    print('socket is open')
else:
    print('socket is cklosed')
s.close()
