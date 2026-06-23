# =====================================================================
#  PROJECT: Office Media Scheduler Pro v1
#  AUTHOR: R4yan4k
#  GITHUB: https://github.com/RayanKhairullah
#  LICENSE: Open Source
# =====================================================================

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
from datetime import datetime
import os
import json
import tempfile
import sys
import subprocess

class AdvancedOfficeScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Office Media Scheduler Pro v1.0 - Developed by R4yan4k")
        self.root.geometry("750x620")
        
        # --- KUSTOMISASI IKON WINDOWS & TASKBAR ---
        # Handle path icon untuk Python script maupun PyInstaller .exe
        if getattr(sys, 'frozen', False):
            # Jika dikompilasi dengan PyInstaller
            base_path = sys._MEIPASS
        else:
            # Jika dijalankan sebagai script Python
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.icon_name = os.path.join(base_path, "icon_logo.ico")
        try:
            if os.path.exists(self.icon_name):
                self.root.iconbitmap(self.icon_name)
        except Exception:
            pass
        
        self.config_file = "scheduler_config.json"
        self.media_library = {}
        self.schedules = {day: [] for day in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]}
        
        self.load_data()
        self.is_running = False
        
        self.setup_ui()
        self.start_global_clock()

    def load_data(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.media_library = data.get("library", {})
                    self.schedules = data.get("schedules", {day: [] for day in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]})
            except Exception:
                pass

    def save_data(self):
        with open(self.config_file, "w") as f:
            json.dump({"library": self.media_library, "schedules": self.schedules}, f, indent=4)

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text=" Menu 1: Manajemen Sound ")
        self.notebook.add(self.tab2, text=" Menu 2: Penjadwalan ")
        self.notebook.add(self.tab3, text=" Menu 3: Monitor ")

        self.build_tab1_management()
        self.build_tab2_schedule()
        self.build_tab3_monitor()
        
        license_lbl = tk.Label(self.root, text="Developed by R4yan4k | GitHub: github.com/RayanKhairullah", fg="gray", font=("Arial", 8))
        license_lbl.pack(side="bottom", pady=4)

    def build_tab1_management(self):
        # Memperbaiki frame menggunakan padx/pady standar Tkinter (Menghilangkan error padding)
        input_frame = tk.LabelFrame(self.tab1, text=" Tambah / Edit Sound ", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Nama Alias Sound:").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_sound_name = tk.Entry(input_frame, width=40)
        self.ent_sound_name.grid(row=0, column=1, pady=2, padx=5, sticky="w")

        tk.Label(input_frame, text="File Path:").grid(row=1, column=0, sticky="w", pady=2)
        self.lbl_file_path = tk.Label(input_frame, text="Belum ada file dipilih...", fg="gray", anchor="w", width=50, relief="sunken", bg="white")
        self.lbl_file_path.grid(row=1, column=1, pady=2, padx=5, sticky="w")
        
        tk.Button(input_frame, text="Browse", command=self.browse_library_file).grid(row=1, column=2, padx=5)
        tk.Button(input_frame, text="Simpan ke Library", bg="#4CAF50", fg="white", command=self.save_to_library).grid(row=2, column=1, columnspan=2, sticky="e", pady=5)

        list_frame = tk.LabelFrame(self.tab1, text=" Daftar Library Sound ", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.lib_listbox = tk.Listbox(list_frame, height=12)
        self.lib_listbox.pack(side="left", fill="both", expand=True)
        self.lib_listbox.bind("<<ListboxSelect>>", self.on_select_library)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.lib_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.lib_listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(self.tab1)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(btn_frame, text="Hapus Berkas Terpilih", bg="#F44336", fg="white", command=self.delete_from_library).pack(side="right", padx=5)
        tk.Button(btn_frame, text="Test Play", bg="#FF9800", fg="white", command=self.test_play_library).pack(side="right", padx=5)

        self.update_library_listbox()

    def browse_library_file(self):
        file_selected = filedialog.askopenfilename(
            title="Pilih Berkas Suara/Video", 
            filetypes=[("Media Files", "*.mp3 *.wav *.mp4 *.avi *.mkv"), ("All Files", "*.*")]
        )
        if file_selected:
            self.lbl_file_path.config(text=file_selected, fg="black")
            base_name = os.path.basename(file_selected) 
            name_without_ext = os.path.splitext(base_name)[0] 
            self.ent_sound_name.delete(0, tk.END)
            self.ent_sound_name.insert(0, name_without_ext)

    def save_to_library(self):
        name = self.ent_sound_name.get().strip()
        path = self.lbl_file_path.cget("text")
        if not name or path == "Belum ada file dipilih...":
            messagebox.showwarning("Peringatan", "Nama alias dan File Path harus diisi!")
            return
        self.media_library[name] = path
        self.save_data()
        self.update_library_listbox()
        self.update_schedule_dropdowns()
        self.ent_sound_name.delete(0, tk.END)
        self.lbl_file_path.config(text="Belum ada file dipilih...", fg="gray")
        messagebox.showinfo("Sukses", f"Sound '{name}' berhasil disimpan.")

    def update_library_listbox(self):
        self.lib_listbox.delete(0, tk.END)
        for name in sorted(self.media_library.keys()):
            self.lib_listbox.insert(tk.END, f"{name}  ->  ({self.media_library[name]})")

    def on_select_library(self, event):
        if not self.lib_listbox.curselection(): return
        index = self.lib_listbox.curselection()[0]
        selected_text = self.lib_listbox.get(index)
        name = selected_text.split("  ->  ")[0]
        self.ent_sound_name.delete(0, tk.END)
        self.ent_sound_name.insert(0, name)
        self.lbl_file_path.config(text=self.media_library[name], fg="black")

    def delete_from_library(self):
        if not self.lib_listbox.curselection(): return
        index = self.lib_listbox.curselection()[0]
        name = self.lib_listbox.get(index).split("  ->  ")[0]
        if messagebox.askyesno("Konfirmasi", f"Hapus '{name}' dari library?"):
            del self.media_library[name]
            for day in self.schedules:
                self.schedules[day] = [item for item in self.schedules[day] if item["sound"] != name]
            self.save_data()
            self.update_library_listbox()
            self.update_schedule_dropdowns()
            self.update_schedule_listbox()

    def test_play_library(self):
        if not self.lib_listbox.curselection(): return
        name = self.lib_listbox.get(self.lib_listbox.curselection()[0]).split("  ->  ")[0]
        t = threading.Thread(target=self.play_sound_via_vbs, args=(self.media_library[name], 1, True), daemon=True)
        t.start()

    def build_tab2_schedule(self):
        top_frame = tk.Frame(self.tab2, pady=5)
        top_frame.pack(fill="x", padx=10)
        
        tk.Label(top_frame, text="Pilih Hari:", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.cb_day_select = ttk.Combobox(top_frame, values=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], width=12, state="readonly")
        self.cb_day_select.set("Senin")
        self.cb_day_select.pack(side="left", padx=5)
        self.cb_day_select.bind("<<ComboboxSelected>>", lambda e: self.update_schedule_listbox())

        tk.Label(top_frame, text=" | Copy Template ke:").pack(side="left", padx=5)
        self.cb_target_day = ttk.Combobox(top_frame, values=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], width=12, state="readonly")
        self.cb_target_day.set("Selasa")
        self.cb_target_day.pack(side="left", padx=5)
        tk.Button(top_frame, text="Copy Jadwal", bg="#2196F3", fg="white", command=self.copy_schedule_template).pack(side="left", padx=5)

        entry_frame = tk.LabelFrame(self.tab2, text=" Tambah Jam, Lagu & Jumlah Putar pada hari terpilih ", padx=10, pady=10)
        entry_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(entry_frame, text="Jam (HH:MM):").pack(side="left", padx=3)
        
        # --- Validasi Input Otomatis, just angka & formatted---
        def validate_time_input(P):
            if P == "": 
                return True
            if len(P) > 5: 
                return False
            for i, char in enumerate(P):
                if i == 2:
                    if char != ":": return False # Karakter ke-3 WAJIB titik dua
                else:
                    if not char.isdigit(): return False # Karakter lainnya WAJIB angka
            return True

        vcmd = (self.root.register(validate_time_input), '%P')
        
        # Buat Entry dengan validasi ketat
        self.ent_sched_time = tk.Entry(entry_frame, width=7, font=("Arial", 11), validate="key", validatecommand=vcmd)
        self.ent_sched_time.insert(0, "08:00")
        self.ent_sched_time.pack(side="left", padx=3)

        # Fitur auto-insert titik dua ketika user mengetik angka ke-2
        def auto_insert_colon(event):
            if event.keysym == "Backspace": 
                return
            current_text = self.ent_sched_time.get()
            if len(current_text) == 2:
                self.ent_sched_time.insert(2, ":")

        self.ent_sched_time.bind("<KeyRelease>", auto_insert_colon)

        tk.Label(entry_frame, text="Pilih Sound:").pack(side="left", padx=3)
        self.cb_sound_select = ttk.Combobox(entry_frame, values=[], state="readonly", width=18)
        self.cb_sound_select.pack(side="left", padx=3)

        tk.Label(entry_frame, text="Putar:").pack(side="left", padx=3)
        self.cb_loop_count = ttk.Combobox(entry_frame, values=["1x", "2x", "3x", "4x", "5x"], state="readonly", width=4)
        self.cb_loop_count.set("1x")
        self.cb_loop_count.pack(side="left", padx=3)

        tk.Button(entry_frame, text="+ Tambah ke Jadwal", bg="#4CAF50", fg="white", command=self.add_time_schedule).pack(side="left", padx=8)

        list_frame = tk.LabelFrame(self.tab2, text=" Daftar Jadwal Hari Terpilih ", padx=10, pady=5)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.sched_listbox = tk.Listbox(list_frame, height=10)
        self.sched_listbox.pack(fill="both", expand=True, side="left")
        
        sb = tk.Scrollbar(list_frame, orient="vertical", command=self.sched_listbox.yview)
        sb.pack(side="right", fill="y")
        self.sched_listbox.config(yscrollcommand=sb.set)

        btn_action_frame = tk.Frame(self.tab2)
        btn_action_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(btn_action_frame, text="Hapus Jadwal Terpilih", bg="#F44336", fg="white", command=self.delete_time_schedule).pack(side="right")

        self.update_schedule_dropdowns()
        self.update_schedule_listbox()

    def update_schedule_dropdowns(self):
        self.cb_sound_select['values'] = sorted(list(self.media_library.keys()))
        if self.media_library: self.cb_sound_select.set(sorted(list(self.media_library.keys()))[0])

    def add_time_schedule(self):
        day = self.cb_day_select.get()
        t_str = self.ent_sched_time.get().strip()
        sound = self.cb_sound_select.get()
        loop_str = self.cb_loop_count.get()
        loop_int = int(loop_str.replace("x", ""))

        if not sound:
            messagebox.showwarning("Peringatan", "Library sound kosong! Isi menu 1 dahulu.")
            return

        # --- validasi Jam ---
        # Cek apakah input kosong atau belum lengkap ditulis (misal baru ngetik "12:")
        if len(t_str) != 5:
            messagebox.showerror("Error", "Format waktu belum lengkap! Isi dengan format HH:MM (Contoh: 08:00)")
            return

        try:
            hours, minutes = t_str.split(":")
            # Karena input sudah pasti angka (validasi dari fungsi validate_time_input diatas), 
            # kita tinggal cek batasan nilai jam dan menitnya saja.
            if int(hours) > 23 or int(minutes) > 59:
                messagebox.showerror("Error", "Waktu tidak valid! Jam maksimal 23 dan Menit maksimal 59 (Contoh: 23:59)")
                return
                
            time.strptime(t_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Waktu yang dimasukkan salah!")
            return

        self.schedules[day].append({"time": t_str, "sound": sound, "loop": loop_int})
        self.schedules[day].sort(key=lambda x: x["time"])
        self.save_data()
        self.update_schedule_listbox()
        self.refresh_monitor_view()
        messagebox.showinfo("Berhasil", f"Jadwal ditambahkan untuk hari {day} jam {t_str} ({loop_str})")

    def update_schedule_listbox(self):
        self.sched_listbox.delete(0, tk.END)
        day = self.cb_day_select.get()
        for idx, item in enumerate(self.schedules[day]):
            loops = item.get("loop", 1) 
            self.sched_listbox.insert(tk.END, f"[{item['time']}] - Sound: {item['sound']} ({loops}x)")

    def delete_time_schedule(self):
        if not self.sched_listbox.curselection(): return
        idx = self.sched_listbox.curselection()[0]
        day = self.cb_day_select.get()
        del self.schedules[day][idx]
        self.save_data()
        self.update_schedule_listbox()
        self.refresh_monitor_view()

    def copy_schedule_template(self):
        source_day = self.cb_day_select.get()
        target_day = self.cb_target_day.get()
        if source_day == target_day:
            messagebox.showwarning("Peringatan", "Hari asal dan tujuan tidak boleh sama!")
            return
        if messagebox.askyesno("Konfirmasi Copy", f"Salin semua jadwal hari {source_day} ke hari {target_day}?"):
            self.schedules[target_day] = list(self.schedules[source_day])
            self.save_data()
            self.refresh_monitor_view()
            messagebox.showinfo("Sukses", f"Jadwal hari {source_day} berhasil dicopy ke {target_day}!")

    def build_tab3_monitor(self):
        clock_frame = tk.Frame(self.tab3, bg="#212121", padx=15, pady=15)
        clock_frame.pack(fill="x", padx=15, pady=15)

        self.lbl_clock = tk.Label(clock_frame, text="00:00:00", fg="#00FF00", bg="#212121", font=("Consolas", 28, "bold"))
        self.lbl_clock.pack()
        self.lbl_day_info = tk.Label(clock_frame, text="Hari, Tanggal", fg="white", bg="#212121", font=("Arial", 12))
        self.lbl_day_info.pack()

        self.btn_engine = tk.Button(self.tab3, text="MULAI ENGINE OTOMATISASI (AKTIFKAN)", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2, command=self.toggle_engine)
        self.btn_engine.pack(fill="x", padx=15, pady=5)

        info_frame = tk.LabelFrame(self.tab3, text=" Jadwal Sound yang Akan Diputar Hari Ini ", padx=10, pady=10)
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.monitor_text = tk.Text(info_frame, bg="#F5F5F5", state="disabled", font=("Arial", 10))
        self.monitor_text.pack(fill="both", expand=True)

        self.refresh_monitor_view()

    def start_global_clock(self):
        def clock_loop():
            day_mapping_eng_indo = {"Monday":"Senin", "Tuesday":"Selasa", "Wednesday":"Rabu", "Thursday":"Kamis", "Friday":"Jumat", "Saturday":"Sabtu", "Sunday":"Minggu"}
            while True:
                now = datetime.now()
                time_str = now.strftime("%H:%M:%S")
                eng_day = now.strftime("%A")
                indo_day = day_mapping_eng_indo.get(eng_day, eng_day)
                date_str = f"{indo_day}, {now.strftime('%d-%m-%Y')}"
                
                try:
                    self.lbl_clock.config(text=time_str)
                    self.lbl_day_info.config(text=date_str)
                except Exception:
                    break
                time.sleep(1)
        
        t = threading.Thread(target=clock_loop, daemon=True)
        t.start()

    def refresh_monitor_view(self):
        day_mapping_eng_indo = {"Monday":"Senin", "Tuesday":"Selasa", "Wednesday":"Rabu", "Thursday":"Kamis", "Friday":"Jumat", "Saturday":"Sabtu", "Sunday":"Minggu"}
        current_day = day_mapping_eng_indo.get(datetime.now().strftime("%A"), "Senin")

        self.monitor_text.config(state="normal")
        self.monitor_text.delete("1.0", tk.END)
        
        status_engine = "AKTIF (Menunggu Waktu)\n" if self.is_running else "NONAKTIF (Jadwal tidak akan berputar)\n"
        self.monitor_text.insert(tk.END, f"STATUS ENGINE: {status_engine}")
        self.monitor_text.insert(tk.END, f"Hari ini ({current_day}) terdapat {len(self.schedules[current_day])} jadwal:\n")
        self.monitor_text.insert(tk.END, "="*50 + "\n")
        
        if not self.schedules[current_day]:
            self.monitor_text.insert(tk.END, " Tidak ada jadwal untuk hari ini.\n")
        else:
            for item in self.schedules[current_day]:
                loops = item.get("loop", 1)
                self.monitor_text.insert(tk.END, f" 🔔 Jam {item['time']} -> Memutar: {item['sound']} ({loops}x)\n")
                
        self.monitor_text.config(state="disabled")

    def toggle_engine(self):
        if not self.is_running:
            self.is_running = True
            self.btn_engine.config(text="MATIKAN ENGINE OTOMATISASI", bg="#F44336")
            self.refresh_monitor_view()
            
            self.scheduler_thread = threading.Thread(target=self.core_scheduler_engine, daemon=True)
            self.scheduler_thread.start()
        else:
            self.is_running = False
            self.btn_engine.config(text="MULAI ENGINE OTOMATISASI (AKTIFKAN)", bg="#4CAF50")
            self.refresh_monitor_view()

    def play_sound_via_vbs(self, file_path, loop_count, is_test=False):
        clean_path = os.path.abspath(file_path).replace("\\", "\\\\")
        
        vbs_content = f"""
        Set Player = CreateObject("WMPlayer.OCX")
        Player.URL = "{clean_path}"
        Player.controls.play
        Do Until Player.playState = 3
            WScript.Sleep 200
        Loop
        Do While Player.playState = 3
            WScript.Sleep 500
        Loop
        """
        
        for _ in range(loop_count):
            if not self.is_running and not is_test: 
                break 
                
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".vbs", mode="w") as f:
                    f.write(vbs_content)
                    vbs_file_path = f.name
                
                # Konfigurasi untuk menyembunyikan jendela CMD
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                
                # Menggunakan subprocess.run (SINKRONUS) agar menunggu lagu selesai baru lanjut
                subprocess.run(
                    f'wscript.exe "{vbs_file_path}"',
                    startupinfo=startupinfo,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=False
                )
                
                os.unlink(vbs_file_path)
            except Exception:
                pass

    def core_scheduler_engine(self):
        day_mapping_eng_indo = {"Monday":"Senin", "Tuesday":"Selasa", "Wednesday":"Rabu", "Thursday":"Kamis", "Friday":"Jumat", "Saturday":"Sabtu", "Sunday":"Minggu"}
        last_played_trigger = ""

        while self.is_running:
            now = datetime.now()
            current_day_indo = day_mapping_eng_indo.get(now.strftime("%A"), "Minggu")
            current_time_hm = now.strftime("%H:%M")
            trigger_key = f"{current_day_indo}-{current_time_hm}"

            today_schedules = self.schedules.get(current_day_indo, [])
            
            for item in today_schedules:
                if item["time"] == current_time_hm and last_played_trigger != trigger_key:
                    sound_name = item["sound"]
                    loop_count = item.get("loop", 1)
                    
                    if sound_name in self.media_library:
                        file_path = self.media_library[sound_name]
                        
                        sound_thread = threading.Thread(
                            target=self.play_sound_via_vbs, 
                            args=(file_path, loop_count, False), 
                            daemon=True
                        )
                        sound_thread.start()
                                
                    last_played_trigger = trigger_key
                    break
            
            time.sleep(10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedOfficeScheduler(root)
    root.mainloop()