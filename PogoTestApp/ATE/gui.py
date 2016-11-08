import tkinter as tk
import tkinter.constants as tkc
from tkinter import messagebox
from tkinter.messagebox import WARNING, ABORTRETRYIGNORE
from ATE.const import *
#import tkmessagebox

class MainForm(tk.Frame):
    
    _fields = None

    def __init__(self, master):
        super().__init__(master)
        #master.resizable(0,0)
        master.geometry("800x480")
        master.title("X231 PCB Tester")
        self.pack()
        self.create_widgets()

    def fullscreen(self, master, enable):
        master.attributes("-fullscreen", enable)

    def center(self, master):
        master.withdraw()
        master.update_idletasks()
        x = (master.winfo_screenwidth() - master.winfo_reqwidth()) / 2
        y = (master.winfo_screenheight() - master.winfo_reqheight()) / 2

        master.geometry("+%d+%d" % (x, y))
        master.deiconify()

    def set_text(self, text):
        self.info_label["text"] = text

    def create_widgets(self):
        padding = 10
        btn_font = ("Arial", 18, "bold")
        header_font = "Arial 10 bold"

        readings_container = tk.Frame(self, width = 760, height = 150)
        readings_container.grid(column = 0, row = 0, columnspan = 3, sticky = tkc.W, pady = 5)

        h1 = tk.Label(readings_container)
        h1["text"] = "Voltage Measures"
        h1["font"] = header_font
        h1.grid(column = 0, row = 0, columnspan = 2, sticky = tkc.W + tkc.N)

        h2 = tk.Label(readings_container)
        h2["text"] = "Digital Outputs"
        h2["font"] = header_font
        h2.grid(column = 2, row = 0, columnspan = 2, sticky = tkc.W + tkc.N)

        h3 = tk.Label(readings_container)
        h3["text"] = "Digital Inputs"
        h3["font"] = header_font
        h3.grid(column = 4, row = 0, columnspan = 2, sticky = tkc.W + tkc.N)

        self._fields = {
            "AD1": {"name": "AD1 Pogo Input Volts", "value": tk.StringVar(), "column": 0, "row": 1 },
            "AD2": {"name": "AD2 Tablet USB Volts", "value": tk.StringVar(), "column": 0, "row": 2 },
            "AD3": {"name": "AD3 Batt Board Power In Volts", "value": tk.StringVar(), "column": 0, "row": 3},
            "AD4": {"name": "AD4 Batt Board Temp Sense Cutoff", "value": tk.StringVar(), "column": 0, "row": 4},
            "AD5": {"name": "AD5 Batt Board Battery Volts", "value": tk.StringVar(), "column": 0, "row": 5},
            "AD6": {"name": "AD6 External USB Volts", "value": tk.StringVar(), "column": 0, "row": 6},
            "AD7": {"name": "AD7 Pogo Battery Output", "value": tk.StringVar(), "column": 0, "row": 7},

            "DOP1": {"name": "DOP1 Tablet Full Load Switch", "value": tk.StringVar(), "column": 2, "row": 1},
            "DOP2": {"name": "DOP2 Tablet Charged Load Switch", "value": tk.StringVar(), "column": 2, "row": 2},
            "DOP3": {"name": "DOP3 OTG Mode Trigger", "value": tk.StringVar(), "column": 2, "row": 3},

            "DIP1": {"name": "DIP1 TP3 Q4 Startup Delay", "value": tk.StringVar(), "column": 4, "row": 1},
            "DIP2": {"name": "DIP2 Tablet OTG Sense", "value": tk.StringVar(), "column": 4, "row": 2},
            "DIP3": {"name": "DIP3 D+ Tablet USB Sense", "value": tk.StringVar(), "column": 4, "row": 3},
            "DIP4": {"name": "DIP4 D- Tablet USB Sense", "value": tk.StringVar(), "column": 4, "row": 4}
        }

        for itm in self._fields.items():
            k = itm[0]
            v = itm[1]

            v["value"].set("...")

            lbl = tk.Label(readings_container)
            lbl["text"] = v["name"]
            lbl.grid(column = v["column"], row = v["row"], sticky = tkc.W + tkc.N)
            #lbl.columnconfigure(v["column"], minsize = 100)

            val = tk.Label(readings_container)
            val["textvariable"] = v["value"]
            val["width"] = 5
            val.grid(column = v["column"] + 1, row = v["row"], sticky = tkc.W + tkc.N, padx = 5)
            #val.columnconfigure(v["column"] + 1, minsize = 20)

        self.test_stage = tk.Label(self)
        self.test_stage["text"] = "Test Stage: {stage_key} {stage_descr}, Duration: {duration}s"
        self.test_stage["font"] = "Arial 10 bold"
        self.test_stage["height"] = 3
        self.test_stage.grid(column = 0, row = 8, columnspan = 3, sticky = tkc.W + tkc.S)

        info_container = tk.Frame(self, width = 760, height = 150)
        info_container.grid(column = 0, row = 9, columnspan = 3)
        info_container.columnconfigure(0, minsize = 760)
        info_container.rowconfigure(0, minsize = 150)

        self.info_label = tk.Label(info_container)
        self.info_label["text"] = "Ready. Press RESET to begin tests."
        #self.info_label["width"] = 85
        #self.info_label["height"] = 21
        self.info_label["bg"] = "white"
        self.info_label["fg"] = "black"
        self.info_label["bd"] = 1
        self.info_label["relief"] = "groove"
        self.info_label["anchor"] = tkc.NW
        self.info_label["wraplength"] = 740
        self.info_label["justify"] = tkc.LEFT
        self.info_label["font"] = ("Courier", 11)
        self.info_label.grid(padx = padding, pady = padding, columnspan = 6, column = 0, row = 0, sticky = tkc.W + tkc.E + tkc.N + tkc.S)
        #self.info_label.grid()
        #self.info_label.columnconfigure(0, minsize = 500)

        self.pass_btn = tk.Button(self)
        self.pass_btn["text"] = "PASS"
        self.pass_btn["fg"] = "green"
        self.pass_btn["font"] = btn_font
        self.pass_btn.grid(padx = padding, pady = padding, sticky = tkc.W, column = 0, row = 10)

        self.reset_btn = tk.Button(self)
        self.reset_btn["text"] = "RESET"
        self.reset_btn["font"] = btn_font
        self.reset_btn.grid(padx = padding, pady = padding, column = 1, row= 10)

        self.fail_btn = tk.Button(self)
        self.fail_btn["text"] = "FAIL"
        self.fail_btn["fg"] = "red"
        self.fail_btn["font"] = btn_font
        self.fail_btn.grid(padx = padding, pady = padding, sticky = tkc.E, column = 2, row = 10)

    def disable_test_buttons(self):
        self.disable_pass_button();
        self.disable_fail_button();

    def enable_test_buttons(self):
        self.enable_pass_button();
        self.enable_fail_button();

    def enable_pass_button(self):
        self.pass_btn["state"] = "normal"

    def enable_fail_button(self):
        self.fail_btn["state"] = "normal"

    def disable_pass_button(self):
        self.pass_btn["state"] = "disabled"

    def disable_fail_button(self):
        self.fail_btn["state"] = "disabled"

    def msgbox(self, title, text):
        messagebox.showinfo(title, text)

    def resetdialogue(self):
        "Asks the user if they want to reset the current test (True), all tests (False) or cancel (None)"
        return messagebox.askretrycancel("RESET", "Do you want to re-run the current test, or cancel the current session and start fresh?\n\nChoose Retry to re-run the current.\nChoose Cancel to abort testing and start again.", icon = WARNING)

    def set_reading_value(self, key, value):
        self._fields[key]["value"].set(value)
