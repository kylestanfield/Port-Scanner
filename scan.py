import asyncio
import socket
import sys
import time

async def connectPort(host, port):
    coroutine = asyncio.open_connection(host, port)
    try:
        reader, writer = await asyncio.wait_for(coroutine, 2.0)
        writer.close()
        return True
    except asyncio.TimeoutError:
        return False

async def main():
    argv = sys.argv
    argc = len(argv)
    if argc != 3:
        print("Usage: python scan.py $Hostname $portStart-portEnd")
        sys.exit(1)

    host = argv[1]
    portRange = argv[2]
    portStart, portEnd = list(map(lambda x: int(x), portRange.split('-')))

    coroutines = [connectPort(host, p) for p in range(portStart, portEnd+1)]
    startTime = time.time()
    results = await asyncio.gather(*coroutines)
    endTime = time.time()

    for port, result in zip(range(portStart, portEnd), results):
        if result:
            print(f"Port {port}: {socket.getservbyport(port)} OPEN")
    print(f"Scanned {portEnd-portStart+1} ports in {'{:.2f}'.format(endTime-startTime)} seconds.")


if __name__ == "__main__":
    asyncio.run(main())