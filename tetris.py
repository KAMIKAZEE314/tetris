import sys
import threading as th
import queue as q

stop_event = th.Event()
thread_list = []

if sys.platform.startswith("win"):
    import msvcrt
    def read_char():
        return msvcrt.getch().decode("utf-8", errors="ignore")
else:
    import tty
    import termios
    def read_char():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def update_screen_worker(stop_event, output_queue):
	while not stop_event.is_set():
		try:
			screen_buffer = output_queue.get(timeout=0.2)
		except q.Empty:
			continue

output_queue = q.Queue()

update_screen_thread = th.Thread(target=update_screen_worker, args=(stop_event, output_queue))
update_screen_thread.start()
thread_list.append(update_screen_thread)

try:
	while True:
		pass
except:
	pass
stop_event.set()
