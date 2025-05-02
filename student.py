from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk
import tkinter.font as tkFont
import os
import csv
from datetime import datetime
import webbrowser

class AdvancedStudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Student Management System")
        self.root.geometry("1400x800+0+0")
        self.root.config(bg='#f8f9fa')
        self.root.focus_force()
        
        # Custom fonts
        self.title_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.label_font = tkFont.Font(family="Segoe UI", size=12)
        self.entry_font = tkFont.Font(family="Segoe UI", size=11)
        self.button_font = tkFont.Font(family="Segoe UI", size=11, weight="bold")
        self.small_font = tkFont.Font(family="Segoe UI", size=9)
        
        # Custom colors
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#e74c3c"
        self.success_color = "#27ae60"
        self.warning_color = "#f39c12"
        self.light_bg = "#ecf0f1"
        self.dark_text = "#2c3e50"
        self.light_text = "#ecf0f1"
        
        # Initialize database
        self.initialize_database()
        
        # Main container
        self.main_frame = Frame(self.root, bg=self.light_bg)
        self.main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.header = Frame(self.main_frame, bg=self.primary_color, height=90)
        self.header.pack(fill=X, pady=(0,15))
        
        # Title with icon
        self.title_frame = Frame(self.header, bg=self.primary_color)
        self.title_frame.pack(side=LEFT, padx=20)
        
        # Load and display icon
        try:
            self.icon = Image.open("student_icon.png").resize((40, 40))
            self.icon_img = ImageTk.PhotoImage(self.icon)
            Label(self.title_frame, image=self.icon_img, bg=self.primary_color).pack(side=LEFT, padx=(0,10))
        except:
            pass  # Continue without icon if image not found
            
        self.title = Label(self.title_frame, text="ADVANCED STUDENT MANAGEMENT SYSTEM", 
                         font=self.title_font, bg=self.primary_color, fg=self.light_text)
        self.title.pack(side=LEFT)
        
        # Add clock
        self.clock_label = Label(self.header, font=("Segoe UI", 12), 
                               bg=self.primary_color, fg=self.light_text)
        self.clock_label.pack(side=RIGHT, padx=20)
        self.update_clock()
        
        # Add a decorative line
        self.decor_line = Frame(self.header, height=3, bg=self.secondary_color)
        self.decor_line.pack(side=BOTTOM, fill=X, padx=30)
        
        # Content area
        self.content_frame = Frame(self.main_frame, bg=self.light_bg)
        self.content_frame.pack(fill=BOTH, expand=True)
        
        # Left panel (Form)
        self.left_panel = Frame(self.content_frame, bg='white', bd=2, relief=GROOVE,
                              highlightbackground="#bdc3c7", highlightthickness=1)
        self.left_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,15))
        
        # Form title with student count
        self.form_title = Frame(self.left_panel, bg=self.primary_color, height=50)
        self.form_title.pack(fill=X)
        
        self.form_title_label = Label(self.form_title, text="Student Details Form", 
                                    font=self.label_font, bg=self.primary_color, 
                                    fg=self.light_text)
        self.form_title_label.pack(side=LEFT, padx=20)
        
        self.student_count_label = Label(self.form_title, font=self.small_font, 
                                       bg=self.primary_color, fg=self.light_text)
        self.student_count_label.pack(side=RIGHT, padx=20)
        self.update_student_count()
        
        # Form content
        self.form_content = Frame(self.left_panel, bg='white', padx=20, pady=20)
        self.form_content.pack(fill=BOTH, expand=True)
        
        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        self.var_search = StringVar()
        self.var_search_by = StringVar(value="Roll No.")
        
        # Form rows
        self.create_form_row("Roll No.*", self.var_roll, 0)
        self.txt_roll = self.entries[0]  # Keep reference to roll entry
        
        self.create_form_row("Full Name*", self.var_name, 1)
        self.create_form_row("Email*", self.var_email, 2)
        
        # Gender combobox
        Label(self.form_content, text="Gender*", font=self.label_font, 
             bg='white').grid(row=3, column=0, sticky='w', pady=(10,5))
        self.txt_gender = ttk.Combobox(self.form_content, textvariable=self.var_gender, 
                                      values=("Select", "Male", "Female", "Other"), 
                                      font=self.entry_font, state='readonly')
        self.txt_gender.grid(row=3, column=1, sticky='ew', pady=(10,5), ipady=5)
        self.txt_gender.current(0)
        
        # Course combobox
        Label(self.form_content, text="Course*", font=self.label_font, 
             bg='white').grid(row=3, column=2, sticky='w', pady=(10,5))
        self.course_list = []
        self.fetch_course()
        self.txt_course = ttk.Combobox(self.form_content, textvariable=self.var_course, 
                                      values=self.course_list, font=self.entry_font, state='readonly')
        self.txt_course.grid(row=3, column=3, sticky='ew', pady=(10,5), ipady=5)
        self.txt_course.set("Select")
        
        self.create_form_row("Date of Birth", self.var_dob, 4)
        self.create_form_row("Contact No.*", self.var_contact, 5)
        self.create_form_row("State", self.var_state, 6)
        self.create_form_row("City", self.var_city, 7)
        self.create_form_row("Pin Code", self.var_pin, 8)
        
        # Address field
        Label(self.form_content, text="Address", font=self.label_font, 
             bg='white').grid(row=9, column=0, sticky='nw', pady=(10,5))
        self.txt_address = Text(self.form_content, font=self.entry_font, height=4, 
                              bd=1, relief=SOLID, highlightbackground="#bdc3c7", 
                              highlightthickness=1)
        self.txt_address.grid(row=9, column=1, columnspan=3, sticky='ew', pady=(10,5))
        
        # Required fields note
        Label(self.form_content, text="* Required fields", font=self.small_font, 
             bg='white', fg='red').grid(row=10, column=0, columnspan=4, sticky='w', pady=(5,0))
        
        # Buttons
        self.button_frame = Frame(self.left_panel, bg='white', pady=10)
        self.button_frame.pack(fill=X, padx=20)
        
        Button(self.button_frame, text='SAVE', font=self.button_font, bg=self.success_color, 
              fg='white', bd=0, padx=20, command=self.add, cursor="hand2").pack(side=LEFT, padx=5)
        Button(self.button_frame, text='UPDATE', font=self.button_font, bg=self.secondary_color, 
              fg='white', bd=0, padx=20, command=self.update, cursor="hand2").pack(side=LEFT, padx=5)
        Button(self.button_frame, text='DELETE', font=self.button_font, bg=self.accent_color, 
              fg='white', bd=0, padx=20, command=self.delete, cursor="hand2").pack(side=LEFT, padx=5)
        Button(self.button_frame, text='CLEAR', font=self.button_font, bg="#7f8c8d", 
              fg='white', bd=0, padx=20, command=self.clear, cursor="hand2").pack(side=LEFT, padx=5)
        Button(self.button_frame, text='EXPORT', font=self.button_font, bg=self.warning_color, 
              fg='white', bd=0, padx=20, command=self.export_data, cursor="hand2").pack(side=LEFT, padx=5)
        
        # Right panel (Table)
        self.right_panel = Frame(self.content_frame, bg='white', bd=2, relief=GROOVE,
                                highlightbackground="#bdc3c7", highlightthickness=1)
        self.right_panel.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Search bar
        self.search_frame = Frame(self.right_panel, bg=self.primary_color, padx=10, pady=10)
        self.search_frame.pack(fill=X)
        
        Label(self.search_frame, text="Search By:", font=self.label_font, 
             bg=self.primary_color, fg=self.light_text).pack(side=LEFT)
        
        self.search_by = ttk.Combobox(self.search_frame, textvariable=self.var_search_by, 
                                     values=("Roll No.", "Name", "Course", "Contact"), 
                                     font=self.entry_font, state='readonly', width=10)
        self.search_by.pack(side=LEFT, padx=5)
        
        self.search_entry = Entry(self.search_frame, textvariable=self.var_search, 
                                font=self.entry_font, bd=1, relief=SOLID)
        self.search_entry.pack(side=LEFT, fill=X, expand=True, padx=10, ipady=3)
        self.search_entry.bind("<Return>", lambda e: self.search())  # Search on Enter key
        
        Button(self.search_frame, text="Search", font=self.button_font, 
              bg=self.secondary_color, fg='white', bd=0, 
              command=self.search, cursor="hand2").pack(side=LEFT, padx=5)
        Button(self.search_frame, text="Show All", font=self.button_font, 
              bg="#95a5a6", fg='white', bd=0, 
              command=self.show_all, cursor="hand2").pack(side=LEFT)
        
        # Table frame
        self.table_frame = Frame(self.right_panel, bg='white')
        self.table_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0,10))
        
        # Scrollbars
        self.scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        
        # Treeview with enhanced styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), 
                       background=self.primary_color, foreground=self.light_text)
        style.configure("Treeview", font=self.entry_font, rowheight=28, 
                       fieldbackground=self.light_bg)
        style.map("Treeview", background=[('selected', self.secondary_color)],
                 foreground=[('selected', 'white')])
        
        self.StudentTable = ttk.Treeview(self.table_frame, 
                                       columns=("roll", "name", "email", "gender", 
                                               "dob", "contact", "course"),
                                       xscrollcommand=self.scroll_x.set, 
                                       yscrollcommand=self.scroll_y.set)
        
        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.scroll_x.config(command=self.StudentTable.xview)
        self.scroll_y.config(command=self.StudentTable.yview)
        
        columns = ("roll", "name", "email", "gender", "dob", "contact", "course")
        for col in columns:
            self.StudentTable.heading(col, text=col.capitalize())
            self.StudentTable.column(col, width=100 if col != "name" else 150, anchor=CENTER)
        
        self.StudentTable["show"] = 'headings'
        self.StudentTable.pack(fill=BOTH, expand=True)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)
        self.StudentTable.bind("<Double-1>", self.show_full_details)
        
        # Status bar
        self.status_bar = Frame(self.main_frame, bg=self.primary_color, height=30)
        self.status_bar.pack(fill=X, pady=(10,0))
        
        self.status_label = Label(self.status_bar, text="Ready", font=("Segoe UI", 10), 
                                bg=self.primary_color, fg=self.light_text)
        self.status_label.pack(side=LEFT, padx=20)
        
        # Help link
        self.help_link = Label(self.status_bar, text="Help", font=("Segoe UI", 10, "underline"), 
                             bg=self.primary_color, fg=self.light_text, cursor="hand2")
        self.help_link.pack(side=RIGHT, padx=20)
        self.help_link.bind("<Button-1>", lambda e: self.open_help())
        
        # Initialize
        self.show()
        
    def initialize_database(self):
        """Initialize database with required tables"""
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            # Check if tables exist
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student'")
            if not cur.fetchone():
                # Create student table if not exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS student(
                        roll INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        gender TEXT,
                        dob TEXT,
                        contact TEXT,
                        course TEXT,
                        state TEXT,
                        city TEXT,
                        pin TEXT,
                        address TEXT
                    )
                """)
                
                # Create courses table if not exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS course(
                        cid INTEGER PRIMARY KEY, 
                        name TEXT, 
                        duration TEXT, 
                        charges TEXT, 
                        description TEXT
                    )
                """)
                
                con.commit()
        except Exception as ex:
            messagebox.showerror("Database Error", f"Error initializing database: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def update_clock(self):
        """Update the clock label with current time"""
        now = datetime.now().strftime("%I:%M:%S %p | %d-%b-%Y")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)
    
    def update_student_count(self):
        """Update the student count label"""
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM student")
            count = cur.fetchone()[0]
            self.student_count_label.config(text=f"Total Students: {count}")
        except Exception as ex:
            self.student_count_label.config(text="Error loading count")
        finally:
            con.close()
        
    def create_form_row(self, label_text, variable, row):
        """Helper method to create consistent form rows"""
        if not hasattr(self, 'entries'):
            self.entries = []
            
        # Add red asterisk for required fields
        req_color = "red" if label_text.endswith("*") else self.dark_text
        Label(self.form_content, text=label_text, font=self.label_font, 
             bg='white', fg=req_color).grid(row=row, column=0, sticky='w', pady=(10,5))
        
        if row in (0, 1, 2):  # First column fields
            entry = Entry(self.form_content, textvariable=variable, font=self.entry_font, 
                         bd=1, relief=SOLID, highlightbackground="#bdc3c7", 
                         highlightthickness=1)
            entry.grid(row=row, column=1, sticky='ew', pady=(10,5), ipady=5)
            self.entries.append(entry)
            
            # Add second column fields
            second_labels = ["Date of Birth", "Contact No.*", "State"]
            if row < 3:
                req_color = "red" if second_labels[row].endswith("*") else self.dark_text
                Label(self.form_content, text=second_labels[row], font=self.label_font, 
                     bg='white', fg=req_color).grid(row=row, column=2, sticky='w', pady=(10,5))
                
                second_vars = [self.var_dob, self.var_contact, self.var_state]
                entry = Entry(self.form_content, textvariable=second_vars[row], 
                            font=self.entry_font, bd=1, relief=SOLID, 
                            highlightbackground="#bdc3c7", highlightthickness=1)
                entry.grid(row=row, column=3, sticky='ew', pady=(10,5), ipady=5)
                self.entries.append(entry)
        
        elif row >= 4:  # Single column fields
            entry = Entry(self.form_content, textvariable=variable, font=self.entry_font, 
                         bd=1, relief=SOLID, highlightbackground="#bdc3c7", 
                         highlightthickness=1)
            entry.grid(row=row, column=1, sticky='ew', pady=(10,5), ipady=5)
            self.entries.append(entry)

    def validate_fields(self):
        """Validate required fields before saving"""
        errors = []
        if not self.var_roll.get():
            errors.append("Roll Number is required")
        if not self.var_name.get():
            errors.append("Full Name is required")
        if not self.var_email.get():
            errors.append("Email is required")
        elif "@" not in self.var_email.get():
            errors.append("Valid Email is required")
        if not self.var_contact.get():
            errors.append("Contact Number is required")
        elif not self.var_contact.get().isdigit() or len(self.var_contact.get()) < 10:
            errors.append("Valid Contact Number is required")
        if self.var_course.get() == "Select":
            errors.append("Course selection is required")
        if self.var_gender.get() == "Select":
            errors.append("Gender selection is required")
            
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors), parent=self.root)
            self.status_label.config(text="Validation errors found")
            return False
        return True

    def clear(self):
        self.show_all()
        self.status_label.config(text="Ready")
        for var in [self.var_roll, self.var_name, self.var_email, self.var_gender, self.var_dob,
                    self.var_contact, self.var_course, self.var_state,
                    self.var_city, self.var_pin, self.var_search]:
            var.set("" if var not in [self.var_gender, self.var_course] else "Select")
        self.txt_address.delete("1.0", END)
        self.txt_roll.config(state=NORMAL)
        self.var_search_by.set("Roll No.")

    def delete(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll No. is required", parent=self.root)
                self.status_label.config(text="Error: Roll No. required")
            else:
                cur.execute("select * from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Please select student from the list first", parent=self.root)
                    self.status_label.config(text="Error: Select student first")
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete this student?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Student deleted successfully", parent=self.root)
                        self.status_label.config(text="Student deleted successfully")
                        self.clear()
                        self.update_student_count()
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
            self.status_label.config(text=f"Error: {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        self.txt_roll.config(state='readonly')
        r = self.StudentTable.focus()
        content = self.StudentTable.item(r)
        row = content["values"]
        if row:
            self.var_roll.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_dob.set(row[4])
            self.var_contact.set(row[5])
            self.var_course.set(row[6])
            self.status_label.config(text=f"Displaying record for {row[1]}")
            
            # Fetch full details for address fields
            con = sqlite3.connect(database="student_results.db")
            cur = con.cursor()
            try:
                cur.execute("SELECT state, city, pin, address FROM student WHERE roll=?", (row[0],))
                details = cur.fetchone()
                if details:
                    self.var_state.set(details[0])
                    self.var_city.set(details[1])
                    self.var_pin.set(details[2])
                    self.txt_address.delete("1.0", END)
                    self.txt_address.insert("1.0", details[3])
            except Exception as ex:
                messagebox.showerror("Error", f"Error loading details: {str(ex)}", parent=self.root)
            finally:
                con.close()

    def show_full_details(self, ev):
        """Show full student details in a messagebox when double-clicking a record"""
        r = self.StudentTable.focus()
        content = self.StudentTable.item(r)
        row = content["values"]
        if row:
            con = sqlite3.connect(database="student_results.db")
            cur = con.cursor()
            try:
                cur.execute("SELECT * FROM student WHERE roll=?", (row[0],))
                details = cur.fetchone()
                if details:
                    # Format the details for display
                    detail_text = f"""
                    Roll No.: {details[0]}
                    Full Name: {details[1]}
                    Email: {details[2]}
                    Gender: {details[3]}
                    Date of Birth: {details[4]}
                    Contact: {details[5]}
                    Course: {details[6]}
                    State: {details[7]}
                    City: {details[8]}
                    Pin Code: {details[9]}
                    
                    Address:
                    {details[10]}
                    """
                    messagebox.showinfo("Student Details", detail_text.strip(), parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error", f"Error loading details: {str(ex)}", parent=self.root)
            finally:
                con.close()

    def update(self):
        if not self.validate_fields():
            return
            
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll No. is required", parent=self.root)
                self.status_label.config(text="Error: Roll No. required")
            else:
                cur.execute("select * from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select student from list", parent=self.root)
                    self.status_label.config(text="Error: Select student first")
                else:
                    cur.execute("""UPDATE student SET name=?, email=?, gender=?, dob=?, 
                                contact=?, course=?, state=?, city=?, 
                                pin=?, address=? WHERE roll=?""",
                              (self.var_name.get(), self.var_email.get(), 
                               self.var_gender.get(), self.var_dob.get(),
                               self.var_contact.get(), self.var_course.get(), 
                               self.var_state.get(), self.var_city.get(), 
                               self.var_pin.get(), self.txt_address.get("1.0", END),
                               self.var_roll.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Student updated successfully", parent=self.root)
                    self.status_label.config(text="Student updated successfully")
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
            self.status_label.config(text=f"Error: {str(ex)}")
        finally:
            con.close()

    def add(self):
        if not self.validate_fields():
            return
            
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll Number is required", parent=self.root)
                self.status_label.config(text="Error: Roll No. required")
            else:
                cur.execute("select * from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Roll No. already exists", parent=self.root)
                    self.status_label.config(text="Error: Roll No. exists")
                else:
                    cur.execute("""INSERT INTO student(roll, name, email, gender, dob, 
                                contact, course, state, city, pin, address) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                              (self.var_roll.get(), self.var_name.get(), 
                               self.var_email.get(), self.var_gender.get(),
                               self.var_dob.get(), self.var_contact.get(), 
                               self.var_course.get(), self.var_state.get(),
                               self.var_city.get(), self.var_pin.get(), 
                               self.txt_address.get("1.0", END)))
                    con.commit()
                    messagebox.showinfo("Success", "Student added successfully", parent=self.root)
                    self.status_label.config(text="Student added successfully")
                    self.show()
                    self.update_student_count()
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
            self.status_label.config(text=f"Error: {str(ex)}")
        finally:
            con.close()

    def show(self):
        """Show all students"""
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            cur.execute("""SELECT roll, name, email, gender, dob, contact, 
                         course FROM student""")
            rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert('', END, values=row)
            self.status_label.config(text=f"Displaying {len(rows)} records")
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
            self.status_label.config(text=f"Error: {str(ex)}")
        finally:
            con.close()

    def show_all(self):
        """Show all students (same as show() now that status is removed)"""
        self.show()

    def fetch_course(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            cur.execute("select name from course")
            rows = cur.fetchall()
            self.course_list = ["Select"] + [row[0] for row in rows]
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
            self.status_label.config(text=f"Error: {str(ex)}")
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            search_term = self.var_search.get()
            search_by = self.var_search_by.get()
            
            if not search_term:
                self.show()
                return
                
            if search_by == "Roll No.":
                query = "SELECT roll, name, email, gender, dob, contact, course FROM student WHERE roll LIKE ?"
                param = f"%{search_term}%"
            elif search_by == "Name":
                query = "SELECT roll, name, email, gender, dob, contact, course FROM student WHERE name LIKE ?"
                param = f"%{search_term}%"
            elif search_by == "Course":
                query = "SELECT roll, name, email, gender, dob, contact, course FROM student WHERE course LIKE ?"
                param = f"%{search_term}%"
            elif search_by == "Contact":
                query = "SELECT roll, name, email, gender, dob, contact, course FROM student WHERE contact LIKE ?"
                param = f"%{search_term}%"
            else:
                query = "SELECT roll, name, email, gender, dob, contact, course FROM student WHERE roll LIKE ? OR name LIKE ?"
                param = (f"%{search_term}%", f"%{search_term}%")
            
            cur.execute(query, (param,) if search_by != "All" else param)
            rows = cur.fetchall()
            
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert('', END, values=row)
                
            self.status_label.config(text=f"Found {len(rows)} matching records")
            
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
            self.status_label.config(text=f"Error: {str(ex)}")
        finally:
            con.close()

    def export_data(self):
        """Export student data to CSV file"""
        try:
            # Ask user for file location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
                title="Save Student Data As"
            )
            
            if not file_path:  # User cancelled
                return
                
            con = sqlite3.connect(database="student_results.db")
            cur = con.cursor()
            
            # Get all student data
            cur.execute("""SELECT roll, name, email, gender, dob, contact, 
                         course, state, city, pin, address FROM student""")
            rows = cur.fetchall()
            
            # Write to CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow([
                    'Roll No', 'Name', 'Email', 'Gender', 'Date of Birth', 
                    'Contact', 'Course', 'State', 'City', 'Pin Code', 'Address'
                ])
                # Write data
                writer.writerows(rows)
                
            messagebox.showinfo("Success", f"Data exported successfully to:\n{file_path}", parent=self.root)
            self.status_label.config(text=f"Data exported to {os.path.basename(file_path)}")
            
        except Exception as ex:
            messagebox.showerror("Export Error", f"Error exporting data: {str(ex)}", parent=self.root)
            self.status_label.config(text=f"Export error: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def open_help(self):
        """Open help documentation in browser"""
        help_url = "https://github.com/yourusername/student-management-system/wiki"
        try:
            webbrowser.open_new_tab(help_url)
            self.status_label.config(text="Opened help documentation")
        except:
            messagebox.showwarning("Help", f"Help documentation available at:\n{help_url}", parent=self.root)
            self.status_label.config(text="Couldn't open browser, see message")

if __name__ == "__main__":
    root = Tk()
    
    # Set window icon if available
    try:
        root.iconbitmap("student_icon.ico")
    except:
        pass
        
    obj = AdvancedStudentClass(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()