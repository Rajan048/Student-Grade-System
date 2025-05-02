from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageOps
import sqlite3
from hashlib import sha256
import os
import time
from tkinter.font import Font
import webbrowser

class AdvancedLogoutSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Logout Portal")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#0f1b2e')
        
        # Custom fonts
        self.title_font = Font(family="Helvetica", size=28, weight="bold")
        self.label_font = Font(family="Segoe UI", size=12)
        self.button_font = Font(family="Segoe UI", size=12, weight="bold")
        self.link_font = Font(family="Segoe UI", size=10, underline=True)
        
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
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=450)
        
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
        self.title_label = Label(inner_frame, text="LOGGED OUT", font=self.title_font, 
                                fg='white', bg='#1e2b3d')
        self.title_label.pack(pady=(0,20))
        
        # Message
        message = Label(inner_frame, text="You have been successfully logged out.", 
                       font=self.label_font, fg='#aaaaaa', bg='#1e2b3d', wraplength=300)
        message.pack(pady=(0,30))
        
        # Login button with hover effect
        self.login_btn = Button(inner_frame, text="LOGIN AGAIN", font=self.button_font, 
                               bg='#3a7bd5', fg='white', bd=0, 
                               activebackground='#00d2ff', activeforeground='white',
                               command=self.login_again)
        self.login_btn.pack(fill=X, padx=30, pady=10, ipady=12)
        
        # Add hover effects
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg='#00d2ff'))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg='#3a7bd5'))
        
        # Exit button
        Button(inner_frame, text="EXIT APPLICATION", font=self.button_font, 
              bg='#f44336', fg='white', bd=0, 
              activebackground='#ff7961', activeforeground='white',
              command=self.root.quit).pack(fill=X, padx=30, pady=10, ipady=12)

    def create_social_buttons(self):
        social_frame = Frame(self.main_frame, bg='#1e2b3d')
        social_frame.pack(side=BOTTOM, fill=X, padx=30, pady=(0, 20))
        
        Label(social_frame, text="Connect with us", font=self.label_font, 
             fg='white', bg='#1e2b3d').pack(pady=(10, 15))
        
        # Social media buttons
        btn_frame = Frame(social_frame, bg='#1e2b3d')
        btn_frame.pack()
        
        for provider in ["Google", "Facebook", "Twitter"]:
            btn = Button(btn_frame, text=provider, font=self.label_font, 
                       bg='#2d3b50', activebackground='#3a7bd5',
                       fg='white', bd=0, 
                       command=lambda p=provider: self.social_redirect(p))
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

    def login_again(self):
        self.root.destroy()
        from login import AdvancedLoginSystem
        login_root = Tk()
        app = AdvancedLoginSystem(login_root)
        login_root.mainloop()

    def social_redirect(self, provider):
        messagebox.showinfo("Social Media", 
                          f"Redirecting to {provider.capitalize()}...", 
                          parent=self.root)
        webbrowser.open_new(f"https://{provider.lower()}.com")

if __name__ == "__main__":
    root = Tk()
    app = AdvancedLogoutSystem(root)
    root.mainloop()