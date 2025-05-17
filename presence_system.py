import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import threading
import time
import datetime
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PresenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("People Recognition & Energy-Saving Control Engine")
        self.root.geometry("1200x700")
        self.root.configure(bg="#fce4ec")  

        self.default_password = "admin"
        self.current_password = self.default_password
        self.admin_logged_in = False
        self.camera_enabled = True
        self.automation_enabled = True

        self.appliance_states = {"LIGHTS": False, "AIRCON": False}
        self.appliance_start_times = {}
        self.daily_durations = {"LIGHTS": datetime.timedelta(), "AIRCON": datetime.timedelta()}
        self.log_file = "appliance_logs.csv"

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()

        self.last_detection_time = None
        self.warning_shown = False
        self.video_capture = cv2.VideoCapture(0)

        self.appliance_images = {
            "LIGHTS": {
                True: ImageTk.PhotoImage(Image.open("light_on.png").resize((200, 180))),
                False: ImageTk.PhotoImage(Image.open("light_off.png").resize((200, 180)))
            },
            "AIRCON": {
                True: ImageTk.PhotoImage(Image.open("aircon_on.png").resize((180, 200))),
                False: ImageTk.PhotoImage(Image.open("aircon_off.png").resize((180, 200)))
            }
        }

        self.setup_gui()
        self.update_frame()

    def styled_button(self, parent, text, command=None, color="#f06292"):
        btn = tk.Button(parent, text=text, command=command,
                        font=("Arial", 16, "bold"), bg=color, fg="white", relief="flat",
                        activebackground="#e91e63", activeforeground="white")
        return btn

    def setup_gui(self):
        top_frame = tk.Frame(self.root, bg="gray")
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        logo_image = Image.open("logo.png") 
        logo_image = logo_image.resize((90, 50))
        logo_tk = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(top_frame, image=logo_tk, bg="grey")
        logo_label.image = logo_tk  
        logo_label.pack(side="left", padx=10)

        tk.Label(top_frame, text="PRESENCE", font=("Arial", 36, "bold"),
                bg="#f06292", fg="white").pack(side="left")

        btn_frame = tk.Frame(top_frame, bg="#fce4ec")
        btn_frame.pack(side="right")

        self.styled_button(btn_frame, "HOME", command=self.reset_to_home).pack(side="left", padx=5)
        self.styled_button(btn_frame, "ADMIN", command=self.toggle_admin_panel).pack(side="left", padx=5)

        self.left_frame = tk.Frame(self.root, bg="#fce4ec")
        self.left_frame.pack(side="left", fill="y", padx=20, pady=20)

        self.appliance_panel = tk.Frame(self.left_frame, bg="#fce4ec")
        self.appliance_panel.pack(side="top", pady=10)

        self.appliance_icons = {}
        for appliance in ["LIGHTS", "AIRCON"]:
            icon_label = tk.Label(self.appliance_panel, image=self.appliance_images[appliance][False], bg="#fce4ec")
            icon_label.pack(pady=10)
            self.appliance_icons[appliance] = icon_label

        self.status_label = tk.Label(self.left_frame, text="🔍 DETECTING...",
                                     font=("Arial", 16, "bold"), bg="#fce4ec", fg="gray")
        self.status_label.pack(pady=20)

        self.right_frame = tk.Frame(self.root, bg="#e61d60")
        self.right_frame.pack(side="left", padx=10)

        tk.Label(self.right_frame, text="LIVE CAMERA FEED", font=("Arial", 14, "bold"), fg="black", bg="#fce4ec").pack(pady=(10, 0))

        self.camera_label = tk.Label(self.right_frame, bg="#fce4ec")
        self.camera_label.pack(pady=(5, 10))

        self.warning_label = tk.Label(self.right_frame, text="", font=("Arial", 14, "bold"),
                                      fg="red", bg="#fce4ec")
        self.warning_label.pack(pady=10)

        bottom_frame = tk.Frame(self.root, bg="#fce4ec")
        bottom_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        columns = ("Time", "Activity")
        self.tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Activity", text="Activity")
        self.tree.column("Time", width=150)
        self.tree.column("Activity", width=400)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="grey", foreground="white", fieldbackground="pink", rowheight=25)
        style.map("Treeview", background=[('selected', "#da2866")])

        scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.admin_panel = tk.Frame(self.root, bg="#fce4ec")

    def update_frame(self):
        if self.camera_enabled:
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.flip(frame, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

                fg_mask = self.bg_subtractor.apply(gray)
                motion_detected = np.sum(fg_mask > 127) > 5000
                face_detected = len(faces) > 0
                detected = face_detected or motion_detected

                if detected:
                    self.last_detection_time = datetime.datetime.now()
                    self.warning_shown = False
                    self.status_label.config(text="✅ OCCUPIED", fg="green")
                    self.warning_label.config(text="")
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
                    self.turn_on_appliances()
                else:
                    if self.last_detection_time:
                        elapsed = (datetime.datetime.now() - self.last_detection_time).total_seconds()
                        if elapsed > 10 and not self.warning_shown:
                            self.warning_label.config(text="⚠️ No detection. Turning off in 5s.")
                            self.warning_shown = True
                        if elapsed > 15:
                            self.turn_off_appliances()
                            self.status_label.config(text="❌ UNOCCUPIED", fg="red")
                            self.warning_label.config(text="")
                            self.last_detection_time = None
                    else:
                        self.status_label.config(text="🔍 DETECTING...", fg="gray")

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
        else:
            blank = Image.new("RGB", (640, 480), "black")
            imgtk = ImageTk.PhotoImage(image=blank)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def log_activity(self, message):
        timestamp = datetime.datetime.now()
        time_str = timestamp.strftime("%H:%M:%S")
        date_str = timestamp.strftime("%Y-%m-%d")
        log_entry = [date_str, time_str, message]
    
        self.tree.insert("", "end", values=(time_str, message))
    
        with open(self.log_file, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(log_entry)


    def turn_on_appliances(self):
        for appliance in self.appliance_states:
            if not self.appliance_states[appliance]:
                self.appliance_states[appliance] = True
                self.appliance_start_times[appliance] = datetime.datetime.now()
                self.appliance_icons[appliance].configure(image=self.appliance_images[appliance][True])
                self.log_activity(f"{appliance} turned ON")

    def turn_off_appliances(self):
        for appliance in self.appliance_states:
            if self.appliance_states[appliance]:
                start_time = self.appliance_start_times.get(appliance)
                if start_time:
                    duration = datetime.datetime.now() - start_time
                    self.daily_durations[appliance] += duration
                self.appliance_states[appliance] = False
                self.appliance_icons[appliance].configure(image=self.appliance_images[appliance][False])
                self.log_activity(f"{appliance} turned OFF after {duration}")

    def reset_to_home(self):
        self.admin_logged_in = False
        self.clear_admin_panel()
        self.admin_panel.pack_forget()
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.appliance_panel.master = self.left_frame
        self.appliance_panel.pack(side="top", pady=10)

    def create_admin_login(self):
        self.clear_admin_panel()
        tk.Label(self.admin_panel, text="ADMIN LOGIN", bg="#fce4ec", font=("Arial", 14, "bold"), fg="#f06292").pack(pady=10)
        tk.Label(self.admin_panel, text="Password", bg="#fce4ec").pack()
        self.password_entry = tk.Entry(self.admin_panel, show="*")
        self.password_entry.pack(pady=5)
        self.styled_button(self.admin_panel, "Login", self.check_admin_login).pack(pady=5)
        self.admin_panel.pack(side="right", fill="both", expand=True)

    def check_admin_login(self):
        if self.password_entry.get() == self.current_password:
            self.admin_logged_in = True
            if self.current_password == self.default_password:
                self.prompt_password_change()
            else:
                self.create_admin_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect password")

    def prompt_password_change(self):
        self.clear_admin_panel()
        tk.Label(self.admin_panel, text="CHANGE DEFAULT PASSWORD", bg="#fce4ec", font=("Arial", 14, "bold"), fg="#f06292").pack(pady=10)
        tk.Label(self.admin_panel, text="New Password", bg="#fce4ec").pack()
        new_pass_entry = tk.Entry(self.admin_panel, show="*")
        new_pass_entry.pack(pady=5)

        def set_new_password():
            new_pass = new_pass_entry.get()
            if new_pass and new_pass != self.default_password:
                self.current_password = new_pass
                messagebox.showinfo("Success", "Password changed successfully!")
                self.create_admin_dashboard()
            else:
                messagebox.showerror("Error", "Password must be different from the default.")

        self.styled_button(self.admin_panel, "Set Password", set_new_password).pack(pady=5)

    def create_admin_dashboard(self):
        self.clear_admin_panel()
        tk.Label(self.admin_panel, text="ADMIN PANEL", bg="#fce4ec", font=("Arial", 14, "bold"), fg="#f06292").pack(pady=10)

        self.automation_btn = self.styled_button(self.admin_panel, "Turn Off Automation", self.toggle_automation)
        self.automation_btn.pack(pady=5, fill="x")

        self.styled_button(self.admin_panel, "View Activity Log", self.view_logs).pack(pady=5, fill="x")
        self.styled_button(self.admin_panel, "View Summary Graph", self.view_summary_graph).pack(pady=5, fill="x")
        self.styled_button(self.admin_panel, "Export Logs", self.export_logs).pack(pady=5, fill="x")
        self.styled_button(self.admin_panel, "Logout", self.logout_admin, color="gray").pack(pady=5, fill="x")

        self.appliance_panel.pack_forget()
        self.appliance_panel.master = self.admin_panel
        self.appliance_panel.pack(side="bottom", anchor="w", padx=10, pady=10)
        self.admin_panel.pack(side="right", fill="both", expand=True)

    def view_logs(self):
        log_win = tk.Toplevel(self.root)
        log_win.title("Activity Logs")
        log_win.geometry("700x500")

    # Create a frame container
        frame = tk.Frame(log_win)
        frame.pack(fill="both", expand=True)

    # Create Treeview widget
        tree = ttk.Treeview(frame)
        tree.pack(side="left", fill="both", expand=True)

    # Define columns
        tree["columns"] = ("Time", "Activity")
        tree.column("#0", width=100, anchor="w")  # Date column (tree column)
        tree.column("Time", width=100)
        tree.column("Activity", width=500)

        tree.heading("#0", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Activity", text="Activity")

    # Vertical scrollbar
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vsb.set)

    # Optional: Horizontal scrollbar
        hsb = ttk.Scrollbar(log_win, orient="horizontal", command=tree.xview)
        hsb.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=hsb.set)

    # Load logs if file exists
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                reader = csv.reader(file)
                logs_by_date = {}
                for row in reader:
                    if len(row) == 3:
                        date, time, message = row
                        logs_by_date.setdefault(date, []).append((time, message))

                for date, entries in sorted(logs_by_date.items(), reverse=True):
                    parent = tree.insert("", "end", text=date, open=False)  # collapsed by default
                    for time, msg in entries:
                        tree.insert(parent, "end", values=(time, msg))


    def view_summary_graph(self):
        if not os.path.exists(self.log_file):
            messagebox.showinfo("Summary", "No logs found.")
            return

        appliance_data = {}
        ongoing = {}

    # Parse the log file and accumulate usage durations
        with open(self.log_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    date_str, time_str, message = row
                    dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                    if "turned ON" in message:
                        appliance = message.split(" turned ON")[0]
                        ongoing[appliance] = dt
                    elif "turned OFF" in message:
                        appliance = message.split(" turned OFF")[0]
                        start_time = ongoing.pop(appliance, None)
                        if start_time:
                            duration = dt - start_time
                            day_data = appliance_data.setdefault(date_str, {})
                            day_data[appliance] = day_data.get(appliance, datetime.timedelta()) + duration

    # Get last 7 days
        last_7_days = sorted(appliance_data.keys(), reverse=True)[:7]
        last_7_days.reverse()

        appliances = sorted({a for d in appliance_data.values() for a in d})
        usage_matrix = []
        for appliance in appliances:
            daily_usage = []
            for day in last_7_days:
                usage = appliance_data.get(day, {}).get(appliance, datetime.timedelta())
                daily_usage.append(usage.total_seconds() / 60)  # minutes
            usage_matrix.append(daily_usage)

    # Plotting
        fig, ax = plt.subplots(figsize=(10, 5))
        x = np.arange(len(last_7_days))
        width = 0.8 / len(appliances)

        for i, (appliance, usage) in enumerate(zip(appliances, usage_matrix)):
            ax.bar(x + i * width, usage, width, label=appliance)

        ax.set_ylabel("Usage Time (minutes)")
        ax.set_title("Appliance Daily Usage - Last 7 Days")
        ax.set_xticks(x + width * (len(appliances) - 1) / 2)
        ax.set_xticklabels(last_7_days, rotation=0)
        ax.legend()

    # Summary text
        summary_lines = []
        for day in last_7_days:
            summary_lines.append(f"\n{day}:")
            for appliance in appliances:
                usage = appliance_data.get(day, {}).get(appliance, datetime.timedelta())
                if usage.total_seconds() > 0:
                    hrs, rem = divmod(usage.total_seconds(), 3600)
                    mins, secs = divmod(rem, 60)
                    summary_lines.append(
                        f"  • {appliance} ON for {int(hrs)} hr {int(mins)} min {int(secs)} sec"
                    )

        summary_text = "\n".join(summary_lines)

    # Tkinter window
        graph_win = tk.Toplevel(self.root)
        graph_win.title("Weekly Usage Summary")
        graph_win.geometry("1000x600")

        container = ttk.Frame(graph_win)
        canvas = tk.Canvas(container)
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set)

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
       

    # Add chart to scrollable frame
        chart_canvas = FigureCanvasTkAgg(fig, master=scroll_frame)
        chart_widget = chart_canvas.get_tk_widget()
        chart_widget.pack(pady=10, padx=10, fill="both", expand=True)

    # Add summary text
        summary_label = tk.Label(scroll_frame, text=summary_text, justify="left", anchor="w", font=("Arial", 10))
        summary_label.pack(padx=10, pady=(0, 10), fill="both", expand=True)


    def export_logs(self, date=None):
        if not os.path.exists(self.log_file):
            messagebox.showinfo("Export", "No log file to export.")
            return
    
    # Ask user where to save
        dest = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not dest:
            return
    
        with open(self.log_file, "r") as src, open(dest, "w", newline="") as out:
            writer = csv.writer(out)
            reader = csv.reader(src)

            for row in reader:
                if len(row) == 3:
                    row_date, time, msg = row
                    if date is None or row_date == date:
                        writer.writerow(row)

        messagebox.showinfo("Export", "Logs exported successfully!")


    def logout_admin(self):
        self.admin_logged_in = False
        self.clear_admin_panel()
        self.appliance_panel.pack_forget()
        self.appliance_panel.master = self.left_frame
        self.appliance_panel.pack(side="top", pady=10)

    def clear_admin_panel(self):
        for widget in self.admin_panel.winfo_children():
            widget.destroy()

    def toggle_admin_panel(self):
        if not self.admin_logged_in:
            self.create_admin_login()
        else:
            self.create_admin_dashboard()

    def toggle_automation(self):
        self.camera_enabled = not self.camera_enabled
        self.automation_btn.config(text="Turn On Automation" if not self.camera_enabled else "Turn Off Automation")
        if not self.camera_enabled:
            self.turn_off_appliances()
            self.status_label.config(text="❌ UNOCCUPIED", fg="red")
            self.warning_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = PresenceGUI(root)
    root.mainloop()


