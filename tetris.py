import sys
import threading as th
import queue as q
import time
import enum

clock = th.Event()
output_clock = th.Event()
stop_event = th.Event()
thread_list = []

class Block_Shapes(enum.Enum):
	FOUR_LONG = [
		[0, 1, 0, 0],
		[0, 1, 0, 0],
		[0, 1, 0, 0],
		[0, 1, 0, 0]
	]
	S_PIECE = [
		[0, 0, 0, 0],
		[0, 0, 1, 1],
		[0, 1, 1, 0],
		[0, 0, 0, 0]
	]
	Z_PIECE = [
		[0, 0, 0, 0],
		[1, 1, 0, 0],
		[0, 1, 1, 0],
		[0, 0, 0, 0]
	]
	T_PIECE = [
		[0, 0, 0, 0],
		[0, 1, 1, 1],
		[0, 0, 1, 0],
		[0, 0, 0, 0]
	]
	RIGHTY = [
		[0, 0, 0, 0],
		[0, 0, 0, 1],
		[0, 1, 1, 1],
		[0, 0, 0, 0]
	]
	LEFTY = [
		[0, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 1, 1, 1],
		[0, 0, 0, 0]
	]
	SQUARE = [
		[0, 0, 0, 0],
		[0, 1, 1, 0],
		[0, 1, 1, 0],
		[0, 0, 0, 0]
	]

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

def update_screen_worker(stop_event, output_clock, output_queue):
	len_old_screen = 0
	screen_buffer = None
	while not stop_event.is_set():
		if not screen_buffer:
			try:
				screen_buffer = output_queue.get(timeout=0.2)
				output_queue.task_done()
			except q.Empty:
				continue
		else:
			if output_clock.is_set():
				print("\033[F\033[2K" * len_old_screen, screen_buffer, sep="")
				len_old_screen = len(screen_buffer.split("\n"))
				screen_buffer = None
				output_clock.clear()

output_queue = q.Queue()

update_screen_thread = th.Thread(target=update_screen_worker, args=(stop_event, output_clock, output_queue))
update_screen_thread.start()
thread_list.append(update_screen_thread)

try:
	time.sleep(1.5)
	output_queue.put("Haii")
	output_clock.set()
	time.sleep(1.5)
	output_queue.put("67")
	output_clock.set()
except:
	pass
stop_event.set()
