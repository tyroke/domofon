import socket
import atexit

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 10001))


def end_connection():
    s.send(bytes("q;", "utf-8"))
    print("wysłano")

atexit.register(end_connection)
while True:
    d = input("wyslij dane") + ";"
    s.send(bytes(d, "utf-8"))
    if d == "q;":
        break



