import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Toplevel, scrolledtext, font
import os
from datetime import datetime
from abc import ABC, abstractmethod

# File paths
FILE_USER = "User.txt"         # Untuk menyimpan data login karyawan
FILE_ABSENSI = "Absensi.txt"   # Untuk menyimpan data absensi
FILE_IZIN = "Izin.txt"         # Untuk menyimpan data izin
FILE_LAPORAN = "Laporan.txt"   # Untuk menyimpan laporan

# Kelas abstrak Karyawan sebagai parent class
class Karyawan(ABC):
    def __init__(self, nama, idKaryawan, password, status, gaji):
        self._nama = nama              # protected attribute
        self._idKaryawan = idKaryawan  # protected attribute
        self.__password = password     # private attribute
        self.__status = status         # private attribute
        self.__gaji = gaji             # private attribute
        
    def absensi(self):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hasil_absensi = f"{self._idKaryawan}:{self._nama}:{self.__status}:{waktu}\n"
        
        # Simpan ke file
        with open(FILE_ABSENSI, "a") as file:
            file.write(hasil_absensi)
            
        return f"{self._nama} (ID: {self._idKaryawan}) telah absen pada {waktu}"
    
    def login(self, nama, idKaryawan, password):
        # Validasi login
        return self._nama == nama and self._idKaryawan == idKaryawan and self.__password == password
    
    def permohonan_izin(self):
        return "String"
    
    def kirim_laporan(self, isi_laporan, judul="Laporan"):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Format: id:nama:status:judul:waktu:isi_laporan:status_laporan:catatan
        data_laporan = f"{self._idKaryawan}:{self._nama}:{self.__status}:{judul}:{waktu}:{isi_laporan}:Menunggu:-\n"
        
        with open(FILE_LAPORAN, "a") as file:
            file.write(data_laporan)
        
        return f"Laporan berhasil dikirim kepada Manager pada {waktu}"
        
    @abstractmethod
    def tampilkanGaji(self):
        pass
    
    # Setter methods
    def setNama(self, nama):
        self._nama = nama
        
    def setIdKaryawan(self, idKaryawan):
        self._idKaryawan = idKaryawan
        
    def setPassword(self, password):
        self.__password = password
        
    def setStatus(self, status):
        self.__status = status
        
    def setGaji(self, gaji):
        self.__gaji = gaji
        
    # Getter methods
    def getNama(self):
        return self._nama
        
    def getId(self):
        return self._idKaryawan
        
    def getStatus(self):
        return self.__status
        
    def getGaji(self):
        return self.__gaji

# Kelas-kelas turunan
class Admin(Karyawan):
    def __init__(self, nama, idKaryawan, password, status, gaji):
        super().__init__(nama, idKaryawan, password, status, gaji)
    
    def absensi(self):
        return super().absensi()
    
    def rekapAbsensi(self):
        # Menampilkan rekap absensi dari file
        if not os.path.exists(FILE_ABSENSI):
            return "Belum ada data absensi"
            
        hasil = "REKAP ABSENSI:\n"
        with open(FILE_ABSENSI, "r") as file:
            for line in file:
                hasil += line
                
        return hasil
        
    def tampilkanGaji(self):
        return f"Gaji Admin {self._nama}: Rp{self.getGaji():,}"

class Manager(Karyawan):
    def __init__(self, nama, idKaryawan, password, gaji):
        super().__init__(nama, idKaryawan, password, "Manager", gaji)
    
    def kelolaKaryawan(self):
        return "Mengelola karyawan"
    
    def tampilkanGaji(self):
        # Manager mendapat bonus 20%
        return f"Gaji Manager {self._nama}: Rp{self.getGaji() * 1.2:,}"
    
    def kelolaPerizinan(self):
        return True
    
    def kelolaLaporan(self):
        return True
    
    def review_laporan(self, id_laporan, status, catatan):
        updated_lines = []
        with open(FILE_LAPORAN, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) >= 8 and parts[0] == id_laporan:
                    parts[6] = status  # Update status
                    parts[7] = catatan  # Update catatan
                    updated_line = ":".join(parts)
                    updated_lines.append(updated_line + "\n")
                else:
                    updated_lines.append(line)
        
        with open(FILE_LAPORAN, "w") as file:
            file.writelines(updated_lines)
        
        return f"Laporan dengan ID {id_laporan} telah di-{status.lower()} dengan catatan: {catatan}"

class HumanResource(Karyawan):
    def __init__(self, nama, idKaryawan, password, gaji):
        super().__init__(nama, idKaryawan, password, "Human Resource", gaji)
    
    def kelolaKaryawan(self):
        return "Mengelola data karyawan"
    
    def absensi(self):
        return super().absensi()
    
    def kelolaGaji(self):
        return "Mengelola gaji karyawan"
    
    def kelolaPerizinan(self):
        return True
    
    def tampilkanGaji(self):
        # HR mendapat bonus 15%
        return f"Gaji HR {self._nama}: Rp{self.getGaji() * 1.15:,}"

class CleaningService(Karyawan):
    def __init__(self, nama, idKaryawan, password, gaji):
        super().__init__(nama, idKaryawan, password, "Cleaning Service", gaji)
    
    def absensi(self):
        return super().absensi()
    
    def tampilkanGaji(self):
        return f"Gaji Cleaning Service {self._nama}: Rp{self.getGaji():,}"
    
    def laporanHasilPekerjaan(self, isi_laporan):
        return self.kirim_laporan(isi_laporan, "Laporan Cleaning Service")

class Internship(Karyawan):
    def __init__(self, nama, idKaryawan, password, gaji):
        super().__init__(nama, idKaryawan, password, "Internship", gaji)
    
    def absensi(self):
        return super().absensi()
    
    def tampilkanGaji(self):
        # Internship mendapat gaji pokok saja
        return f"Gaji Internship {self._nama}: Rp{self.getGaji():,}"
    
    def laporan(self, isi_laporan):
        return self.kirim_laporan(isi_laporan, "Laporan Internship")

class Marketing(Karyawan):
    def __init__(self, nama, idKaryawan, password, gaji):
        super().__init__(nama, idKaryawan, password, "Marketing", gaji)
    
    def absensi(self):
        return super().absensi()
    
    def tampilkanGaji(self):
        # Marketing mendapat bonus 10%
        return f"Gaji Marketing {self._nama}: Rp{self.getGaji() * 1.1:,}"
    
    def laporan(self, isi_laporan):
        return self.kirim_laporan(isi_laporan, "Laporan Marketing")

