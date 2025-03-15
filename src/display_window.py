import tkinter as tk
from tkinter import messagebox, Label
from authenticator import Authenticator


class AuthenticatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Authenticator")
        self.authenticators = []
        self.get_saved_authenticators()
        for i, authenticator in enumerate(self.authenticators):
            auth = Authenticator(authenticator["label"], authenticator["seed"])
            labels = auth.get_labels()
            self.label = tk.Label(root, text=labels["label"]).grid(
                column=0, row=i, padx=10, pady=10
            )
            self.pin = tk.Label(root, text=labels["pin"]).grid(column=1, row=i)
            self.seconds_remaining = tk.Label(root, text=labels["seconds_remaining"])
            self.seconds_remaining.grid(column=2, row=i, padx=5)
            self.update_timer(self.seconds_remaining, labels["seconds_remaining"])

    def update_timer(self, label: Label, seconds_remaining: int):
        remaining = seconds_remaining - 1
        if remaining == -1:
            self.get_new_pins()
        else:
            label["text"] = str(remaining)
            self.root.after(1000, self.update_timer, label, remaining)

    def get_new_pins(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        for i, authenticator in enumerate(self.authenticators):
            auth = Authenticator(authenticator["label"], authenticator["seed"])
            labels = auth.get_labels()
            self.label = tk.Label(self.root, text=labels["label"]).grid(
                column=0, row=i, padx=10, pady=10
            )
            self.pin = tk.Label(self.root, text=labels["pin"]).grid(column=1, row=i)
            self.seconds_remaining = tk.Label(
                self.root, text=labels["seconds_remaining"]
            )
            self.seconds_remaining.grid(column=2, row=i, padx=5)
            self.update_timer(self.seconds_remaining, labels["seconds_remaining"])

    def get_saved_authenticators(self):
        with open("authenticators.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                label, seed = line.strip().split(",")
                self.authenticators.append({"label": label, "seed": seed})


if __name__ == "__main__":
    root = tk.Tk()
    app = AuthenticatorApp(root)
    root.mainloop()
