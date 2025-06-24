import tkinter as tk
from tkinter import ttk, messagebox
from diagnostic_system import DiagnosticSystem

class DiagnosisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Експертна система діагностики ПК")
        self.system = DiagnosticSystem()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        self.create_input_tab()
        self.create_history_tab()

    def create_input_tab(self):
        self.input_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.input_tab, text="Введення симптомів")

        self.power_var = tk.BooleanVar()
        self.fans_var = tk.StringVar(value="yes")
        self.temp_var = tk.StringVar()
        self.noise_var = tk.BooleanVar()

        tk.Checkbutton(self.input_tab, text="Комп’ютер не вмикається", variable=self.power_var).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(self.input_tab, text="Чути вентилятори?").grid(row=1, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.input_tab, text="Так", variable=self.fans_var, value="yes").grid(row=1, column=1)
        tk.Radiobutton(self.input_tab, text="Ні", variable=self.fans_var, value="no").grid(row=1, column=2)

        tk.Label(self.input_tab, text="Температура (°C):").grid(row=2, column=0, sticky="w", padx=10)
        tk.Entry(self.input_tab, textvariable=self.temp_var).grid(row=2, column=1, columnspan=2, sticky="we", padx=10)

        tk.Checkbutton(self.input_tab, text="Є шум", variable=self.noise_var).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        tk.Button(self.input_tab, text="Отримати діагноз", command=self.get_diagnosis).grid(row=4, column=0, columnspan=3, pady=10)

    def create_history_tab(self):
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="Історія діагнозів")

        tk.Button(self.history_tab, text="Оновити", command=self.load_history).pack(pady=5)

        columns = ("timestamp", "symptoms", "diagnosis")
        self.tree = ttk.Treeview(self.history_tab, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="w", stretch=True, width=150)

        self.tree.pack(expand=True, fill="both", padx=10, pady=5)
        self.load_history()

    def get_diagnosis(self):
        try:
            data = {
                "power": not self.power_var.get(),
                "fans": self.fans_var.get() == "yes",
                "temp": self.temp_var.get(),
                "noise": self.noise_var.get()
            }

            diagnoses = self.system.diagnose(data)
            self.system.save_to_csv(data, diagnoses)
            messagebox.showinfo("Діагноз", "\n".join(diagnoses))

        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def load_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        df = self.system.load_history(10)
        if not df.empty:
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=(row["timestamp"], row["symptoms"], row["diagnosis"]))
        else:
            self.tree.insert("", "end", values=("Немає даних", "", ""))

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosisApp(root)
    root.mainloop()
