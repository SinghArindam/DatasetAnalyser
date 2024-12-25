import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Analysis and Predictions")
        self.geometry("1000x600")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.dataset = None

        self.create_sidebar_buttons()
        self.create_switch_button()
        self.analysis_tab()

    def create_sidebar_buttons(self):
        analysis_button = ctk.CTkButton(self.sidebar, text="Analysis", command=self.analysis_tab)
        analysis_button.pack(fill="x", pady=10, padx=10)

        predictions_button = ctk.CTkButton(self.sidebar, text="Predictions", command=self.predictions_tab)
        predictions_button.pack(fill="x", pady=10, padx=10)

    def create_switch_button(self):
        self.switch_var = ctk.StringVar(value="on")
        switch_button = ctk.CTkSwitch(self.sidebar, text="Light/Dark Mode", command=self.toggle_mode, variable=self.switch_var, onvalue="on", offvalue="off")
        switch_button.pack(pady=20, padx=10)

    def toggle_mode(self):
        mode = "dark" if self.switch_var.get() == "on" else "light"
        ctk.set_appearance_mode(mode)

    def analysis_tab(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Analysis", font=("Arial", 20)).pack(pady=10)

        load_button = ctk.CTkButton(self.main_frame, text="Load Dataset", command=self.load_dataset)
        load_button.pack(pady=10)

        self.analysis_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=10)
        self.analysis_frame.pack(fill="both", expand=True, pady=10, padx=10)

    def load_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.dataset = pd.read_csv(file_path)
                self.display_plots()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset: {e}")

    def display_plots(self):
        for widget in self.analysis_frame.winfo_children():
            widget.destroy()

        if self.dataset is not None:
            numerical_columns = self.dataset.select_dtypes(include=['number']).columns
            num_cols = len(numerical_columns)

            if num_cols == 0:
                ctk.CTkLabel(self.analysis_frame, text="No numerical columns found in the dataset.").pack(pady=10)
                return

            fig, axes = plt.subplots(nrows=(num_cols + 1) // 2, ncols=2, figsize=(10, 5 * ((num_cols + 1) // 2)))
            axes = axes.flatten() if num_cols > 1 else [axes]

            for i, column in enumerate(numerical_columns):
                self.dataset[column].plot(ax=axes[i], title=column)
                axes[i].set_xlabel("Index")
                axes[i].set_ylabel(column)

            for j in range(i + 1, len(axes)):
                fig.delaxes(axes[j])

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.analysis_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)
            canvas.draw()

    def predictions_tab(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Predictions", font=("Arial", 20)).pack(pady=10)

        self.prediction_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=10)
        self.prediction_frame.pack(fill="both", expand=True, pady=10, padx=10)

        predict_button = ctk.CTkButton(self.main_frame, text="Generate Predictions", command=self.show_predictions)
        predict_button.pack(pady=10)

    def show_predictions(self):
        for widget in self.prediction_frame.winfo_children():
            widget.destroy()

        if self.dataset is None:
            ctk.CTkLabel(self.prediction_frame, text="No dataset loaded. Please load a dataset first.", text_color="red").pack(pady=10)
            return

        categories = self.dataset["Category"].unique() if "Category" in self.dataset.columns else []
        subcategories = self.dataset["Subcategory"].unique() if "Subcategory" in self.dataset.columns else []

        if not categories.any() or not subcategories.any():
            ctk.CTkLabel(self.prediction_frame, text="Dataset does not contain 'Category' or 'Subcategory' columns.", text_color="red").pack(pady=10)
            return

        ctk.CTkLabel(self.prediction_frame, text="Predictions for All Categories and Subcategories", font=("Arial", 14)).pack(pady=10)

        table_frame = ctk.CTkFrame(self.prediction_frame)
        table_frame.pack(pady=20)

        header = ["Category", "Subcategory", "Sales", "Growth", "Customers"]
        for col_idx, header_text in enumerate(header):
            ctk.CTkLabel(table_frame, text=header_text, font=("Arial", 12, "bold"), anchor="center", padx=10, pady=5).grid(row=0, column=col_idx, padx=10, pady=5)

        row_idx = 1
        for category in categories:
            for subcategory in subcategories:
                predictions = {
                    "Sales": round(random.uniform(500, 1500), 2),
                    "Growth": f"{round(random.uniform(2, 10), 2)}%",
                    "Customers": random.randint(50, 500),
                }

                data = [category, subcategory, predictions["Sales"], predictions["Growth"], predictions["Customers"]]
                for col_idx, value in enumerate(data):
                    ctk.CTkLabel(table_frame, text=value, anchor="center", padx=10, pady=5).grid(row=row_idx, column=col_idx, padx=10, pady=5)

                row_idx += 1

        table_frame.pack(anchor="center")

if __name__ == "__main__":
    import random
    app = App()
    app.mainloop()
