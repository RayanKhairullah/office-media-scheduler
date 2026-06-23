# Office Media Scheduler Pro v1 

A professional, lightweight, and automation-focused desktop application designed for managing scheduled audio/video announcements and media in environments like offices, schools, factories, or retail stores. Built with Python 3.14+ and Tkinter.

## 🌟 Key Features

- **Menu 1: Sound Management (Library):** Register, test-play, edit, and delete audio/video files with ease. Automatically populates alias names based on selected filenames.
- **Menu 2: Advanced Scheduling:** Create multi-time schedules for any day of the week. Supports overlapping times, different songs at different times, and advanced loop count settings. Includes a powerful **Copy Template** feature to duplicate a day's schedule to another day instantly.
- **Menu 3: Live Monitor:** Displays a digital clock with the current date/day and an organized preview of today's active schedule. Includes a master toggle to instantly activate or deactivate the automation engine.
- **Smart Queueing Engine:** Uses an internal Windows VBScript runner (`WMPlayer.OCX`) that perfectly queues loop repeats sequentially without audio overlapping or freezing the GUI.
- **Antivirus Friendly:** Zero external binary dependencies. Extremely secure against Windows Defender false-positives.
- **Persistent Storage:** Automations are safely saved to a local `scheduler_config.json` file.

## 🛠️ System Requirements
- Windows OS (7 / 8 / 10 / 11) with Windows Media Player component enabled.
- Python 3.10 to 3.14+ (if running from source code).

## 🚀 Installation & Running

1. Clone the repository:
   ```bash
   git clone https://github.com/RayanKhairullah/office-media-scheduler.git
   cd office-media-scheduler
   ```
2. Place your custom application icon named `icon_logo.ico` in the root directory.
3. Install tools untuk compile
   ```bash
   pip install pyinstaller
4. Run the application:
   ```bash
   python scheduler_app.py
## Jalankan perintah build dengan icon kustom Anda
   ```bash
   pyinstaller --clean --noconsole --onefile --icon=icon_logo.ico --add-data "icon_logo.ico;." scheduler_app.py