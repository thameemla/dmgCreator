import ttkbootstrap as tb
from ttkbootstrap import Style, PRIMARY, SUCCESS, INFO, DANGER, WARNING
from tkinter import filedialog, ttk
import os
import threading
import shutil


class AppBuilderUI:
    def __init__(self):
        self.root = tb.Window(themename="litera")  # Using a clean, modern theme
        self.root.title("macOS App Builder")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        # Global variables
        self.py_file_path = ""
        self.icn_file_path = ""
        self.app_name = ""

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tb.Frame(self.root, bootstyle="light")
        header.pack(fill="x", padx=20, pady=(20, 0))

        title = tb.Label(
            header,
            text="macOS App Builder",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        title.pack(side="left")

        # Main content
        content = tb.Frame(self.root)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Form section
        form_frame = tb.LabelFrame(
            content,
            text="Application Details",
            padding=20,
            bootstyle="primary"
        )
        form_frame.pack(fill="x", padx=10)

        # App Name Section
        name_frame = tb.Frame(form_frame)
        name_frame.pack(fill="x", pady=(0, 15))

        tb.Label(
            name_frame,
            text="Application Name",
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w")

        self.app_name_entry = tb.Entry(name_frame, font=("Helvetica", 10))
        self.app_name_entry.pack(fill="x", pady=(5, 0))

        # File Selection Section
        files_frame = tb.Frame(form_frame)
        files_frame.pack(fill="x", pady=15)

        # Python File Selection
        py_frame = tb.Frame(files_frame)
        py_frame.pack(fill="x", pady=(0, 10))

        tb.Label(
            py_frame,
            text="Python Source File",
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w")

        py_select_frame = tb.Frame(py_frame)
        py_select_frame.pack(fill="x", pady=(5, 0))

        self.py_path_label = tb.Label(
            py_select_frame,
            text="No file selected",
            bootstyle="secondary",
            font=("Helvetica", 9)
        )
        self.py_path_label.pack(side="left", fill="x", expand=True)

        self.py_browse_btn = tb.Button(
            py_select_frame,
            text="Browse",
            command=self.browse_py_file,
            bootstyle="outline-primary",
            width=15
        )
        self.py_browse_btn.pack(side="right", padx=(10, 0))

        # Icon File Selection
        icon_frame = tb.Frame(files_frame)
        icon_frame.pack(fill="x")

        tb.Label(
            icon_frame,
            text="Application Icon (.icns)",
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w")

        icon_select_frame = tb.Frame(icon_frame)
        icon_select_frame.pack(fill="x", pady=(5, 0))

        self.icon_path_label = tb.Label(
            icon_select_frame,
            text="No file selected",
            bootstyle="secondary",
            font=("Helvetica", 9)
        )
        self.icon_path_label.pack(side="left", fill="x", expand=True)

        self.icon_browse_btn = tb.Button(
            icon_select_frame,
            text="Browse",
            command=self.browse_icn_file,
            bootstyle="outline-primary",
            width=15
        )
        self.icon_browse_btn.pack(side="right", padx=(10, 0))

        # Mac Model Selection
        model_frame = tb.LabelFrame(
            content,
            text="Target Architecture",
            padding=20,
            bootstyle="primary"
        )
        model_frame.pack(fill="x", padx=10, pady=20)

        self.mac_model = tb.StringVar()

        for model in ["M1", "Intel"]:
            tb.Radiobutton(
                model_frame,
                text=model,
                variable=self.mac_model,
                value=model,
                bootstyle="primary-toolbutton"
            ).pack(side="left", padx=10, expand=True)

        # Status Section
        status_frame = tb.Frame(content)
        status_frame.pack(fill="x", padx=10, pady=(0, 20))

        self.status_label = tb.Label(
            status_frame,
            text="Ready to build",
            bootstyle="secondary",
            font=("Helvetica", 10)
        )
        self.status_label.pack(anchor="w")

        self.progress_bar = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            style="primary.Horizontal.TProgressbar"
        )

        # Build Button
        self.build_btn = tb.Button(
            content,
            text="Build Application",
            command=self.create,
            bootstyle="success",
            width=20,
            padding=10
        )
        self.build_btn.pack(pady=10)

    def browse_py_file(self):
        self.py_file_path = filedialog.askopenfilename(
            title="Select Python Source File",
            filetypes=(("Python Files", "*.py"), ("All Files", "*.*"))
        )
        if self.py_file_path:
            filename = os.path.basename(self.py_file_path)
            self.py_path_label.config(
                text=f"Selected: {filename}",
                bootstyle="success"
            )

    def browse_icn_file(self):
        self.icn_file_path = filedialog.askopenfilename(
            title="Select Application Icon",
            filetypes=(("Icon Files", "*.icns"), ("All Files", "*.*"))
        )
        if self.icn_file_path:
            filename = os.path.basename(self.icn_file_path)
            self.icon_path_label.config(
                text=f"Selected: {filename}",
                bootstyle="success"
            )

    def update_status(self, message, status="info"):
        status_styles = {
            "info": "secondary",
            "success": "success",
            "error": "danger",
            "warning": "warning"
        }
        self.status_label.config(
            text=message,
            bootstyle=status_styles.get(status, "secondary")
        )

    def run_commands(self):
        try:
            dmg_path = os.path.expanduser(f"~/Desktop/{self.app_name}.dmg")

            # Cleanup previous builds
            if os.path.exists(dmg_path):
                os.remove(dmg_path)

            dist_folder = os.path.join(os.getcwd(), "dist")
            if os.path.exists(dist_folder):
                shutil.rmtree(dist_folder)
            os.makedirs(dist_folder)

            # Build command based on architecture
            if self.mac_model.get() == "M1":
                command = f"pyinstaller --name '{self.app_name}' --windowed --icon '{self.icn_file_path}' '{self.py_file_path}'"
            else:
                command = f"pyinstaller --target-arch=x86_64 --name '{self.app_name}' --windowed --icon '{self.icn_file_path}' '{self.py_file_path}'"

            self.update_status("Building application...", "info")
            os.system(command + ' -y')

            app_path = os.path.join(dist_folder, f"{self.app_name}.app")
            if not os.path.exists(app_path):
                raise Exception("Application build failed")

            # Cleanup and create DMG
            extra_folder = os.path.join(dist_folder, self.app_name)
            if os.path.exists(extra_folder):
                shutil.rmtree(extra_folder)

            temp_dmg_pattern = os.path.expanduser("~/Desktop/rw.*.dmg")
            os.system(f"rm -f {temp_dmg_pattern}")

            self.update_status("Creating DMG file...", "info")
            os.system(rf"""
            create-dmg \
              --volname "{self.app_name}" \
              --volicon "{self.icn_file_path}" \
              --window-pos 200 120 \
              --window-size 600 300 \
              --icon-size 100 \
              --icon "{self.app_name}.app" 175 120 \
              --hide-extension "{self.app_name}.app" \
              --app-drop-link 425 120 \
              --no-internet-enable \
              "{dmg_path}" \
              "dist"
            """)

            os.system(f"rm -f {temp_dmg_pattern}")

            self.update_status(f"Success! DMG file created at: {dmg_path}", "success")

        except Exception as e:
            self.update_status(f"Error: {str(e)}", "error")

        finally:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.build_btn.config(state="normal")
            self.py_browse_btn.config(state="normal")
            self.icon_browse_btn.config(state="normal")

    def create(self):
        # Validate inputs
        self.app_name = self.app_name_entry.get().strip()

        if not self.app_name:
            self.update_status("Please enter an application name", "warning")
            return
        if not self.py_file_path:
            self.update_status("Please select a Python source file", "warning")
            return
        if not self.icn_file_path:
            self.update_status("Please select an application icon", "warning")
            return
        if not self.mac_model.get():
            self.update_status("Please select target architecture", "warning")
            return

        # Start build process
        self.progress_bar.pack(fill="x", pady=(10, 0))
        self.progress_bar.start(10)

        self.build_btn.config(state="disabled")
        self.py_browse_btn.config(state="disabled")
        self.icon_browse_btn.config(state="disabled")

        threading.Thread(target=self.run_commands, daemon=True).start()


if __name__ == "__main__":
    app = AppBuilderUI()
    app.root.mainloop()
