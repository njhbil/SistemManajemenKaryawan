import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Toplevel, scrolledtext, font
import os
import platform
from datetime import datetime
from abc import ABC, abstractmethod
import math
import time
import traceback
from tkinter import PhotoImage
import random

# File paths for Hotel Management System
FILE_USER = "Staff.txt"           # Staff login data
FILE_ABSENSI = "Attendance.txt"   # Staff attendance records
FILE_IZIN = "Leaves.txt"          # Leave requests
FILE_LAPORAN = "Reports.txt"      # Reports and feedback
FILE_CHECKIN = "CheckIn.txt"      # Guest check-in records

# Default staff data initialization function
def initialize_default_staff():
    """Initialize default staff data if Staff.txt doesn't exist or is empty"""
    # Check if file doesn't exist or is empty
    if not os.path.exists(FILE_USER) or os.path.getsize(FILE_USER) == 0:
        with open(FILE_USER, "w") as file:
            # format: nama:id:password:status:gaji
            file.write("manager:1001:manager123:Manager:8000000\n")
            file.write("admin:1002:admin123:Admin:7000000\n")
            file.write("hr:1003:hr123:HumanResource:6500000\n")
            file.write("cleaning:1004:clean123:CleaningService:4000000\n")
            file.write("marketing:1005:market123:Marketing:5500000\n")
            file.write("intern:1006:intern123:Internship:3000000\n")
        print("Default staff data initialized successfully!")

# Abstract Staff class as parent class for Hotel Staff
class Staff(ABC):
    def __init__(self, nama, idStaff, password, status, gaji):
        self._nama = nama              # protected attribute
        self._idStaff = idStaff        # protected attribute
        self.__password = password     # private attribute
        self.__status = status         # private attribute
        self.__gaji = gaji             # private attribute
    
    def attendance_checkin(self):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hasil_absensi = f"{self._idStaff}:{self._nama}:{self.__status}:{waktu}\n"
        
        # Save to attendance file
        with open(FILE_ABSENSI, "a") as file:
            file.write(hasil_absensi)
            
        return f"{self._nama} (ID: {self._idStaff}) checked in at {waktu}"
    
    def login(self, nama, idStaff, password):
        # Login validation
        return self._nama == nama and self._idStaff == idStaff and self.__password == password
    
    def request_leave(self):
        return "Leave request submitted"
    
    def submit_report(self, isi_laporan, judul="Daily Report"):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Format: id:nama:status:judul:waktu:isi_laporan:status_laporan:catatan
        data_laporan = f"{self._idStaff}:{self._nama}:{self.__status}:{judul}:{waktu}:{isi_laporan}:Pending:-\n"
        
        with open(FILE_LAPORAN, "a") as file:
            file.write(data_laporan)
        
        return f"Report successfully submitted to Management at {waktu}"        
    
    @abstractmethod
    def display_salary(self):
        pass
    
    # Setter methods
    def setNama(self, nama):
        self._nama = nama
        
    def setIdStaff(self, idStaff):
        self._idStaff = idStaff
        
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
        return self._idStaff
        
    def getStatus(self):
        return self.__status
        
    def getGaji(self):
        return self.__gaji

# Staff Classes
class Manager(Staff):
    def __init__(self, nama, idStaff, password, gaji):
        super().__init__(nama, idStaff, password, "Manager", gaji)
    
    def attendance_checkin(self):
        return super().attendance_checkin()
    
    def attendance_summary(self):
        # Display attendance summary from file
        if not os.path.exists(FILE_ABSENSI):
            return "No attendance data available"
            
        hasil = "ATTENDANCE SUMMARY:\n"
        with open(FILE_ABSENSI, "r") as file:
            for line in file:
                hasil += line
                
        return hasil
    
    def rekapAbsensi(self):
        return self.attendance_summary()
    
    def display_salary(self):
        return f"Manager {self._nama} Salary: ${self.getGaji():,}"
        
    def review_laporan(self, id_laporan, status, catatan):
        updated_lines = []
        with open(FILE_LAPORAN, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) >= 8 and parts[0] == id_laporan:
                    parts[6] = status  # Update status
                    parts[7] = catatan  # Update notes
                    updated_line = ":".join(parts)
                    updated_lines.append(updated_line + "\n")
                else:
                    updated_lines.append(line)
        
        with open(FILE_LAPORAN, "w") as file:
            file.writelines(updated_lines)
        
        return f"Report ID {id_laporan} has been {status.lower()} with notes: {catatan}"

class Admin(Staff):
    def __init__(self, nama, idStaff, password, gaji):
        super().__init__(nama, idStaff, password, "Admin", gaji)
    
    def attendance_checkin(self):
        return super().attendance_checkin()
    
    def display_salary(self):
        return f"Admin {self._nama} Salary: ${self.getGaji():,}"
    
    def manage_all_staff(self):
        return "Admin has access to all staff management functions"
    
    def rekapAbsensi(self):
        if not os.path.exists(FILE_ABSENSI):
            return "No attendance data available"
            
        hasil = "ATTENDANCE SUMMARY:\n"
        with open(FILE_ABSENSI, "r") as file:
            for line in file:
                hasil += line
                
        return hasil
    
    def review_laporan(self, id_laporan, status, catatan):
        updated_lines = []
        with open(FILE_LAPORAN, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) >= 8 and parts[0] == id_laporan:
                    parts[6] = status  # Update status
                    parts[7] = catatan  # Update notes
                    updated_line = ":".join(parts)
                    updated_lines.append(updated_line + "\n")
                else:
                    updated_lines.append(line)
        
        with open(FILE_LAPORAN, "w") as file:
            file.writelines(updated_lines)
        
        return f"Report ID {id_laporan} has been {status.lower()} with notes: {catatan}"
    
    def system_admin_report(self, isi_laporan):
        return self.submit_report(isi_laporan, "System Administration Report")

class HumanResource(Staff):
    def __init__(self, nama, idStaff, password, gaji):
        super().__init__(nama, idStaff, password, "HumanResource", gaji)
    
    def attendance_checkin(self):
        return super().attendance_checkin()
    
    def display_salary(self):
        return f"HR {self._nama} Salary: ${self.getGaji():,}"
    
    def manage_employee_data(self):
        return "HR manages employee data and policies"
    
    def manage_leaves(self):
        return True
    
    def manage_payroll(self):
        return "Managing staff payroll"
    
    def rekapAbsensi(self):
        if not os.path.exists(FILE_ABSENSI):
            return "No attendance data available"
            
        hasil = "ATTENDANCE SUMMARY:\n"
        with open(FILE_ABSENSI, "r") as file:
            for line in file:
                hasil += line
                
        return hasil
    
    def hr_report(self, isi_laporan):
        return self.submit_report(isi_laporan, "Human Resource Report")

class CleaningService(Staff):
    def __init__(self, nama, idStaff, password, gaji):
        super().__init__(nama, idStaff, password, "CleaningService", gaji)
    
    def attendance_checkin(self):
        return super().attendance_checkin()
    
    def display_salary(self):
        return f"Cleaning Staff {self._nama} Salary: ${self.getGaji():,}"
    
    def room_service_report(self, isi_laporan):
        return self.submit_report(isi_laporan, "Room Service Report")
    
    def cleaning_task_report(self, area, isi_laporan):
        return self.submit_report(f"Area: {area} - {isi_laporan}", "Cleaning Service Report")

class Marketing(Staff):
    def __init__(self, nama, idStaff, password, gaji):
        super().__init__(nama, idStaff, password, "Marketing", gaji)
    
    def attendance_checkin(self):
        return super().attendance_checkin()
    
    def display_salary(self):
        # Marketing gets commission bonus
        return f"Marketing {self._nama} Salary: ${self.getGaji() * 1.15:,}"
    
    def marketing_campaign_report(self, isi_laporan):
        return self.submit_report(isi_laporan, "Marketing Campaign Report")

class Internship(Staff):
    def __init__(self, nama, idStaff, password, gaji):
        super().__init__(nama, idStaff, password, "Internship", gaji)
    
    def attendance_checkin(self):
        return super().attendance_checkin()
    
    def display_salary(self):
        return f"Intern {self._nama} Allowance: ${self.getGaji():,}"
    
    def guest_service_report(self, isi_laporan):
        return self.submit_report(isi_laporan, "Guest Service Report")
    
    def intern_learning_report(self, isi_laporan):
        return self.submit_report(isi_laporan, "Internship Learning Report")

# Theme configuration for luxury hotel interface
class HotelTheme:
    def __init__(self):
        # Color palette inspired by luxury hotels
        self.primary_gold = "#FFB000"        # Luxury gold
        self.secondary_gold = "#FFD700"      # Bright gold
        self.accent_copper = "#B87333"       # Copper accent
        self.system_background = "#1A1A1A"   # Rich black
        self.surface_dark = "#2D2D2D"        # Dark surface
        self.surface_light = "#3A3A3A"       # Light surface
        self.text_primary = "#FFFFFF"        # White text
        self.text_secondary = "#CCCCCC"      # Light gray text
        self.success_emerald = "#50C878"     # Emerald green
        self.warning_amber = "#FFBF00"       # Amber warning
        self.danger_ruby = "#E0115F"         # Ruby red
          # Font configuration
        self.font_brand = ("Segoe UI", 24, "bold")
        self.font_title = ("Segoe UI", 18, "bold")
        self.font_heading = ("Segoe UI", 12, "bold")
        self.font_body = ("Segoe UI", 10)
        self.font_small = ("Segoe UI", 8)

