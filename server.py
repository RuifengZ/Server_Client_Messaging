import socket
import sys
from thread import *

usernames = ['john123', 'mary23', 'wowe']
passwords = ['azsx123', 'password', 'wow123']

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 2163  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket Created')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code: ' + str(msg[0]) + 'Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

s.listen(1)
print('Socket now listening')


# keep talking with client

def clientthread(conn):
    #conn.send('Login to the server.\n\r'.encode())
    conn.send('Username: '.encode())
    while 1:
        # Listen for username and password
        reply = conn.recv(1024)
        # Check if username has been input and switch to password input if true
        nameinput = reply.strip().decode()

        conn.send('Password: '.encode())
        reply = conn.recv(1024)
        passinput = reply.strip().decode()
        if nameinput in usernames and passinput == passwords[usernames.index(nameinput)]:
            break
        else:
            conn.send('Invalid Username or Password \n\rUsername: '.encode())

    while 1:
        conn.send('Welcome to the server.\n\r 1) Message\n\r 2) Change Password\n\r 3) Logout\n\r'.encode())

        reply = conn.recv(1024)
        if '2'.encode() == reply.strip():
            conn.send('Enter New Password: '.encode())
            # Listen for new password
            reply = conn.recv(1024)
            # Change user password
            passwords[usernames.index(nameinput)] = reply.strip().decode()

        if '3'.encode() == reply.strip():
            conn.send('Logging Out...'.encode())
            connections.remove(conn)
            conn.close()
	    break;
    # if reply[:9] == '!sendall '.encode():
    #     reply = 'OK... '.encode() + reply[9:] + '\n'.encode()
    #     for c in connections:
    #         c.sendall(reply)


# list of all connections
connections = []
while 1:
    # wait to accept connection and display client information
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    connections.append(conn)
    # start new thread takes 1st argument as a function name to be run
    # second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))

# s.close()
