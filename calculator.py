import tkinter as tk
from tkinter import ttk

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("323x510+600+100")
        self.configure(bg="#FAF9F6")
        self.result_vr = tk.StringVar()

        self.create_widgets()
        self.bind_keys()           # ← NEW

    # ---------------- UI ----------------
    def create_widgets(self):
        display_frame = tk.Frame(self, bg="#FAF9F6")
        display_frame.pack(fill="both")

        ttk.Entry(
            display_frame,
            textvariable=self.result_vr,
            font=("Segoe UI", 38),
            justify="right"
        ).pack(fill="both", padx=10, pady=49)

        btns_frm = tk.Frame(self, bg="#FAF9F6")
        btns_frm.pack(fill="both", expand=True)

        # Memory row removed ↓
        btns = [
            ['%',  'CE', 'C',  'o'],
            ['1/x','x^2','rtx','/'],
            ['7',  '8',  '9',  '*'],
            ['4',  '5',  '6',  '-'],
            ['1',  '2',  '3',  '+'],
            ['+/-','0',  '.',  '=']
        ]

        for r, row in enumerate(btns):
            for c, label in enumerate(row):
                tk.Button(
                    btns_frm,
                    text=label,
                    font=("Segoe UI", 14),
                    height=2, width=4,
                    relief=tk.GROOVE,
                    bg="#0F52BA" if label == "=" else "white",
                    fg="white"  if label == "=" else "black",
                    command=lambda b=label: self.on_button_click(b)
                ).grid(row=r, column=c, padx=2, pady=.7, sticky="nsew")

        for i in range(4):
            btns_frm.columnconfigure(i, weight=1)
        for i in range(len(btns)):
            btns_frm.rowconfigure(i, weight=1)

    # ------------- KEYBOARD -------------
    def bind_keys(self):
        # digits, operators, dot
        for key in "0123456789+-*/.%":
            self.bind(key, self.key_input)
        # special keys
        self.bind("<Return>",     self.key_input)   # Enter
        self.bind("<BackSpace>",  self.key_input)   # backspace
        self.bind("<Escape>",     self.key_input)   # clear
        self.focus_set()  # ensure the window receives key presses

    def key_input(self, event):
        mapping = {                 # translate to button labels
            "Return": "=",
            "BackSpace": "o",
            "Escape": "C"
        }
        char = event.char if event.char else mapping.get(event.keysym, "")
        if char:
            self.on_button_click(char)

    # -------- BUTTON HANDLER --------
    def on_button_click(self, char):
        current = self.result_vr.get()

        if char == "C":
            self.result_vr.set("")

        elif char == "CE":                           # clear last entry
            for i in range(len(current) - 1, -1, -1):
                if current[i] in "+-*/":
                    self.result_vr.set(current[:i + 1])
                    break
            else:
                self.result_vr.set("")

        elif char == "o":                            # backspace
            self.result_vr.set(current[:-1])

        elif char == "1/x":
            try: self.result_vr.set(str(1 / float(current)))
            except Exception: self.result_vr.set("Error")

        elif char == "x^2":
            try: self.result_vr.set(str(float(current) ** 2))
            except Exception: self.result_vr.set("Error")

        elif char == "rtx":                          # √x
            try: self.result_vr.set(str(float(current) ** 0.5))
            except Exception: self.result_vr.set("Error")

        elif char == "+/-":                          # toggle sign
            if current.startswith("-"):
                self.result_vr.set(current[1:])
            elif current:
                self.result_vr.set("-" + current)

        elif char == "%":
            try: self.result_vr.set(str(float(current) / 100))
            except Exception: self.result_vr.set("Error")

        elif char == "=":
            try: self.result_vr.set(str(eval(current)))
            except Exception: self.result_vr.set("Error")

        else:                                        # digits & operators
            self.result_vr.set(current + char)


if __name__ == "__main__":
    Calculator().mainloop()
