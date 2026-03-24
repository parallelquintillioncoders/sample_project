# 🚀 High Performance File System Scanner

A fast, multithreaded Python tool to analyze directories with **real-time insights**, **size breakdowns**, and **parallel processing**.

---

## ⚡ Features

* 🔥 **Aggressive Multithreading**

  * Uses up to `CPU × 4` threads (auto-scaled)
* 📊 **Live Progress Dashboard**

  * Files processed
  * Folder count
  * Total size
  * Processing speed (files/sec)
  * Active threads
  * Queue depth
  * ETA (adaptive)
* 💾 **Accurate Size Analysis**

  * Per-extension size aggregation
  * Supports massive sizes (KB → YB)
* 🧠 **Smart ETA Calculation**

  * Based on real queue drain + speed
* 🏁 **Completion Metrics**

  * Total runtime
* 🔍 **Top Largest Files**

  * Heap-based (memory efficient)

---

## 🧠 Why This Tool Exists

Most file scanners:

* Lie about progress ❌
* Freeze UI ❌
* Use fixed threads ❌

This tool:

* Shows **real-time system behavior**
* Maximizes **safe parallelism**
* Gives **actionable storage insights**

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/file-scanner.git
cd file-scanner
python scanner.py
```

> No external dependencies required (pure Python)

---

## ▶️ Usage

```bash
python scanner.py
```

Then enter the directory path:

```
Enter path: /your/folder/path
```

---

## 📊 Sample Output

```
🚀 Files: 12450 | 📁 2300 | 💾 15.6 GB | ⚡ 850.2/s
🔥 Threads: 16/32 | 📦 Queue: 120 | ⏳ ETA: 0h 2m 10s
```

### Final Report

```
🎯 FINAL REPORT
============================================================
📦 Total Files     : 45231
📁 Total Folders   : 8123
💾 Total Size      : 120.45 GB
⏱️ Completion Time : 0h 3m 42s
```

---

## 📊 Extension Breakdown

```
Ext        Files      Size
---------------------------------------------
.mp4       120        80.5 GB
.jpg       5400       15.2 GB
.log       12000      10.1 GB
```

---

## 🔥 Top Space Consumers

```
12.5 GB     /videos/movie1.mp4
8.2 GB      /backup/archive.zip
```

---

## ⚙️ Configuration

Modify inside the script:

```python
MAX_WORKERS = min(64, CPU_COUNT * 4)
TOP_LARGEST_FILES = 20
REFRESH_INTERVAL = 1
```

---

## ⚠️ Performance Reality

* SSD → 🚀 Fast scaling
* HDD → ⚠️ Limited by disk speed
* Millions of files → ⏳ Time-consuming

> More threads ≠ always faster (I/O bottleneck)

---

## 🧩 Limitations

* ETA is **approximate**, not exact
* No duplicate detection (yet)
* No GUI (CLI only)

---

## 💡 Future Improvements

* CSV / JSON export
* Duplicate file detection
* Interactive CLI filters
* GUI dashboard (like WinDirStat)
* Rust-based ultra-fast version

---

## 🧠 Tech Stack

* Python 3
* `os.scandir()` for fast filesystem access
* `threading` for parallelism
* `heapq` for memory-efficient top files

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built for performance-focused filesystem analysis.

---

## 💬 Final Thought

This isn’t just a scanner —
it’s a **visibility tool for your storage reality**.
