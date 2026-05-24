import os
import pandas as pd
from datetime import datetime

USER_DATA_PATH = "user_data.csv"

def init_files():
    """初始化用户数据文件和data文件夹，防止由于不存在而报错"""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(USER_DATA_PATH):
        df = pd.DataFrame(columns=["username", "password", "data_path"])
        df.to_csv(USER_DATA_PATH, index=False, encoding="utf-8-sig")


def get_sys_time():
    """获取当前系统时间，使用澳洲日期格式"""
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def login(username, password):

    df = pd.read_csv(USER_DATA_PATH)

    if username not in df["username"].astype(str).tolist():
        return None

    user_row = df[df["username"].astype(str) == username].iloc[0]
    real_password = str(user_row["password"])

    # 判断密码是否正确
    if password == real_password:
        return user_row["data_path"]
    else:
        return None


def create_new_user(username, password, password_repeat):
    """注册新用户"""
    df = pd.read_csv(USER_DATA_PATH)

    if username == "" or password == "":
        return False, "Please enter both username and password"

    if username in df["username"].astype(str).tolist():
        return False, "This username is already taken"

    if password != password_repeat:
        return False, "Passwords do not match"

    data_path = f"data/{username}_expense.csv"

    # 给新用户创建一个专属的数据文件
    df_new = pd.DataFrame(columns=[
        "amount",
        "record_type",
        "category",
        "note",
        "date",
        "sys_date"
    ])
    df_new.to_csv(data_path, index=False, encoding="utf-8-sig")

    new_user = pd.DataFrame([{
        "username": username,
        "password": password,
        "data_path": data_path
    }])

    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DATA_PATH, index=False, encoding="utf-8-sig")

    return True, data_path


def load_user_data(data_path):
    """读取用户账单数据"""
    if os.path.exists(data_path):
        return pd.read_csv(data_path)

    return pd.DataFrame(columns=[
        "amount",
        "record_type",
        "category",
        "note",
        "date",
        "sys_date"
    ])


def save_user_data(data_path, df):
    """保存用户账单数据"""
    df.to_csv(data_path, index=False, encoding="utf-8-sig")

def add_record(data_path, record):
    """添加一条账单记录"""
    df = load_user_data(data_path)
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    save_user_data(data_path, df)


def delete_record(data_path, row_index):
    """根据行号删除一条账单记录"""
    df = load_user_data(data_path)

    if row_index not in df.index:
        return False

    df = df.drop(index=row_index)
    df = df.reset_index(drop=True)

    save_user_data(data_path, df)
    return True


def calculate_summary(data_path):
    """计算总收入、总支出和当前结余"""
    df = load_user_data(data_path)

    if len(df) == 0:
        return 0, 0, 0

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    total_income = df[df["record_type"] == "income"]["amount"].sum()
    total_expense = df[df["record_type"] == "expense"]["amount"].sum()
    current_balance = total_income - total_expense

    return total_income, total_expense, current_balance