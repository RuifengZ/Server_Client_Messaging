# handling errors in python socket programs

import socket  # for sockets
import sys  # for exit
import getpass


def get_reply(s):
    reply = s.recv(1024)
    # print('Reply: ')
    print(reply.decode())
    return reply.decode()

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


# Now receive data
while 1:
    reply = get_reply(s)
    if reply == 'Logging Out...':
        break
    if reply == 'Password: ':
        uinput = getpass.getpass('')
    else:
        uinput = raw_input()
    s.sendall(uinput.encode())

s.close()


