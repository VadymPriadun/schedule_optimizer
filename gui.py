import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import time
from scheduler import ScheduleProblem
from algorithms.greedy import greedy_schedule
from algorithms.branch_and_bound import branch_and_bound_schedule
from algorithms.hopcroft_karp_scheduler import hopcroft_karp_schedule
from utils.exporter import export_to_excel, export_to_html
from utils.validator import validate_schedule

class ScheduleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Система формування розкладу занять — Курсова робота")
        self.root.geometry("1100x800")
        self.root.configure(bg="#1e1e2e")

        self.problem = ScheduleProblem()
        self.current_file = "data/input.json"

        self.setup_ui()
        self.load_default_file()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Темна тема
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), background="#1e1e2e", foreground="#bd93f9")
        style.configure("TButton", font=("Segoe UI", 11), padding=10)
        style.configure("TLabel", background="#1e1e2e", foreground="#f8f8f2")
        style.map("TButton",
                  background=[("active", "#6272a4")],
                  foreground=[("active", "white")])

        # Заголовок
        title = ttk.Label(self.root, text="Оптимальний розклад занять ВНЗ", style="Title.TLabel")
        title.pack(pady=(20, 10))

        # Панель вибору файлу
        top_frame = tk.Frame(self.root, bg="#1e1e2e")
        top_frame.pack(pady=10)

        ttk.Button(top_frame, text="Вибрати JSON-файл", command=self.choose_file).pack(side=tk.LEFT, padx=10)
        self.file_label = ttk.Label(top_frame, text=f"Файл: {os.path.basename(self.current_file)}", foreground="#f1fa8c")
        self.file_label.pack(side=tk.LEFT, padx=20)

        # Кнопки алгоритмів
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Жадібний алгоритм", width=25, command=self.run_greedy).grid(row=0, column=0, padx=15, pady=10)
        ttk.Button(btn_frame, text="Перебір з відсіченням", width=25, command=self.run_branch).grid(row=0, column=1, padx=15, pady=10)
        ttk.Button(btn_frame, text="Хопкрофт–Карп", width=25, command=self.run_hopcroft).grid(row=0, column=2, padx=15, pady=10)

        self.progress = ttk.Progressbar(self.root, length=800, mode='determinate')
        self.progress.pack(pady=10)

        # Область виводу
        self.log_area = scrolledtext.ScrolledText(
            self.root,
            bg="#282a36",
            fg="#f8f8f2",
            font=("Consolas", 11),
            insertbackground="white"
        )
        self.log_area.pack(padx=20, pady=(0,20), fill=tk.BOTH, expand=True)

    def log(self, text):
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        self.log_area.delete(1.0, tk.END)

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Оберіть JSON-файл з даними",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir="data"
        )
        if file_path:
            self.current_file = file_path
            self.file_label.config(text=f"Файл: {os.path.basename(file_path)}")
            self.load_file(file_path)

    def load_default_file(self):
        if os.path.exists("data/input.json"):
            self.load_file("data/input.json")
        else:
            self.log("data/input.json не знайдено — натисніть кнопку, щоб вибрати файл")

    def load_file(self, path):
        try:
            self.problem.load_from_json(path)
            self.clear_log()
            self.log("Дані успішно завантажено!")
            self.log(f"   Уроків: {len(self.problem.lessons)}")
            self.log(f"   Груп: {len(self.problem.groups)}")
            self.log(f"   Викладачів: {len(self.problem.teachers)}")
            self.log(f"   Аудиторій: {len(self.problem.classrooms)}")
            self.log(f"   Слотів: {len(self.problem.timeslots)}\n")
            self.log("Оберіть алгоритм:")
        except Exception as e:
            messagebox.showerror("Помилка завантаження", str(e))
            self.log(f"Помилка: {e}")

    def run_algorithm(self, func, name):
        if len(self.problem.lessons) == 0:
            messagebox.showwarning("Немає даних", "Завантажте JSON-файл!")
            return

        self.clear_log()
        self.log(f"Запуск: {name} ...")
        self.progress['value'] = 0
        self.root.update()

        start = time.time()
        schedule = func(self.problem)
        duration = time.time() - start

        self.progress['value'] = 100

        placed = len(schedule)
        total = len(self.problem.lessons)

        self.log(f"\n{name} завершив за {duration:.4f} сек")
        self.log(f"Розміщено: {placed}/{total} пар ({placed/total*100:.1f}%)")

        if validate_schedule(schedule, self.problem):
            self.log("Розклад коректний!")
            export_to_excel(schedule, self.problem)
            export_to_html(schedule, self.problem)
            self.log("Збережено у папку results/")
        else:
            self.log("УВАГА: Є конфлікти!")

        self.log("\n" + "═" * 100)
        self.log(" РОЗКЛАД ЗАНЯТЬ ".center(100))
        self.log("═" * 100)

        days = ["Понед", "Вів", "Сер", "Чет", "Пт"]
        times = ["08:30", "10:25", "12:20", "14:10", "16:00", "17:50"]

        for d in range(5):
            self.log(f"\n{days[d]:>70}")
            for p in range(6):
                slot = (d, p)
                entries = [
                    f"{l.subject.name[:20]:20} │ {l.teacher.name[:12]} │ ауд.{c.id} │ {l.group.name}"
                    for (l, c, s) in schedule.keys() if s == slot
                ]
                if entries:
                    self.log(f"{times[p]} → {entries[0]}")
                    for e in entries[1:]:
                        self.log(" " * 12 + e)
                else:
                    self.log(f"{times[p]} → —")

    def run_greedy(self):
        self.run_algorithm(greedy_schedule, "Жадібний алгоритм")

    def run_branch(self):
        self.run_algorithm(branch_and_bound_schedule, "Перебір з відсіченням")

    def run_hopcroft(self):
        self.run_algorithm(hopcroft_karp_schedule, "Алгоритм Хопкрофта–Карпа")


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    root = tk.Tk()
    app = ScheduleGUI(root)
    root.mainloop()