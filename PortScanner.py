import socket
import threading
import argparse
import errno
from queue import Queue

open_ports = []
lock = threading.Lock()

def scan_port(target, port, timeout, grab_banner):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        result = s.connect_ex((target, port))

        if result == 0:
            banner = ""
            if grab_banner:
                try:
                    s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = s.recv(1024).decode(errors="ignore").strip()
                except:
                    banner = "No banner"

            with lock:
                open_ports.append((port, banner))
                print(f"[OPEN] {port} | {banner}")

        elif result == errno.ECONNREFUSED:
            pass
        else:
            pass

        s.close()

    except Exception:
        pass


def worker(queue, target, timeout, grab_banner):
    while not queue.empty():
        port = queue.get()
        scan_port(target, port, timeout, grab_banner)
        queue.task_done()


def main():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Threads")
    parser.add_argument("--timeout", type=float, default=1, help="Timeout")
    parser.add_argument("--banner", action="store_true", help="Banner grabbing")

    args = parser.parse_args()

    target = socket.gethostbyname(args.target)
    start_port, end_port = map(int, args.ports.split("-"))

    print(f"\nScanning {target} from port {start_port} to {end_port}\n")

    queue = Queue()

    for port in range(start_port, end_port + 1):
        queue.put(port)

    threads = []

    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(queue, target, args.timeout, args.banner))
        t.daemon = True
        t.start()
        threads.append(t)

    queue.join()

    print("\nScan complete.\n")
    print("Open ports:")

    for port, banner in sorted(open_ports):
        print(f"{port} | {banner}")


if __name__ == "__main__":
    main()
