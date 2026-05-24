import tkinter as tk
from tkinter import messagebox

from data_manager import login, create_new_user


class LoginPage:
    def __init__(self, root, open_budget_page_callback):
        self.root = root
        self.open_budget_page_callback = open_budget_page_callback

        self.show_login_page()

    def clear_window(self):
        # 清除界面
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_page(self):
        # login页面
        self.clear_window()

        title = tk.Label(
            self.root,
            text="Welcome to Smart Budget Buddy",
            font=("Microsoft YaHei", 20)
        )
        title.pack(pady=30)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # 获取用户名输入
        tk.Label(frame, text="Username:", font=("Microsoft YaHei", 12)).grid(
            row=0, column=0, pady=10
        )
        self.username_entry = tk.Entry(frame, font=("Microsoft YaHei", 12))
        self.username_entry.grid(row=0, column=1, pady=10)

        # 获取密码输入
        tk.Label(frame, text="Password:", font=("Microsoft YaHei", 12)).grid(
            row=1, column=0, pady=10
        )
        self.password_entry = tk.Entry(frame, show="*", font=("Microsoft YaHei", 12))
        self.password_entry.grid(row=1, column=1, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        # 页面上的按钮
        tk.Button(
            btn_frame,
            text="Login",
            width=12,
            command=self.handle_login
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Register",
            width=12,
            command=self.show_register_page
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            btn_frame,
            text="Exit",
            width=12,
            command=self.root.destroy
        ).grid(row=0, column=2, padx=10)

    def handle_login(self):
        # 判断登陆是否成功,并在页面上显示结果
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        data_path = login(username, password)

        if data_path is None:
            messagebox.showerror("Login Failed", "Username does not exist or password is incorrect")
        else:
            messagebox.showinfo("Login Successful", f"Logged in as: {username}")
            self.open_budget_page_callback(username, data_path)

    def show_register_page(self):
        # 注册界面
        self.clear_window()

        title = tk.Label(
            self.root,
            text="Create New Account",
            font=("Microsoft YaHei", 20)
        )
        title.pack(pady=30)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", font=("Microsoft YaHei", 12)).grid(
            row=0, column=0, pady=10
        )
        self.reg_username_entry = tk.Entry(frame, font=("Microsoft YaHei", 12))
        self.reg_username_entry.grid(row=0, column=1, pady=10)

        tk.Label(frame, text="Password:", font=("Microsoft YaHei", 12)).grid(
            row=1, column=0, pady=10
        )
        self.reg_password_entry = tk.Entry(frame, show="*", font=("Microsoft YaHei", 12))
        self.reg_password_entry.grid(row=1, column=1, pady=10)

        tk.Label(frame, text="Confirm Password:", font=("Microsoft YaHei", 12)).grid(
            row=2, column=0, pady=10
        )
        self.reg_password_repeat_entry = tk.Entry(frame, show="*", font=("Microsoft YaHei", 12))
        self.reg_password_repeat_entry.grid(row=2, column=1, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Confirm",
            width=12,
            command=self.handle_register
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Back to Login",
            width=12,
            command=self.show_login_page
        ).grid(row=0, column=1, padx=10)

    def handle_register(self):
        # 注册结果判断和显示
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        password_repeat = self.reg_password_repeat_entry.get().strip()

        success, result = create_new_user(username, password, password_repeat)

        if not success:
            messagebox.showerror("Registration Failed", result)
        else:
            data_path = result
            messagebox.showinfo(
                "Registration Successful",
                f"User {username} has been created and logged in automatically"
            )
            self.open_budget_page_callback(username, data_path)