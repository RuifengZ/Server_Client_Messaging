import socket
import sys
from thread import *

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.conn = None
        self.unread = []

    def changePass(self, newPass):
        self.password = newPass

    def setConn(self, conn):
        self.conn = conn

class Message:
    def __init__(self, sender, text):
        self.sender = sender
        self.text = text

accounts = [User('john123', 'azsx123'), User('mary23', 'password'), User('wowe', 'wow123')]
currentUser = 0

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

def send_msg(conn, user):
    conn.send(('To ' + user.username + ': ').encode())
    msg = conn.recv(1024) + '\n\r'.encode()
    if user.conn != None:
        user.conn.send(msg)
    else:
        user.unread.append(Message(accounts[currentUser].username, msg))

# keep talking with client
def clientthread(conn):
    #conn.send('Login to the server.\n\r'.encode())
    currentUser = None
    LoggedIn = False
    while LoggedIn == False:
        # Listen for username and password
        conn.send('Username: '.encode())
        reply = conn.recv(1024)
        nameinput = reply.strip().decode()
        conn.send('Password: '.encode())
        reply = conn.recv(1024)
        passinput = reply.strip().decode()
        # Check is username and password matches account
        for user in accounts:
            if nameinput == user.username and passinput == user.password:
                currentUser = accounts.index(user)
                accounts[currentUser].setConn(conn)
                LoggedIn = True
                break
        else:
            conn.send('Invalid Username or Password \n\r'.encode())

    while 1:
        conn.send(('\n\rWelcome to the server.\n\r 1) Message\n\r 2) Unread Messages:' + str(len(accounts[currentUser].unread)) + '\n\r 3) Broadcast Message\n\r 4) Change Password\n\r 5) Logout\n\r').encode())
        reply = conn.recv(1024)
        
        if '1'.encode() == reply.strip():
            msg_sent = False
            while msg_sent != True:
                conn.send('Who do you want to msg?: '.encode())
                sendTo = conn.recv(1024).strip().decode()
                for user in accounts:
                    if sendTo == user.username:
                        send_msg(conn, user)
                        msg_sent = True
                        break
                else:
                    conn.send('User does not exist.'.encode())

        if '2'.encode() == reply.strip():
            unreadMsgs = accounts[currentUser].unread
            sendUnread = ''
            for umsg in unreadMsgs:
                sendUnread += umsg.sender + ': ' + umsg.text.strip().decode() + '\n\r'
            conn.send(sendUnread.encode())
            conn.send('1) Back'.encode())
            while 1:
                if conn.recv(1024).strip() == '1'.encode():
                    break

        if '3'.encode() == reply.strip():
            conn.send('Broadcast Message: '.encode())
            bmsg = conn.recv(1024) + '\n\r'.encode()
            for aconn in connections:
                aconn.send(bmsg)

        if '4'.encode() == reply.strip():
            conn.send('!Enter New Password: '.encode())
            # Listen for new password
            reply = conn.recv(1024)
            # Change user password
            accounts[currentUser].changePass(reply.strip().decode())

        if '5'.encode() == reply.strip():
            conn.send('Logging Out...'.encode())
            connections.remove(conn)
            accounts[currentUser].setConn(None)
            conn.close()
            break

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
