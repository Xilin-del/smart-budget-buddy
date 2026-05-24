import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from data_manager import (
    get_sys_time,
    load_user_data,
    add_record,
    delete_record,
    calculate_summary
)

# 支出的类型
EXPENSE_CATEGORY_LIST = [
    "Food",
    "Transportation",
    "Shopping",
    "Education",
    "Entertainment",
    "Medical",
    "Housing",
    "Communication",
    "Daily Supplies",
    "Travel",
    "Other"
]

# 收入的类型
INCOME_CATEGORY_LIST = [
    "Salary",
    "Bonus",
    "Part-time Job",
    "Investment",
    "Gift Money",
    "Living Allowance",
    "Other"
]


class BudgetPage:
    def __init__(self, root, username, data_path, logout_callback):
        self.root = root
        self.username = username
        self.data_path = data_path
        self.logout_callback = logout_callback

        self.show_budget_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_category_options(self, event=None):
        """根据选择的(支出\收入),显示不同的类型"""
        record_type = self.record_type_box.get()

        if record_type == "expense":
            self.category_box["values"] = EXPENSE_CATEGORY_LIST
            self.category_box.current(0)

        elif record_type == "income":
            self.category_box["values"] = INCOME_CATEGORY_LIST
            self.category_box.current(0)

    def show_budget_page(self):
        self.clear_window()

        self.root.geometry("850x650")

        title = tk.Label(
            self.root,
            text=f"Smart Budget Buddy - Current User: {self.username}",
            font=("Microsoft YaHei", 18)
        )
        title.pack(pady=10)

        self.create_summary_area()
        self.create_form_area()
        self.create_button_area()
        self.create_table_area()

        self.update_summary()
        self.refresh_table()

    def get_balance_mood(self, current_balance):
        """根据当前统计输入表情"""
        if current_balance >= 1000:
            return "😄"
        elif current_balance >= 100:
            return "🙂"
        elif current_balance >= 0:
            return "😐"
        else:
            return "😭"

    def create_summary_area(self):
        summary_frame = tk.LabelFrame(
            self.root,
            text="Financial Summary",
            font=("Microsoft YaHei", 12)
        )
        summary_frame.pack(padx=20, pady=10, fill="x")

        self.income_label = tk.Label(summary_frame, font=("Microsoft YaHei", 11))
        self.income_label.grid(row=0, column=0, padx=30, pady=10)

        self.expense_label = tk.Label(summary_frame, font=("Microsoft YaHei", 11))
        self.expense_label.grid(row=0, column=1, padx=30, pady=10)

        self.balance_label = tk.Label(summary_frame, font=("Microsoft YaHei", 11))
        self.balance_label.grid(row=0, column=2, padx=30, pady=10)

        self.mood_label = tk.Label(
            summary_frame,
            text="🙂",
            font=("Microsoft YaHei", 28)
        )
        self.mood_label.grid(row=0, column=3, padx=30, pady=10)

    def create_form_area(self):
        form_frame = tk.LabelFrame(
            self.root,
            text="Add New Record",
            font=("Microsoft YaHei", 12)
        )
        form_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(form_frame, text="Amount:").grid(row=0, column=0, padx=10, pady=8)
        self.amount_entry = tk.Entry(form_frame)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(form_frame, text="Record Type:").grid(row=0, column=2, padx=10, pady=8)
        self.record_type_box = ttk.Combobox(
            form_frame,
            values=["income", "expense"],
            state="readonly"
        )
        self.record_type_box.grid(row=0, column=3, padx=10, pady=8)
        self.record_type_box.current(1)

        self.record_type_box.bind("<<ComboboxSelected>>", self.update_category_options)

        tk.Label(form_frame, text="Category:").grid(row=1, column=0, padx=10, pady=8)
        self.category_box = ttk.Combobox(
            form_frame,
            values=EXPENSE_CATEGORY_LIST,
            state="readonly"
        )
        self.category_box.grid(row=1, column=1, padx=10, pady=8)
        self.category_box.current(0)

        tk.Label(form_frame, text="Date:").grid(row=1, column=2, padx=10, pady=8)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=1, column=3, padx=10, pady=8)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(form_frame, text="Note:").grid(row=2, column=0, padx=10, pady=8)
        self.note_entry = tk.Entry(form_frame, width=60)
        self.note_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=8)

    def create_table_area(self):
        table_frame = tk.LabelFrame(
            self.root,
            text="Record List",
            font=("Microsoft YaHei", 12)
        )
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        columns = (
            "index",
            "amount",
            "record_type",
            "category",
            "note",
            "date",
            "sys_date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("index", text="No.")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("record_type", text="Type")
        self.tree.heading("category", text="Category")
        self.tree.heading("note", text="Note")
        self.tree.heading("date", text="Date")
        self.tree.heading("sys_date", text="Recorded Time")

        self.tree.column("index", width=50, anchor="center")
        self.tree.column("amount", width=80, anchor="center")
        self.tree.column("record_type", width=80, anchor="center")
        self.tree.column("category", width=100, anchor="center")
        self.tree.column("note", width=150, anchor="center")
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("sys_date", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)

    def create_button_area(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Save Record",
            width=12,
            command=self.handle_add_record
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            btn_frame,
            text="Delete Selected",
            width=14,
            command=self.handle_delete_record
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            btn_frame,
            text="Refresh",
            width=12,
            command=self.refresh_table
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            btn_frame,
            text="Logout",
            width=12,
            command=self.logout_callback
        ).grid(row=0, column=3, padx=8)

        tk.Button(
            btn_frame,
            text="Exit",
            width=12,
            command=self.root.destroy
        ).grid(row=0, column=4, padx=8)

    def update_summary(self):
        total_income, total_expense, current_balance = calculate_summary(self.data_path)

        self.income_label.config(text=f"Total Income: {total_income:.2f}")
        self.expense_label.config(text=f"Total Expense: {total_expense:.2f}")
        self.balance_label.config(text=f"Current Balance: {current_balance:.2f}")

        mood = self.get_balance_mood(current_balance)
        self.mood_label.config(text=mood)

    def handle_add_record(self):
        # 添加记录
        amount_text = self.amount_entry.get().strip()
        record_type = self.record_type_box.get().strip()
        category = self.category_box.get().strip()
        date = self.date_entry.get().strip()
        note = self.note_entry.get().strip()

        # 判断输入金额是否合法
        try:
            amount = float(amount_text)
            if amount <= 0:
                messagebox.showerror("Input Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number")
            return

        if record_type not in ["income", "expense"]:
            messagebox.showerror("Input Error", "Please select a valid record type")
            return

        if category == "":
            messagebox.showerror("Input Error", "Please select a category")
            return

        if date == "":
            messagebox.showerror("Input Error", "Date cannot be empty")
            return

        record = {
            "amount": amount,
            "record_type": record_type,
            "category": category,
            "note": note,
            "date": date,
            "sys_date": get_sys_time()
        }

        add_record(self.data_path, record)

        messagebox.showinfo("Saved", "Record saved successfully!")

        self.amount_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)

        self.update_summary()
        self.refresh_table()

    def handle_delete_record(self):
        # 删除记录
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("No Record Selected", "Please select a record to delete first")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete the selected record?"
        )

        if not confirm:
            return

        item = selected_item[0]
        values = self.tree.item(item, "values")

        row_index = int(values[0])

        success = delete_record(self.data_path, row_index)

        if success:
            messagebox.showinfo("Deleted", "Record deleted successfully")
            self.update_summary()
            self.refresh_table()
        else:
            messagebox.showerror("Delete Failed", "An error occurred while deleting the record")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        df = load_user_data(self.data_path)

        if len(df) == 0:
            return

        df_display = df.tail(20).iloc[::-1]

        for index, row in df_display.iterrows():
            self.tree.insert(
                "",
                tk.END,
                values=(
                    index,
                    row["amount"],
                    row["record_type"],
                    row["category"],
                    row["note"],
                    row["date"],
                    row["sys_date"]
                )
            )