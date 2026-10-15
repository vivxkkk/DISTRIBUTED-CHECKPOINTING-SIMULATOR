
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

APP_TITLE = "Distributed Checkpointing Simulator"
DATA_FILE = "checkpoints.json"


class DistributedCheckpointingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1050x720")
        self.root.minsize(850, 600)
        self.root.configure(bg="#101827")

        self.processes = {
            "P1": {"counter": 0, "messages": 0, "status": "Running"},
            "P2": {"counter": 0, "messages": 0, "status": "Running"},
            "P3": {"counter": 0, "messages": 0, "status": "Running"},
        }

        self.message_queue = []
        self.checkpoint = None
        self.checkpoint_number = 0

        self.setup_style()
        self.build_ui()
        self.update_display()
        self.log("Simulator initialized. All processes are running.")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#1d293b",
            foreground="white",
            fieldbackground="#1d293b",
            rowheight=30,
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#27364b",
            foreground="white",
            font=("Arial", 10, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "white")]
        )
        style.configure(
            "TCombobox",
            fieldbackground="#1d293b",
            background="#27364b",
            foreground="black"
        )

    def build_ui(self):
        header = tk.Frame(self.root, bg="#172338", pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="DISTRIBUTED CHECKPOINTING SIMULATOR",
            font=("Arial", 20, "bold"),
            bg="#172338",
            fg="#60a5fa"
        ).pack()

        tk.Label(
            header,
            text="Process Execution  |  Checkpoint  |  Failure  |  Recovery",
            font=("Arial", 10),
            bg="#172338",
            fg="#cbd5e1"
        ).pack(pady=(5, 0))

        main = tk.Frame(self.root, bg="#101827", padx=20, pady=15)
        main.pack(fill="both", expand=True)

        tk.Label(
            main,
            text="DISTRIBUTED PROCESSES",
            font=("Arial", 12, "bold"),
            bg="#101827",
            fg="white"
        ).pack(anchor="w", pady=(0, 8))

        cards = tk.Frame(main, bg="#101827")
        cards.pack(fill="x", pady=(0, 15))

        self.card_labels = {}

        for name in self.processes:
            card = tk.Frame(
                cards,
                bg="#1d293b",
                padx=15,
                pady=13,
                highlightbackground="#34445c",
                highlightthickness=1
            )
            card.pack(side="left", fill="both", expand=True, padx=5)

            tk.Label(
                card, text=name, font=("Arial", 17, "bold"),
                bg="#1d293b", fg="#60a5fa"
            ).pack(anchor="w")

            counter_label = tk.Label(
                card, text="Counter: 0", font=("Arial", 11),
                bg="#1d293b", fg="white"
            )
            counter_label.pack(anchor="w", pady=(8, 3))

            messages_label = tk.Label(
                card, text="Messages received: 0",
                font=("Arial", 10), bg="#1d293b", fg="#cbd5e1"
            )
            messages_label.pack(anchor="w", pady=3)

            status_label = tk.Label(
                card, text="Status: Running",
                font=("Arial", 10, "bold"),
                bg="#1d293b", fg="#4ade80"
            )
            status_label.pack(anchor="w", pady=(3, 0))

            self.card_labels[name] = (
                counter_label, messages_label, status_label
            )

        tk.Label(
            main, text="CONTROL PANEL",
            font=("Arial", 12, "bold"),
            bg="#101827", fg="white"
        ).pack(anchor="w", pady=(0, 8))

        controls = tk.Frame(main, bg="#1d293b", padx=12, pady=12)
        controls.pack(fill="x", pady=(0, 12))

        tk.Label(
            controls, text="Select Process:",
            bg="#1d293b", fg="white"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.selected_process = tk.StringVar(value="P1")
        self.process_selector = ttk.Combobox(
            controls,
            textvariable=self.selected_process,
            values=list(self.processes.keys()),
            state="readonly",
            width=8
        )
        self.process_selector.grid(row=0, column=1, padx=5, pady=5)

        self.make_button(
            controls, "Execute Process",
            self.execute_process, "#2563eb"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.make_button(
            controls, "Send Message",
            self.send_message, "#7c3aed"
        ).grid(row=0, column=3, padx=5, pady=5)

        self.make_button(
            controls, "Create Checkpoint",
            self.create_checkpoint, "#047857"
        ).grid(row=0, column=4, padx=5, pady=5)

        self.make_button(
            controls, "Simulate Failure",
            self.simulate_failure, "#b91c1c"
        ).grid(row=1, column=2, padx=5, pady=7)

        self.make_button(
            controls, "Rollback Recovery",
            self.rollback_recovery, "#0369a1"
        ).grid(row=1, column=3, padx=5, pady=7)

        self.make_button(
            controls, "Reset Simulation",
            self.reset_simulation, "#475569"
        ).grid(row=1, column=4, padx=5, pady=7)

        checkpoint_frame = tk.Frame(
            main, bg="#172338", padx=12, pady=10
        )
        checkpoint_frame.pack(fill="x", pady=(0, 12))

        tk.Label(
            checkpoint_frame, text="LAST CHECKPOINT",
            font=("Arial", 10, "bold"),
            bg="#172338", fg="#fbbf24"
        ).pack(anchor="w")

        self.checkpoint_label = tk.Label(
            checkpoint_frame,
            text="No checkpoint created yet",
            font=("Arial", 10),
            bg="#172338", fg="white"
        )
        self.checkpoint_label.pack(anchor="w", pady=(5, 0))

        log_header = tk.Frame(main, bg="#101827")
        log_header.pack(fill="x")

        tk.Label(
            log_header, text="EVENT LOG",
            font=("Arial", 12, "bold"),
            bg="#101827", fg="white"
        ).pack(side="left")

        self.make_button(
            log_header, "Clear Log", self.clear_log, "#475569"
        ).pack(side="right")

        log_frame = tk.Frame(main, bg="#1d293b")
        log_frame.pack(fill="both", expand=True, pady=(8, 0))

        self.log_box = tk.Text(
            log_frame,
            bg="#0b1220",
            fg="#d1d5db",
            insertbackground="white",
            font=("Consolas", 10),
            wrap="word",
            height=9,
            relief="flat",
            padx=10,
            pady=8
        )
        scrollbar = ttk.Scrollbar(
            log_frame, command=self.log_box.yview
        )
        self.log_box.configure(yscrollcommand=scrollbar.set)

        self.log_box.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.log_box.configure(state="disabled")

    def make_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=10,
            pady=7,
            cursor="hand2"
        )

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{timestamp}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def update_display(self):
        for name, process in self.processes.items():
            counter, messages, status = self.card_labels[name]

            counter.config(text=f"Counter: {process['counter']}")
            messages.config(
                text=f"Messages received: {process['messages']}"
            )
            status.config(text=f"Status: {process['status']}")

            if process["status"] == "Running":
                status.config(fg="#4ade80")
            else:
                status.config(fg="#f87171")

        if self.checkpoint is None:
            self.checkpoint_label.config(
                text="No checkpoint created yet"
            )
        else:
            self.checkpoint_label.config(
                text=(
                    f"Checkpoint #{self.checkpoint_number} | "
                    f"{self.checkpoint['time']} | "
                    f"Saved state of {len(self.checkpoint['processes'])} "
                    "processes"
                )
            )

    def get_selected(self):
        return self.selected_process.get()

    def execute_process(self):
        name = self.get_selected()
        process = self.processes[name]

        if process["status"] != "Running":
            messagebox.showwarning(
                "Process Failed",
                f"{name} has failed. Recover it before execution."
            )
            return

        process["counter"] += 1
        self.log(
            f"{name} executed an operation. "
            f"Counter = {process['counter']}."
        )
        self.update_display()

    def send_message(self):
        sender = self.get_selected()

        if self.processes[sender]["status"] != "Running":
            messagebox.showwarning(
                "Process Failed", f"{sender} is not running."
            )
            return

        receivers = [
            name for name in self.processes
            if name != sender
            and self.processes[name]["status"] == "Running"
        ]

        if not receivers:
            messagebox.showwarning(
                "No Receiver", "There is no other running process."
            )
            return

        receiver = receivers[0]
        self.processes[sender]["counter"] += 1
        self.processes[receiver]["messages"] += 1

        message = f"{sender} -> {receiver}"
        self.message_queue.append(message)

        self.log(f"Message sent: {sender} -> {receiver}.")
        self.update_display()

    def create_checkpoint(self):
        self.checkpoint_number += 1

        saved_processes = {
            name: process.copy()
            for name, process in self.processes.items()
        }

        self.checkpoint = {
            "number": self.checkpoint_number,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processes": saved_processes,
            "message_queue": self.message_queue.copy()
        }

        self.save_checkpoint_to_file()

        self.log(
            f"Checkpoint #{self.checkpoint_number} created. "
            "All process states and message history were saved."
        )
        self.update_display()

    def simulate_failure(self):
        name = self.get_selected()
        process = self.processes[name]

        if process["status"] == "Failed":
            messagebox.showinfo(
                "Already Failed", f"{name} has already failed."
            )
            return

        process["status"] = "Failed"
        self.log(
            f"FAILURE: {name} has stopped. "
            "Its current state is unavailable."
        )
        self.update_display()

    def rollback_recovery(self):
        if self.checkpoint is None:
            messagebox.showwarning(
                "No Checkpoint",
                "Create a checkpoint before attempting recovery."
            )
            return

        failed = [
            name for name, process in self.processes.items()
            if process["status"] == "Failed"
        ]

        if not failed:
            messagebox.showinfo(
                "No Failure", "Simulate a process failure first."
            )
            return

        for name, saved_process in self.checkpoint["processes"].items():
            self.processes[name] = saved_process.copy()

        self.message_queue = self.checkpoint["message_queue"].copy()

        self.log(
            f"ROLLBACK: Restored all processes to checkpoint "
            f"#{self.checkpoint['number']}."
        )
        self.log(
            "Recovery completed. All processes are running "
            "from the saved global state."
        )
        self.update_display()

    def reset_simulation(self):
        if not messagebox.askyesno(
            "Reset Simulation",
            "Reset all process states and delete the current checkpoint?"
        ):
            return

        for name in self.processes:
            self.processes[name] = {
                "counter": 0,
                "messages": 0,
                "status": "Running"
            }

        self.message_queue = []
        self.checkpoint = None
        self.checkpoint_number = 0

        if os.path.exists(DATA_FILE):
            try:
                os.remove(DATA_FILE)
            except OSError:
                self.log("Warning: Could not delete checkpoint file.")

        self.log("Simulation reset. All processes are running.")
        self.update_display()

    def save_checkpoint_to_file(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(self.checkpoint, file, indent=4)
            self.log(f"Checkpoint saved to {DATA_FILE}.")
        except OSError as error:
            self.log(f"Could not save checkpoint file: {error}")

    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def on_close(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DistributedCheckpointingSimulator(root)
    root.mainloop()
