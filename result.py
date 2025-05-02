from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import webbrowser
from tkinter.font import Font
import time

class AdvancedResultSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg='#f8f9fa')
        self.root.focus_force()

        # ===== Custom Fonts =====
        self.title_font = Font(family="Helvetica", size=24, weight="bold")
        self.label_font = Font(family="Segoe UI", size=12)
        self.button_font = Font(family="Segoe UI", size=12, weight="bold")
        self.result_font = Font(family="Consolas", size=11)

        # ===== Variables =====
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_subject = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.roll_list = []
        self.fetch_roll()

        # ===== Main Container =====
        self.main_frame = Frame(self.root, bg='#ffffff', bd=0, highlightthickness=0)
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # ===== Header =====
        header = Frame(self.main_frame, bg='#343a40', bd=0)
        header.place(x=0, y=0, relwidth=1, height=70)

        Label(header, text="STUDENT RESULT MANAGEMENT SYSTEM", font=self.title_font, bg='#343a40', fg='white').pack(side=LEFT, padx=20)
        Button(header, text="Help", font=self.button_font, bg='#17a2b8', fg='white', bd=0, command=self.show_help).pack(side=RIGHT, padx=20)

        # ===== Left Panel =====
        left_panel = Frame(self.main_frame, bg='#ffffff', bd=0)
        left_panel.place(x=30, y=90, width=500, height=580)

        form_container = Frame(left_panel, bg='#f1f3f5', bd=0)
        form_container.place(x=0, y=0, width=500, height=580)

        Label(form_container, text="Add/Edit Results", font=("Helvetica", 18, "bold"), bg='#f1f3f5', fg='#343a40').place(x=0, y=20, relwidth=1)

        self.create_form_field(form_container, "Select Student", self.var_roll, y_pos=80, is_combo=True)
        Button(form_container, text='Search', font=self.button_font, bg='#28a745', fg='white', bd=0, command=self.search).place(x=350, y=80, width=120, height=35)

        self.create_form_field(form_container, "Name", self.var_name, y_pos=140, readonly=True)
        self.create_form_field(form_container, "Course", self.var_course, y_pos=200, readonly=True)
        self.create_form_field(form_container, "Subject", self.var_subject, y_pos=260)
        self.create_form_field(form_container, "Marks Obtained", self.var_marks, y_pos=320)
        self.create_form_field(form_container, "Full Marks", self.var_full_marks, y_pos=380)

        btn_frame = Frame(form_container, bg='#f1f3f5')
        btn_frame.place(x=50, y=440, width=400)

        Button(btn_frame, text='Submit', font=self.button_font, bg='#007bff', fg='white', bd=0, command=self.add).pack(side=LEFT, padx=10, ipadx=20, ipady=8)
        Button(btn_frame, text='Clear', font=self.button_font, bg='#6c757d', fg='white', bd=0, command=self.clear).pack(side=LEFT, padx=10, ipadx=20, ipady=8)
        Button(btn_frame, text='Clear All', font=self.button_font, bg='#dc3545', fg='white', bd=0, command=self.clear_all).pack(side=LEFT, padx=10, ipadx=20, ipady=8)

        # ===== Right Panel =====
        right_panel = Frame(self.main_frame, bg='#ffffff', bd=0)
        right_panel.place(x=550, y=90, width=770, height=580)

        results_container = Frame(right_panel, bg='#f1f3f5', bd=0)
        results_container.place(x=0, y=0, width=770, height=580)

        Label(results_container, text="Student Results", font=("Helvetica", 18, "bold"), bg='#f1f3f5', fg='#343a40').place(x=0, y=20, relwidth=1)

        table_frame = Frame(results_container, bg='#ffffff', bd=0)
        table_frame.place(x=20, y=70, width=730, height=400)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background='#343a40', foreground='white')
        style.configure("Treeview", font=self.result_font, rowheight=25)
        style.map("Treeview", background=[('selected', '#007bff')])

        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)

        self.result_table = ttk.Treeview(table_frame, columns=("subject", "marks", "full", "grade", "percent"),
                                         yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.result_table.yview)
        scroll_x.config(command=self.result_table.xview)

        self.result_table.heading("subject", text="Subject")
        self.result_table.heading("marks", text="Marks")
        self.result_table.heading("full", text="Full Marks")
        self.result_table.heading("grade", text="Grade")
        self.result_table.heading("percent", text="Percentage")

        self.result_table.column("subject", width=180, anchor=W)
        self.result_table.column("marks", width=80, anchor=CENTER)
        self.result_table.column("full", width=100, anchor=CENTER)
        self.result_table.column("grade", width=80, anchor=CENTER)
        self.result_table.column("percent", width=100, anchor=CENTER)

        self.result_table['show'] = 'headings'
        self.result_table.pack(fill=BOTH, expand=1)

        self.delete_button = Button(results_container, text='Delete Selected', font=self.button_font,
                                    bg='#dc3545', fg='white', bd=0, command=self.delete_selected, state=DISABLED)
        self.delete_button.place(x=580, y=490, width=150, height=40)

        summary_frame = Frame(results_container, bg='#e9ecef', bd=0)
        summary_frame.place(x=20, y=490, width=530, height=70)

        self.total_marks_label = Label(summary_frame, text="Total Marks: 0", font=("Segoe UI", 12, "bold"), bg='#e9ecef')
        self.total_marks_label.pack(side=LEFT, padx=20, pady=10)

        self.percentage_label = Label(summary_frame, text=" Percentage: 0%", font=("Segoe UI", 12, "bold"), bg='#e9ecef')
        self.percentage_label.pack(side=LEFT, padx=20, pady=10)

        self.grade_label = Label(summary_frame, text="Grade:", font=("Segoe UI", 12, "bold"), bg='#e9ecef')
        self.grade_label.pack(side=LEFT, padx=20, pady=10)

        self.result_table.bind("<<TreeviewSelect>>", self.on_select_row)
        self.root.bind("<F5>", lambda e: self.load_existing_results())

    # === More backend functions will continue here (fetch_roll, search, add, clear, load_existing_results, etc.) ===


    def create_form_field(self, parent, label_text, variable, y_pos, readonly=False, is_combo=False):
        field_frame = Frame(parent, bg='#f1f3f5')
        field_frame.place(x=50, y=y_pos, width=400)

        Label(field_frame, text=label_text, font=self.label_font, bg='#f1f3f5', fg='#495057').pack(anchor=W)

        if is_combo:
            self.txt_student = ttk.Combobox(field_frame, textvariable=variable, 
                                          values=self.roll_list, font=self.label_font)
            self.txt_student.pack(fill=X, pady=5, ipady=8)
            self.txt_student.set("Select")
        elif readonly:
            Entry(field_frame, textvariable=variable, font=self.label_font, 
                 bg='#e9ecef', fg='#495057', state='readonly', bd=1, relief='solid').pack(fill=X, pady=5, ipady=8)
        else:
            Entry(field_frame, textvariable=variable, font=self.label_font, 
                 bg='white', fg='#495057', bd=1, relief='solid').pack(fill=X, pady=5, ipady=8)

    def show_help(self):
        help_window = Toplevel(self.root)
        help_window.title("Help Documentation")
        help_window.geometry("600x400+200+200")
        help_window.resizable(False, False)
        
        help_text = """RESULT MANAGEMENT SYSTEM HELP GUIDE

1. Search Student:
   - Select student roll number from dropdown
   - Click Search button to load student details

2. Add Results:
   - Enter subject details
   - Enter marks obtained and full marks
   - Click Submit to save

3. Manage Results:
   - Select a subject to delete
   - Click Delete Selected to remove

4. Shortcuts:
   - F5: Refresh results
   - Enter: Submit form
"""
        Label(help_window, text=help_text, font=("Consolas", 11), justify=LEFT).pack(padx=20, pady=20)
        
        Button(help_window, text="Open Online Documentation", font=self.button_font,
              bg="#007bff", fg="white", command=lambda: webbrowser.open("https://example.com/docs")).pack(pady=10)

    # ====== Backend Functions ======
    def fetch_roll(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll FROM student")
            rows = cur.fetchall()
            self.roll_list = [row[0] for row in rows]
            if hasattr(self, 'txt_student'):
                self.txt_student['values'] = self.roll_list
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def search(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            if not self.var_roll.get() or self.var_roll.get() == "Select":
                messagebox.showerror("Error", "Please select a student", parent=self.root)
                return

            cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
                self.load_existing_results()
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def add(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            if not all([self.var_roll.get(), self.var_name.get(), self.var_course.get(), 
                       self.var_subject.get(), self.var_marks.get(), self.var_full_marks.get()]):
                messagebox.showerror("Error", "All fields are required.", parent=self.root)
                return

            if not self.var_marks.get().isdigit() or not self.var_full_marks.get().isdigit():
                messagebox.showerror("Error", "Marks must be numeric values", parent=self.root)
                return

            subject = self.var_subject.get().strip()

            # Check if marks exceed full marks
            if int(self.var_marks.get()) > int(self.var_full_marks.get()):
                messagebox.showerror("Error", "Marks obtained cannot exceed full marks", parent=self.root)
                return

            cur.execute("SELECT * FROM result WHERE roll=? AND course=? AND subject=?",
                        (self.var_roll.get(), self.var_course.get(), subject))
            if cur.fetchone():
                messagebox.showerror("Error", f"Result for {subject} already exists.", parent=self.root)
            else:
                cur.execute("INSERT INTO result (roll, name, course, subject, marks_ob, full_marks) VALUES (?, ?, ?, ?, ?, ?)",
                            (self.var_roll.get(), self.var_name.get(), self.var_course.get(), subject, 
                             self.var_marks.get(), self.var_full_marks.get()))
                con.commit()
                messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
                self.clear()
                self.load_existing_results()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.var_subject.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")

    def clear_all(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.clear()
        self.result_table.delete(*self.result_table.get_children())
        self.total_marks_label.config(text="Total Marks: 0")
        self.percentage_label.config(text="Overall Percentage: 0%")
        self.grade_label.config(text="Overall Grade: -")
        self.delete_button.config(state=DISABLED)

    def load_existing_results(self):
        if not self.var_roll.get() or self.var_roll.get() == "Select":
            return

        self.result_table.delete(*self.result_table.get_children())
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        total_marks = 0
        total_full = 0
        try:
            cur.execute("SELECT subject, marks_ob, full_marks FROM result WHERE roll=? AND course=?",
                        (self.var_roll.get(), self.var_course.get()))
            rows = cur.fetchall()
            for row in rows:
                subject, marks, full = row
                marks = int(marks)
                full = int(full)
                percent = round((marks / full) * 100, 2) if full else 0
                grade = self.get_grade(percent)
                self.result_table.insert('', END, values=(subject, marks, full, grade, f"{percent}%"))
                total_marks += marks
                total_full += full

            self.total_marks_label.config(text=f"Total Marks: {total_marks}")
            if total_full > 0:
                overall_percent = round((total_marks / total_full) * 100, 2)
                self.percentage_label.config(text=f"Percentage: {overall_percent}%")
                overall_grade = self.get_grade(overall_percent)
                self.grade_label.config(text=f"Grade: {overall_grade}")
            else:
                self.percentage_label.config(text="Overall Percentage: 0%")
                self.grade_label.config(text="Grade:")
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading results: {str(ex)}")

    def get_grade(self, percent):
        if percent >= 90:
            return "A+"
        elif percent >= 80:
            return "A"
        elif percent >= 70:
            return "B"
        elif percent >= 60:
            return "C"
        elif percent >= 50:
            return "D"
        else:
            return "F"

    def delete_selected(self):
        selected_item = self.result_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a subject to delete", parent=self.root)
            return

        values = self.result_table.item(selected_item, "values")
        subject = values[0]

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete result for '{subject}'?", parent=self.root)
        if not confirm:
            return

        try:
            con = sqlite3.connect(database="student_results.db")
            cur = con.cursor()
            cur.execute("DELETE FROM result WHERE roll=? AND course=? AND subject=?",
                        (self.var_roll.get(), self.var_course.get(), subject))
            con.commit()
            messagebox.showinfo("Deleted", f"Result for '{subject}' deleted successfully.", parent=self.root)
            self.load_existing_results()
        except Exception as ex:
            messagebox.showerror("Error", f"Error while deleting: {str(ex)}")

    def on_select_row(self, event):
        if self.result_table.focus():
            self.delete_button.config(state=NORMAL)
        else:
            self.delete_button.config(state=DISABLED)

if __name__ == "__main__":
    root = Tk()
    obj = AdvancedResultSystem(root)
    root.mainloop()