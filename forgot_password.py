from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
from hashlib import sha256
import os
import time
from tkinter.font import Font

class ForgotPassword:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Recovery")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#0f1b2e')
        
        # Custom fonts
        self.title_font = Font(family="Helvetica", size=24, weight="bold")
        self.label_font = Font(family="Segoe UI", size=12)
        self.button_font = Font(family="Segoe UI", size=12, weight="bold")
        
        # Variables
        self.var_email = StringVar()
        self.var_new_pass = StringVar()
        self.var_confirm_pass = StringVar()
        
        # Setup background
        self.setup_background()
        
        # Create main container
        self.create_main_container()
        
        # Add floating animation to frame
        self.animate_frame()
        
        # Bind keyboard shortcuts
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.bind("<F11>", lambda e: self.root.attributes("-fullscreen", 
                            not self.root.attributes("-fullscreen")))
        self.root.bind("<Return>", lambda e: self.reset_password())

    def setup_background(self):
        # Create gradient background
        self.bg_canvas = Canvas(self.root, highlightthickness=0, bg='#0f1b2e')
        self.bg_canvas.pack(fill=BOTH, expand=True)
        
        # Add decorative elements
        self.bg_canvas.create_oval(-200, -200, 400, 400, fill='#1a2b4a', outline='')
        self.bg_canvas.create_oval(1500, -100, 2500, 900, fill='#1a2b4a', outline='')
        
        # Add subtle grid pattern
        for i in range(0, 2000, 40):
            self.bg_canvas.create_line(i, 0, i, 2000, fill='#1a3a5a', width=1, dash=(2,4))
            self.bg_canvas.create_line(0, i, 2000, i, fill='#1a3a5a', width=1, dash=(2,4))

    def create_main_container(self):
        # Main frame with solid color
        self.main_frame = Frame(self.bg_canvas, bg='#1e2b3d', bd=0, 
                              highlightthickness=0, relief='ridge')
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=500)
        
        # Inner frame for content
        inner_frame = Frame(self.main_frame, bg='#1e2b3d', bd=0)
        inner_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
        
        # Title
        Label(inner_frame, text="PASSWORD RECOVERY", font=self.title_font, 
             fg='white', bg='#1e2b3d').pack(pady=(0,20))
        
        # Email field
        self.create_input_field(inner_frame, "Email Address", self.var_email)
        
        # New Password field
        self.create_password_field(inner_frame, "New Password", self.var_new_pass)
        
        # Confirm Password field
        self.create_password_field(inner_frame, "Confirm Password", self.var_confirm_pass)
        
        # Update button with hover effect
        self.update_btn = Button(inner_frame, text="UPDATE PASSWORD", font=self.button_font, 
                                bg='#3a7bd5', fg='white', bd=0, 
                                activebackground='#00d2ff', activeforeground='white',
                                command=self.reset_password)
        self.update_btn.pack(fill=X, padx=30, pady=20, ipady=12)
        
        # Add hover effects
        self.update_btn.bind("<Enter>", lambda e: self.update_btn.config(bg='#00d2ff'))
        self.update_btn.bind("<Leave>", lambda e: self.update_btn.config(bg='#3a7bd5'))
        
        # Back to login link
        Button(inner_frame, text="Back to Login", font=self.label_font, 
              fg='#4fc3f7', bg='#1e2b3d', bd=0, activeforeground='#81d4fa',
              command=self.back_to_login).pack(side=BOTTOM, pady=(0,10))

    def create_input_field(self, parent, label_text, text_variable):
        field_frame = Frame(parent, bg='#1e2b3d')
        field_frame.pack(fill=X, padx=30, pady=(0, 15))
        
        # Label
        Label(field_frame, text=label_text, font=self.label_font, 
             fg='#aaaaaa', bg='#1e2b3d').pack(anchor=NW)
        
        # Entry field
        Entry(field_frame, textvariable=text_variable, font=self.label_font, 
             bg='#2d3b50', fg='white', bd=0, highlightthickness=0,
             insertbackground='white').pack(fill=X, ipady=8)
        
        # Bottom border
        Canvas(field_frame, height=2, bg='#3a7bd5', highlightthickness=0).pack(fill=X)

    def create_password_field(self, parent, label_text, text_variable):
        pass_frame = Frame(parent, bg='#1e2b3d')
        pass_frame.pack(fill=X, padx=30, pady=(0, 15))
        
        # Password label
        Label(pass_frame, text=label_text, font=self.label_font, 
             fg='#aaaaaa', bg='#1e2b3d').pack(anchor=NW)
        
        # Password entry with show/hide toggle
        pass_entry = Entry(pass_frame, textvariable=text_variable, 
                         font=self.label_font, show="•", bg='#2d3b50', 
                         fg='white', bd=0, highlightthickness=0,
                         insertbackground='white')
        pass_entry.pack(fill=X, ipady=8, side=LEFT)
        
        # Show/hide password button
        toggle_pass_btn = Button(pass_frame, text="👁️", 
                                bg='#2d3b50', activebackground='#3a7bd5',
                                fg='white', bd=0, 
                                command=lambda e=pass_entry: self.toggle_password(e))
        toggle_pass_btn.pack(side=RIGHT, padx=(5,0))
        
        # Bottom border
        Canvas(pass_frame, height=2, bg='#3a7bd5', highlightthickness=0).pack(fill=X)

    def toggle_password(self, entry):
        if entry['show'] == '':
            entry.config(show='•')
        else:
            entry.config(show='')

    def animate_frame(self):
        for i in range(0, 20, 2):
            self.main_frame.place(relx=0.5, rely=0.5 + i/1000, anchor="center")
            self.root.update()
            time.sleep(0.01)
        
        for i in range(20, 0, -1):
            self.main_frame.place(relx=0.5, rely=0.5 + i/1000, anchor="center")
            self.root.update()
            time.sleep(0.01)

    def reset_password(self):
        email = self.var_email.get()
        new_pass = self.var_new_pass.get()
        confirm_pass = self.var_confirm_pass.get()
        
        if not email or not new_pass or not confirm_pass:
            self.shake_frame()
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return
            
        if new_pass != confirm_pass:
            self.shake_frame()
            messagebox.showerror("Error", "Passwords do not match!", parent=self.root)
            return
            
        if len(new_pass) < 8:
            self.shake_frame()
            messagebox.showerror("Error", "Password must be at least 8 characters!", parent=self.root)
            return
            
        # Show loading animation
        self.show_loading(True)
        
        # Simulate network delay
        self.root.after(1500, lambda: self.process_password_reset(email, new_pass))

    def process_password_reset(self, email, new_pass):
        con = sqlite3.connect("student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE email=?", (email,))
            if cur.fetchone() is None:
                self.show_loading(False)
                self.shake_frame()
                messagebox.showerror("Error", "Email not found", parent=self.root)
            else:
                cur.execute("UPDATE users SET password=? WHERE email=?", 
                          (self.hash_password(new_pass), email))
                con.commit()
                self.show_loading(False)
                messagebox.showinfo("Success", "Password updated successfully", parent=self.root)
                self.back_to_login()
        except Exception as ex:
            self.show_loading(False)
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)

    def show_loading(self, show):
        if show:
            self.update_btn.config(text="", state=DISABLED)
            self.loading_canvas = Canvas(self.update_btn, width=100, height=30, 
                                       bg='#3a7bd5', highlightthickness=0)
            self.loading_canvas.place(relx=0.5, rely=0.5, anchor="center")
            
            # Create loading dots
            self.loading_dots = []
            for i in range(3):
                dot = self.loading_canvas.create_oval(10+i*20, 10, 20+i*20, 20, 
                                                     fill='white', outline='')
                self.loading_dots.append(dot)
            
            self.animate_loading(0)
        else:
            if hasattr(self, 'loading_canvas'):
                self.loading_canvas.destroy()
            self.update_btn.config(text="UPDATE PASSWORD", state=NORMAL)

    def animate_loading(self, index):
        if not hasattr(self, 'loading_canvas'):
            return
            
        # Reset all dots to normal size
        for i in range(3):
            self.loading_canvas.coords(self.loading_dots[i], 
                                      10+i*20, 10, 20+i*20, 20)
        
        # Enlarge current dot
        self.loading_canvas.coords(self.loading_dots[index], 
                                  7+index*20, 7, 23+index*20, 23)
        
        next_index = (index + 1) % 3
        self.root.after(300, lambda: self.animate_loading(next_index))

    def shake_frame(self):
        x, y = self.main_frame.winfo_x(), self.main_frame.winfo_y()
        for i in range(0, 21, 5):
            self.main_frame.place(x=x+i, y=y)
            self.root.update()
            time.sleep(0.02)
        for i in range(20, -21, -5):
            self.main_frame.place(x=x+i, y=y)
            self.root.update()
            time.sleep(0.02)
        for i in range(-20, 1, 5):
            self.main_frame.place(x=x+i, y=y)
            self.root.update()
            time.sleep(0.02)
        self.main_frame.place(x=x, y=y)

    def back_to_login(self):
        self.root.destroy()
        from login import LoginSystem
        login_root = Tk()
        obj = LoginSystem(login_root)
        login_root.mainloop()

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    root = Tk()
    obj = ForgotPassword(root)
    root.mainloop()