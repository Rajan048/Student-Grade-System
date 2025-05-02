from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg='#f0f2f5')  # Modern light background

        # Variables
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()
        self.original_name = ""  # To track original course name during updates

        # Style Configuration
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Segoe UI", 12), background="#f0f2f5")
        self.style.configure("TEntry", font=("Segoe UI", 12), padding=5)
        self.style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=6)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#1a73e8", foreground="white")
        self.style.map("Treeview", background=[('selected', '#1a73e8')])

        # Title
        title = Label(self.root, text="Manage Course Details", font=("Segoe UI", 20, "bold"),
                      bg='#1a73e8', fg='white').place(x=10, y=10, width=1320, height=50)

        # Left Frame (Form)
        form_frame = ttk.LabelFrame(self.root, text="", style="TLabel")
        form_frame.place(x=20, y=80, width=640, height=500)

        # Form Elements
        ttk.Label(form_frame, text="Course Name*").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.txt_courseName = ttk.Entry(form_frame, textvariable=self.var_course, width=30)
        self.txt_courseName.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        ttk.Label(form_frame, text="Duration*").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.duration_combo = ttk.Combobox(form_frame, textvariable=self.var_duration, 
                                         values=["1 Year", "2 Years", "3 Years", "6 Months"], 
                                         state="readonly", width=28)
        self.duration_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        ttk.Label(form_frame, text="Charges*").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.txt_charges = ttk.Entry(form_frame, textvariable=self.var_charges, width=30,
                                   validate="key", validatecommand=(self.root.register(self.validate_charges), '%P'))
        self.txt_charges.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        ttk.Label(form_frame, text="Description").grid(row=3, column=0, padx=10, pady=10, sticky=NW)
        
        # Text Widget with Scrollbar
        self.txt_description = Text(form_frame, font=("Segoe UI", 12), wrap=WORD, height=5, width=40)
        scrolly = ttk.Scrollbar(form_frame, orient=VERTICAL, command=self.txt_description.yview)
        self.txt_description.configure(yscrollcommand=scrolly.set)
        self.txt_description.grid(row=3, column=1, padx=10, pady=10, sticky=W)
        scrolly.grid(row=3, column=2, sticky='ns', pady=10)

        # Buttons
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        btn_style = {"style": "TButton", "width": 10}
        ttk.Button(btn_frame, text='Save', command=self.add, **btn_style).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text='Update', command=self.update, **btn_style).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text='Delete', command=self.delete, **btn_style).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text='Clear', command=self.clear, **btn_style).grid(row=0, column=3, padx=5)

        # Right Frame (Search + Table)
        search_frame = ttk.LabelFrame(self.root, text="Search Courses")
        search_frame.place(x=680, y=80, width=640, height=100)

        ttk.Label(search_frame, text="Course Name:").place(x=10, y=20)
        ttk.Entry(search_frame, textvariable=self.var_search, width=30).place(x=120, y=20)
        ttk.Button(search_frame, text='Search', command=self.search, width=10).place(x=370, y=18)
        ttk.Button(search_frame, text='Show All', command=self.show, width=10).place(x=480, y=18)

        # Table Frame
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.C_Frame.place(x=680, y=190, width=640, height=390)

        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "description"),
                                       show="headings", selectmode="browse")
        
        # Configure Scrollbars
        scrollx = ttk.Scrollbar(self.C_Frame, orient=HORIZONTAL, command=self.CourseTable.xview)
        scrolly = ttk.Scrollbar(self.C_Frame, orient=VERTICAL, command=self.CourseTable.yview)
        self.CourseTable.configure(xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        self.CourseTable.pack(fill=BOTH, expand=1)

        # Configure Columns
        columns = {
            "cid": ("Course ID", 80),
            "name": ("Course Name", 150),
            "duration": ("Duration", 100),
            "charges": ("Charges", 100),
            "description": ("Description", 200)
        }
        
        for col, (heading, width) in columns.items():
            self.CourseTable.heading(col, text=heading)
            self.CourseTable.column(col, width=width, anchor=CENTER)

        self.CourseTable.bind("<<TreeviewSelect>>", self.get_data)
        self.show()

    def validate_charges(self, value):
        if value == "" or value.isdigit():
            return True
        return False

    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0', END)
        self.txt_courseName.config(state=NORMAL)
        self.original_name = ""
        self.show()

    def delete(self):
        if not self.var_course.get():
            messagebox.showerror("Error", "Please select a course first", parent=self.root)
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this course?"):
            try:
                with sqlite3.connect(database="student_results.db") as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM course WHERE name=?", (self.original_name,))
                    cur.execute("INSERT INTO course_id_tracker (cid) VALUES ((SELECT cid FROM course WHERE name=?))", 
                              (self.original_name,))
                    con.commit()
                    messagebox.showinfo("Success", "Course deleted successfully", parent=self.root)
                    self.clear()
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {str(e)}", parent=self.root)

    def get_data(self, ev):
        selected = self.CourseTable.focus()
        if not selected:
            return
        
        data = self.CourseTable.item(selected, 'values')
        if data:
            self.original_name = data[1]  # Store original name for updates
            self.var_course.set(data[1])
            self.var_duration.set(data[2])
            self.var_charges.set(data[3])
            self.txt_description.delete('1.0', END)
            self.txt_description.insert(END, data[4])

    def update(self):
        if not self.validate_fields():
            return
        
        try:
            with sqlite3.connect(database="student_results.db") as con:
                cur = con.cursor()
                
                # Check if name was changed and new name exists
                if self.var_course.get() != self.original_name:
                    cur.execute("SELECT name FROM course WHERE name=?", (self.var_course.get(),))
                    if cur.fetchone():
                        messagebox.showerror("Error", "Course name already exists", parent=self.root)
                        return
                
                cur.execute('''UPDATE course SET 
                            name=?, duration=?, charges=?, description=?
                            WHERE name=?''',
                          (self.var_course.get(), self.var_duration.get(),
                           self.var_charges.get(), self.txt_description.get("1.0", END),
                           self.original_name))
                con.commit()
                messagebox.showinfo("Success", "Course updated successfully", parent=self.root)
                self.show()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}", parent=self.root)

    def add(self):
        if not self.validate_fields():
            return
        
        try:
            with sqlite3.connect(database="student_results.db") as con:
                cur = con.cursor()
                cur.execute("SELECT name FROM course WHERE name=?", (self.var_course.get(),))
                if cur.fetchone():
                    messagebox.showerror("Error", "Course already exists", parent=self.root)
                    return
                
                # Get available cid or generate new
                cur.execute("SELECT cid FROM course_id_tracker LIMIT 1")
                reused_id = cur.fetchone()
                if reused_id:
                    cid = reused_id[0]
                    cur.execute("DELETE FROM course_id_tracker WHERE cid=?", (cid,))
                else:
                    cur.execute("SELECT MAX(cid) FROM course")
                    max_id = cur.fetchone()[0] or 0
                    cid = max_id + 1
                
                cur.execute('''INSERT INTO course 
                            (cid, name, duration, charges, description)
                            VALUES (?, ?, ?, ?, ?)''',
                          (cid, self.var_course.get(), self.var_duration.get(),
                           self.var_charges.get(), self.txt_description.get("1.0", END)))
                con.commit()
                messagebox.showinfo("Success", "Course added successfully", parent=self.root)
                self.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}", parent=self.root)

    def validate_fields(self):
        if not all([self.var_course.get(), self.var_duration.get(), self.var_charges.get()]):
            messagebox.showerror("Error", "Required fields: Name, Duration, Charges", parent=self.root)
            return False
        if not self.var_charges.get().isdigit():
            messagebox.showerror("Error", "Charges must be a number", parent=self.root)
            return False
        return True

    def show(self):
        try:
            with sqlite3.connect(database="student_results.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM course ORDER BY name")
                rows = cur.fetchall()
                self.CourseTable.delete(*self.CourseTable.get_children())
                for row in rows:
                    self.CourseTable.insert('', END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}", parent=self.root)

    def search(self):
        query = self.var_search.get()
        try:
            with sqlite3.connect(database="student_results.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM course WHERE name LIKE ? COLLATE NOCASE", (f'%{query}%',))
                rows = cur.fetchall()
                self.CourseTable.delete(*self.CourseTable.get_children())
                for row in rows:
                    self.CourseTable.insert('', END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()