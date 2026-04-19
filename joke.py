import tkinter as tk
from tkinter import messagebox, colorchooser
import os
import subprocess
import shutil

class OlegBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Oleg's Builder PRO")  # Новое название
        self.root.geometry("500x900")
        
        lbl = {"font": ("Arial", 9, "bold")}
        
        tk.Label(root, text="Oleg's Winlocker Builder", font=("Arial", 16, "bold"), fg="#2c3e50").pack(pady=10)
        tk.Label(root, text="НАСТРОЙКИ ПРИЛОЖЕНИЯ", font=("Arial", 10, "italic"), fg="red").pack()

        # Поля ввода
        self.spam_count = self.create_entry("Кол-во окон:", "5")
        self.spam_text = self.create_entry("Текст в окнах:", "УПС!")
        self.spam_time = self.create_entry("Время тряски (сек):", "5")
        self.lock_text = self.create_entry("Текст блокировки:", "КОМПЬЮТЕР ЗАБЛОКИРОВАН!")
        self.lock_pass = self.create_entry("Пароль:", "1234")
        self.btn_text = self.create_entry("Текст на кнопке:", "РАЗБЛОКИРОВАТЬ")
        self.lock_time = self.create_entry("Задержка (1-5 сек):", "3")
        self.joke_text = self.create_entry("Текст после ошибки:", "ЭТО БЫЛА ШУТКА!")
        self.win_w = self.create_entry("Ширина окон:", "400")
        self.win_h = self.create_entry("Высота окон:", "200")
        
        self.bg_color = "#ff0000"
        tk.Button(root, text="ВЫБРАТЬ ЦВЕТ ФОНА", command=self.pick_color).pack(pady=5)

        self.file_name = self.create_entry("НАЗВАНИЕ ФАЙЛА (без .py):", "prikol")

        # --- ВЫБОР СИМВОЛИКИ ---
        tk.Label(root, text="ВЫБЕРИТЕ СИМВОЛИКУ:", **lbl).pack(pady=5)
        self.flag_var = tk.StringVar(value="Без флага")
        flag_options = ["Без флага", "Россия (РФ)", "Российская Империя"]
        self.flag_menu = tk.OptionMenu(root, self.flag_var, *flag_options)
        self.flag_menu.pack(pady=5)

        # ВЫБОР ФОРМАТА
        tk.Label(root, text="ВЫБЕРИТЕ ФОРМАТ:", **lbl).pack(pady=10)
        self.format_var = tk.StringVar(value="py")
        tk.Radiobutton(root, text=".py (Код)", variable=self.format_var, value="py").pack()
        tk.Radiobutton(root, text=".exe (Готовый файл)", variable=self.format_var, value="exe").pack()

        tk.Button(root, text="СОЗДАТЬ", bg="#27ae60", fg="white", 
                  font=("Arial", 12, "bold"), command=self.generate, height=2).pack(pady=20)

    def create_entry(self, text, default):
        tk.Label(self.root, text=text).pack()
        e = tk.Entry(self.root, width=40, justify="center")
        e.insert(0, default)
        e.pack()
        return e

    def pick_color(self):
        color = colorchooser.askcolor()
        if color: self.bg_color = color[1]

    def generate(self):
        s_time = min(int(self.spam_time.get()), 10) * 1000
        l_time = max(1, min(int(self.lock_time.get()), 5)) * 1000
        name = self.file_name.get().strip() or "joke"
        py_file = f"{name}.py"
        exe_file = f"{name}.exe"
        
        mode = self.flag_var.get()
        flag_draw_logic = ""
        if mode == "Россия (РФ)":
            flag_draw_logic = 'colors = ["white", "blue", "red"]\n    for i in range(3): canvas.create_rectangle(0, i*30, 150, (i+1)*30, fill=colors[i], outline="")'
        elif mode == "Российская Империя":
            flag_draw_logic = 'colors = ["black", "#FFD700", "white"]\n    for i in range(3): canvas.create_rectangle(0, i*30, 150, (i+1)*30, fill=colors[i], outline="")'
        
        flag_func = f"""
def draw_flag(parent):
    if "{mode}" == "Без флага": return
    canvas = tk.Canvas(parent, width=150, height=90, highlightthickness=0)
    canvas.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)
    {flag_draw_logic}
"""

        code = f"""
import tkinter as tk
import random
import time

{flag_func}

def start_joke():
    spam = []
    for _ in range({self.spam_count.get()}):
        w = tk.Toplevel()
        w.geometry("{self.win_w.get()}x{self.win_h.get()}")
        w.configure(bg="{self.bg_color}")
        draw_flag(w)
        tk.Label(w, text="{self.spam_text.get()}", font=("Arial", 15), bg="{self.bg_color}").pack(expand=True)
        spam.append(w)

    start = time.time() * 1000
    while time.time() * 1000 - start < {s_time}:
        for w in spam:
            nx = random.randint(0, root.winfo_screenwidth()-200)
            ny = random.randint(0, root.winfo_screenheight()-200)
            w.geometry(f"+{{nx}}+{{ny}}")
        root.update()
        time.sleep(0.05)
    for w in spam: w.destroy()

    lock = tk.Toplevel()
    lock.attributes("-topmost", True)
    lock.overrideredirect(True)
    lock.geometry(f"{{root.winfo_screenwidth()}}x{{root.winfo_screenheight()}}+0+0")
    lock.configure(bg="{self.bg_color}")
    draw_flag(lock)

    content = tk.Frame(lock, bg="{self.bg_color}")
    content.pack(expand=True)
    tk.Label(content, text="{self.lock_text.get()}", font=("Arial", 30), bg="{self.bg_color}").pack()
    pwd_entry = tk.Entry(content, font=("Arial", 20), show="*")
    pwd_entry.pack(pady=20)
    
    def check():
        if pwd_entry.get() == "{self.lock_pass.get()}":
            root.destroy()
        else:
            lock.destroy()
            show_final()

    tk.Button(content, text="{self.btn_text.get()}", command=check, width=20).pack()
    root.after({l_time}, lambda: None) 

def show_final():
    final = tk.Tk()
    final.geometry("{self.win_w.get()}x{self.win_h.get()}")
    final.configure(bg="{self.bg_color}")
    draw_flag(final)
    tk.Label(final, text="{self.joke_text.get()}", font=("Arial", 12), bg="{self.bg_color}").pack(expand=True)
    final.mainloop()

root = tk.Tk()
root.withdraw()
start_joke()
root.mainloop()
"""
        with open(py_file, "w", encoding="utf-8") as f:
            f.write(code.strip())

        if self.format_var.get() == "exe":
            messagebox.showinfo("Сборка", "Запуск Oleg's Builder. Пожалуйста, подождите...")
            try:
                subprocess.run(["pyinstaller", "--onefile", "--noconsole", py_file], check=True)
                if os.path.exists(os.path.join("dist", exe_file)):
                    if os.path.exists(exe_file): os.remove(exe_file)
                    os.rename(os.path.join("dist", exe_file), exe_file)
                
                shutil.rmtree("dist", ignore_errors=True)
                shutil.rmtree("build", ignore_errors=True)
                if os.path.exists(f"{name}.spec"): os.remove(f"{name}.spec")
                os.remove(py_file)
                
                messagebox.showinfo("Успех", f"Приложение создано!\nУстановочные данные и мусор удалены.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сборки: {e}")
        else:
            messagebox.showinfo("Успех", f"Код {py_file} успешно сгенерирован!")

if __name__ == "__main__":
    app = OlegBuilder(tk.Tk())
    tk.mainloop()
