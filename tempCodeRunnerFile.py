from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageOps
import sqlite3
from hashlib import sha256
import os
import time
from tkinter.font import Font
import webbrowser

class AdvancedLoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Login Portal")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#0f1b2e')
        
        # Custom fonts
        self.title_font = Font(family="Helvetica", size=28, weight="bold")
        self.label_font = Font(family="Segoe UI", size=12)
        self.button_font = Font(family="Segoe UI", size=12, weight="bold")
        self.link_font = Font(family="Segoe UI", size=10, underline=True)
        
        # Variables
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.remember_me = BooleanVar(value=False)
        
        # Setup background
        self.setup_background()
        
        # Create main container
        self.create_main_container()
        
        # Add floating animation to frame
        self.animate_frame()
        
        # Add social media buttons
        self.create_social_buttons()
        
        # Add theme toggle
        self.create_theme_toggle()
        
        # Bind keyboard shortcuts
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.bind("<F11>", lambda e: self.root.attributes("-fullscreen", 
                            not self.root.attributes("-fullscreen")))
        self.root.bind("<Return>", lambda e: self.login())
        
        # Load saved credentials if "remember me" was checked
        self.load_saved_credentials()

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
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=550)
        
        # Inner frame for content
        inner_frame = Frame(self.main_frame, bg='#1e2b3d', bd=0)
        inner_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
        
        # App logo (placeholder)
        try:
            self.logo_img = ImageTk.PhotoImage(Image.open("images/logo.png").resize((80, 80)))
            Label(inner_frame, image=self.logo_img, bg='#1e2b3d').pack(pady=(10,5))
        except:
            # Fallback if logo doesn't exist
            Label(inner_frame, text="🔒", font=("Helvetica", 40), bg='#1e2b3d', fg='white').pack(pady=(10,5))
        
        # Title
        self.title_label = Label(inner_frame, text="SECURE LOGIN", font=self.title_font, 
                                fg='white', bg='#1e2b3d')
        self.title_label.pack(pady=(0,20))
        
        # Email field
        self.create_input_field(inner_frame, "Email Address", self.var_email)
        
        # Password field with show/hide toggle
        self.create_password_field(inner_frame)
        
        # Remember me and forgot password
        options_frame = Frame(inner_frame, bg='#1e2b3d')
        options_frame.pack(fill=X, padx=30, pady=(5, 20))
        
        Checkbutton(options_frame, text="Remember me", variable=self.remember_me, 
                   font=self.label_font, fg='white', bg='#1e2b3d', 
                   activebackground='#1e2b3d', selectcolor='#0f1b2e').pack(side=LEFT)
        
        Button(options_frame, text="Forgot Password?", font=self.link_font, 
              fg='#4fc3f7', bg='#1e2b3d', bd=0, activeforeground='#81d4fa',
              command=self.forgot_password_window).pack(side=RIGHT)
        
        # Login button with hover effect
        self.login_btn = Button(inner_frame, text="LOGIN", font=self.button_font, 
                               bg='#3a7bd5', fg='white', bd=0, 
                               activebackground='#00d2ff', activeforeground='white',
                               command=self.login)
        self.login_btn.pack(fill=X, padx=30, pady=10, ipady=12)
        
        # Add hover effects
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg='#00d2ff'))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg='#3a7bd5'))
        
        # Register link
        register_frame = Frame(inner_frame, bg='#1e2b3d')
        register_frame.pack(fill=X, padx=30, pady=(20, 10))
        
        Label(register_frame, text="Don't have an account?", font=self.label_font, 
             fg='white', bg='#1e2b3d').pack(side=LEFT)
        
        Button(register_frame, text="Register Now", font=self.link_font, 
              fg='#4fc3f7', bg='#1e2b3d', bd=0, activeforeground='#81d4fa',
              command=self.register_window).pack(side=LEFT, padx=5)

    def create_input_field(self, parent, label_text, text_variable):
        field_frame = Frame(parent, bg='#1e2b3d')
        field_frame.pack(fill=X, padx=30, pady=(0, 15))
        
        # Label
        placeholder = Label(field_frame, text=label_text, font=self.label_font, 
                          fg='#aaaaaa', bg='#1e2b3d')
        placeholder.pack(anchor=NW)
        
        # Entry field
        entry = Entry(field_frame, textvariable=text_variable, font=self.label_font, 
                     bg='#2d3b50', fg='white', bd=0, highlightthickness=0,
                     insertbackground='white')
        entry.pack(fill=X, ipady=8)
        
        # Bottom border
        Canvas(field_frame, height=2, bg='#3a7bd5', highlightthickness=0).pack(fill=X)

    def create_password_field(self, parent):
        self.pass_frame = Frame(parent, bg='#1e2b3d')
        self.pass_frame.pack(fill=X, padx=30, pady=(0, 15))
        
        # Password label
        pass_label = Label(self.pass_frame, text="Password", font=self.label_font, 
                         fg='#aaaaaa', bg='#1e2b3d')
        pass_label.pack(anchor=NW)
        
        # Password entry with show/hide toggle
        self.pass_entry = Entry(self.pass_frame, textvariable=self.var_password, 
                              font=self.label_font, show="•", bg='#2d3b50', 
                              fg='white', bd=0, highlightthickness=0,
                              insertbackground='white')
        self.pass_entry.pack(fill=X, ipady=8, side=LEFT)
        
        # Show/hide password button
        self.toggle_pass_btn = Button(self.pass_frame, text="👁️", 
                                    bg='#2d3b50', activebackground='#3a7bd5',
                                    fg='white', bd=0, command=self.toggle_password)
        self.toggle_pass_btn.pack(side=RIGHT, padx=(5,0))
        
        # Bottom border
        Canvas(self.pass_frame, height=2, bg='#3a7bd5', highlightthickness=0).pack(fill=X)

    def toggle_password(self):
        if self.pass_entry['show'] == '':
            self.pass_entry.config(show='•')
            self.toggle_pass_btn.config(text="👁️")
        else:
            self.pass_entry.config(show='')
            self.toggle_pass_btn.config(text="👁️")

    def create_social_buttons(self):
        social_frame = Frame(self.main_frame, bg='#1e2b3d')
        social_frame.pack(side=BOTTOM, fill=X, padx=30, pady=(0, 20))
        
        Label(social_frame, text="Or login with", font=self.label_font, 
             fg='white', bg='#1e2b3d').pack(pady=(10, 15))
        
        # Social media buttons
        btn_frame = Frame(social_frame, bg='#1e2b3d')
        btn_frame.pack()
        
        for provider in ["Google", "Facebook", "Twitter"]:
            btn = Button(btn_frame, text=provider, font=self.label_font, 
                       bg='#2d3b50', activebackground='#3a7bd5',
                       fg='white', bd=0, 
                       command=lambda p=provider: self.social_login(p))
            btn.pack(side=LEFT, padx=10, ipadx=10, ipady=5)
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#3a7bd5'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#2d3b50'))

    def create_theme_toggle(self):
        self.dark_mode = True
        self.theme_btn = Button(self.root, text="🌙", font=("Arial", 14), 
                              bg='#0f1b2e', activebackground='#1a2b4a', 
                              fg='white', bd=0, command=self.toggle_theme)
        self.theme_btn.place(relx=0.95, rely=0.05, anchor=NE)

    def toggle_theme(self):
        if self.dark_mode:
            # Switch to light mode
            self.bg_canvas.config(bg='#f5f7fa')
            self.main_frame.config(bg='#ffffff')
            self.title_label.config(fg='#2d3748')
            self.theme_btn.config(text="☀️", bg='#f5f7fa', activebackground='#e2e8f0')
            
            # Update all child widgets
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, Frame):
                    widget.config(bg='#ffffff')
                if isinstance(widget, Label) and widget != self.title_label:
                    widget.config(bg='#ffffff', fg='#4b5563')
            
            self.dark_mode = False
        else:
            # Switch to dark mode
            self.bg_canvas.config(bg='#0f1b2e')
            self.main_frame.config(bg='#1e2b3d')
            self.title_label.config(fg='white')
            self.theme_btn.config(text="🌙", bg='#0f1b2e', activebackground='#1a2b4a')
            
            # Update all child widgets
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, Frame):
                    widget.config(bg='#1e2b3d')
                if isinstance(widget, Label) and widget != self.title_label:
                    widget.config(bg='#1e2b3d', fg='#aaaaaa')
            
            self.dark_mode = True

    def animate_frame(self):
        for i in range(0, 20, 2):
            self.main_frame.place(relx=0.5, rely=0.5 + i/1000, anchor="center")
            self.root.update()
            time.sleep(0.01)
        
        for i in range(20, 0, -1):
            self.main_frame.place(relx=0.5, rely=0.5 + i/1000, anchor="center")
            self.root.update()
            time.sleep(0.01)

    def login(self):
        email = self.var_email.get()
        password = self.var_password.get()
        
        if not email or not password:
            self.shake_frame()
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return
            
        # Simulate loading animation
        self.show_loading(True)
        
        # Simulate network delay
        self.root.after(1500, lambda: self.authenticate_user(email, password))

    def authenticate_user(self, email, password):
        con = sqlite3.connect("student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE email=? AND password=?", 
                       (email, self.hash_password(password)))
            row = cur.fetchone()
            
            if row is None:
                self.show_loading(False)
                self.shake_frame()
                messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
            else:
                # Save credentials if "remember me" is checked
                if self.remember_me.get():
                    self.save_credentials(email, password)
                else:
                    self.clear_saved_credentials()
                
                # Open dashboard after successful login
                self.open_dashboard()
                
        except Exception as ex:
            self.show_loading(False)
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)

    def show_loading(self, show):
        if show:
            self.login_btn.config(text="", state=DISABLED)
            self.loading_canvas = Canvas(self.login_btn, width=100, height=30, 
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
            self.login_btn.config(text="LOGIN", state=NORMAL)

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

    def open_dashboard(self):
        self.root.destroy()
        from dashboard import RMS
        dash_root = Tk()
        obj = RMS(dash_root)
        dash_root.mainloop()

    def register_window(self):
        self.root.destroy()
        from register import Register
        reg_root = Tk()
        obj = Register(reg_root)
        reg_root.mainloop()

    def forgot_password_window(self):
        self.root.destroy()
        from forgot_password import ForgotPassword
        fp_root = Tk()
        obj = ForgotPassword(fp_root)
        fp_root.mainloop()

    def social_login(self, provider):
        # Show loading animation
        self.show_loading(True)
        
        # Simulate social login process
        self.root.after(2000, lambda: self.handle_social_login(provider))

    def handle_social_login(self, provider):
        self.show_loading(False)
        messagebox.showinfo("Social Login", 
                          f"Redirecting to {provider.capitalize()} login...", 
                          parent=self.root)
        webbrowser.open_new(f"https://{provider.lower()}.com/login")

    def save_credentials(self, email, password):
        # In a real app, use proper encryption for storing credentials
        try:
            with open("user_creds.txt", "w") as f:
                f.write(f"{email},{password}")
        except:
            pass

    def load_saved_credentials(self):
        try:
            if os.path.exists("user_creds.txt"):
                with open("user_creds.txt", "r") as f:
                    email, password = f.read().split(",")
                    self.var_email.set(email)
                    self.var_password.set(password)
                    self.remember_me.set(True)
        except:
            pass

    def clear_saved_credentials(self):
        try:
            if os.path.exists("user_creds.txt"):
                os.remove("user_creds.txt")
        except:
            pass

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    root = Tk()
    app = AdvancedLoginSystem(root)
    root.mainloop()