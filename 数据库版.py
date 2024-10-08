import os
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
global conn
# 创建数据库连接
try:
    conn = mysql.connector.connect(
        host="",  # MySQL服务器地址
        user="",   # 用户名
        password="",  # 密码
        database="",  # 数据库名称
        ssl_disabled=True
    )
    if conn.is_connected():  # 检查连接是否有效
        cursor = conn.cursor()  # 确保连接成功后再创建游标
    else:
        print("Connection is not available.")
except mysql.connector.Error as err:
    print(f"Error: {err}")  # 打印错误信息
    conn = None  # 确保连接为 None，以便后续检查

def load_accounts():
    tree.delete(*tree.get_children())
    cursor = conn.cursor()
    cursor.execute("SELECT 游戏, 账号, 密码, SSFN FROM Games")
    
    for (game, account, password, ssfn) in cursor.fetchall():
        tree.insert("", "end", values=(game, account, password, ssfn))

def open_add_game_window():
    add_game_window = tk.Toplevel(app)
    add_game_window.title("添加游戏")
    
    tk.Label(add_game_window, text="游戏名:").grid(row=0, column=0, padx=5, pady=5)
    game_entry = ttk.Entry(add_game_window)
    game_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_game_window, text="账号:").grid(row=1, column=0, padx=5, pady=5)
    account_entry = ttk.Entry(add_game_window)
    account_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(add_game_window, text="密码:").grid(row=2, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(add_game_window)
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(add_game_window, text="SSFN (可选):").grid(row=3, column=0, padx=5, pady=5)
    ssfn_entry = ttk.Entry(add_game_window)
    ssfn_entry.grid(row=3, column=1, padx=5, pady=5)

    def add_game():
        game = game_entry.get()
        account = account_entry.get()
        password = password_entry.get()
        ssfn = ssfn_entry.get()
        
        if game and account and password:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Games (游戏, 账号, 密码, SSFN) VALUES (%s, %s, %s, %s)", 
                           (game, account, password, ssfn if ssfn else None))
            conn.commit()
            tree.insert("", "end", values=(game, account, password, ssfn))
            messagebox.showinfo("成功", "账号信息已保存。")
            add_game_window.destroy()
        else:
            messagebox.showwarning("输入错误", "请填写游戏名、账号和密码。")

    tk.Button(add_game_window, text="保存", command=add_game).grid(row=4, column=0, columnspan=2, pady=5)

def delete_account():
    selected_item = tree.selection()
    if selected_item:
        for item in selected_item:
            values = tree.item(item, "values")
            tree.delete(item)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Games WHERE 账号 = %s", (values[1],))
            conn.commit()

            messagebox.showinfo("成功", f"账号 {values[1]} 已删除。")
    else:
        messagebox.showwarning("选择错误", "请选择要删除的账号。")

def update_account():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("选择错误", "请选择要修改的账号。")
        return

    for item in selected_item:
        values = tree.item(item, "values")
        
        edit_window = tk.Toplevel(app)
        edit_window.title("修改账号")
        
        tk.Label(edit_window, text="游戏名:").grid(row=0, column=0, padx=5, pady=5)
        game_edit = ttk.Entry(edit_window)
        game_edit.grid(row=0, column=1, padx=5, pady=5)
        game_edit.insert(0, values[0])

        tk.Label(edit_window, text="账号:").grid(row=1, column=0, padx=5, pady=5)
        account_edit = ttk.Entry(edit_window)
        account_edit.grid(row=1, column=1, padx=5, pady=5)
        account_edit.insert(0, values[1])

        tk.Label(edit_window, text="密码:").grid(row=2, column=0, padx=5, pady=5)
        password_edit = ttk.Entry(edit_window)
        password_edit.grid(row=2, column=1, padx=5, pady=5)
        password_edit.insert(0, values[2])

        tk.Label(edit_window, text="SSFN:").grid(row=3, column=0, padx=5, pady=5)
        ssfn_edit = ttk.Entry(edit_window)
        ssfn_edit.grid(row=3, column=1, padx=5, pady=5)
        ssfn_edit.insert(0, values[3])

        def save_changes():
            new_game = game_edit.get()
            new_account = account_edit.get()
            new_password = password_edit.get()
            new_ssfn = ssfn_edit.get()
            
            if new_game and new_account and new_password:
                tree.item(item, values=(new_game, new_account, new_password, new_ssfn))
                cursor = conn.cursor()
                cursor.execute("UPDATE Games SET 游戏 = %s, 密码 = %s, SSFN = %s WHERE 账号 = %s", 
                               (new_game, new_password, new_ssfn if new_ssfn else None, values[1]))
                conn.commit()
                messagebox.showinfo("成功", "账号信息已更新。")
                edit_window.destroy()
            else:
                messagebox.showwarning("输入错误", "请填写完整的信息。")

        tk.Button(edit_window, text="保存", command=save_changes).grid(row=4, column=0, columnspan=2, pady=5)

def search_accounts():
    search_term = search_entry.get().lower()
    tree.delete(*tree.get_children()) 

    cursor = conn.cursor()
    cursor.execute("SELECT 游戏, 账号, 密码, SSFN FROM Games WHERE 游戏 LIKE %s OR 账号 LIKE %s", 
                   (f"%{search_term}%", f"%{search_term}%"))
    
    found = False
    for (game, account, password, ssfn) in cursor.fetchall():
        tree.insert("", "end", values=(game, account, password, ssfn))
        found = True

    if found:
        messagebox.showinfo("搜索结果", "搜索完成，已显示匹配的账号。")
    else:
        messagebox.showinfo("搜索结果", "未找到匹配的账号。")

app = tk.Tk()
app.title("账号管理")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Button(frame, text="添加游戏", command=open_add_game_window).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame, text="修改账号", command=update_account).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame, text="删除账号", command=delete_account).grid(row=1, column=0, padx=5, pady=5)

# 搜索框和按钮
ttk.Label(frame, text="搜索:").grid(row=2, column=0, padx=5, pady=5)
search_entry = ttk.Entry(frame)
search_entry.grid(row=2, column=1, padx=5, pady=5)
ttk.Button(frame, text="搜索", command=search_accounts).grid(row=3, column=0, columnspan=2, pady=5)

tree = ttk.Treeview(frame, columns=("游戏", "账号", "密码", "SSFN"), show="headings")
tree.heading("游戏", text="游戏")
tree.heading("账号", text="账号")
tree.heading("密码", text="密码")
tree.heading("SSFN", text="SSFN")
tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

load_accounts()

app.mainloop()
cursor.close()
conn.close()