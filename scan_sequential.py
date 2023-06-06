import socket
import sys
import time

argv = sys.argv
argc = len(argv)

if argc != 3:
    print("Usage: python scan_sequential.py $Hostname $portStart-portEnd")
    sys.exit(1)

host = argv[1]
portRange = argv[2]
portStart, portEnd = list(map(lambda x: int(x), portRange.split('-')))

startTime = time.time()
for i in range(portStart, portEnd):
    try:
        s = socket.create_connection((host, i))
        s.close()
        print(f"Port {i} is open: {socket.getservbyport(i)}.")
    except socket.error:
        print(f"Port {i} is closed.")
endTime = time.time()
print(f"Scanned {portEnd-portStart} ports in {'{:.2f}'.format(endTime-startTime)} seconds.")