# UI Theme and Styles
class AppTheme:
    def __init__(self):
        self.bg_color = "#f5f5f5"
        self.primary_color = "#1976D2"
        self.accent_color = "#FF5722"
        self.text_color = "#212121"
        self.light_text = "#ffffff"
        self.card_bg = "#ffffff"
        self.success_color = "#4CAF50"
        self.warning_color = "#FFC107"
        self.danger_color = "#F44336"
        
        self.title_font = ("Helvetica", 16, "bold")
        self.heading_font = ("Helvetica", 14, "bold")
        self.text_font = ("Helvetica", 10)
        self.small_text = ("Helvetica", 8)
        
    def apply_to_widget(self, widget, is_button=False):
        widget.config(bg=self.bg_color, fg=self.text_color)
        
        if is_button:
            widget.config(bg=self.primary_color, fg=self.light_text, 
                         activebackground=self.accent_color,
                         activeforeground=self.light_text,
                         relief=tk.FLAT, padx=10, pady=5,
                         font=self.text_font)
    
    def configure_ttk_styles(self):
        style = ttk.Style()
        
        # Configure TButton
        style.configure("TButton", 
                       background=self.primary_color, 
                       foreground=self.light_text,
                       font=self.text_font,
                       padding=5)
        
        # Configure Treeview
        style.configure("Treeview", 
                       background=self.card_bg,
                       foreground=self.text_color,
                       rowheight=25,
                       fieldbackground=self.card_bg)
        
        style.configure("Treeview.Heading",
                       background=self.primary_color,
                       foreground=self.light_text,
                       font=self.text_font)
        
        # Configure tabs
        style.configure("TNotebook", background=self.bg_color)
        style.configure("TNotebook.Tab", 
                       background=self.primary_color,
                       foreground=self.light_text,
                       padding=[10, 5],
                       font=self.text_font)
        
        style.map("TNotebook.Tab",
                 background=[("selected", self.accent_color)],
                 foreground=[("selected", self.light_text)])

