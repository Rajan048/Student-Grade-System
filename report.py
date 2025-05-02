from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import os

class ReportViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Viewer")
        self.root.geometry("1100x520+100+100")
        self.root.config(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.var_search = StringVar()

        # Header
        Label(self.root, text="📄 Student Result Viewer", font=("Segoe UI", 22, "bold"), bg="#2f3542", fg="white").pack(fill=X, pady=10)

        # Search Section
        search_frame = Frame(self.root, bg="#f5f6fa")
        search_frame.pack(pady=20)

        Label(search_frame, text="🔎 Roll No.", font=("Segoe UI", 14), bg="#f5f6fa").grid(row=0, column=0, padx=10)
        Entry(search_frame, textvariable=self.var_search, font=("Segoe UI", 13), width=25, bd=1, relief=SOLID).grid(row=0, column=1, padx=5)

        self.create_button("Search", "#0984e3", self.search, search_frame).grid(row=0, column=2, padx=10)
        self.create_button("Clear", "#576574", self.clear, search_frame).grid(row=0, column=3, padx=5)

        # Result Frame
        result_frame = Frame(self.root, bg="#ffffff", bd=2, relief=GROOVE)
        result_frame.pack(padx=20, pady=10, fill=X)

        headers = ["Roll No", "Name", "Course", "Marks Obtained", "Total Marks", "Percentage", "Grade"]
        self.labels = {}
        for idx, header in enumerate(headers):
            Label(result_frame, text=header, font=("Segoe UI", 12, "bold"), bg="#dcdde1", fg="#2f3542").grid(row=0, column=idx, padx=5, pady=5, ipadx=5)
            key = header.lower().replace(" ", "")
            self.labels[key] = Label(result_frame, text="", font=("Segoe UI", 12), bg="white", width=15, relief=GROOVE, anchor='center')
            self.labels[key].grid(row=1, column=idx, padx=5, pady=5)

        # Action Buttons
        action_frame = Frame(self.root, bg="#f5f6fa")
        action_frame.pack(pady=20)

        self.create_button("🗑 Delete Result", "#e17055", self.delete, action_frame, width=20).pack(side=LEFT, padx=20)
        self.create_button("📄 Download PDF", "#00b894", self.export_pdf, action_frame, width=22).pack(side=LEFT)

    def create_button(self, text, bg, command, parent, width=12):
        return Button(parent, text=text, font=("Segoe UI", 11, "bold"), bg=bg, fg="white", bd=0,
                      cursor="hand2", activebackground=bg, activeforeground="white", width=width, height=1, command=command)

    def search(self):
        roll = self.var_search.get().strip()
        if not roll:
            return messagebox.showerror("Error", "Roll No. is required", parent=self.root)

        try:
            con = sqlite3.connect("student_results.db")
            cur = con.cursor()
            cur.execute("SELECT name, course FROM student WHERE roll=?", (roll,))
            student = cur.fetchone()

            if not student:
                return messagebox.showerror("Error", "Student not found", parent=self.root)

            self.labels['rollno'].config(text=roll)
            self.labels['name'].config(text=student[0])
            self.labels['course'].config(text=student[1])

            cur.execute("SELECT subject, marks_ob, full_marks FROM result WHERE roll=?", (roll,))
            self.results = cur.fetchall()

            if not self.results:
                self.clear()
                return messagebox.showinfo("Info", "No result found", parent=self.root)

            total_obt = sum(float(row[1]) for row in self.results)
            total_full = sum(float(row[2]) for row in self.results)
            percentage = (total_obt / total_full) * 100 if total_full else 0
            grade = self.get_grade(percentage)

            self.labels['marksobtained'].config(text=f"{total_obt:.2f}")
            self.labels['totalmarks'].config(text=f"{total_full:.2f}")
            self.labels['percentage'].config(text=f"{percentage:.2f} %")
            self.labels['grade'].config(text=grade)

        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)

    def get_grade(self, percentage):
        if percentage >= 90: return 'A+'
        elif percentage >= 80: return 'A'
        elif percentage >= 70: return 'B'
        elif percentage >= 60: return 'C'
        elif percentage >= 50: return 'D'
        return 'F'

    def clear(self):
        self.var_search.set("")
        for lbl in self.labels.values():
            lbl.config(text="")
        self.results = []

    def delete(self):
        roll = self.var_search.get().strip()
        if not roll:
            return messagebox.showerror("Error", "Search student first", parent=self.root)

        try:
            con = sqlite3.connect("student_results.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM result WHERE roll=?", (roll,))
            if not cur.fetchone():
                return messagebox.showerror("Error", "No result found", parent=self.root)

            if messagebox.askyesno("Confirm", "Are you sure to delete the result?", parent=self.root):
                cur.execute("DELETE FROM result WHERE roll=?", (roll,))
                con.commit()
                messagebox.showinfo("Deleted", "Result deleted", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", str(ex), parent=self.root)

    def export_pdf(self):
        if not hasattr(self, 'results') or not self.results:
            return messagebox.showerror("Error", "No data to export", parent=self.root)

        file_name = f"Result_{self.labels['rollno'].cget('text')}.pdf"
        c = canvas.Canvas(file_name, pagesize=A4)
        width, height = A4
        y = height - inch

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, y, "Student Result Report")
        y -= 40

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Roll No: {self.labels['rollno'].cget('text')}")
        c.drawString(250, y, f"Name: {self.labels['name'].cget('text')}")
        c.drawString(450, y, f"Course: {self.labels['course'].cget('text')}")
        y -= 30
        c.line(50, y, 550, y)
        y -= 20

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Subject")
        c.drawString(180, y, "Obtained")
        c.drawString(300, y, "Full Marks")
        c.drawString(420, y, "Grade")
        y -= 20

        c.setFont("Helvetica", 11)
        for subject, marks_ob, full_marks in self.results:
            perc = (float(marks_ob) / float(full_marks)) * 100
            grade = self.get_grade(perc)
            c.drawString(50, y, subject)
            c.drawString(180, y, str(marks_ob))
            c.drawString(300, y, str(full_marks))
            c.drawString(420, y, grade)
            y -= 20

        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total Obtained: {self.labels['marksobtained'].cget('text')}")
        c.drawString(250, y, f"Total Marks: {self.labels['totalmarks'].cget('text')}")
        c.drawString(450, y, f"Percentage: {self.labels['percentage'].cget('text')}")
        y -= 20
        c.drawString(50, y, f"Final Grade: {self.labels['grade'].cget('text')}")

        c.save()
        messagebox.showinfo("Exported", f"PDF saved as {file_name}", parent=self.root)
        os.startfile(file_name)

if __name__ == "__main__":
    root = Tk()
    app = ReportViewer(root)
    root.mainloop()
