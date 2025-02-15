import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.ttk import Treeview
from pathlib import Path
import IBM_STT
from tkinter import messagebox
from tkinter import *
import csv
from PIL import ImageTk, Image
from tkinter import filedialog
import pandas as pd
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

OptionList = ['', "IBM", "Microsoft"]

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # self.resizable(False, False)

        #self.geometry("600x300")
        self.title("Transcription service")
        self.title_font = tkfont.Font(family='Helvetica', size=15, weight="bold")


        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (loginpage, homepage, analysing, analysis, results, account_details):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("loginpage")

    
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class loginpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        frame = ttk.Frame(self)

        #---Widgets---#
        welcome = ttk.Label(frame, text="Welcome")
        username = ttk.Label(frame, text="Username", anchor="center")
        passwd = ttk.Label(frame, text="Password", anchor="center")
        username_input = ttk.Entry(frame)
        passwd_input = ttk.Entry(frame)
        login = ttk.Button(frame, text="Login", command=lambda: controller.show_frame("homepage"))

        #---Grid--#
        frame.pack()
        welcome.pack()
        username.pack()
        username_input.pack()
        passwd.pack()
        passwd_input.pack()
        login.pack()


class homepage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        frame = ttk.Frame(self)

        # -----Variables---#

        services = tk.StringVar(self)
        services.set(OptionList[0])
        self.file_selected = tk.StringVar(value="No file selected...")

        # ----Widgets-----#

        services = StringVar(frame)
        services.set("IBM")
        text = ttk.Label(frame, text="Choose a service", padding=10)
        services_select = ttk.OptionMenu(frame, services, *OptionList)
        delete_from_server = tk.Checkbutton(frame, text="Erase from server")
        start_analysis = ttk.Button(frame, text="Start Analysis", command=lambda: startAnalysis(self, self.file_selected, services.get()), padding=10)
        upload_button = ttk.Button(frame, text='Select a file...', command=self.Upload, padding=10)
        file_display = ttk.Label(frame, textvariable=self.file_selected)
        account_button = ttk.Button(frame, text="Account details", command=lambda: controller.show_frame("account_details"), padding=10)

        # ----Grid----#
        frame.grid(sticky="NSEW")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        services_select.grid(row=1, column=0, padx=20, pady=20)
        text.grid(row=0, column=0,padx=20,pady=5, sticky="NSEW")
        delete_from_server.grid(row=1, column=3, padx=30, pady=30, sticky="NSEW")
        start_analysis.grid(row=0, column=3, sticky="NSEW", padx=0, pady=0)
        upload_button.grid(row=2, column=0, sticky="NSEW", padx=5, pady=5)
        file_display.grid(row=2, column=2, sticky="W")
        account_button.grid(row=3, column=0, columnspan=2,padx=30,pady=20, sticky="NSEW")
        #username.grid(row=2, column=3)
        #password.grid(row=3, column=3)

        # ---Configuration---#

        text.config(font=("Segoe UI", 15))

        def startAnalysis(self, file, service):
            if file.get() != "No file selected...":
                controller.show_frame("analysing")
                if service == "IBM":
                    IBM_STT.IBM_STT(str(Path(file.get())))
                    controller.show_frame("analysis")
                elif service == "Microsoft":
                    tk.messagebox.showinfo(title="Info", message="We are still working on this service.")
                else:
                    tk.messagebox.showinfo(title="Missing service", message="No chosen service")
                    return controller.show_frame("analysis")
            else:
                tk.messagebox.showerror(title="Missing file", message="No file to transcribe.")
    
    def Upload(self, event=None):
        try:
            filename = filedialog.askopenfile().name
            print('Selected:', Path(filename).name)
            self.file_selected.set(Path(filename).name)

        except ValueError:
            tk.messagebox.showerror(title="Uh oh", message="Upload failed.")

class analysing(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        frame = ttk.Frame(self)

        # --- Widgets ---#
        text = ttk.Label(frame, text="Analysing, this might take a minute or two.")
        progressionbar = ttk.Progressbar(frame, orient="horizontal", value = 0 ,length=200, mode="determinate")


        #--Grid--#

        text.pack()
        progressionbar.pack()
        frame.pack()


class analysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        frame = ttk.Frame(self)


        # ---Widgets---#
        text = ttk.Label(frame, text="Analysis Completed!")
        progressionbar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
        continue_button = tk.Button(frame, text="Continue",command=lambda: controller.show_frame("results"))

        # ---Grid---#
        text.grid(row=0,column=3)
        progressionbar.grid(row=1, column=3, columnspan=1,padx=200,pady=100, sticky='NSEW')
        continue_button.grid(row=2, column=2, columnspan=2)
        frame.grid(sticky="NSEW")


        # ---Configuration---#

        progressionbar["maximum"] = 100
        progressionbar["value"] = 100




class results(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        frame = ttk.Frame(self)
        df = pd.read_csv('data.csv')
        

        #---Widgets---#
        self.createtable()
        self.filletable(df)
        delete_file = tk.Button(frame, text="Delete file", padx=5, pady=5)
        save_as = tk.Button(frame, text="Save as...", padx=5, pady=5)
        analyse = tk.Button(frame, text="Analyse", padx=5, pady=5)
        return_to_home = tk.Button(frame, text="Return to home", command=lambda: controller.show_frame("homepage"), padx=5, pady=5)

        #---Grid---#
        self.grid(sticky="NSEW")
        frame.grid(sticky="NSEW",)
        delete_file.grid(row=0,column=6,columnspan=2)
        save_as.grid(row=0, column=4, columnspan=2)
        analyse.grid(row=0, column=2, columnspan=2)
        return_to_home.grid(row=0, column=8, columnspan=2)
        

        #---Configuration--#
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def createtable(self):
        tv = Treeview(self)
        tv['columns'] = ('timefrom', 'timeto', 'Gap', 'Speaker', 'Confidence')
        tv.heading("#0", text='', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('timefrom', text='Time From')
        tv.column('timefrom', anchor='center', width=100)
        tv.heading('timeto', text='Time To')
        tv.column('timeto', anchor='center', width=100)
        tv.heading('Speaker', text='Speaker')
        tv.column('Speaker', anchor='center', width=100)
        tv.heading('Gap', text='Gap between speakers')
        tv.column('Gap', anchor='center', width=100)
        tv.heading('Confidence', text='Confidence')
        tv.column('Confidence', anchor='center', width=100)
        self.treeview = tv
        tv.grid(sticky="NSWE")


    def filletable(self, df):
        i = 0
        lengths = df.shape
        while(i < lengths[0]):
            self.treeview.insert('', 'end', text=i, values=(df['TimeFrom'][i], df['TimeTo'][i], df['Speaker'][i], df['Gap between speakers'][i], df['Confidence'][i]))
            i += 1

class account_details(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        frame = ttk.Frame(self)

        frame.pack()
        label = ttk.Label(frame, text="Account details, work in progress")
        return_button = ttk.Button(frame, text="Return to home", command= lambda: controller.show_frame("homepage"))
        label.pack()
        return_button.pack()



if __name__ == "__main__":
    root = main()
    root.resizable()
    root.mainloop()
