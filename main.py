import tkinter as tk

from data_manager import init_files
from login_page import LoginPage
from budget_page import BudgetPage


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Budget Buddy")
        self.root.geometry("700x400")

        self.show_login_page()

    def show_login_page(self):
        # 显示login界面
        self.root.geometry("700x400")

        LoginPage(
            root=self.root,
            open_budget_page_callback=self.show_budget_page
        )

    def show_budget_page(self, username, data_path):
        # 显示记账界面
        BudgetPage(
            root=self.root,
            username=username,
            data_path=data_path,
            logout_callback=self.show_login_page
        )


if __name__ == "__main__":
    init_files()

    root = tk.Tk()
    app = App(root)
    root.mainloop()