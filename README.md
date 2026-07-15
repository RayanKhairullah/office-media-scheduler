# Office Media Scheduler Pro v1.0

![License](https://img.shields.io/badge/license-Open%20Source-green)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

A professional, lightweight, and automation-focused desktop application designed for managing scheduled audio/video announcements and media in environments like offices, schools, factories, or retail stores. Built with Python 3.10+ and Tkinter.

**Developed by:** [R4yan4k](https://github.com/RayanKhairullah)

---

## ✨ Key Features

### 🎵 Sound Management (Menu 1)
- Register, test-play, edit, and delete audio/video files with ease
- Support formats: MP3, WAV, MP4, AVI, MKV
- Automatically populates alias names based on selected filenames
- Intuitive library management interface

### 📅 Advanced Scheduling (Menu 2)
- Create multi-time schedules for any day of the week
- Support overlapping times and different songs at different times
- Advanced loop count settings (1x - 5x per trigger)
- **Copy Template** feature to duplicate schedules across days
- Automatic time format validation (HH:MM)

### 🖥️ Live Monitor (Menu 3)
- Digital clock with current date/day display
- **NTP Time Synchronization** - Always accurate time from internet
- Organized preview of today's active schedule
- Master toggle to activate/deactivate automation engine
- Real-time status indicators

### 🌐 NTP Time Synchronization ⭐ NEW!
- **Automatic internet time sync** - No dependency on PC CMOS battery
- Works even when system clock is wrong
- Auto-reconnect every 1 hour
- Fallback to local time if offline
- Clear indicator: `[NTP]` or `[Lokal]`

### ⚡ Auto-Start Engine ⭐ NEW!
- Engine automatically activates when program opens
- No manual button click needed
- Ready to run schedules immediately

### 🚀 Auto-Start on PC Boot ⭐ NEW!
- 2 installation methods available:
  - **Startup Folder** (easy, no admin required)
  - **Task Scheduler** (advanced, with delay options)
- One-click install/uninstall scripts
- Complete guide included

### 🎯 Smart Queueing Engine
- Uses internal Windows VBScript runner (`WMPlayer.OCX`)
- Perfect sequential loop queueing without audio overlap
- Non-blocking - GUI stays responsive
- Emergency stop with ESC key

### 🛡️ Security & Reliability
- Antivirus friendly - zero external binary dependencies
- Persistent storage via `scheduler_config.json`
- Thread-safe audio process management
- Extremely secure against Windows Defender false-positives

---

## 🛠️ System Requirements

- Windows OS (7 / 8 / 10 / 11)
- Windows Media Player component enabled
- Python 3.10+ (if running from source)
- Internet connection (recommended for NTP sync)

---

## 📦 Installation & Build

### 1. Clone Repository
```bash
git clone https://github.com/RayanKhairullah/scheduler_app.git
cd scheduler_app
```

### 2. Install PyInstaller
```bash
pip install pyinstaller
```

### 3. Build Executable
```bash
pyinstaller --clean --noconsole --onefile --icon=icon_logo.ico --add-data "icon_logo.ico;." scheduler_app.py
```

The `.exe` file will be available in `dist/` folder.

### 4. Run from Source (Optional)
```bash
python scheduler_app.py
```

---

## 🚀 Auto-Start Setup

### Quick Start
Run `AUTO_START_MENU.bat` for interactive menu.

### Method 1: Startup Folder (Recommended)
```
1. Run: install_autostart_startup.bat
2. Done! Program will auto-start on login
```

**Advantages:**
- ✅ No Administrator rights needed
- ✅ Easy install/uninstall
- ✅ User can disable via Task Manager

### Method 2: Task Scheduler (Advanced)
```
1. Right-click: install_autostart_taskscheduler.bat
2. Select: "Run as administrator"
3. Program will auto-start with 30s delay
```

**Advantages:**
- ✅ Startup delay (avoid bottleneck)
- ✅ Higher priority
- ✅ Detailed configuration via GUI

### Uninstall Auto-Start
- **Method 1:** Run `uninstall_autostart_startup.bat`
- **Method 2:** Run `uninstall_autostart_taskscheduler.bat` (as admin)

📖 See `AUTO_START_GUIDE.txt` for complete guide.

---

## 💡 How to Use

### Step 1: Add Media Files (Menu 1)
1. Click **"Browse"** to select audio/video file
2. Enter alias name (auto-filled from filename)
3. Click **"Simpan ke Library"**
4. Test play to preview

### Step 2: Create Schedule (Menu 2)
1. Select day from dropdown
2. Enter time (format: HH:MM)
3. Select sound from library
4. Set loop count (1x-5x)
5. Click **"+ Tambah ke Jadwal"**

**Additional Features:**
- Copy schedule to another day
- Delete selected schedule

### Step 3: Monitor & Control (Menu 3)
1. View real-time clock with NTP sync
2. Check engine status (auto-active)
3. See today's schedule list
4. Turn off engine if needed

### Emergency Stop
- Press `ESC` key anytime
- Or click **"MATIKAN ENGINE"** button

---

## 🔧 Troubleshooting

### ❓ Time Not Accurate
**Solution:** Program uses automatic NTP sync
- Ensure internet connection available
- If offline, program falls back to local time
- Check indicator: `[NTP]` or `[Lokal]` in clock display

### ❓ Program Not Auto-Starting
**For Startup Folder method:**
- Check Task Manager > Startup tab
- Ensure shortcut exists in Startup folder

**For Task Scheduler method:**
- Open Task Scheduler
- Look for "Office_Media_Scheduler_Pro" task
- Ensure .exe file hasn't been moved

### ❓ Schedule Not Playing
- Verify engine is active (check Menu 3)
- Check time format in schedule (HH:MM)
- Ensure sound exists in library
- Verify NTP time is synced

### ❓ CMOS Battery Issue
No problem! Program automatically syncs with internet time (NTP), so PC clock accuracy doesn't matter.

---

## 📂 File Structure

```
scheduler_app/
├── scheduler_app.py                      # Main source code
├── scheduler_app.exe                     # Executable (after build)
├── scheduler_config.json                 # Library & schedule data
├── icon_logo.ico                         # Application icon
├── README.md                             # This file
│
├── AUTO_START_MENU.bat                   # Interactive installer menu
├── install_autostart_startup.bat         # Method 1 installer
├── uninstall_autostart_startup.bat       # Method 1 uninstaller
├── install_autostart_taskscheduler.bat   # Method 2 installer (admin)
├── uninstall_autostart_taskscheduler.bat # Method 2 uninstaller (admin)
└── AUTO_START_GUIDE.txt                  # Complete setup guide
```

---

## 🛡️ License

Open Source - Free to use and modify

---

## 👨‍💻 Developer

**R4yan4k**  
GitHub: [github.com/RayanKhairullah](https://github.com/RayanKhairullah)

---

## 🆕 Changelog

### v1.0 (Latest - 2024)
- ✅ **NTP Time Synchronization** - Internet time sync (solve CMOS battery issue)
- ✅ **Auto-start engine** on program launch
- ✅ **Auto-start on PC boot** (2 methods with installer scripts)
- ✅ **Automatic time format validation** (HH:MM)
- ✅ Interactive installer menu
- ✅ Complete setup guides
- ✅ Interface improvements
- ✅ Bug fixes & optimization
- ✅ Thread-safe audio process management

### v0.9 (Initial Release)
- Basic sound library management
- Multi-day scheduling system
- Live monitor with digital clock
- VBScript-based audio player
- Template copy feature

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## ⭐ Support

If this application is useful for you, please give it a star on GitHub!

**Found a bug?** Open an issue on GitHub repository.

---

## 📞 Contact

For questions or support:
- GitHub: [github.com/RayanKhairullah](https://github.com/RayanKhairullah)
- Open an issue in the repository

---

**Made with ❤️ by R4yan4k**