# GUI Interface
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.theme = controller.theme
        self.configure(bg=self.theme.bg_color)
        
        # UI Components
        header_frame = tk.Frame(self, bg=self.theme.primary_color)
        header_frame.pack(fill="x", pady=0)
        
        tk.Label(header_frame, 
                text="SISTEM MANAJEMEN KARYAWAN", 
                font=("Arial", 18, "bold"),
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=20).pack()
        
        main_frame = tk.Frame(self, bg=self.theme.bg_color)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        login_frame = tk.Frame(main_frame, bg=self.theme.card_bg,
                              highlightbackground=self.theme.primary_color,
                              highlightthickness=1, padx=20, pady=20)
        login_frame.pack(pady=20, padx=20, fill="both", expand=False)
        
        tk.Label(login_frame, text="LOGIN", 
                font=self.theme.heading_font,
                bg=self.theme.card_bg,
                fg=self.theme.primary_color).pack(pady=(0, 20))
        
        # Username
        tk.Label(login_frame, text="Username:", 
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(anchor="w")
        self.username_entry = tk.Entry(login_frame, width=30, 
                                     font=self.theme.text_font,
                                     relief=tk.GROOVE, bd=2)
        self.username_entry.pack(fill="x", pady=(0, 15))
        
        # ID Karyawan
        tk.Label(login_frame, text="ID Karyawan:", 
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(anchor="w")
        self.id_entry = tk.Entry(login_frame, width=30, 
                               font=self.theme.text_font,
                               relief=tk.GROOVE, bd=2)
        self.id_entry.pack(fill="x", pady=(0, 15))
        
        # Password
        tk.Label(login_frame, text="Password:", 
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(anchor="w")
        self.password_entry = tk.Entry(login_frame, width=30, show="*", 
                                     font=self.theme.text_font,
                                     relief=tk.GROOVE, bd=2)
        self.password_entry.pack(fill="x", pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(login_frame, bg=self.theme.card_bg)
        button_frame.pack(pady=10)
        
        login_btn = tk.Button(button_frame, text="Login", width=15, 
                            command=self.do_login,
                            bg=self.theme.primary_color,
                            fg=self.theme.light_text,
                            font=self.theme.text_font,
                            relief=tk.FLAT, padx=10, pady=5)
        login_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = tk.Button(button_frame, text="Exit", width=15, 
                           command=self.controller.destroy,
                           bg=self.theme.danger_color,
                           fg=self.theme.light_text,
                           font=self.theme.text_font,
                           relief=tk.FLAT, padx=10, pady=5)
        exit_btn.pack(side=tk.LEFT)
    
    def do_login(self):
        username = self.username_entry.get().strip()
        id_karyawan = self.id_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not id_karyawan or not password:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
            
        # Cek file user
        if not os.path.exists(FILE_USER):
            # Jika belum ada file, buat admin default
            with open(FILE_USER, "w") as file:
                # format: nama:id:password:status:gaji
                file.write("admin:1001:admin123:Admin:5000000\n")
                file.write("manager:1002:manager123:Manager:8000000\n")
            
        # Verifikasi login
        with open(FILE_USER, "r") as file:
            for line in file:
                data = line.strip().split(":")
                if len(data) >= 5:
                    saved_user, saved_id, saved_pass, saved_status, saved_gaji = data
                    if username == saved_user and id_karyawan == saved_id and password == saved_pass:
                        # Buat objek sesuai dengan status
                        if saved_status == "Admin":
                            user = Admin(saved_user, saved_id, saved_pass, saved_status, int(saved_gaji))
                        elif saved_status == "Manager":
                            user = Manager(saved_user, saved_id, saved_pass, int(saved_gaji))
                        elif saved_status == "Human Resource":
                            user = HumanResource(saved_user, saved_id, saved_pass, int(saved_gaji))
                        elif saved_status == "Cleaning Service":
                            user = CleaningService(saved_user, saved_id, saved_pass, int(saved_gaji))
                        elif saved_status == "Internship":
                            user = Internship(saved_user, saved_id, saved_pass, int(saved_gaji))
                        elif saved_status == "Marketing":
                            user = Marketing(saved_user, saved_id, saved_pass, int(saved_gaji))
                        else:
                            user = None
                            
                        if user:
                            self.controller.current_user = user
                            messagebox.showinfo("Login Berhasil", f"Selamat datang {saved_user}")
                            self.controller.show_frame("MainMenuPage")
                            return
        
        messagebox.showerror("Login Gagal", "Username, ID, atau password salah!")

class MainMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.theme = controller.theme
        self.configure(bg=self.theme.bg_color)
        
        # Header Frame
        header_frame = tk.Frame(self, bg=self.theme.primary_color)
        header_frame.pack(fill="x", pady=0)
        
        self.title_label = tk.Label(header_frame, 
                                  text="MENU UTAMA", 
                                  font=("Arial", 18, "bold"),
                                  bg=self.theme.primary_color, 
                                  fg=self.theme.light_text,
                                  padx=20, pady=15)
        self.title_label.pack(side=tk.LEFT)
        
        # Logout button in header
        logout_btn = tk.Button(header_frame, 
                              text="Logout", 
                              command=self.logout,
                              bg=self.theme.danger_color,
                              fg=self.theme.light_text,
                              font=self.theme.text_font,
                              relief=tk.FLAT, padx=10, pady=5)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # User info frame
        user_frame = tk.Frame(self, bg=self.theme.bg_color)
        user_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = tk.Label(user_frame, 
                                   text="", 
                                   font=self.theme.text_font,
                                   bg=self.theme.bg_color,
                                   fg=self.theme.text_color)
        self.status_label.pack(anchor="w")
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tab 1: Basic Functions
        basic_tab = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(basic_tab, text="Fungsi Dasar")
        
        # Arrange in grid with card-like frames
        self._create_card(basic_tab, "Absensi", "Catat kehadiran Anda", 
                         self.menu_absensi, 0, 0)
        
        self._create_card(basic_tab, "Lihat Gaji", "Informasi gaji Anda", 
                         self.menu_gaji, 0, 1)
        
        self._create_card(basic_tab, "Ajukan Izin", "Permohonan tidak masuk", 
                         self.menu_izin, 1, 0)
        
        self._create_card(basic_tab, "Kirim Laporan", "Laporan hasil kerja", 
                         self.menu_laporan, 1, 1)
        
        # Tab 2: Admin Functions
        admin_tab = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(admin_tab, text="Fungsi Admin")
        
        self._create_card(admin_tab, "Rekap Absensi", "Lihat rekap kehadiran", 
                         self.menu_rekap, 0, 0)
        
        self._create_card(admin_tab, "Kelola Karyawan", "Tambah/ubah data karyawan", 
                         self.menu_kelola_karyawan, 0, 1)
        
        self._create_card(admin_tab, "Kelola Perizinan", "Approval izin karyawan", 
                         self.menu_kelola_perizinan, 1, 0)
        
        self._create_card(admin_tab, "Kelola Gaji", "Atur gaji karyawan", 
                         self.menu_kelola_gaji, 1, 1)
        
        # Tab 3: Manager Functions
        manager_tab = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(manager_tab, text="Fungsi Manager")
        
        self._create_card(manager_tab, "Review Laporan", "Evaluasi laporan karyawan", 
                         self.menu_review_laporan, 0, 0)
        
    def _create_card(self, parent, title, subtitle, command, row, col):
        card = tk.Frame(parent, bg=self.theme.card_bg,
                      highlightbackground=self.theme.primary_color,
                      highlightthickness=1, padx=15, pady=15)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Configure grid weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        # Card content
        tk.Label(card, text=title, 
                font=self.theme.heading_font,
                bg=self.theme.card_bg,
                fg=self.theme.text_color).pack(anchor="w")
        
        tk.Label(card, text=subtitle, 
                font=self.theme.small_text,
                bg=self.theme.card_bg,
                fg="gray").pack(anchor="w", pady=(0, 10))
        
        btn = tk.Button(card, text="Buka", 
                      command=command,
                      bg=self.theme.primary_color,
                      fg=self.theme.light_text,
                      font=self.theme.text_font,
                      relief=tk.FLAT, padx=10, pady=5)
        btn.pack(pady=10)
        
    def on_show_frame(self):
        # Update label sesuai dengan user yang login
        user = self.controller.current_user
        self.status_label.config(text=f"Logged in as: {user.getNama()} ({user.getStatus()})")
        
        # Show appropriate tabs based on user role
        if isinstance(user, Admin):
            self.notebook.tab(1, state="normal")  # Admin tab
            self.notebook.tab(2, state="hidden")  # Manager tab
        elif isinstance(user, Manager):
            self.notebook.tab(1, state="normal")  # Admin tab
            self.notebook.tab(2, state="normal")  # Manager tab
        elif isinstance(user, HumanResource):
            self.notebook.tab(1, state="normal")  # Admin tab
            self.notebook.tab(2, state="hidden")  # Manager tab
        else:
            self.notebook.tab(1, state="hidden")  # Admin tab
            self.notebook.tab(2, state="hidden")  # Manager tab
    
    def menu_absensi(self):
        hasil = self.controller.current_user.absensi()
        messagebox.showinfo("Absensi Berhasil", hasil)
    
    def menu_gaji(self):
        hasil = self.controller.current_user.tampilkanGaji()
        messagebox.showinfo("Informasi Gaji", hasil)
    
    def menu_izin(self):
        top = Toplevel(self)
        top.title("Form Pengajuan Izin")
        top.geometry("500x400")
        top.grab_set()  # Modal dialog
        top.configure(bg=self.theme.bg_color)
        
        # Header
        header_frame = tk.Frame(top, bg=self.theme.primary_color)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="FORM PENGAJUAN IZIN", 
                font=self.theme.heading_font,
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=10).pack()
        
        # Form Content
        content_frame = tk.Frame(top, bg=self.theme.bg_color, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        form_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        form_frame.pack(pady=10, fill="x")
        
        # Form fields
        tk.Label(form_frame, text="Alasan:", 
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.text_font).grid(row=0, column=0, sticky="w", pady=5)
        alasan_entry = tk.Entry(form_frame, width=30, font=self.theme.text_font)
        alasan_entry.grid(row=0, column=1, pady=5, padx=5, sticky="we")
        
        tk.Label(form_frame, text="Tanggal Mulai (YYYY-MM-DD):", 
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.text_font).grid(row=1, column=0, sticky="w", pady=5)
        tgl_mulai = tk.Entry(form_frame, width=30, font=self.theme.text_font)
        tgl_mulai.grid(row=1, column=1, pady=5, padx=5, sticky="we")
        
        tk.Label(form_frame, text="Tanggal Selesai (YYYY-MM-DD):", 
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.text_font).grid(row=2, column=0, sticky="w", pady=5)
        tgl_selesai = tk.Entry(form_frame, width=30, font=self.theme.text_font)
        tgl_selesai.grid(row=2, column=1, pady=5, padx=5, sticky="we")
        
        # Configure column weights
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Detailed description
        tk.Label(content_frame, text="Detail Keterangan:", 
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(anchor="w", pady=(10, 5))
                
        detail_text = scrolledtext.ScrolledText(content_frame, 
                                              width=40, height=6,
                                              font=self.theme.text_font)
        detail_text.pack(fill="both", expand=True, pady=5)
        
        def submit_izin():
            alasan = alasan_entry.get().strip()
            mulai = tgl_mulai.get().strip()
            selesai = tgl_selesai.get().strip()
            detail = detail_text.get("1.0", tk.END).strip()
            
            if not alasan or not mulai or not selesai:
                messagebox.showerror("Error", "Semua field harus diisi!")
                return
                
            # Validate date format
            try:
                mulai_date = datetime.strptime(mulai, "%Y-%m-%d")
                selesai_date = datetime.strptime(selesai, "%Y-%m-%d")
                
                # Check if end date is after start date
                if selesai_date < mulai_date:
                    messagebox.showerror("Error", "Tanggal selesai harus setelah tanggal mulai!")
                    return
                    
                # Check if dates are in the past
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                if mulai_date < today:
                    messagebox.showerror("Error", "Tanggal mulai tidak boleh di masa lalu!")
                    return
                    
            except ValueError:
                messagebox.showerror("Error", "Format tanggal harus YYYY-MM-DD (contoh: 2023-12-31)")
                return
            
            try:
                # Format: idKaryawan:nama:status:alasan:tglMulai:tglSelesai:waktuPengajuan:statusIzin:detail
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data_izin = f"{self.controller.current_user.getId()}:{self.controller.current_user.getNama()}:"
                data_izin += f"{self.controller.current_user.getStatus()}:{alasan}:{mulai}:{selesai}:{now}:Menunggu:{detail}\n"
                
                with open(FILE_IZIN, "a") as file:
                    file.write(data_izin)
                
                messagebox.showinfo("Sukses", "Izin berhasil diajukan")
                top.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=20, fill="x")
        
        submit_btn = tk.Button(button_frame, 
                              text="Submit", 
                              command=submit_izin,
                              bg=self.theme.primary_color,
                              fg=self.theme.light_text,
                              font=self.theme.text_font,
                              relief=tk.FLAT, padx=10, pady=5)
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(button_frame, 
                              text="Batal", 
                              command=top.destroy,
                              bg=self.theme.danger_color,
                              fg=self.theme.light_text,
                              font=self.theme.text_font,
                              relief=tk.FLAT, padx=10, pady=5)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def menu_laporan(self):
        if not hasattr(self.controller.current_user, "kirim_laporan"):
            messagebox.showerror("Error", "Fitur tidak tersedia untuk karyawan ini.")
            return
            
        top = Toplevel(self)
        top.title("Form Laporan Kerja")
        top.geometry("600x500")
        top.grab_set()  # Modal dialog
        top.configure(bg=self.theme.bg_color)
        
        # Header
        header_frame = tk.Frame(top, bg=self.theme.primary_color)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="FORM LAPORAN KERJA", 
                font=self.theme.heading_font,
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=10).pack()
        
        # Form Content
        content_frame = tk.Frame(top, bg=self.theme.bg_color, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(content_frame, text="Judul Laporan:", 
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(anchor="w", pady=5)
        
        title_entry = tk.Entry(content_frame, width=50, font=self.theme.text_font)
        title_entry.pack(fill="x", pady=5)
        
        # Laporan content
        tk.Label(content_frame, text="Isi Laporan:", 
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(anchor="w", pady=5)
                
        report_text = scrolledtext.ScrolledText(content_frame, 
                                              width=60, height=15,
                                              font=self.theme.text_font)
        report_text.pack(fill="both", expand=True, pady=5)
        
        def submit_laporan():
            judul = title_entry.get().strip()
            isi = report_text.get("1.0", tk.END).strip()
            
            if not judul or not isi:
                messagebox.showerror("Error", "Judul dan isi laporan harus diisi!")
                return
            
            hasil = self.controller.current_user.kirim_laporan(isi, judul)
            messagebox.showinfo("Sukses", hasil)
            top.destroy()
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=20, fill="x")
        
        submit_btn = tk.Button(button_frame, 
                              text="Kirim Laporan", 
                              command=submit_laporan,
                              bg=self.theme.primary_color,
                              fg=self.theme.light_text,
                              font=self.theme.text_font,
                              relief=tk.FLAT, padx=10, pady=5)
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(button_frame, 
                              text="Batal", 
                              command=top.destroy,
                              bg=self.theme.danger_color,
                              fg=self.theme.light_text,
                              font=self.theme.text_font,
                              relief=tk.FLAT, padx=10, pady=5)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def menu_rekap(self):
        if not isinstance(self.controller.current_user, Admin):
            messagebox.showerror("Error", "Anda tidak memiliki akses!")
            return
            
        admin = self.controller.current_user
        hasil = admin.rekapAbsensi()
        
        top = Toplevel(self)
        top.title("Rekap Absensi")
        top.geometry("700x500")
        top.configure(bg=self.theme.bg_color)
        
        # Header
        header_frame = tk.Frame(top, bg=self.theme.primary_color)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="REKAP ABSENSI KARYAWAN", 
                font=self.theme.heading_font,
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=10).pack(side=tk.LEFT)
        
        # Content
        content_frame = tk.Frame(top, bg=self.theme.bg_color, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Text area with scrollbar
        text_area = scrolledtext.ScrolledText(content_frame, 
                                            width=80, height=20,
                                            font=("Consolas", 10))
        text_area.pack(fill="both", expand=True)
        text_area.insert(tk.END, hasil)
        text_area.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10, fill="x")
        
        export_btn = tk.Button(button_frame, 
                              text="Export to PDF", 
                              command=lambda: messagebox.showinfo("Info", "Fungsi export akan tersedia pada pembaruan selanjutnya."),
                              bg=self.theme.primary_color,
                              fg=self.theme.light_text,
                              font=self.theme.text_font,
                              relief=tk.FLAT, padx=10, pady=5)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(button_frame, 
                             text="Tutup", 
                             command=top.destroy,
                             bg=self.theme.danger_color,
                             fg=self.theme.light_text,
                             font=self.theme.text_font,
                             relief=tk.FLAT, padx=10, pady=5)
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def menu_kelola_karyawan(self):
        if not isinstance(self.controller.current_user, (Manager, HumanResource)):
            messagebox.showerror("Error", "Anda tidak memiliki akses!")
            return
        
        top = Toplevel(self)
        top.title("Kelola Karyawan")
        top.geometry("800x600")
        top.configure(bg=self.theme.bg_color)
        
        # Header
        header_frame = tk.Frame(top, bg=self.theme.primary_color)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="KELOLA DATA KARYAWAN", 
                font=self.theme.heading_font,
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=10).pack(side=tk.LEFT)
        
        # Content
        content_frame = tk.Frame(top, bg=self.theme.bg_color, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Search frame
        search_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(search_frame, text="Cari:", 
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(search_frame, width=30, font=self.theme.text_font)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame, 
                              text="Cari", 
                              bg=self.theme.primary_color,
                              fg=self.theme.light_text,
                              font=self.theme.text_font,
                              relief=tk.FLAT, padx=10, pady=2)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        btn_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        btn_frame.pack(fill="x", pady=10)
        
        add_btn = tk.Button(btn_frame, 
                           text="Tambah Karyawan", 
                           command=lambda: self.tambah_karyawan(top),
                           bg=self.theme.success_color,
                           fg=self.theme.light_text,
                           font=self.theme.text_font,
                           relief=tk.FLAT, padx=10, pady=5)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = tk.Button(btn_frame, 
                            text="Ubah Status", 
                            command=lambda: self.ubah_status(top),
                            bg=self.theme.warning_color,
                            fg=self.theme.light_text,
                            font=self.theme.text_font,
                            relief=tk.FLAT, padx=10, pady=5)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        gaji_btn = tk.Button(btn_frame, 
                            text="Ubah Gaji", 
                            command=lambda: self.ubah_gaji(top),
                            bg=self.theme.accent_color,
                            fg=self.theme.light_text,
                            font=self.theme.text_font,
                            relief=tk.FLAT, padx=10, pady=5)
        gaji_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview untuk menampilkan data karyawan
        columns = ("ID", "Nama", "Status", "Gaji")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", style="Treeview")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        y_scrollbar.pack(side="right", fill="y")
        
        x_scrollbar = ttk.Scrollbar(content_frame, orient="horizontal", command=tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Load data karyawan
        self.load_karyawan_data(tree)

    def menu_review_laporan(self):
        if not isinstance(self.controller.current_user, Manager):
            messagebox.showerror("Error", "Anda tidak memiliki akses!")
            return
            
        top = Toplevel(self)
        top.title("Review Laporan")
        top.geometry("900x600")
        top.configure(bg=self.theme.bg_color)
        
        # Header
        header_frame = tk.Frame(top, bg=self.theme.primary_color)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="REVIEW LAPORAN KARYAWAN", 
                font=self.theme.heading_font,
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=10).pack(side=tk.LEFT)
        
        # Split view - left side for list, right side for content
        main_frame = tk.Frame(top, bg=self.theme.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create PanedWindow for split view
        pw = tk.PanedWindow(main_frame, orient="horizontal", 
                           bg=self.theme.bg_color,
                           sashwidth=5, sashrelief=tk.RAISED)
        pw.pack(fill="both", expand=True)
        
        # Left frame - list of reports
        left_frame = tk.Frame(pw, bg=self.theme.card_bg, padx=10, pady=10)
        
        # Filter options
        filter_frame = tk.Frame(left_frame, bg=self.theme.card_bg)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(filter_frame, 
                text="Filter Status:", 
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(side=tk.LEFT, padx=5)
        
        filter_var = tk.StringVar()
        filter_combo = ttk.Combobox(filter_frame, width=15, textvariable=filter_var)
        filter_combo['values'] = ('Semua', 'Menunggu', 'Disetujui', 'Ditolak')
        filter_combo.current(0)
        filter_combo.pack(side=tk.LEFT, padx=5)
        
        # Reports list
        columns = ("ID", "Nama", "Status", "Judul", "Tanggal", "Status Laporan")
        report_tree = ttk.Treeview(left_frame, columns=columns, show="headings", style="Treeview", height=20)
        
        for col, width in zip(columns, [50, 100, 100, 150, 100, 100]):
            report_tree.heading(col, text=col)
            report_tree.column(col, width=width)
        
        report_tree.pack(fill="both", expand=True)
        
        # Right frame - report content
        right_frame = tk.Frame(pw, bg=self.theme.card_bg, padx=10, pady=10)
        
        # Add frames to paned window
        pw.add(left_frame, width=500)
        pw.add(right_frame, width=400)
        
        # Right content - display selected report
        tk.Label(right_frame, 
                text="Detail Laporan", 
                font=self.theme.heading_font,
                bg=self.theme.card_bg,
                fg=self.theme.text_color).pack(pady=(0, 10))
        
        detail_frame = tk.Frame(right_frame, bg=self.theme.card_bg)
        detail_frame.pack(fill="both", expand=True)
        
        # Report info labels
        info_frame = tk.Frame(detail_frame, bg=self.theme.card_bg)
        info_frame.pack(fill="x", pady=5)
        
        tk.Label(info_frame, text="Judul:", 
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.text_font).grid(row=0, column=0, sticky="w")
        report_title_var = tk.StringVar()
        tk.Label(info_frame, textvariable=report_title_var, 
                bg=self.theme.card_bg,
                fg=self.theme.primary_color,
                font=self.theme.text_font).grid(row=0, column=1, sticky="w")
        
        tk.Label(info_frame, text="Pengirim:", 
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.text_font).grid(row=1, column=0, sticky="w")
        report_sender_var = tk.StringVar()
        tk.Label(info_frame, textvariable=report_sender_var, 
                bg=self.theme.card_bg,
                fg=self.theme.primary_color,
                font=self.theme.text_font).grid(row=1, column=1, sticky="w")
        
        tk.Label(info_frame, text="Tanggal:", 
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.text_font).grid(row=2, column=0, sticky="w")
        report_date_var = tk.StringVar()
        tk.Label(info_frame, textvariable=report_date_var, 
                bg=self.theme.card_bg,
                fg=self.theme.primary_color,
                font=self.theme.text_font).grid(row=2, column=1, sticky="w")
        
        # Report content
        tk.Label(detail_frame, text="Isi Laporan:", 
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(anchor="w", pady=(10, 5))
                
        report_content = scrolledtext.ScrolledText(detail_frame, 
                                                height=10, width=40,
                                                font=self.theme.text_font)
        report_content.pack(fill="both", expand=True)
        report_content.config(state=tk.DISABLED)
        
        # Manager comment
        tk.Label(detail_frame, text="Catatan Manager:", 
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.text_font).pack(anchor="w", pady=(10, 5))
                
        manager_comment = scrolledtext.ScrolledText(detail_frame, 
                                                  height=5, width=40,
                                                  font=self.theme.text_font)
        manager_comment.pack(fill="x")
        
        # Action buttons
        btn_frame = tk.Frame(detail_frame, bg=self.theme.card_bg)
        btn_frame.pack(fill="x", pady=10)
        
        approve_btn = tk.Button(btn_frame, 
                              text="Setujui", 
                              bg=self.theme.success_color,
                              fg=self.theme.light_text,
                              font=self.theme.text_font,
                              relief=tk.FLAT, padx=10, pady=5,
                              command=lambda: update_status("Disetujui"))
        approve_btn.pack(side=tk.LEFT, padx=5)
        
        reject_btn = tk.Button(btn_frame, 
                             text="Tolak", 
                             bg=self.theme.danger_color,
                             fg=self.theme.light_text,
                             font=self.theme.text_font,
                             relief=tk.FLAT, padx=10, pady=5,
                             command=lambda: update_status("Ditolak"))
        reject_btn.pack(side=tk.LEFT, padx=5)
        
        revise_btn = tk.Button(btn_frame, 
                             text="Minta Revisi", 
                             bg=self.theme.warning_color,
                             fg=self.theme.light_text,
                             font=self.theme.text_font,
                             relief=tk.FLAT, padx=10, pady=5,
                             command=lambda: update_status("Perlu Revisi"))
        revise_btn.pack(side=tk.LEFT, padx=5)
        
        # Function to handle status updates
        def update_status(status):
            selected = report_tree.selection()
            if not selected:
                messagebox.showerror("Error", "Pilih laporan terlebih dahulu!")
                return
                
            comment = manager_comment.get("1.0", tk.END).strip()
            if not comment:
                messagebox.showerror("Error", "Berikan catatan untuk karyawan!")
                return
                
            item = report_tree.item(selected[0])
            report_id = item['values'][0]
            
            # Update report status
            result = self.controller.current_user.review_laporan(report_id, status, comment)
            messagebox.showinfo("Sukses", result)
            
            # Refresh the list
            load_reports()
            
            # Clear detail view
            report_title_var.set("")
            report_sender_var.set("")
            report_date_var.set("")
            report_content.config(state=tk.NORMAL)
            report_content.delete("1.0", tk.END)
            report_content.config(state=tk.DISABLED)
            manager_comment.delete("1.0", tk.END)
        
        # Function to display report detail when selected
        def on_report_select(event):
            selected = report_tree.selection()
            if not selected:
                return
                
            item = report_tree.item(selected[0])
            values = item['values']
            report_id = values[0]
            
            # Fetch report content from file
            if os.path.exists(FILE_LAPORAN):
                with open(FILE_LAPORAN, "r") as file:
                    for line in file:
                        parts = line.strip().split(":")
                        if len(parts) >= 8 and parts[0] == str(report_id):
                            report_title_var.set(parts[3])
                            report_sender_var.set(f"{parts[1]} ({parts[2]})")
                            report_date_var.set(parts[4])
                            
                            report_content.config(state=tk.NORMAL)
                            report_content.delete("1.0", tk.END)
                            report_content.insert(tk.END, parts[5])
                            report_content.config(state=tk.DISABLED)
                            
                            # If report already has comment, show it
                            if parts[7] != "-":
                                manager_comment.delete("1.0", tk.END)
                                manager_comment.insert(tk.END, parts[7])
                            else:
                                manager_comment.delete("1.0", tk.END)
                            
                            break
        
        report_tree.bind('<<TreeviewSelect>>', on_report_select)
        
        # Function to filter reports based on status
        def filter_reports(event=None):
            load_reports()
        
        filter_combo.bind('<<ComboboxSelected>>', filter_reports)
        
        # Function to load reports
        def load_reports():
            # Clear existing data
            for item in report_tree.get_children():
                report_tree.delete(item)
                
            # Get filter value
            filter_status = filter_var.get()
                
            # Load from file
            if os.path.exists(FILE_LAPORAN):
                with open(FILE_LAPORAN, "r") as file:
                    for line in file:
                        parts = line.strip().split(":")
                        if len(parts) >= 8:
                            id_karyawan = parts[0]
                            nama = parts[1]
                            status = parts[2]
                            judul = parts[3]
                            tanggal = parts[4]
                            status_laporan = parts[6]
                            
                            # Apply filter if not "Semua"
                            if filter_status == "Semua" or status_laporan == filter_status:
                                report_tree.insert("", "end", values=(
                                    id_karyawan, nama, status, judul, tanggal, status_laporan
                                ))
        
        # Initial load
        load_reports()
    
    def load_karyawan_data(self, tree):
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
            
        # Load from file
        if os.path.exists(FILE_USER):
            with open(FILE_USER, "r") as file:
                for line in file:
                    data = line.strip().split(":")
                    if len(data) >= 5:
                        nama, id_karyawan, _, status, gaji = data
                        tree.insert("", "end", values=(id_karyawan, nama, status, f"Rp{int(gaji):,}"))
    
    def tambah_karyawan(self, parent):
        dialog = Toplevel(parent)
        dialog.title("Tambah Karyawan")
        dialog.geometry("400x350")
        dialog.grab_set()
        dialog.configure(bg=self.theme.bg_color)
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_color)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="TAMBAH KARYAWAN BARU", 
                font=self.theme.heading_font,
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=10).pack()
        
        # Form Content
        content_frame = tk.Frame(dialog, bg=self.theme.bg_color, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        form = tk.Frame(content_frame, bg=self.theme.bg_color)
        form.pack(pady=10)
        
        tk.Label(form, text="Nama:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=0, column=0, sticky="w", pady=5)
        nama_entry = tk.Entry(form, width=30, font=self.theme.text_font)
        nama_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(form, text="Password:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=1, column=0, sticky="w", pady=5)
        password_entry = tk.Entry(form, width=30, show="*", font=self.theme.text_font)
        password_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(form, text="Status:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=2, column=0, sticky="w", pady=5)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(form, width=28, textvariable=status_var)
        status_combo['values'] = ('Admin', 'Human Resource', 'Cleaning Service', 'Internship', 'Marketing')
        status_combo.grid(row=2, column=1, pady=5)
        status_combo.current(0)
        
        tk.Label(form, text="Gaji Pokok:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=3, column=0, sticky="w", pady=5)
        gaji_entry = tk.Entry(form, width=30, font=self.theme.text_font)
        gaji_entry.grid(row=3, column=1, pady=5)
        gaji_entry.insert(0, "3000000")
        
        def do_tambah():
            nama = nama_entry.get().strip()
            password = password_entry.get().strip()
            status = status_var.get()
            gaji = gaji_entry.get().strip()
            
            if not nama or not password or not status or not gaji:
                messagebox.showerror("Error", "Semua field harus diisi!")
                return
            
            try:
                gaji_int = int(gaji)
            except ValueError:
                messagebox.showerror("Error", "Gaji harus berupa angka!")
                return
            
            # Generate ID (last ID + 1)
            new_id = "1001"  # Default if no file
            if os.path.exists(FILE_USER):
                with open(FILE_USER, "r") as file:
                    lines = file.readlines()
                    if lines:
                        last_line = lines[-1].strip().split(":")
                        if len(last_line) >= 2:
                            try:
                                new_id = str(int(last_line[1]) + 1)
                            except ValueError:
                                pass
            
            # Tambah karyawan baru
            with open(FILE_USER, "a") as file:
                file.write(f"{nama}:{new_id}:{password}:{status}:{gaji}\n")
            
            messagebox.showinfo("Sukses", f"Karyawan {nama} berhasil ditambahkan dengan ID {new_id}")
            dialog.destroy()
        
        button_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Tambah", width=15, command=do_tambah,
                 bg=self.theme.primary_color, fg=self.theme.light_text,
                 font=self.theme.text_font, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Batal", width=15, command=dialog.destroy,
                 bg=self.theme.danger_color, fg=self.theme.light_text,
                 font=self.theme.text_font, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=5)
    
    def ubah_status(self, parent):
        # Get the tree widget (should be the last child)
        tree = None
        for child in parent.winfo_children():
            if isinstance(child, tk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Treeview):
                        tree = subchild
                        break
        
        if not tree:
            messagebox.showerror("Error", "Tidak dapat menemukan data karyawan!")
            return
            
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih karyawan terlebih dahulu!")
            return
            
        item = tree.item(selected[0])
        id_karyawan = item['values'][0]
        nama = item['values'][1]
        current_status = item['values'][2]
        
        dialog = Toplevel(parent)
        dialog.title("Ubah Status")
        dialog.geometry("350x200")
        dialog.grab_set()
        dialog.configure(bg=self.theme.bg_color)
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_color)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="UBAH STATUS KARYAWAN", 
                font=self.theme.heading_font,
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=10).pack()
        
        # Form Content
        content_frame = tk.Frame(dialog, bg=self.theme.bg_color, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        form = tk.Frame(content_frame, bg=self.theme.bg_color)
        form.pack(pady=10)
        
        tk.Label(form, text="Nama:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(form, text=nama, bg=self.theme.bg_color, fg=self.theme.primary_color, font=self.theme.text_font).grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(form, text="Status Sekarang:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(form, text=current_status, bg=self.theme.bg_color, fg=self.theme.primary_color, font=self.theme.text_font).grid(row=1, column=1, sticky="w", pady=5)
        
        tk.Label(form, text="Status Baru:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=2, column=0, sticky="w", pady=5)
        new_status_var = tk.StringVar()
        new_status_combo = ttk.Combobox(form, width=28, textvariable=new_status_var)
        new_status_combo['values'] = ('Admin', 'Human Resource', 'Cleaning Service', 'Internship', 'Marketing')
        new_status_combo.grid(row=2, column=1, pady=5)
        new_status_combo.current(0)
        
        def do_ubah():
            new_status = new_status_var.get()
            
            if not new_status:
                messagebox.showerror("Error", "Pilih status baru!")
                return
                
            # Update file
            updated_lines = []
            with open(FILE_USER, "r") as file:
                for line in file:
                    data = line.strip().split(":")
                    if len(data) >= 5 and data[1] == str(id_karyawan):
                        # Update status
                        data[3] = new_status
                        updated_line = ":".join(data)
                        updated_lines.append(updated_line + "\n")
                    else:
                        updated_lines.append(line)
            
            with open(FILE_USER, "w") as file:
                file.writelines(updated_lines)
                
            messagebox.showinfo("Sukses", f"Status {nama} berhasil diubah menjadi {new_status}")
            dialog.destroy()
            
            # Refresh treeview
            self.load_karyawan_data(tree)
        
        button_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Simpan", width=15, command=do_ubah,
                 bg=self.theme.primary_color, fg=self.theme.light_text,
                 font=self.theme.text_font, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Batal", width=15, command=dialog.destroy,
                 bg=self.theme.danger_color, fg=self.theme.light_text,
                 font=self.theme.text_font, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=5)
    
    def ubah_gaji(self, parent):
        # Get the tree widget
        tree = None
        for child in parent.winfo_children():
            if isinstance(child, tk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Treeview):
                        tree = subchild
                        break
        
        if not tree:
            messagebox.showerror("Error", "Tidak dapat menemukan data karyawan!")
            return
            
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih karyawan terlebih dahulu!")
            return
            
        item = tree.item(selected[0])
        id_karyawan = item['values'][0]
        nama = item['values'][1]
        current_gaji = item['values'][3].replace("Rp", "").replace(",", "")
        
        dialog = Toplevel(parent)
        dialog.title("Ubah Gaji")
        dialog.geometry("350x200")
        dialog.grab_set()
        dialog.configure(bg=self.theme.bg_color)
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_color)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="UBAH GAJI KARYAWAN", 
                font=self.theme.heading_font,
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=10).pack()
        
        # Form Content
        content_frame = tk.Frame(dialog, bg=self.theme.bg_color, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        form = tk.Frame(content_frame, bg=self.theme.bg_color)
        form.pack(pady=10)
        
        tk.Label(form, text="Nama:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(form, text=nama, bg=self.theme.bg_color, fg=self.theme.primary_color, font=self.theme.text_font).grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(form, text="Gaji Sekarang:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(form, text=f"Rp{int(current_gaji):,}", bg=self.theme.bg_color, fg=self.theme.primary_color, font=self.theme.text_font).grid(row=1, column=1, sticky="w", pady=5)
        
        tk.Label(form, text="Gaji Baru:", bg=self.theme.bg_color, fg=self.theme.text_color, font=self.theme.text_font).grid(row=2, column=0, sticky="w", pady=5)
        gaji_entry = tk.Entry(form, width=20, font=self.theme.text_font)
        gaji_entry.grid(row=2, column=1, pady=5)
        gaji_entry.insert(0, current_gaji)
        
        def do_ubah():
            try:
                new_gaji = int(gaji_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Gaji harus berupa angka!")
                return
                
            # Update file
            updated_lines = []
            with open(FILE_USER, "r") as file:
                for line in file:
                    data = line.strip().split(":")
                    if len(data) >= 5 and data[1] == str(id_karyawan):
                        # Update gaji
                        data[4] = str(new_gaji)
                        updated_line = ":".join(data)
                        updated_lines.append(updated_line + "\n")
                    else:
                        updated_lines.append(line)
            
            with open(FILE_USER, "w") as file:
                file.writelines(updated_lines)
                
            messagebox.showinfo("Sukses", f"Gaji {nama} berhasil diubah menjadi Rp{new_gaji:,}")
            dialog.destroy()
            
            # Refresh treeview
            self.load_karyawan_data(tree)
        
        button_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Simpan", width=15, command=do_ubah,
                 bg=self.theme.primary_color, fg=self.theme.light_text,
                 font=self.theme.text_font, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Batal", width=15, command=dialog.destroy,
                 bg=self.theme.danger_color, fg=self.theme.light_text,
                 font=self.theme.text_font, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=5)
    
    def menu_kelola_perizinan(self):
        if not isinstance(self.controller.current_user, (Manager, HumanResource)):
            messagebox.showerror("Error", "Anda tidak memiliki akses!")
            return
            
        top = Toplevel(self)
        top.title("Kelola Perizinan")
        top.geometry("800x500")
        top.configure(bg=self.theme.bg_color)
        
        # Header
        header_frame = tk.Frame(top, bg=self.theme.primary_color)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="KELOLA PERIZINAN KARYAWAN", 
                font=self.theme.heading_font,
                bg=self.theme.primary_color,
                fg=self.theme.light_text,
                padx=20, pady=10).pack(side=tk.LEFT)
        
        # Content
        content_frame = tk.Frame(top, bg=self.theme.bg_color, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Treeview untuk menampilkan data izin
        columns = ("ID", "Nama", "Status", "Alasan", "Dari", "Sampai", "Waktu Pengajuan", "Status Izin")
        tree = ttk.Treeview(content_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=90)
        
        tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Load data izin
        self.load_izin_data(tree)
        
        # Frame untuk tombol action
        btn_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Setujui", width=15, 
                 command=lambda: self.update_izin_status(tree, "Disetujui"),
                 bg=self.theme.success_color, fg=self.theme.light_text,
                 font=self.theme.text_font, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Tolak", width=15,
                 command=lambda: self.update_izin_status(tree, "Ditolak"),
                 bg=self.theme.danger_color, fg=self.theme.light_text,
                 font=self.theme.text_font, relief=tk.FLAT, padx=10, pady=5).pack(side=tk.LEFT, padx=10)
    
    def load_izin_data(self, tree):
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
            
        # Load from file
        if os.path.exists(FILE_IZIN):
            with open(FILE_IZIN, "r") as file:
                for line in file:
                    data = line.strip().split(":")
                    if len(data) >= 8:
                        tree.insert("", "end", values=data)
    
    def update_izin_status(self, tree, new_status):
        # Get selected item
        selected = tree.selection()
        
        if not selected:
            messagebox.showerror("Error", "Pilih data izin terlebih dahulu!")
            return
            
        item = tree.item(selected[0])
        values = item['values']
        id_karyawan = values[0]
        nama = values[1]
        
        # Update file
        updated_lines = []
        with open(FILE_IZIN, "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(":")
                if len(data) >= 8 and data[0] == str(id_karyawan) and data[1] == nama:
                    # Update status izin (index 7)
                    data[7] = new_status
                    updated_line = ":".join(data)
                    updated_lines.append(updated_line + "\n")
                else:
                    updated_lines.append(line)
        
        with open(FILE_IZIN, "w") as file:
            file.writelines(updated_lines)
            
        messagebox.showinfo("Sukses", f"Status izin {nama} berhasil diubah menjadi {new_status}")
        
        # Refresh treeview
        self.load_izin_data(tree)
    
    def menu_kelola_gaji(self):
        if not isinstance(self.controller.current_user, HumanResource):
            messagebox.showerror("Error", "Anda tidak memiliki akses!")
            return
            
        # Use the same interface as kelola karyawan but focus on salary
        self.menu_kelola_karyawan()
    
    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Karyawan")
        self.geometry("900x650")
        self.resizable(True, True)
        self.current_user = None
        
        # Initialize theme
        self.theme = AppTheme()
        self.theme.configure_ttk_styles()
        self.configure(bg=self.theme.bg_color)
        
        # Set custom icon (placeholder)
        # self.iconbitmap('icon.ico')  # Uncomment if you have an icon
        
        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Frame container
        container = tk.Frame(self, bg=self.theme.bg_color)
        container.pack(fill="both", expand=True)
        
        # Setup frames
        self.frames = {}
        for F in (LoginPage, MainMenuPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.show_frame("LoginPage")
        
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        
        # Call on_show_frame if exists
        if hasattr(frame, "on_show_frame"):
            frame.on_show_frame()

# --- MAIN PROGRAM ---
if __name__ == "__main__":
    # Create files if not exist
    for file in [FILE_USER, FILE_ABSENSI, FILE_IZIN, FILE_LAPORAN]:
        if not os.path.exists(file):
            open(file, 'w').close()
    
    # Create default admin if user file is empty
    if os.path.getsize(FILE_USER) == 0:
        with open(FILE_USER, "w") as file:
            file.write("admin:1001:admin123:Admin:5000000\n")
            file.write("manager:1002:manager123:Manager:8000000\n")
            file.write("hr:1003:hr123:Human Resource:6000000\n")
    
    app = App()
    app.mainloop()