import echo_util
import threading
import urllib3
import facebook
import requests
import facebook_funcs

HOST = echo_util.HOST
PORT = echo_util.PORT
TOKEN = facebook_funcs.TOKEN


def handle_client(sock, addr): #modificat a.i sa putem lua id si alte comenzi din client.py
    """ Receive data from the client via sock and echo it back """
    while True:
        try:
            msg = echo_util.recv_msg(sock) # Blocks until received
            # complete message
            print('{}: {}'.format(addr, msg))
            #opt = int(msg)
            if int(msg) == 1:
                facebook_funcs.get_all_posts(TOKEN)
                msg = ''
            elif int(msg) == 2:
                msg = ''
                for friend in facebook_funcs.get_albums(TOKEN):
                    msg += friend 
                print(msg)
            elif int(msg) == 3:
                msg = facebook_funcs.get_basic_data(TOKEN)
                print(msg)
            elif int(msg) == 4:
                facebook_funcs.get_posts_by_date(TOKEN)
            elif int(msg) == 5:
                print(facebook_funcs.get_number_of_friends(TOKEN))
            elif int(msg) == 6:
                facebook_funcs.get_languages(TOKEN)
            else:
                print('Wrong option. If you want to quit, press CTRL+C, or select a new option.')
          #  print(msg)
            #echo_util.send_msg(sock, msg) # Blocks until sent
        except (ConnectionError, BrokenPipeError):
            print('Closed connection to {}'.format(addr))
            sock.close()
            break


if __name__ == '__main__':
    listen_sock = echo_util.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))

    while True:
        client_sock, addr = listen_sock.accept()
        # Thread will run function handle_client() autonomously
        # and concurrently to this while loop
        thread = threading.Thread(target = handle_client, args = [client_sock, addr], daemon=True)
        thread.start()
        print('Connection from {}'.format(addr))
