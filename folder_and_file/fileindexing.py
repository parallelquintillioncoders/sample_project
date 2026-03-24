import os
import threading
import time
from collections import defaultdict
import heapq
import multiprocessing

# ================= CONFIG =================
CPU_COUNT = multiprocessing.cpu_count()
MAX_WORKERS = min(64, CPU_COUNT * 4)   # aggressive scaling
TOP_LARGEST_FILES = 20
REFRESH_INTERVAL = 1
# ==========================================

# Shared data
extension_count = defaultdict(int)
extension_size = defaultdict(int)

total_files = 0
total_folders = 0
total_size = 0

largest_files = []
lock = threading.Lock()

active_threads = 0
stop_flag = False

# ETA tracking
last_files = 0
last_time = time.time()
last_queue_size = 0


# ---------- FORMAT ----------
def format_size(size_bytes):
    units = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    size = float(size_bytes)
    i = 0
    while size >= 1024 and i < len(units)-1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}"


def format_time(seconds):
    if seconds < 0:
        return "estimating..."
    if seconds < 1:
        return "<1s"

    mins, sec = divmod(int(seconds), 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs}h {mins}m {sec}s"


# ---------- WORKER ----------
def worker(queue):
    global total_files, total_folders, total_size, active_threads

    while True:
        try:
            path = queue.pop()
        except IndexError:
            return

        with lock:
            active_threads += 1

        try:
            with os.scandir(path) as entries:
                subdirs = []

                for entry in entries:
                    try:
                        if entry.is_file(follow_symlinks=False):
                            ext = os.path.splitext(entry.name)[1].lower() or "NO_EXT"
                            size = entry.stat(follow_symlinks=False).st_size

                            with lock:
                                extension_count[ext] += 1
                                extension_size[ext] += size
                                total_files += 1
                                total_size += size

                                if len(largest_files) < TOP_LARGEST_FILES:
                                    heapq.heappush(largest_files, (size, entry.path))
                                else:
                                    heapq.heappushpop(largest_files, (size, entry.path))

                        elif entry.is_dir(follow_symlinks=False):
                            subdirs.append(entry.path)

                    except:
                        continue

                with lock:
                    total_folders += len(subdirs)

                queue.extend(subdirs)

        except:
            pass

        finally:
            with lock:
                active_threads -= 1


# ---------- PROGRESS ----------
def show_progress(start, queue):
    global last_files, last_time, last_queue_size

    while not stop_flag:
        time.sleep(REFRESH_INTERVAL)

        with lock:
            now = time.time()
            elapsed = now - start

            speed = total_files / elapsed if elapsed else 0

            # recent speed
            delta_files = total_files - last_files
            delta_time = now - last_time
            recent_speed = delta_files / delta_time if delta_time else 0

            last_files = total_files
            last_time = now

            # queue-based ETA
            current_queue = len(queue)
            queue_change = last_queue_size - current_queue
            last_queue_size = current_queue

            if queue_change > 0 and recent_speed > 0:
                eta = current_queue / (recent_speed + 1e-5)
            else:
                eta = -1

            print(
                f"\r🚀 Files: {total_files} | 📁 {total_folders} | "
                f"💾 {format_size(total_size)} | ⚡ {speed:.1f}/s | "
                f"🔥 Threads: {active_threads}/{MAX_WORKERS} | "
                f"📦 Queue: {current_queue} | "
                f"⏳ ETA: {format_time(eta)}",
                end="",
                flush=True
            )


# ---------- SCAN ----------
def scan(root):
    global stop_flag

    start = time.time()
    queue = [root]

    threading.Thread(target=show_progress, args=(start, queue), daemon=True).start()

    threads = []
    for _ in range(MAX_WORKERS):
        t = threading.Thread(target=worker, args=(queue,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    stop_flag = True
    time.sleep(0.2)

    return time.time() - start


# ---------- OUTPUT ----------
def print_summary(runtime):
    print("\n\n🎯 FINAL REPORT")
    print("="*60)
    print(f"📦 Total Files     : {total_files}")
    print(f"📁 Total Folders   : {total_folders}")
    print(f"💾 Total Size      : {format_size(total_size)}")
    print(f"⏱️ Completion Time : {format_time(runtime)}")


def print_ext_table():
    print("\n📊 STORAGE BREAKDOWN (Heavy Hitters)\n")
    print(f"{'Ext':<10}{'Files':<10}{'Size':<15}")
    print("-"*45)

    for ext, size in sorted(extension_size.items(), key=lambda x: -x[1]):
        print(f"{ext:<10}{extension_count[ext]:<10}{format_size(size):<15}")


def print_top_files():
    print("\n🔥 TOP SPACE CONSUMERS\n")
    for size, path in sorted(largest_files, reverse=True):
        print(f"{format_size(size):<12} {path}")


# ---------- MAIN ----------
if __name__ == "__main__":
    path = input("Enter path: ").strip()

    if not os.path.exists(path):
        print("❌ Invalid path")
        exit()

    print(f"\n🚀 Using {MAX_WORKERS} threads (max safe utilization)\n")

    runtime = scan(path)

    print_summary(runtime)
    print_ext_table()
    print_top_files()