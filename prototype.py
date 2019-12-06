import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.ttk import Treeview

from PIL import ImageTk, Image
from tkinter import filedialog
import pandas as pd
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

OptionList = ["IBM", "Microsoft"]


class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # self.resizable(False, False)

        self.geometry("600x300")
        self.title("Transcription service")
        self.title_font = tkfont.Font(family='Helvetica', size=15, weight="bold")


        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (homepage, analysis, results):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("homepage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class homepage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # -----Variables---#

        services = tk.StringVar(self)
        services.set(OptionList[0])
        self.file_selected = tk.StringVar(value="No file selected...")

        # ----Widgets-----#

        text = ttk.Label(self, text="Choose a service", padding=10)
        services_select = ttk.OptionMenu(self, services, *OptionList)
        delete_from_server = tk.Checkbutton(self, text="Erase from server")
        start_analysis = ttk.Button(self, text="Start Analysis", command=lambda: controller.show_frame("analysis"), padding=10)
        upload_button = ttk.Button(self, text='Select a file...', command=self.Upload, padding=10)
        file_display = ttk.Label(self, textvariable=self.file_selected)
        account_button = ttk.Button(self, text="Account details", padding=10)

        # ----Grid----#
        services_select.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")
        text.grid(row=0, column=0,padx=20,pady=5, sticky="NSEW")
        delete_from_server.grid(row=1, column=3, columnspan=1, padx=30, pady=30, sticky="NSEW")
        start_analysis.grid(row=0, column=3, columnspan=1, sticky="NSEW", padx=0, pady=0)
        upload_button.grid(row=2, column=0, sticky="NSEW", padx=5, pady=5)
        file_display.grid(row=2, column=2, sticky="NSEW", padx=50, pady=20)
        account_button.grid(row=3, column=1, columnspan=2,padx=30,pady=20, sticky="NSEW")

        # ---Configuration---#

        text.config(font=("Segoe UI", 15))

    def Upload(self, event=None):
        try:
            filename = filedialog.askopenfile().name
            print('Selected:', filename)
            self.file_selected.set(filename)
        except ValueError:
            pass


class analysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # ---Widgets---#

        progressionbar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        continue_button = tk.Button(self, text="Continue",command=lambda: controller.show_frame("results"))

        # ---Grid---#

        progressionbar.grid(row=1, column=3, columnspan=1,padx=200,pady=100, sticky='NSEW')
        continue_button.grid(row=2, column=2, columnspan=2)

        # ---Configuration---#

        progressionbar["maximum"] = 100
        progressionbar["value"] = 100


class results(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        df = pd.read_csv(r'/Users/alighariani/Documents/UCL/2nd/Systems engineering/Python prototype/data.csv')
        print(df)
        self.createtable()
        self.filletable(df)
        delete_file = tk.Button(self, text="Delete file")
        save_as = tk.Button(self, text="Save as...")
        analyse = tk.Button(self, text="Analyse")
        return_to_home = tk.Button(self, text="Return to home", command=lambda: controller.show_frame("homepage"))
        delete_file.grid(row=1,column=0)
        save_as.grid(row=2)
        analyse.grid()
        return_to_home.grid()
        self.grid(sticky="NSEW")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        # text = ttk.Label(self, text="test")
        # text.pack()
    def createtable(self):
        tv = Treeview(self)
        tv['columns'] = ('timefrom', 'timeto', 'timebetween', 'membertalking')
        tv.heading("#0", text='', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('timefrom', text='Time From')
        tv.column('timefrom', anchor='center', width=100)
        tv.heading('timeto', text='Time To')
        tv.column('timeto', anchor='center', width=100)
        tv.heading('timebetween', text='Time Between')
        tv.column('timebetween', anchor='center', width=100)
        tv.heading('membertalking', text='Member Talking')
        tv.column('membertalking', anchor='center', width=100)
        self.treeview = tv
        tv.grid(sticky="NSWE")
    def filletable(self, df):
        i = 0
        while(i < 8):
            self.treeview.insert('', 'end', text=i, values=(df['Time From'][i], df['Time To'][i], df['Time Between'][i], df['Member talking'][i]))
            i += 1




if __name__ == "__main__":
    root = main()
    root.resizable(width=False, height=False)
    root.mainloop()