# Class untuk aplikasi utama
class SistemManajemenKaryawan(tk.Tk):
    def __init__(self):
        super().__init__()
        self.theme = HotelTheme()
        
        # Setup window
        self.title("Employee Management System")
        self.geometry("1024x768")
        self.configure(bg=self.theme.system_background)
        
        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Container for frames
        container = tk.Frame(self, bg=self.theme.system_background)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to store frames
        self.frames = {}
        
        # Initialize frames
        for F in (LoginPage, MainMenuPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show login page first
        self.show_frame(LoginPage)
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.theme = controller.theme
        self.configure(bg=self.theme.system_background)
          # UI Components
        header_frame = tk.Frame(self, bg=self.theme.primary_gold)
        header_frame.pack(fill="x", pady=0)
        
        tk.Label(header_frame, 
                text="🏨 LUXURY HOTEL MANAGEMENT SYSTEM", 
                font=self.theme.font_brand,
                bg=self.theme.primary_gold,
                fg=self.theme.system_background,
                padx=20, pady=20).pack()
        
        # Main container
        container = tk.Frame(self, bg=self.theme.system_background)
        container.pack(fill="both", expand=True, padx=20, pady=20)
          # Left side - Welcome info with improved layout
        welcome_container = tk.Frame(container, bg=self.theme.surface_dark,
                                    highlightbackground=self.theme.primary_gold,
                                    highlightthickness=2, padx=15, pady=15)
        welcome_container.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))
        
        # Main welcome header (spans full width)
        header_frame = tk.Frame(welcome_container, bg=self.theme.surface_dark)
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="🌟 WELCOME TO LUXURY HOTEL", 
                font=self.theme.font_title,
                bg=self.theme.surface_dark,
                fg=self.theme.primary_gold).pack()
        
        # Live clock centered under header
        self.create_live_clock(header_frame)
        
        # Content area with three columns
        content_frame = tk.Frame(welcome_container, bg=self.theme.surface_dark)
        content_frame.pack(fill="both", expand=True)
        
        # Configure column weights for proper distribution
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_columnconfigure(2, weight=1)
        
        # Left column - System Overview
        left_column = tk.Frame(content_frame, bg=self.theme.surface_dark, padx=10)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        tk.Label(left_column, text="📊 SYSTEM OVERVIEW", 
                font=self.theme.font_heading,
                bg=self.theme.surface_dark,
                fg=self.theme.accent_copper).pack(pady=(0, 10))
        
        stats_info = self.get_system_stats()
        for stat in stats_info:
            tk.Label(left_column, text=stat, 
                    font=self.theme.font_body,
                    bg=self.theme.surface_dark,
                    fg=self.theme.text_secondary).pack(anchor="w", pady=2)
        
        # Center column - Premium Features (first half)
        center_column = tk.Frame(content_frame, bg=self.theme.surface_dark, padx=10)
        center_column.grid(row=0, column=1, sticky="nsew", padx=5)
        
        tk.Label(center_column, text="✨ PREMIUM FEATURES", 
                font=self.theme.font_heading,
                bg=self.theme.surface_dark,
                fg=self.theme.primary_gold).pack(pady=(0, 10))
        
        features_part1 = [
            "🔐 Secure Staff Authentication",
            "⏰ Real-time Attendance Tracking", 
            "📋 Advanced Report Management"
        ]
        
        for feature in features_part1:
            tk.Label(center_column, text=feature, 
                    font=self.theme.font_body,
                    bg=self.theme.surface_dark,
                    fg=self.theme.text_secondary).pack(anchor="w", pady=2)
        
        # Right column - Premium Features (second half)
        right_column = tk.Frame(content_frame, bg=self.theme.surface_dark, padx=10)
        right_column.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        tk.Label(right_column, text="🎯 ADVANCED TOOLS", 
                font=self.theme.font_heading,
                bg=self.theme.surface_dark,
                fg=self.theme.success_emerald).pack(pady=(0, 10))
        
        features_part2 = [
            "💰 Automated Payroll System",
            "🏖️ Smart Leave Management",
            "📊 Executive Analytics Dashboard"
        ]
        
        for feature in features_part2:
            tk.Label(right_column, text=feature, 
                    font=self.theme.font_body,
                    bg=self.theme.surface_dark,
                    fg=self.theme.text_secondary).pack(anchor="w", pady=2)
          # Right side - Login form
        login_frame = tk.Frame(container, bg=self.theme.surface_dark,
                              highlightbackground=self.theme.primary_gold,
                              highlightthickness=2, padx=20, pady=20)
        login_frame.pack(side=tk.RIGHT, fill="y", padx=(10, 0))
        
        tk.Label(login_frame, text="🔑 STAFF LOGIN", 
                font=self.theme.font_title,
                bg=self.theme.surface_dark,
                fg=self.theme.primary_gold).pack(pady=(0, 20))
        
        # Username
        tk.Label(login_frame, text="Staff Name:", 
                bg=self.theme.surface_dark,
                fg=self.theme.text_primary,
                font=self.theme.font_body).pack(anchor="w")
        self.username_entry = tk.Entry(login_frame, width=25, 
                                     font=self.theme.font_body,
                                     bg=self.theme.surface_light,
                                     fg=self.theme.text_primary,
                                     insertbackground=self.theme.primary_gold,
                                     relief=tk.FLAT, bd=0)
        self.username_entry.pack(fill="x", pady=(0, 15))
        
        # Staff ID
        tk.Label(login_frame, text="Staff ID:", 
                bg=self.theme.surface_dark,
                fg=self.theme.text_primary,
                font=self.theme.font_body).pack(anchor="w")
        self.id_entry = tk.Entry(login_frame, width=25, 
                               font=self.theme.font_body,
                               bg=self.theme.surface_light,
                               fg=self.theme.text_primary,
                               insertbackground=self.theme.primary_gold,
                               relief=tk.FLAT, bd=0)
        self.id_entry.pack(fill="x", pady=(0, 15))
        
        # Password
        tk.Label(login_frame, text="Password:", 
                bg=self.theme.surface_dark,
                fg=self.theme.text_primary,
                font=self.theme.font_body).pack(anchor="w")
        self.password_entry = tk.Entry(login_frame, width=25, show="*", 
                                     font=self.theme.font_body,
                                     bg=self.theme.surface_light,
                                     fg=self.theme.text_primary,
                                     insertbackground=self.theme.primary_gold,
                                     relief=tk.FLAT, bd=0)
        self.password_entry.pack(fill="x", pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(login_frame, bg=self.theme.surface_dark)
        button_frame.pack(pady=10)
        
        login_btn = tk.Button(button_frame, text="🚀 LOGIN", width=15, 
                            command=self.do_login,
                            bg=self.theme.primary_gold,
                            fg=self.theme.system_background,
                            font=self.theme.font_heading,
                            relief=tk.FLAT, padx=10, pady=8,
                            cursor="hand2")
        login_btn.pack(pady=(0, 10))
        
        exit_btn = tk.Button(button_frame, text="❌ EXIT", width=15, 
                           command=self.controller.destroy,
                           bg=self.theme.danger_ruby,
                           fg=self.theme.text_primary,
                           font=self.theme.font_heading,
                           relief=tk.FLAT, padx=10, pady=8,
                           cursor="hand2")
        exit_btn.pack()
          # Default login info
        info_frame = tk.Frame(login_frame, bg=self.theme.surface_dark)
        info_frame.pack(pady=(20, 0))
        
        # tk.Label(info_frame, text="🔍 DEFAULT LOGIN:", 
        #         font=self.theme.font_small,
        #         bg=self.theme.surface_dark,
        #         fg=self.theme.warning_amber).pack()
    
    
    def create_live_clock(self, parent):
        """Create a live clock display"""
        # Create clock frame
        clock_frame = tk.Frame(parent, bg=self.theme.surface_dark)
        clock_frame.pack(pady=(10, 15))
        
        # Clock label
        self.clock_label = tk.Label(clock_frame, 
                                   font=self.theme.font_heading,
                                   bg=self.theme.surface_dark,
                                   fg=self.theme.primary_gold)
        self.clock_label.pack()
        
        # Update clock
        self.update_clock()
    
    def update_clock(self):
        """Update the live clock display"""
        current_time = datetime.now().strftime("🕐 %H:%M:%S\n📅 %A, %B %d, %Y")
        if hasattr(self, 'clock_label'):
            self.clock_label.configure(text=current_time)
            # Schedule next update
            self.after(1000, self.update_clock)
    
    def get_system_stats(self):
        """Get current system statistics"""
        stats = []
        
        try:
            # Count total staff
            staff_count = 0
            if os.path.exists(FILE_USER):
                with open(FILE_USER, "r") as file:
                    staff_count = len(file.readlines())
            stats.append(f"👥 Total Staff: {staff_count}")
            
            # Count attendance records today
            today = datetime.now().strftime("%Y-%m-%d")
            attendance_today = 0
            if os.path.exists(FILE_ABSENSI):
                with open(FILE_ABSENSI, "r") as file:
                    for line in file:
                        if today in line:
                            attendance_today += 1
            stats.append(f"✅ Check-ins Today: {attendance_today}")
            
            # Count pending leave requests
            pending_leaves = 0
            if os.path.exists(FILE_IZIN):
                with open(FILE_IZIN, "r") as file:
                    for line in file:
                        if "Pending" in line:
                            pending_leaves += 1
            stats.append(f"📋 Pending Leaves: {pending_leaves}")
            
            # Count pending reports
            pending_reports = 0
            if os.path.exists(FILE_LAPORAN):
                with open(FILE_LAPORAN, "r") as file:
                    for line in file:
                        if "Pending" in line:
                            pending_reports += 1
            stats.append(f"📊 Pending Reports: {pending_reports}")
            
        except Exception as e:
            stats.append("📊 System Stats Loading...")
        
        return stats
    
    def do_login(self):
        username = self.username_entry.get().strip()
        id_karyawan = self.id_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not id_karyawan or not password:
            messagebox.showerror("Error", "All fields must be filled!")
            return
            
        # Ensure staff data exists (double check)
        initialize_default_staff()
        
        # Verifikasi login
        with open(FILE_USER, "r") as file:
            for line in file:
                data = line.strip().split(":")
                if len(data) >= 5:
                    saved_user, saved_id, saved_pass, saved_status, saved_gaji = data
                    if username == saved_user and id_karyawan == saved_id and password == saved_pass:
                        # Create objects based on staff role
                        if saved_status == "Manager":
                            user = Manager(saved_user, saved_id, saved_pass, int(saved_gaji))
                        elif saved_status == "Admin":
                            user = Admin(saved_user, saved_id, saved_pass, int(saved_gaji))
                        elif saved_status == "HumanResource":
                            user = HumanResource(saved_user, saved_id, saved_pass, int(saved_gaji))
                        elif saved_status == "CleaningService":
                            user = CleaningService(saved_user, saved_id, saved_pass, int(saved_gaji))
                        elif saved_status == "Marketing":
                            user = Marketing(saved_user, saved_id, saved_pass, int(saved_gaji))
                        elif saved_status == "Internship":
                            user = Internship(saved_user, saved_id, saved_pass, int(saved_gaji))
                        else:
                            user = None
                            
                        if user:
                            self.controller.current_user = user
                            messagebox.showinfo("Login Successful", f"Welcome {saved_user}")
                            self.controller.show_frame(MainMenuPage)
                            return
        
        messagebox.showerror("Login Failed", "Username, ID, or password is incorrect!")

class MainMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.theme = controller.theme
        self.configure(bg=self.theme.system_background)
        
        # Header Frame with hotel luxury design
        header_frame = tk.Frame(self, bg=self.theme.primary_gold)
        header_frame.pack(fill="x", pady=0)
        
        self.title_label = tk.Label(header_frame, 
                                  text="🏨 HOTEL MANAGEMENT DASHBOARD", 
                                  font=self.theme.font_title,
                                  bg=self.theme.primary_gold, 
                                  fg=self.theme.system_background,
                                  padx=20, pady=15)
        self.title_label.pack(side=tk.LEFT)
        
        # Logout button in header with luxury styling
        logout_btn = tk.Button(header_frame, 
                              text="LOGOUT", 
                              command=self.logout,
                              bg=self.theme.danger_ruby,
                              fg=self.theme.text_primary,
                              font=self.theme.font_heading,
                              relief=tk.FLAT, padx=15, pady=8,
                              cursor="hand2")
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # User info frame with elegant styling
        user_frame = tk.Frame(self, bg=self.theme.system_background)
        user_frame.pack(fill="x", padx=20, pady=15)
        
        self.status_label = tk.Label(user_frame, 
                                   text="", 
                                   font=self.theme.font_body,
                                   bg=self.theme.system_background,
                                   fg=self.theme.text_secondary)
        self.status_label.pack(anchor="w")
        
        # Create luxurious tabbed interface
        style = ttk.Style()
        style.configure("Hotel.TNotebook", background=self.theme.system_background, borderwidth=0)
        style.configure("Hotel.TNotebook.Tab", 
                       background=self.theme.surface_dark,
                       foreground=self.theme.text_secondary,
                       padding=[20, 12],
                       font=self.theme.font_heading)
        style.map("Hotel.TNotebook.Tab",
                 background=[("selected", self.theme.primary_gold)],
                 foreground=[("selected", self.theme.system_background)])
        
        self.notebook = ttk.Notebook(self, style="Hotel.TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Tab 1: Essential Hotel Operations
        essential_tab = tk.Frame(self.notebook, bg=self.theme.system_background)
        self.notebook.add(essential_tab, text="🏨 Essential Operations")
        
        # Create elegant hotel operation cards
        self._create_luxury_card(essential_tab, "⏰ Check In/Out", "Staff attendance tracking", 
                         self.menu_checkin_checkout, 0, 0)
        
        self._create_luxury_card(essential_tab, "💰 View Salary", "Your compensation details", 
                         self.menu_gaji, 0, 1)
        
        self._create_luxury_card(essential_tab, "🏖️ Request Leave", "Time off requests", 
                         self.menu_izin, 1, 0)
        
        self._create_luxury_card(essential_tab, "📋 Submit Report", "Daily work reports", 
                         self.menu_laporan, 1, 1)
        
        # Tab 2: Management Functions
        management_tab = tk.Frame(self.notebook, bg=self.theme.system_background)
        self.notebook.add(management_tab, text="👑 Management")
        
        self._create_luxury_card(management_tab, "📊 Attendance Summary", "Staff attendance overview", 
                         self.menu_attendance_report, 0, 0)
        
        self._create_luxury_card(management_tab, "👥 Manage Staff", "Hotel staff administration", 
                         self.menu_kelola_karyawan, 0, 1)
        
        self._create_luxury_card(management_tab, "✅ Approve Leaves", "Leave request approvals", 
                         self.menu_kelola_perizinan, 1, 0)
        
        self._create_luxury_card(management_tab, "💼 Payroll Management", "Staff salary management", 
                         self.menu_kelola_gaji, 1, 1)
        
        # Tab 3: Executive Functions
        executive_tab = tk.Frame(self.notebook, bg=self.theme.system_background)
        self.notebook.add(executive_tab, text="🎯 Executive")
        
        self._create_luxury_card(executive_tab, "📈 Review Reports", "Staff report evaluation", 
                         self.menu_review_laporan, 0, 0)
        
        self._create_luxury_card(executive_tab, "📊 Analytics Dashboard", "Performance insights", 
                         self.menu_team_analytics, 0, 1)
        
        self._create_luxury_card(executive_tab, "🔔 Send Notifications", "Staff communications", 
                         self.menu_send_notification, 1, 0)
    
    def _create_luxury_card(self, parent, title, description, command, row, col):
        """Create a luxury-styled card for hotel operations"""
        card_frame = tk.Frame(parent, bg=self.theme.surface_dark, 
                             highlightbackground=self.theme.primary_gold,
                             highlightthickness=1, padx=20, pady=15)
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Configure grid weights for responsiveness
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Title
        title_label = tk.Label(card_frame, text=title, 
                              font=self.theme.font_heading,
                              bg=self.theme.surface_dark,
                              fg=self.theme.primary_gold)
        title_label.pack(pady=(0, 5))
        
        # Description
        desc_label = tk.Label(card_frame, text=description, 
                             font=self.theme.font_body,
                             bg=self.theme.surface_dark,
                             fg=self.theme.text_secondary,
                             wraplength=200)
        desc_label.pack(pady=(0, 15))
        
        # Action button
        action_btn = tk.Button(card_frame, text="Access", 
                              command=command,
                              bg=self.theme.primary_gold,
                              fg=self.theme.system_background,
                              font=self.theme.font_heading,
                              relief=tk.FLAT, padx=15, pady=8,
                              cursor="hand2")
        action_btn.pack()
        
        # Hover effects
        def on_enter(e):
            card_frame.configure(highlightthickness=2)
            action_btn.configure(bg=self.theme.secondary_gold)
        
        def on_leave(e):
            card_frame.configure(highlightthickness=1)
            action_btn.configure(bg=self.theme.primary_gold)
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        action_btn.bind("<Enter>", on_enter)
        action_btn.bind("<Leave>", on_leave)
        
        return card_frame

    def menu_checkin_checkout(self):
        """Staff check-in/check-out for hotel management"""
        hasil = self.controller.current_user.attendance_checkin()
        messagebox.showinfo("Check-in Successful", hasil)
    def menu_gaji(self):
        hasil = self.controller.current_user.display_salary()
        messagebox.showinfo("Salary Information", hasil)
    def menu_izin(self):
        """Leave request functionality"""
        dialog = Toplevel(self)
        dialog.title("Request Leave")
        dialog.geometry("500x600")
        dialog.configure(bg=self.theme.system_background)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_gold)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="🏖️ REQUEST LEAVE", 
                font=self.theme.font_title,
                bg=self.theme.primary_gold,
                fg=self.theme.system_background,
                pady=15).pack()
        
        # Main form
        main_frame = tk.Frame(dialog, bg=self.theme.system_background, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Leave type
        tk.Label(main_frame, text="Leave Type:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).pack(anchor="w", pady=(0, 5))
        
        leave_type = tk.StringVar(value="Annual Leave")
        type_combo = ttk.Combobox(main_frame, textvariable=leave_type,
                                 values=["Annual Leave", "Sick Leave", "Emergency Leave", "Personal Leave"],
                                 font=self.theme.font_body, state="readonly")
        type_combo.pack(fill="x", pady=(0, 15))
        
        # Start date
        tk.Label(main_frame, text="Start Date (YYYY-MM-DD):", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).pack(anchor="w", pady=(0, 5))
        
        start_date_entry = tk.Entry(main_frame, font=self.theme.font_body,
                                   bg=self.theme.surface_light,
                                   fg=self.theme.text_primary,
                                   insertbackground=self.theme.primary_gold)
        start_date_entry.pack(fill="x", pady=(0, 15))
        start_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # End date
        tk.Label(main_frame, text="End Date (YYYY-MM-DD):", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).pack(anchor="w", pady=(0, 5))
        
        end_date_entry = tk.Entry(main_frame, font=self.theme.font_body,
                                 bg=self.theme.surface_light,
                                 fg=self.theme.text_primary,
                                 insertbackground=self.theme.primary_gold)
        end_date_entry.pack(fill="x", pady=(0, 15))
        
        # Reason
        tk.Label(main_frame, text="Reason:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).pack(anchor="w", pady=(0, 5))
        
        reason_text = tk.Text(main_frame, height=4, font=self.theme.font_body,
                             bg=self.theme.surface_light,
                             fg=self.theme.text_primary,
                             insertbackground=self.theme.primary_gold)
        reason_text.pack(fill="x", pady=(0, 15))
        
        # Define submit function
        def submit_leave():
            leave_type_val = leave_type.get()
            start_date = start_date_entry.get().strip()
            end_date = end_date_entry.get().strip()
            reason = reason_text.get("1.0", tk.END).strip()
            if not start_date or not end_date or not reason:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            # Generate leave ID
            leave_id = f"LV{datetime.now().strftime('%Y%m%d%H%M%S')}"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Format: leave_id:staff_id:staff_name:leave_type:start_date:end_date:reason:status:request_time:approved_by
            leave_data = f"{leave_id}:{self.controller.current_user.getId()}:{self.controller.current_user.getNama()}:{leave_type_val}:{start_date}:{end_date}:{reason}:Pending:{current_time}:-\n"
            
            with open(FILE_IZIN, "a") as file:
                file.write(leave_data)
            
            messagebox.showinfo("Success", f"Leave request submitted successfully!\nLeave ID: {leave_id}")
            dialog.destroy()
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        button_frame.pack(fill="x", pady=10)
        
        submit_btn = tk.Button(button_frame, text="SUBMIT REQUEST",
                              command=submit_leave,
                              bg=self.theme.primary_gold,
                              fg=self.theme.system_background,
                              font=self.theme.font_heading,
                              relief=tk.FLAT, padx=20, pady=5,
                              cursor="hand2")
        submit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(button_frame, text="CANCEL", 
                              command=dialog.destroy,
                              bg=self.theme.danger_ruby,
                              fg=self.theme.text_primary,
                              font=self.theme.font_heading,
                              relief=tk.FLAT, padx=20, pady=5,
                              cursor="hand2")
        cancel_btn.pack(side=tk.LEFT)

    def menu_laporan(self):
        """Report submission functionality"""
        dialog = Toplevel(self)
        dialog.title("Submit Report")
        dialog.geometry("600x500")
        dialog.configure(bg=self.theme.system_background)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_gold)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="📋 SUBMIT WORK REPORT", 
                font=self.theme.font_title,
                bg=self.theme.primary_gold,
                fg=self.theme.system_background,
                pady=15).pack()
        
        # Main form
        main_frame = tk.Frame(dialog, bg=self.theme.system_background, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Report type
        tk.Label(main_frame, text="Report Type:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).pack(anchor="w", pady=(0, 5))
        
        report_type = tk.StringVar(value="Daily Report")
        type_combo = ttk.Combobox(main_frame, textvariable=report_type,
                                 values=["Daily Report", "Weekly Summary", "Incident Report", 
                                        "Guest Feedback", "Maintenance Report", "Special Task Report"],
                                 font=self.theme.font_body, state="readonly")
        type_combo.pack(fill="x", pady=(0, 15))
        
        # Report title
        tk.Label(main_frame, text="Report Title:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).pack(anchor="w", pady=(0, 5))
        
        title_entry = tk.Entry(main_frame, font=self.theme.font_body,
                              bg=self.theme.surface_light,
                              fg=self.theme.text_primary,
                              insertbackground=self.theme.primary_gold)
        title_entry.pack(fill="x", pady=(0, 15))
        
        # Report content
        tk.Label(main_frame, text="Report Content:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).pack(anchor="w", pady=(0, 5))
        
        content_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        content_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        content_text = scrolledtext.ScrolledText(content_frame, height=8, font=self.theme.font_body,
                                               bg=self.theme.surface_light,
                                               fg=self.theme.text_primary,
                                               insertbackground=self.theme.primary_gold,
                                               wrap=tk.WORD)
        content_text.pack(fill="both", expand=True)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        button_frame.pack(fill="x", pady=10)
        
        def submit_report():
            report_type_val = report_type.get()
            title = title_entry.get().strip()
            content = content_text.get("1.0", tk.END).strip()
            
            if not title or not content:
                messagebox.showerror("Error", "Title and content are required!")
                return
            
            # Use the submit_report method from the staff class
            full_report = f"Title: {title}\n\nContent:\n{content}"
            result = self.controller.current_user.submit_report(full_report, report_type_val)
            
            messagebox.showinfo("Success", result)
            dialog.destroy()
        
        submit_btn = tk.Button(button_frame, text="SUBMIT REPORT", 
                              command=submit_report,
                              bg=self.theme.primary_gold,
                              fg=self.theme.system_background,
                              font=self.theme.font_heading,
                              relief=tk.FLAT, padx=20, pady=5,
                              cursor="hand2")
        submit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(button_frame, text="CANCEL", 
                              command=dialog.destroy,
                              bg=self.theme.danger_ruby,
                              fg=self.theme.text_primary,
                              font=self.theme.font_heading,
                              relief=tk.FLAT, padx=20, pady=5,
                              cursor="hand2")
        cancel_btn.pack(side=tk.LEFT)
    def menu_attendance_report(self):
        """Access to attendance reports - for managers and HR"""
        # Check if user has permission
        user_role = self.controller.current_user.getStatus()
        if user_role not in ["Manager", "HumanResource", "Admin"]:
            messagebox.showerror("Access Denied", "You don't have permission to view attendance reports!")
            return
        
        dialog = Toplevel(self)
        dialog.title("Attendance Reports")
        dialog.geometry("900x600")
        dialog.configure(bg=self.theme.system_background)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (900 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"900x600+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_gold)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="📊 ATTENDANCE REPORTS", 
                font=self.theme.font_title,
                bg=self.theme.primary_gold,
                fg=self.theme.system_background,
                pady=15).pack()
        
        # Main content
        main_frame = tk.Frame(dialog, bg=self.theme.system_background, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        controls_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(controls_frame, text="Filter by Date:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).pack(side=tk.LEFT, padx=(0, 10))
        
        date_entry = tk.Entry(controls_frame, font=self.theme.font_body,
                             bg=self.theme.surface_light,
                             fg=self.theme.text_primary,
                             insertbackground=self.theme.primary_gold,
                             width=12)
        date_entry.pack(side=tk.LEFT, padx=(0, 10))
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Report text area
        report_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        report_frame.pack(fill="both", expand=True)
        
        report_text = scrolledtext.ScrolledText(report_frame, font=self.theme.font_body,
                                              bg=self.theme.surface_light,
                                              fg=self.theme.text_primary,
                                              wrap=tk.WORD)
        report_text.pack(fill="both", expand=True, pady=(0, 15))
        
        def load_attendance_data():
            filter_date = date_entry.get().strip()
            report_text.delete("1.0", tk.END)
            
            if not os.path.exists(FILE_ABSENSI):
                report_text.insert("1.0", "No attendance data available.")
                return
            
            try:
                with open(FILE_ABSENSI, "r") as file:
                    lines = file.readlines()
                
                if not lines:
                    report_text.insert("1.0", "No attendance records found.")
                    return
                
                # Build report
                report = f"🏨 HOTEL STAFF ATTENDANCE REPORT\n"
                report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                report += "=" * 80 + "\n\n"
                
                total_records = 0
                filtered_records = 0
                
                for line in lines:
                    parts = line.strip().split(":")
                    if len(parts) >= 4:
                        staff_id, name, role, timestamp = parts[:4]
                        total_records += 1
                        
                        if not filter_date or filter_date in timestamp:
                            filtered_records += 1
                            report += f"Staff ID: {staff_id}\n"
                            report += f"Name: {name}\n"
                            report += f"Role: {role}\n"
                            report += f"Check-in Time: {timestamp}\n"
                            report += "-" * 40 + "\n"
                
                report += f"\nSUMMARY:\n"
                report += f"Total Records: {total_records}\n"
                report += f"Filtered Records: {filtered_records}\n"
                
                if filter_date:
                    report += f"Filter Applied: {filter_date}\n"
                
                report_text.insert("1.0", report)
                
            except Exception as e:
                report_text.insert("1.0", f"Error loading attendance data: {str(e)}")
        
        # Load initial data
        load_attendance_data()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        button_frame.pack(fill="x")
        
        refresh_btn = tk.Button(button_frame, text="REFRESH", 
                               command=load_attendance_data,
                               bg=self.theme.primary_gold,
                               fg=self.theme.system_background,
                               font=self.theme.font_heading,
                               relief=tk.FLAT, padx=20, pady=5,
                               cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = tk.Button(button_frame, text="CLOSE", 
                             command=dialog.destroy,
                             bg=self.theme.danger_ruby,
                             fg=self.theme.text_primary,
                             font=self.theme.font_heading,
                             relief=tk.FLAT, padx=20, pady=5,
                             cursor="hand2")
        close_btn.pack(side=tk.RIGHT)
    def menu_kelola_karyawan(self):
        """Staff management functionality"""
        # Check if user has permission
        user_role = self.controller.current_user.getStatus()
        if user_role not in ["Manager", "HumanResource"]:
            messagebox.showerror("Access Denied", "You don't have permission to manage staff!")
            return
        
        dialog = Toplevel(self)
        dialog.title("Staff Management")
        dialog.geometry("1000x700")
        dialog.configure(bg=self.theme.system_background)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (1000 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"1000x700+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_gold)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="👥 STAFF MANAGEMENT", 
                font=self.theme.font_title,
                bg=self.theme.primary_gold,
                fg=self.theme.system_background,
                pady=15).pack()
        
        # Main content with notebook
        main_frame = tk.Frame(dialog, bg=self.theme.system_background, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Tab 1: View Staff
        view_tab = tk.Frame(notebook, bg=self.theme.system_background)
        notebook.add(view_tab, text="View Staff")
        
        # Staff list
        staff_frame = tk.Frame(view_tab, bg=self.theme.system_background, padx=10, pady=10)
        staff_frame.pack(fill="both", expand=True)
        
        # Treeview for staff list
        columns = ("ID", "Name", "Role", "Salary")
        staff_tree = ttk.Treeview(staff_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            staff_tree.heading(col, text=col)
            staff_tree.column(col, width=150)
        
        staff_tree.pack(fill="both", expand=True, side=tk.LEFT)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(staff_frame, orient=tk.VERTICAL, command=staff_tree.yview)
        staff_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tab 2: Add Staff
        add_tab = tk.Frame(notebook, bg=self.theme.system_background)
        notebook.add(add_tab, text="Add New Staff")
        
        add_frame = tk.Frame(add_tab, bg=self.theme.system_background, padx=20, pady=20)
        add_frame.pack(fill="both", expand=True)
        
        # Add staff form
        tk.Label(add_frame, text="Staff Name:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=0, column=0, sticky="w", pady=5)
        
        name_entry = tk.Entry(add_frame, font=self.theme.font_body,
                             bg=self.theme.surface_light,
                             fg=self.theme.text_primary,
                             insertbackground=self.theme.primary_gold, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(add_frame, text="Staff ID:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=1, column=0, sticky="w", pady=5)
        
        id_entry = tk.Entry(add_frame, font=self.theme.font_body,
                           bg=self.theme.surface_light,
                           fg=self.theme.text_primary,
                           insertbackground=self.theme.primary_gold, width=30)
        id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(add_frame, text="Password:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=2, column=0, sticky="w", pady=5)
        
        password_entry = tk.Entry(add_frame, font=self.theme.font_body,
                                 bg=self.theme.surface_light,
                                 fg=self.theme.text_primary,
                                 insertbackground=self.theme.primary_gold, width=30)
        password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(add_frame, text="Role:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=3, column=0, sticky="w", pady=5)
        
        role_var = tk.StringVar(value="Admin")
        role_combo = ttk.Combobox(add_frame, textvariable=role_var,
                                 values=["Manager", "Admin", "HumanResource", "CleaningService", "Marketing", "Internship"],
                                 font=self.theme.font_body, state="readonly", width=27)
        role_combo.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(add_frame, text="Salary:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=4, column=0, sticky="w", pady=5)
        
        salary_entry = tk.Entry(add_frame, font=self.theme.font_body,
                               bg=self.theme.surface_light,
                               fg=self.theme.text_primary,
                               insertbackground=self.theme.primary_gold, width=30)
        salary_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        def load_staff_data():
            # Clear existing data
            for item in staff_tree.get_children():
                staff_tree.delete(item)
            
            if os.path.exists(FILE_USER):
                with open(FILE_USER, "r") as file:
                    for line in file:
                        parts = line.strip().split(":")
                        if len(parts) >= 5:
                            name, staff_id, password, role, salary = parts[:5]
                            staff_tree.insert("", "end", values=(staff_id, name, role, f"${int(salary):,}"))
        
        def add_staff():
            name = name_entry.get().strip()
            staff_id = id_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get()
            salary = salary_entry.get().strip()
            
            if not all([name, staff_id, password, role, salary]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                salary_int = int(salary)
                if salary_int < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Salary must be a valid positive number!")
                return
            
            # Check if staff ID already exists
            if os.path.exists(FILE_USER):
                with open(FILE_USER, "r") as file:
                    for line in file:
                        parts = line.strip().split(":")
                        if len(parts) >= 2 and parts[1] == staff_id:
                            messagebox.showerror("Error", "Staff ID already exists!")
                            return
            
            # Add new staff
            staff_data = f"{name}:{staff_id}:{password}:{role}:{salary}\n"
            with open(FILE_USER, "a") as file:
                file.write(staff_data)
            
            messagebox.showinfo("Success", f"Staff {name} added successfully!")
            
            # Clear form
            name_entry.delete(0, tk.END)
            id_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)            
            salary_entry.delete(0, tk.END)
            
            # Refresh staff list
            load_staff_data()
        
        add_btn = tk.Button(add_frame, text="ADD STAFF", 
                           command=add_staff,
                           bg=self.theme.primary_gold,
                           fg=self.theme.system_background,
                           font=self.theme.font_heading,
                           relief=tk.FLAT, padx=20, pady=5,
                           cursor="hand2")
        add_btn.grid(row=5, column=1, padx=10, pady=20, sticky="w")
        
        # Tab 3: Change Status/Promotion
        promotion_tab = tk.Frame(notebook, bg=self.theme.system_background)
        notebook.add(promotion_tab, text="Change Status/Promotion")
        
        promotion_frame = tk.Frame(promotion_tab, bg=self.theme.system_background, padx=20, pady=20)
        promotion_frame.pack(fill="both", expand=True)
        
        # Instructions
        tk.Label(promotion_frame, text="Update Employee Status and Promotions", 
                font=self.theme.font_heading,
                bg=self.theme.system_background,
                fg=self.theme.primary_gold).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Staff ID selection
        tk.Label(promotion_frame, text="Staff ID:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=1, column=0, sticky="w", pady=5)
        
        promotion_id_var = tk.StringVar()
        promotion_id_combo = ttk.Combobox(promotion_frame, textvariable=promotion_id_var,
                                         font=self.theme.font_body, state="readonly", width=27)
        promotion_id_combo.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Current info display
        tk.Label(promotion_frame, text="Current Name:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=2, column=0, sticky="w", pady=5)
        
        current_name_label = tk.Label(promotion_frame, text="Select staff first", 
                                     font=self.theme.font_body,
                                     bg=self.theme.system_background,
                                     fg=self.theme.text_secondary)
        current_name_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(promotion_frame, text="Current Role:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=3, column=0, sticky="w", pady=5)
        
        current_role_label = tk.Label(promotion_frame, text="Select staff first", 
                                     font=self.theme.font_body,
                                     bg=self.theme.system_background,
                                     fg=self.theme.text_secondary)
        current_role_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(promotion_frame, text="Current Salary:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=4, column=0, sticky="w", pady=5)
        
        current_salary_label = tk.Label(promotion_frame, text="Select staff first", 
                                       font=self.theme.font_body,
                                       bg=self.theme.system_background,
                                       fg=self.theme.text_secondary)
        current_salary_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        # New role selection
        tk.Label(promotion_frame, text="New Role:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=5, column=0, sticky="w", pady=5)
        
        new_role_var = tk.StringVar(value="Manager")
        new_role_combo = ttk.Combobox(promotion_frame, textvariable=new_role_var,
                                     values=["Manager", "Admin", "HumanResource", "CleaningService", "Marketing", "Internship"],
                                     font=self.theme.font_body, state="readonly", width=27)
        new_role_combo.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        
        # New salary
        tk.Label(promotion_frame, text="New Salary:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=6, column=0, sticky="w", pady=5)
        
        new_salary_entry = tk.Entry(promotion_frame, font=self.theme.font_body,
                                   bg=self.theme.surface_light,
                                   fg=self.theme.text_primary,
                                   insertbackground=self.theme.primary_gold, width=30)
        new_salary_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        
        # Promotion reason
        tk.Label(promotion_frame, text="Reason for Change:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=7, column=0, sticky="w", pady=5)
        
        reason_entry = tk.Entry(promotion_frame, font=self.theme.font_body,
                               bg=self.theme.surface_light,
                               fg=self.theme.text_primary,
                               insertbackground=self.theme.primary_gold, width=30)
        reason_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")
        
        def load_staff_for_promotion():
            """Load staff IDs for the promotion dropdown"""
            staff_ids = []
            if os.path.exists(FILE_USER):
                with open(FILE_USER, "r") as file:
                    for line in file:
                        parts = line.strip().split(":")
                        if len(parts) >= 5:
                            name, staff_id, password, role, salary = parts[:5]
                            staff_ids.append(f"{staff_id} - {name}")
            promotion_id_combo['values'] = staff_ids
        
        def on_staff_selection(event):
            """Update current info when staff is selected"""
            selected = promotion_id_var.get()
            if not selected:
                return
            
            staff_id = selected.split(" - ")[0]
            
            if os.path.exists(FILE_USER):
                with open(FILE_USER, "r") as file:
                    for line in file:
                        parts = line.strip().split(":")
                        if len(parts) >= 5 and parts[1] == staff_id:
                            name, staff_id, password, role, salary = parts[:5]
                            current_name_label.config(text=name)
                            current_role_label.config(text=role)
                            current_salary_label.config(text=f"${int(salary):,}")
                            new_role_var.set(role)
                            new_salary_entry.delete(0, tk.END)
                            new_salary_entry.insert(0, salary)
                            break
        
        promotion_id_combo.bind("<<ComboboxSelected>>", on_staff_selection)
        
        def update_staff_status():
            """Update staff role and salary"""
            selected = promotion_id_var.get()
            if not selected:
                messagebox.showerror("Error", "Please select a staff member!")
                return
            
            staff_id = selected.split(" - ")[0]
            new_role = new_role_var.get()
            new_salary = new_salary_entry.get().strip()
            reason = reason_entry.get().strip()
            
            if not new_salary:
                messagebox.showerror("Error", "New salary is required!")
                return
            
            if not reason:
                messagebox.showerror("Error", "Reason for change is required!")
                return
            
            try:
                salary_int = int(new_salary)
                if salary_int < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Salary must be a valid positive number!")
                return
            
            if not os.path.exists(FILE_USER):
                messagebox.showerror("Error", "No staff data found!")
                return
            
            # Update staff data
            updated_lines = []
            staff_found = False
            old_name = ""
            old_role = ""
            old_salary = ""
            
            with open(FILE_USER, "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(":")
                    if len(parts) >= 5 and parts[1] == staff_id:
                        old_name = parts[0]
                        old_role = parts[3]
                        old_salary = parts[4]
                        # Update role and salary
                        parts[3] = new_role
                        parts[4] = str(salary_int)
                        updated_line = ":".join(parts)
                        updated_lines.append(updated_line + "\n")
                        staff_found = True
                    else:
                        updated_lines.append(line)
            
            if not staff_found:
                messagebox.showerror("Error", "Staff member not found!")
                return
            
            # Write updated data
            with open(FILE_USER, "w") as file:
                file.writelines(updated_lines)
            
            # Log the promotion/status change
            log_entry = f"Staff Status Update - Staff ID: {staff_id}, Name: {old_name}, "
            log_entry += f"Role: {old_role} → {new_role}, Salary: ${old_salary} → ${salary_int:,}, "
            log_entry += f"Reason: {reason}, Updated by: {self.controller.current_user.getNama()}, "
            log_entry += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            with open("PromotionLog.txt", "a") as file:
                file.write(log_entry)
            
            messagebox.showinfo("Success", f"Staff status updated successfully!\n\n"
                                          f"Staff: {old_name}\n"
                                          f"Role: {old_role} → {new_role}\n"
                                          f"Salary: ${old_salary} → ${salary_int:,}")
            
            # Clear form and refresh data
            promotion_id_var.set("")
            current_name_label.config(text="Select staff first")
            current_role_label.config(text="Select staff first")
            current_salary_label.config(text="Select staff first")
            new_salary_entry.delete(0, tk.END)
            reason_entry.delete(0, tk.END)
            
            # Refresh all staff data
            load_staff_data()
            load_staff_for_promotion()
        
        update_status_btn = tk.Button(promotion_frame, text="UPDATE STATUS", 
                                     command=update_staff_status,
                                     bg=self.theme.success_emerald,
                                     fg=self.theme.text_primary,
                                     font=self.theme.font_heading,
                                     relief=tk.FLAT, padx=20, pady=5,
                                     cursor="hand2")
        update_status_btn.grid(row=8, column=1, padx=10, pady=20, sticky="w")
        
        # Load initial data
        load_staff_data()
        load_staff_for_promotion()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        button_frame.pack(fill="x", pady=10)
        
        refresh_btn = tk.Button(button_frame, text="REFRESH", 
                               command=lambda: [load_staff_data(), load_staff_for_promotion()],
                               bg=self.theme.primary_gold,
                               fg=self.theme.system_background,
                               font=self.theme.font_heading,
                               relief=tk.FLAT, padx=20, pady=5,
                               cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = tk.Button(button_frame, text="CLOSE", 
                             command=dialog.destroy,
                             bg=self.theme.danger_ruby,
                             fg=self.theme.text_primary,
                             font=self.theme.font_heading,
                             relief=tk.FLAT, padx=20, pady=5,
                             cursor="hand2")
        close_btn.pack(side=tk.RIGHT)
    def menu_kelola_perizinan(self):
        """Leave approval functionality"""
        # Check if user has permission
        user_role = self.controller.current_user.getStatus()
        if user_role not in ["Manager", "HumanResource"]:
            messagebox.showerror("Access Denied", "You don't have permission to approve leaves!")
            return
        
        dialog = Toplevel(self)
        dialog.title("Leave Management")
        dialog.geometry("1000x600")
        dialog.configure(bg=self.theme.system_background)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (1000 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"1000x600+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_gold)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="✅ LEAVE REQUEST MANAGEMENT", 
                font=self.theme.font_title,
                bg=self.theme.primary_gold,
                fg=self.theme.system_background,
                pady=15).pack()
        
        # Main content
        main_frame = tk.Frame(dialog, bg=self.theme.system_background, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Leave requests list
        list_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        list_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Treeview for leave requests
        columns = ("Leave ID", "Staff", "Type", "Start Date", "End Date", "Status")
        leave_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            leave_tree.heading(col, text=col)
            leave_tree.column(col, width=140)
        
        leave_tree.pack(fill="both", expand=True, side=tk.LEFT)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=leave_tree.yview)
        leave_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def load_leave_data():
            # Clear existing data
            for item in leave_tree.get_children():
                leave_tree.delete(item)
            
            if not os.path.exists(FILE_IZIN):
                return
            
            with open(FILE_IZIN, "r") as file:
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) >= 9:
                        leave_id, staff_id, staff_name, leave_type, start_date, end_date, reason, status, request_time = parts[:9]
                        leave_tree.insert("", "end", values=(leave_id, staff_name, leave_type, start_date, end_date, status))
        
        def view_details():
            selected = leave_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a leave request to view details!")
                return
            
            item = leave_tree.item(selected[0])
            leave_id = item['values'][0]
            
            # Find full details
            if not os.path.exists(FILE_IZIN):
                return
            
            with open(FILE_IZIN, "r") as file:
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) >= 9 and parts[0] == leave_id:
                        leave_id, staff_id, staff_name, leave_type, start_date, end_date, reason, status, request_time = parts[:9]
                        
                        details = f"Leave Request Details\n" + "="*50 + "\n\n"
                        details += f"Leave ID: {leave_id}\n"
                        details += f"Staff ID: {staff_id}\n"
                        details += f"Staff Name: {staff_name}\n"
                        details += f"Leave Type: {leave_type}\n"
                        details += f"Start Date: {start_date}\n"
                        details += f"End Date: {end_date}\n"
                        details += f"Current Status: {status}\n"
                        details += f"Request Time: {request_time}\n\n"
                        details += f"Reason:\n{reason}\n"
                        
                        messagebox.showinfo("Leave Request Details", details)
                        break
        
        def update_leave_status(new_status):
            selected = leave_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a leave request!")
                return
            
            item = leave_tree.item(selected[0])
            leave_id = item['values'][0]
            
            if not os.path.exists(FILE_IZIN):
                return
            
            # Update the leave status
            updated_lines = []
            with open(FILE_IZIN, "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(":")
                    if len(parts) >= 9 and parts[0] == leave_id:
                        parts[7] = new_status  # Update status
                        if len(parts) >= 10:
                            parts[9] = self.controller.current_user.getNama()  # Update approved_by
                        else:
                            parts.append(self.controller.current_user.getNama())
                        updated_line = ":".join(parts)
                        updated_lines.append(updated_line + "\n")
                    else:
                        updated_lines.append(line)
            
            with open(FILE_IZIN, "w") as file:
                file.writelines(updated_lines)
            
            messagebox.showinfo("Success", f"Leave request {new_status.lower()} successfully!")
            load_leave_data()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        button_frame.pack(fill="x")
        
        details_btn = tk.Button(button_frame, text="VIEW DETAILS", 
                               command=view_details,
                               bg=self.theme.accent_copper,
                               fg=self.theme.text_primary,
                               font=self.theme.font_heading,
                               relief=tk.FLAT, padx=15, pady=5,
                               cursor="hand2")
        details_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        approve_btn = tk.Button(button_frame, text="APPROVE", 
                               command=lambda: update_leave_status("Approved"),
                               bg=self.theme.success_emerald,
                               fg=self.theme.text_primary,
                               font=self.theme.font_heading,
                               relief=tk.FLAT, padx=15, pady=5,
                               cursor="hand2")
        approve_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        reject_btn = tk.Button(button_frame, text="REJECT", 
                              command=lambda: update_leave_status("Rejected"),
                              bg=self.theme.danger_ruby,
                              fg=self.theme.text_primary,
                              font=self.theme.font_heading,
                              relief=tk.FLAT, padx=15, pady=5,
                              cursor="hand2")
        reject_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_btn = tk.Button(button_frame, text="REFRESH", 
                               command=load_leave_data,
                               bg=self.theme.primary_gold,
                               fg=self.theme.system_background,
                               font=self.theme.font_heading,
                               relief=tk.FLAT, padx=15, pady=5,
                               cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = tk.Button(button_frame, text="CLOSE", 
                             command=dialog.destroy,
                             bg=self.theme.surface_dark,
                             fg=self.theme.text_primary,
                             font=self.theme.font_heading,
                             relief=tk.FLAT, padx=15, pady=5,
                             cursor="hand2")
        close_btn.pack(side=tk.RIGHT)
        
        # Load initial data
        load_leave_data()
    def menu_kelola_gaji(self):
        """Payroll management functionality"""
        # Check if user has permission
        user_role = self.controller.current_user.getStatus()
        if user_role not in ["Manager", "HumanResource"]:
            messagebox.showerror("Access Denied", "You don't have permission to manage payroll!")
            return
        
        dialog = Toplevel(self)
        dialog.title("Payroll Management")
        dialog.geometry("900x600")
        dialog.configure(bg=self.theme.system_background)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (900 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"900x600+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_gold)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="💼 PAYROLL MANAGEMENT", 
                font=self.theme.font_title,
                bg=self.theme.primary_gold,
                fg=self.theme.system_background,
                pady=15).pack()
        
        # Main content with notebook
        main_frame = tk.Frame(dialog, bg=self.theme.system_background, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=(0, 15))
        
        # Tab 1: View Payroll
        view_tab = tk.Frame(notebook, bg=self.theme.system_background)
        notebook.add(view_tab, text="View Payroll")
        
        payroll_frame = tk.Frame(view_tab, bg=self.theme.system_background, padx=10, pady=10)
        payroll_frame.pack(fill="both", expand=True)
        
        # Treeview for payroll
        columns = ("Staff ID", "Name", "Role", "Base Salary", "Bonus", "Total")
        payroll_tree = ttk.Treeview(payroll_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            payroll_tree.heading(col, text=col)
            payroll_tree.column(col, width=120)
        
        payroll_tree.pack(fill="both", expand=True, side=tk.LEFT)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(payroll_frame, orient=tk.VERTICAL, command=payroll_tree.yview)
        payroll_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tab 2: Update Salary
        update_tab = tk.Frame(notebook, bg=self.theme.system_background)
        notebook.add(update_tab, text="Update Salary")
        
        update_frame = tk.Frame(update_tab, bg=self.theme.system_background, padx=20, pady=20)
        update_frame.pack(fill="both", expand=True)
        
        tk.Label(update_frame, text="Staff ID:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=0, column=0, sticky="w", pady=5)
        
        staff_id_entry = tk.Entry(update_frame, font=self.theme.font_body,
                                 bg=self.theme.surface_light,
                                 fg=self.theme.text_primary,
                                 insertbackground=self.theme.primary_gold, width=20)
        staff_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(update_frame, text="New Salary:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=1, column=0, sticky="w", pady=5)
        
        new_salary_entry = tk.Entry(update_frame, font=self.theme.font_body,
                                   bg=self.theme.surface_light,
                                   fg=self.theme.text_primary,
                                   insertbackground=self.theme.primary_gold, width=20)
        new_salary_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(update_frame, text="Reason:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).grid(row=2, column=0, sticky="w", pady=5)
        
        reason_entry = tk.Entry(update_frame, font=self.theme.font_body,
                               bg=self.theme.surface_light,
                               fg=self.theme.text_primary,
                               insertbackground=self.theme.primary_gold, width=40)
        reason_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        def load_payroll_data():
            # Clear existing data
            for item in payroll_tree.get_children():
                payroll_tree.delete(item)
            
            if not os.path.exists(FILE_USER):
                return
            
            total_payroll = 0
            with open(FILE_USER, "r") as file:
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) >= 5:
                        name, staff_id, password, role, salary = parts[:5]
                        base_salary = int(salary)
                        
                        # Calculate bonus based on role
                        if role == "Manager":
                            bonus = int(base_salary * 0.15)
                        elif role == "HumanResource":
                            bonus = int(base_salary * 0.10)
                        elif role == "Marketing":
                            bonus = int(base_salary * 0.12)
                        else:
                            bonus = int(base_salary * 0.05)
                        
                        total = base_salary + bonus
                        total_payroll += total
                        
                        payroll_tree.insert("", "end", values=(
                            staff_id, name, role, 
                            f"${base_salary:,}", 
                            f"${bonus:,}", 
                            f"${total:,}"
                        ))
            
            # Add total row
            payroll_tree.insert("", "end", values=(
                "", "TOTAL", "", "", "", f"${total_payroll:,}"
            ), tags=("total",))
            
            # Style the total row
            payroll_tree.tag_configure("total", background=self.theme.primary_gold, foreground=self.theme.system_background)
        
        def update_salary():
            staff_id = staff_id_entry.get().strip()
            new_salary = new_salary_entry.get().strip()
            reason = reason_entry.get().strip()
            
            if not staff_id or not new_salary:
                messagebox.showerror("Error", "Staff ID and new salary are required!")
                return
            
            try:
                salary_int = int(new_salary)
                if salary_int < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Salary must be a valid positive number!")
                return
            
            if not os.path.exists(FILE_USER):
                messagebox.showerror("Error", "No staff data found!")
                return
            
            # Update salary
            updated_lines = []
            staff_found = False
            
            with open(FILE_USER, "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(":")
                    if len(parts) >= 5 and parts[1] == staff_id:
                        parts[4] = str(salary_int)  # Update salary
                        updated_line = ":".join(parts)
                        updated_lines.append(updated_line + "\n")
                        staff_found = True
                    else:
                        updated_lines.append(line)
            
            if not staff_found:
                messagebox.showerror("Error", "Staff ID not found!")
                return
            
            with open(FILE_USER, "w") as file:
                file.writelines(updated_lines)
            
            # Log the salary change
            log_entry = f"Salary Update - Staff ID: {staff_id}, New Salary: ${salary_int:,}, Reason: {reason}, Updated by: {self.controller.current_user.getNama()}, Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            with open("SalaryLog.txt", "a") as file:
                file.write(log_entry)
            
            messagebox.showinfo("Success", f"Salary updated successfully for Staff ID: {staff_id}")
            
            # Clear form
            staff_id_entry.delete(0, tk.END)
            new_salary_entry.delete(0, tk.END)
            reason_entry.delete(0, tk.END)
            
            # Refresh payroll data
            load_payroll_data()
        
        update_btn = tk.Button(update_frame, text="UPDATE SALARY", 
                              command=update_salary,
                              bg=self.theme.primary_gold,
                              fg=self.theme.system_background,
                              font=self.theme.font_heading,
                              relief=tk.FLAT, padx=20, pady=5,
                              cursor="hand2")
        update_btn.grid(row=3, column=1, padx=10, pady=20, sticky="w")
        
        # Load initial data
        load_payroll_data()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        button_frame.pack(fill="x")
        
        refresh_btn = tk.Button(button_frame, text="REFRESH", 
                               command=load_payroll_data,
                               bg=self.theme.primary_gold,
                               fg=self.theme.system_background,
                               font=self.theme.font_heading,
                               relief=tk.FLAT, padx=20, pady=5,
                               cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = tk.Button(button_frame, text="CLOSE", 
                             command=dialog.destroy,
                             bg=self.theme.danger_ruby,
                             fg=self.theme.text_primary,
                             font=self.theme.font_heading,
                             relief=tk.FLAT, padx=20, pady=5,
                             cursor="hand2")
        close_btn.pack(side=tk.RIGHT)
    def menu_review_laporan(self):
        """Report review functionality"""
        # Check if user has permission
        user_role = self.controller.current_user.getStatus()
        if user_role not in ["Manager"]:
            messagebox.showerror("Access Denied", "You don't have permission to review reports!")
            return
        
        dialog = Toplevel(self)
        dialog.title("Report Review System")
        dialog.geometry("1200x700")
        dialog.configure(bg=self.theme.system_background)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (1200 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"1200x700+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.theme.primary_gold)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="📈 REPORT REVIEW SYSTEM", 
                font=self.theme.font_title,
                bg=self.theme.primary_gold,
                fg=self.theme.system_background,
                pady=15).pack()
        
        # Main content with split view
        main_frame = tk.Frame(dialog, bg=self.theme.system_background, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Left panel - Report list
        left_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))
        
        # Filter frame
        filter_frame = tk.Frame(left_frame, bg=self.theme.system_background)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(filter_frame, text="Filter by Status:", 
                font=self.theme.font_body,
                bg=self.theme.system_background,
                fg=self.theme.text_primary).pack(side=tk.LEFT, padx=(0, 10))
        
        status_filter = tk.StringVar(value="All")
        status_combo = ttk.Combobox(filter_frame, textvariable=status_filter,
                                   values=["All", "Pending", "Approved", "Rejected"],
                                   font=self.theme.font_body, state="readonly", width=10)
        status_combo.pack(side=tk.LEFT)
        
        # Reports list
        reports_frame = tk.Frame(left_frame, bg=self.theme.system_background)
        reports_frame.pack(fill="both", expand=True)
        
        columns = ("Report ID", "Staff", "Type", "Date", "Status")
        reports_tree = ttk.Treeview(reports_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            reports_tree.heading(col, text=col)
            reports_tree.column(col, width=100)
        
        reports_tree.pack(fill="both", expand=True, side=tk.LEFT)
        
        # Scrollbar for reports list
        reports_scrollbar = ttk.Scrollbar(reports_frame, orient=tk.VERTICAL, command=reports_tree.yview)
        reports_tree.configure(yscrollcommand=reports_scrollbar.set)
        reports_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Report details
        right_frame = tk.Frame(main_frame, bg=self.theme.surface_dark, relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True)
        
        # Details header
        details_header = tk.Frame(right_frame, bg=self.theme.primary_gold)
        details_header.pack(fill="x")
        
        tk.Label(details_header, text="📄 REPORT DETAILS", 
                font=self.theme.font_heading,
                bg=self.theme.primary_gold,
                fg=self.theme.system_background,
                pady=10).pack()
        
        # Details content
        details_content = tk.Frame(right_frame, bg=self.theme.surface_dark, padx=15, pady=15)
        details_content.pack(fill="both", expand=True)
        
        # Report details text area
        details_text = scrolledtext.ScrolledText(details_content, height=15, font=self.theme.font_body,
                                                bg=self.theme.surface_light,
                                                fg=self.theme.text_primary,
                                                wrap=tk.WORD, state=tk.DISABLED)
        details_text.pack(fill="both", expand=True, pady=(0, 15))
        
        # Manager comment section
        comment_frame = tk.Frame(details_content, bg=self.theme.surface_dark)
        comment_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(comment_frame, text="Manager Comment:", 
                font=self.theme.font_body,
                bg=self.theme.surface_dark,
                fg=self.theme.text_primary).pack(anchor="w")
        
        comment_text = tk.Text(comment_frame, height=3, font=self.theme.font_body,
                              bg=self.theme.surface_light,
                              fg=self.theme.text_primary,
                              insertbackground=self.theme.primary_gold)
        comment_text.pack(fill="x", pady=(5, 0))
        
        # Action buttons
        action_frame = tk.Frame(details_content, bg=self.theme.surface_dark)
        action_frame.pack(fill="x")
        
        selected_report_id = tk.StringVar()
        
        def load_reports():
            # Clear existing data
            for item in reports_tree.get_children():
                reports_tree.delete(item)
            
            if not os.path.exists(FILE_LAPORAN):
                return
            
            filter_status = status_filter.get()
            
            with open(FILE_LAPORAN, "r") as file:
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) >= 8:
                        report_id, staff_id, staff_name, title, timestamp, content, status, notes = parts[:8]
                        
                        if filter_status == "All" or status == filter_status:
                            # Format timestamp for display
                            try:
                                date_part = timestamp.split()[0]
                            except:
                                date_part = timestamp
                            
                            reports_tree.insert("", "end", values=(
                                report_id, staff_name, title, date_part, status
                            ))
        
        def on_report_select(event):
            selected = reports_tree.selection()
            if not selected:
                return
            
            item = reports_tree.item(selected[0])
            report_id = item['values'][0]
            selected_report_id.set(report_id)
            
            # Load report details
            if not os.path.exists(FILE_LAPORAN):
                return
            
            with open(FILE_LAPORAN, "r") as file:
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) >= 8 and parts[0] == report_id:
                        report_id, staff_id, staff_name, title, timestamp, content, status, notes = parts[:8]
                        
                        details = f"Report ID: {report_id}\n"
                        details += f"Staff ID: {staff_id}\n"
                        details += f"Staff Name: {staff_name}\n"
                        details += f"Report Type: {title}\n"
                        details += f"Submission Time: {timestamp}\n"
                        details += f"Current Status: {status}\n\n"
                        details += "=" * 50 + "\n"
                        details += "REPORT CONTENT:\n"
                        details += "=" * 50 + "\n\n"
                        details += content + "\n\n"
                        
                        if notes and notes != "-":
                            details += "=" * 50 + "\n"
                            details += "MANAGER NOTES:\n"
                            details += "=" * 50 + "\n"
                            details += notes
                        
                        details_text.config(state=tk.NORMAL)
                        details_text.delete("1.0", tk.END)
                        details_text.insert("1.0", details)
                        details_text.config(state=tk.DISABLED)
                        
                        # Load existing comment
                        comment_text.delete("1.0", tk.END)
                        if notes and notes != "-":
                            comment_text.insert("1.0", notes)
                        
                        break
        
        def update_report_status(new_status):
            report_id = selected_report_id.get()
            if not report_id:
                messagebox.showwarning("Warning", "Please select a report first!")
                return
            
            comment = comment_text.get("1.0", tk.END).strip()
            if not comment:
                comment = f"Report {new_status.lower()} by {self.controller.current_user.getNama()}"
            
            # Use the review_laporan method from Manager/Admin class
            result = self.controller.current_user.review_laporan(report_id, new_status, comment)
            messagebox.showinfo("Success", result)
            
            # Refresh the reports list and clear details
            load_reports()
            details_text.config(state=tk.NORMAL)
            details_text.delete("1.0", tk.END)
            details_text.config(state=tk.DISABLED)
            comment_text.delete("1.0", tk.END)
            selected_report_id.set("")
        
        approve_btn = tk.Button(action_frame, text="APPROVE", 
                               command=lambda: update_report_status("Approved"),
                               bg=self.theme.success_emerald,
                               fg=self.theme.text_primary,
                               font=self.theme.font_heading,
                               relief=tk.FLAT, padx=15, pady=5,
                               cursor="hand2")
        approve_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        reject_btn = tk.Button(action_frame, text="REJECT", 
                              command=lambda: update_report_status("Rejected"),
                              bg=self.theme.danger_ruby,
                              fg=self.theme.text_primary,
                              font=self.theme.font_heading,
                              relief=tk.FLAT, padx=15, pady=5,
                              cursor="hand2")
        reject_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        revision_btn = tk.Button(action_frame, text="REQUEST REVISION", 
                                command=lambda: update_report_status("Needs Revision"),
                                bg=self.theme.warning_amber,
                                fg=self.theme.system_background,
                                font=self.theme.font_heading,
                                relief=tk.FLAT, padx=15, pady=5,
                                cursor="hand2")
        revision_btn.pack(side=tk.LEFT)
        
        # Bind selection event
        reports_tree.bind("<<TreeviewSelect>>", on_report_select)
        
        # Filter change event
        def on_filter_change(*args):
            load_reports()
        
        status_filter.trace("w", on_filter_change)
        
        # Bottom buttons
        bottom_frame = tk.Frame(main_frame, bg=self.theme.system_background)
        bottom_frame.pack(fill="x", pady=(10, 0))
        
        refresh_btn = tk.Button(bottom_frame, text="REFRESH", 
                               command=load_reports,
                               bg=self.theme.primary_gold,
                               fg=self.theme.system_background,
                               font=self.theme.font_heading,
                               relief=tk.FLAT, padx=20, pady=5,
                               cursor="hand2")
        refresh_btn.pack(side=tk.LEFT)
        
        close_btn = tk.Button(bottom_frame, text="CLOSE", 
                             command=dialog.destroy,
                             bg=self.theme.surface_dark,
                             fg=self.theme.text_primary,
                             font=self.theme.font_heading,
                             relief=tk.FLAT, padx=20, pady=5,
                             cursor="hand2")
        close_btn.pack(side=tk.RIGHT)
        
        # Load initial data
        load_reports()
    
    def menu_team_analytics(self):
        """Team analytics dashboard"""
        messagebox.showinfo("Coming Soon", "Team analytics dashboard will be available in the next update.")
    
    def menu_send_notification(self):
        """Send notifications to staff"""
        messagebox.showinfo("Coming Soon", "Notification system will be available in the next update.")    
    def logout(self):
            self.controller.current_user = None
            self.controller.show_frame(LoginPage)

if __name__ == "__main__":

    initialize_default_staff()
    app = SistemManajemenKaryawan()
    app.mainloop()
