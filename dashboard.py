import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance
import sqlite3
from course import CourseClass
from student import AdvancedStudentClass
from result import AdvancedResultSystem
from report import ReportViewer
from logout import AdvancedLogoutSystem

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Management System")
        self.root.state('zoomed')
        self.root.config(bg='#ecf0f1')

        self.load_icons()

        # Left Sidebar
        self.sidebar = tk.Frame(self.root, bg="#2D3E50", width=250)
        self.sidebar.pack(side="left", fill="y")

        # Sidebar header (logo)
        tk.Label(
            self.sidebar,
            text="  Student Result System",
            image=self.logo_img,
            compound=tk.LEFT,
            font=("Segoe UI", 18, "bold"),
            bg="#2D3E50",
            fg="white"
        ).pack(anchor="w", padx=20, pady=20)

        # Sidebar Menu
        self.make_sidebar_button(self.sidebar, "Course", self.icon_course, "#3498DB", self.add_course).pack(fill="x", pady=10)
        self.make_sidebar_button(self.sidebar, "Student", self.icon_student, "#8E44AD", self.add_student).pack(fill="x", pady=10)
        self.make_sidebar_button(self.sidebar, "Result", self.icon_result, "#27AE60", self.add_result).pack(fill="x", pady=10)
        self.make_sidebar_button(self.sidebar, "View Results", self.icon_report, "#E67E22", self.add_report).pack(fill="x", pady=10)
        self.make_sidebar_button(self.sidebar, "Logout", self.icon_logout, "#C0392B", self.logout).pack(fill="x", pady=10)
        self.make_sidebar_button(self.sidebar, "Exit", self.icon_exit, "#C0392B", self.exit_app).pack(fill="x", pady=10)

        # Main Content Area
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(side="right", fill="both", expand=True)

        # Header Section
        header = tk.Frame(main_frame, bg="#1F1F2E", height=60)
        header.pack(side="top", fill="x")

        tk.Label(
            header,
            text="  Dashboard",
            font=("Segoe UI", 22, "bold"),
            bg="#1F1F2E",
            fg="white"
        ).pack(anchor="w", padx=20, pady=10)

        # Stats Section (Metric Cards)
        stats = tk.Frame(main_frame, bg="#ecf0f1", pady=20)
        stats.pack(side="top", fill="x")

        # Equal spacing across 3 columns
        stats.grid_columnconfigure(0, weight=1)
        stats.grid_columnconfigure(1, weight=1)
        stats.grid_columnconfigure(2, weight=1)

        self.lb1_course = self.create_stat_card(stats, "Total Courses\n[ 0 ]", "#1ABC9C", 0)
        self.lb1_student = self.create_stat_card(stats, "Total Students\n[ 0 ]", "#2980B9", 1)
        self.lb1_result = self.create_stat_card(stats, "Total Results\n[ 0 ]", "#8E44AD", 2)

        # Center Image Section
        bg_img = Image.open("images/bg1.jpg").resize((1000, 500))
        self.bg_img = ImageTk.PhotoImage(bg_img)
        tk.Label(main_frame, image=self.bg_img, bg="#ecf0f1").pack(pady=20)

        # Footer
        footer = tk.Label(
            main_frame,
            text="NIET - Student Result Management System | Contact: 99xxxxx87",
            font=("Segoe UI", 10),
            bg="#1F1F2E",
            fg="white",
            pady=10
        )
        footer.pack(side="bottom", fill="x")

        self.update_details()

    def load_icons(self):
        try:
            self.logo_img = ImageTk.PhotoImage(file="images/logo_p.png")
            size = (24, 24)
            self.icon_course = ImageTk.PhotoImage(Image.open("images/icon_course.png").resize(size))
            self.icon_student = ImageTk.PhotoImage(Image.open("images/icon_student.png").resize(size))
            self.icon_result = ImageTk.PhotoImage(Image.open("images/icon_result.png").resize(size))
            self.icon_report = ImageTk.PhotoImage(Image.open("images/icon_report.png").resize(size))
            self.icon_logout = ImageTk.PhotoImage(Image.open("images/icon_logout.png").resize(size))
            self.icon_exit = ImageTk.PhotoImage(Image.open("images/icon_exit.png").resize(size))
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load icons: {str(e)}")

    def make_sidebar_button(self, parent, text, icon, bg, command):
        return tk.Button(
            parent,
            text="  " + text,
            image=icon,
            compound=tk.LEFT,
            font=("Segoe UI", 14, "bold"),
            bg=bg,
            fg="white",
            cursor="hand2",
            activebackground="#34495E",
            relief=tk.FLAT,
            command=command,
            padx=20,
            pady=10
        )

    def create_stat_card(self, parent, text, bg, col):
        card = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 18, "bold"),
            bg=bg,
            fg="white",
            width=20,
            height=4,
            bd=2,
            relief=tk.GROOVE,
            anchor="center"
        )
        card.grid(row=0, column=col, padx=20, pady=10, sticky="nsew")
        return card

    def update_details(self):
        con = None
        try:
            con = sqlite3.connect("student_results.db")
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM course")
            course = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM student")
            student = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM result")
            result = cur.fetchone()[0]

            self.lb1_course.config(text=f"Total Courses\n[ {course} ]")
            self.lb1_student.config(text=f"Total Students\n[ {student} ]")
            self.lb1_result.config(text=f"Total Results\n[ {student} ]")

        except sqlite3.OperationalError as e:
            self.lb1_course.config(text="Total Courses\n[ 0 ]")
            self.lb1_student.config(text="Total Students\n[ 0 ]")
            self.lb1_result.config(text="Total Results\n[ 0 ]")
        except Exception as ex:
            messagebox.showerror("Error", f"Dashboard error: {str(ex)}")
        finally:
            if con:
                con.close()

    def add_course(self):
        self.new_win = tk.Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = tk.Toplevel(self.root)
        self.new_obj = AdvancedStudentClass(self.new_win)

    def add_result(self):
        self.new_win = tk.Toplevel(self.root)
        self.new_obj = AdvancedResultSystem(self.new_win)

    def add_report(self):
        self.new_win = tk.Toplevel(self.root)
        self.new_obj = ReportViewer(self.new_win)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root):
            self.root.destroy()
            login_win = tk.Tk()
            AdvancedLogoutSystem(login_win)
            login_win.mainloop()

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    obj = RMS(root)
    root.mainloop()
