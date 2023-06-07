import asyncio
import socket
import sys
import time

async def connectPort(host, port):
    coroutine = asyncio.open_connection(host, port)
    try:
        _, writer = await asyncio.wait_for(coroutine, 2.0)
        writer.close()
        return True
    except asyncio.TimeoutError:
        return False

async def worker(host, queue):
    while True:
        port = await queue.get()
        if port is None:
            queue.task_done()
            return
        if await connectPort(host, port):
            print(f"Port {port}: {socket.getservbyport(port)} OPEN")
        queue.task_done()

async def main():
    argv = sys.argv
    argc = len(argv)
    if argc < 3 or argc > 4:
        print("Usage: python scan.py $Hostname $portStart-portEnd [$WORKERS]")
        sys.exit(1)

    host = argv[1]
    portRange = argv[2]
    portStart, portEnd = list(map(lambda x: int(x), portRange.split('-')))
    workerLimit = 256
    if argc == 4:
        workerLimit = int(argv[3])

    queue = asyncio.Queue()
    startTime = time.time()

    workers = [asyncio.create_task(worker(host, queue)) for _ in range(workerLimit)]
    for port in range(portStart, portEnd+1):
        await queue.put(port)
    for _ in range(workerLimit):
        await queue.put(None)
    await queue.join()
    
    endTime = time.time()
    print(f"Scanned {portEnd-portStart+1} ports in {'{:.2f}'.format(endTime-startTime)} seconds.")


if __name__ == "__main__":
    asyncio.run(main())