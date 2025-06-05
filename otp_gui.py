import tkinter as tk
from tkinter import messagebox
import pyotp
import time
import qrcode
from PIL import Image, ImageTk
import os

# -----------------------------
#  Configuration
APP_PASSWORD = "admin123"  # You can change this
SECRET_FILE = "secret.key"
# -----------------------------

#  Load existing secret or create a new one
def load_or_create_secret():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, 'r') as f:
            return f.read()
    else:
        secret = pyotp.random_base32()
        with open(SECRET_FILE, 'w') as f:
            f.write(secret)
        return secret

#  Generate QR code for Authenticator apps
def generate_qr(secret):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name="user@pyauth", issuer_name="PyAuth")
    qr_img = qrcode.make(uri)
    qr_img.save("qr_code.png")

#  Launch the OTP Authenticator GUI
def launch_otp_app(secret):
    global totp, root, otp_label, timer_label
    totp = pyotp.TOTP(secret)

    root = tk.Tk()
    root.title("PyAuth - OTP Authenticator")
    root.geometry("400x400")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text="🔐 PyAuth OTP App", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    otp_label = tk.Label(root, text="", font=("Courier", 28), fg="green", bg="#f0f0f0")
    otp_label.pack(pady=10)

    timer_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0")
    timer_label.pack(pady=5)

    #  Refresh OTP every second
    def generate_otp():
        otp = totp.now()
        seconds_remaining = 30 - int(time.time()) % 30
        otp_label.config(text=f"OTP: {otp}")
        timer_label.config(text=f"Expires in: {seconds_remaining}s")

    def auto_refresh():
        generate_otp()
        root.after(1000, auto_refresh)

    #  Show QR Code popup
    def show_qr():
        qr_window = tk.Toplevel(root)
        qr_window.title("Scan QR with Google Authenticator")
        qr_image = Image.open("qr_code.png").resize((250, 250))
        qr_photo = ImageTk.PhotoImage(qr_image)
        qr_label = tk.Label(qr_window, image=qr_photo)
        qr_label.image = qr_photo
        qr_label.pack(padx=10, pady=10)

    #  Reset secret + QR code
    def reset_secret():
        global secret, totp
        secret = pyotp.random_base32()
        with open(SECRET_FILE, 'w') as f:
            f.write(secret)
        totp = pyotp.TOTP(secret)
        generate_qr(secret)
        messagebox.showinfo("Reset Complete", "Secret & QR code reset.\nScan the new QR code with your Authenticator app.")

    # Buttons
    tk.Button(root, text="Show QR Code", bg="#9C27B0", fg="white", font=("Helvetica", 12), command=show_qr).pack(pady=10)
    tk.Button(root, text="Reset QR / Secret", bg="#f44336", fg="white", font=("Helvetica", 12), command=reset_secret).pack(pady=5)

    auto_refresh()
    root.mainloop()

#  Password Login Window
def show_login():
    login = tk.Tk()
    login.title("PyAuth Login")
    login.geometry("300x150")
    login.configure(bg="white")

    tk.Label(login, text="Enter App Password:", font=("Helvetica", 12), bg="white").pack(pady=10)
    password_entry = tk.Entry(login, show="*", width=25)
    password_entry.pack()

    def validate():
        if password_entry.get() == APP_PASSWORD:
            login.destroy()
            secret = load_or_create_secret()
            generate_qr(secret)
            launch_otp_app(secret)
        else:
            messagebox.showerror("Access Denied", "Incorrect password!")

    tk.Button(login, text="Login", command=validate, bg="#4CAF50", fg="white").pack(pady=10)
    login.mainloop()

#  Start the app
show_login()
