import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from PIL import ImageTk, Image
from tkinter import filedialog

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

OptionList = ["IBM", "Microsoft"]


class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.resizable(False, False)
        self.title("Transcription service")
        # self.configure(background="#112d4e")
        container = ttk.Frame(self)
        container.grid(padx=60, pady=30, sticky="EW")
        frame = homepage(container)
        frame.grid(row=0, column=0, sticky="NSEW")

    #
    # def show_frame(self,container):
    #     frame = self.frames[container]
    #     frame.tkraise()


class homepage(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        # -----Variables---#

        services = tk.StringVar(self)
        services.set(OptionList[0])
        self.file_selected = tk.StringVar(value="No file selected...")

        # ----Widgets-----#

        text = ttk.Label(self, text="Choose a service", padding=5)
        services_select = tk.OptionMenu(self, services, *OptionList)
        delete_from_server = ttk.Checkbutton(self, text="Erase from server")
        start_analysis = ttk.Button(self, text="Start Analysis")
        upload_button = ttk.Button(self, text='Select a file', command=self.Upload)
        file_display = ttk.Label(self, textvariable=self.file_selected)
        account_button = ttk.Button(self, text="Account details")

        # ----Grid----#
        services_select.grid(row=1, column=0, padx=5, pady=5)
        text.grid(row=0, column=0)
        delete_from_server.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        start_analysis.grid(row=0, column=1, columnspan=2, sticky="EW", padx=5, pady=5)
        upload_button.grid(row=2, column=0, sticky="W", padx=10, pady=10)
        file_display.grid(row=2, column=2, sticky="E", padx=5, pady=5)
        account_button.grid(row=3, column=0, columnspan=3)

        # ---Configuration---#

        text.config(font=("Segoe UI", 15))

    def Upload(self, event=None):
        try:
            filename = filedialog.askopenfile().name
            print('Selected:', filename)
            self.file_selected.set(f"{filename}")
        except ValueError:
            pass


class analysis(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        # ---Widgets---#

        progressionbar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        continue_button = ttk.Button(self, text="Continue")

        # ---Grid---#

        progressionbar.grid(row=1, column=2, columnspan=2, sticky='NSEW')
        continue_button.grid(row=2, column=2, columnspan=2)

        # ---Configuration---#

        progressionbar["maximum"] = 100
        progressionbar["value"] = 100


root = main()
font.nametofont("TkDefaultFont").configure(size=15)
root.columnconfigure(0, weight=1)
root.mainloop()
