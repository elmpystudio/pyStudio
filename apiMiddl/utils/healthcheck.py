import socket
from termcolor import colored as c
from django.conf import settings

# TODO

def check_port_if_listening(ip, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.settimeout(3)
    location = (ip, port) 
    result_of_check = a_socket.connect_ex(location) 
    return result_of_check == 0

def healthcheck():

    # minio
    if not check_port_if_listening(settings.MINIO_SERVER["IP"], settings.MINIO_SERVER["PORT"]): 
        msg = "Minio : couldn't connect to server on %s:%d, check if docker container is up!" % (ip, port)
        print( c("[-]", 'red') + " " + msg  )
    else:
        msg = "Minio : OK" 
        print( c("[+]", 'green') + " " + msg  )

    # tableau server
    location = (ip, port)= settings.TABLEAU_SERVER.split("//")[1].split(":")
    if not check_port_if_listening(location): 
        msg = "Tableau: couldn't connect to server on %s:%d!" % location
        print( c("[-]", 'red') + " " + msg  )
    else:
        msg = "Tableu: OK" 
        print( c("[+]", 'green') + " " + msg  )



healthcheck()
