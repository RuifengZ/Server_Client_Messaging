# handling errors in python socket programs

import socket  # for sockets
import sys  # for exit
import select
import getpass


def get_reply(s):
    try:
        # receive data from client (data, addr)
        reply = s.recv(1024).decode()
        print(reply)
        return reply.decode()
    except socket.error:
        return None

try:
    # create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    sys.exit()

print('Socket Created')

host = 'localhost'
port = 2163

try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()

print('IP address of ' + host + ' is ' + remote_ip)

# Connect to remote sever
s.connect((remote_ip, port))
print('Socket Connected to ' + host + ' on ip ' + remote_ip)

s.setblocking(False)

# Now receive data
while 1:
    reply = get_reply(s)
    if reply == 'Logging Out...':
        break
    if reply == 'Password: ':
        uinput = getpass.getpass('')
        s.sendall(uinput.encode())
    elif reply != None:
        noInput = True
        while noInput:
            get_reply(s)
            uinput, w, x = select.select([sys.stdin], [], [], 1)
            if uinput:
                noInput = False
                uinput = sys.stdin.readline()
                s.sendall(uinput.encode())

s.close()

