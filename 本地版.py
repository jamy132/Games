import os
import tkinter as tk
from tkinter import messagebox, ttk

filename = "accounts.txt" #改成你想要的名字

def load_accounts():
    tree.delete(*tree.get_children())
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        for line in lines:
            data = line.strip().split(", ")
            account_data = {item.split(": ")[0]: item.split(": ")[1] for item in data}
            tree.insert("", "end", values=(account_data["游戏"], account_data["账号"], account_data["密码"], account_data.get("SSFN", "")))

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
    password_entry = ttk.Entry(add_game_window, show="*")
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
            with open(filename, 'a') as file:
                if ssfn:
                    file.write(f"游戏: {game}, 账号: {account}, 密码: {password}, SSFN: {ssfn}\n")
                else:
                    file.write(f"游戏: {game}, 账号: {account}, 密码: {password}\n")
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
            with open(filename, 'r') as file:
                lines = file.readlines()
            with open(filename, 'w') as file:
                for line in lines:
                    if values[1] not in line:
                        file.write(line)
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
        password_edit = ttk.Entry(edit_window, show="*")
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
                with open(filename, 'r') as file:
                    lines = file.readlines()
                with open(filename, 'w') as file:
                    for line in lines:
                        if values[1] not in line:
                            file.write(line)
                    if new_ssfn:
                        file.write(f"游戏: {new_game}, 账号: {new_account}, 密码: {new_password}, SSFN: {new_ssfn}\n")
                    else:
                        file.write(f"游戏: {new_game}, 账号: {new_account}, 密码: {new_password}\n")
                messagebox.showinfo("成功", "账号信息已更新。")
                edit_window.destroy()
            else:
                messagebox.showwarning("输入错误", "请填写完整的信息。")

        tk.Button(edit_window, text="保存", command=save_changes).grid(row=4, column=0, columnspan=2, pady=5)

def search_accounts():
    search_term = search_entry.get().lower()
    tree.delete(*tree.get_children())  

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        found = False  
        for line in lines:
            data = line.strip().split(", ")
            account_data = {item.split(": ")[0]: item.split(": ")[1] for item in data}
            if (search_term in account_data["游戏"].lower()) or (search_term in account_data["账号"].lower()):
                tree.insert("", "end", values=(account_data["游戏"], account_data["账号"], account_data["密码"], account_data.get("SSFN", "")))
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