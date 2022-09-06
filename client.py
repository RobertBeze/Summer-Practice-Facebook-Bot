import sys, socket
import echo_util
from facebook import *
from facebook_funcs import *


HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = echo_util.PORT

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))  #connect to server
        print("here")
    except ConnectionError:
        print('Socket error on connection')
        sys.exit(1)

    print('\nConnected to {}:{}'.format(HOST, PORT))
    o = main_menu()
    echo_util.send_msg(sock,str(o))
  #  print("Closing connection")
    sock.close()

