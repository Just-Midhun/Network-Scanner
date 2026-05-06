# Python Network Scanner (From Scratch)

## 1. Overview

I’m building a basic network scanner from scratch in Python to understand how connections, sockets, and networking behave at a lower level.

Instead of jumping straight to tools like `nmap`, I wanted to recreate core concepts manually. This includes connection handling, threading, race conditions, and basic service detection.

This is Version 1, focused on single target IP scanning.

---

## 2. Version 1 Features

* Scan a single IP address
* Custom port range scanning (`-p 1-1024`)
* Multithreading for speed (`-t 100`)
* Queue-based task distribution
* Banner grabbing (`--banner`) to identify services

---

## 3. Concepts Implemented

### 3.1 Threading

* Used Python threading to speed up scanning
* Multiple port checks run concurrently

### 3.2 Queue (Critical Section Handling)

* Thread-safe queue for task distribution
* Prevents race conditions
* Maintains clean concurrency between threads

### 3.3 Socket Programming

* TCP connect scans
* Attempt connection, check response, classify port state

### 3.4 Banner Grabbing

* Reads initial response from open ports
* Helps identify running services

---

## 4. Lab Setup

### Initial Issue

Bridge networking did not work for scanning.

### Fix

* Switched VM to host-only network
* Created a private network between host and VM

This allowed consistent communication for testing.

---

## 5. Usage

```bash
python PortScanner.py 192.168.158.133 -p 1-1024 -t 100 --banner
```

---

## 6. Sample Output

```
Scanning 192.168.158.133 from port 1 to 1024

[OPEN] 80 | HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.13.9
Date: Wed, 06 May 2026 11:18:36 GMT
Content-type: text/html; charset=utf-8
Content-Length: 1936

Scan complete.

Open ports:
80 | HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.13.9
Date: Wed, 06 May 2026 11:18:36 GMT
Content-type: text/html; charset=utf-8
Content-Length: 1936
```

---

## 7. Test Service

Ran a simple HTTP server on the target VM:

```bash
python3 -m http.server 80
```

Results:

* Detected port 80 as open
* Captured HTTP response headers
* Identified server as SimpleHTTP/0.6

---

## 8. What I Learned

* Threading is useful for I/O-heavy tasks
* Race conditions appear even in simple tools
* Networking issues are often environment-related
* Banner grabbing depends on service behavior
* VM networking modes affect connectivity significantly

---

## 9. Limitations (Version 1)

* Single IP only
* TCP connect scan only
* No timeout tuning
* No UDP scanning
* No OS fingerprinting

---

## 10. Next Steps (Version 2 and beyond)

* [ ] CIDR or subnet scanning
* [ ] UDP scan support
* [ ] Timeout and retry tuning
* [ ] Service fingerprinting
* [ ] Output formats like JSON
* [ ] Improved CLI

---

## 11. Note

This project is for educational purposes only.
Only scan systems you own or have permission to test.

