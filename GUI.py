from tkinter import Tk, Label, Button, filedialog, Entry, StringVar
from datetime import datetime

class FileSelectorGUI:
    def __init__(self):
        self.win = Tk()
        self.win.title("LSW Holdown Report - File Selector")

        self.input_file_path = None
        self.output_file_path = None

        #job info
        self.lsw_model_version = StringVar()
        self.project = StringVar()
        self.job_num = StringVar()
        self.author = StringVar()

        # label and selection for input file
        Label(self.win, text="Select a LSW shearwall input file (.txt):",font=('Arial 13 bold')).grid(row=0, column=0,padx=30,pady=10, sticky="w")
        Button(self.win, text="Browse", command=self.select_input_file).grid(row=0, column=2, ipadx=10,ipady=3, padx=30)
        self.input_path_label = Label(self.win, text="")
        self.input_path_label.grid(row=0, column=1)

        # label and selection for output file
        Label(self.win, text="Select a LSW tension force output file (.pdf):", font=('Arial 13 bold')).grid(row=1, column=0,padx=30, sticky="w")
        Button(self.win, text="Browse", command=self.select_output_file).grid(row=1, column=2,ipadx=10,ipady=3, padx=30)
        self.output_path_label = Label(self.win, text="")
        self.output_path_label.grid(row=1, column=1)

        Label(self.win, text="Please Enter Header Info:", font=('Arial 13 bold')).grid(row=2, column=0,padx=30)
        Label(self.win, text="LSW Model Version:", font=('Arial 13 ')).grid(row=3, column=0,padx=30, sticky="e")
        Entry(self.win, textvariable=self.lsw_model_version).grid(row=3, column=1,padx=30)
        Label(self.win, text="Project:", font=('Arial 13 ')).grid(row=4, column=0,padx=30, sticky="e")
        Entry(self.win, textvariable=self.project).grid(row=4, column=1,padx=30)
        Label(self.win, text="Job Number:", font=('Arial 13 ')).grid(row=5, column=0,padx=30, sticky="e")
        Entry(self.win, textvariable=self.job_num).grid(row=5, column=1,padx=30)
        Label(self.win, text="Your Name:", font=('Arial 13 ')).grid(row=6, column=0,padx=30, sticky="e")
        Entry(self.win, textvariable=self.author).grid(row=6, column=1,padx=30)

        Button(self.win, text="Submit", command=self.win.destroy).grid(row=8, column=1, columnspan=2, ipadx=25,ipady=3, pady=25)

    def select_input_file(self):
        file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
        if file:
            self.input_file_path = file.name
            self.input_path_label.config(text= f'"{self.input_file_path}"', font=('Arial 10 italic'))
            

    def select_output_file(self):
        file = filedialog.askopenfile(mode='r', filetypes=[('PDF Files', '*.pdf')])
        if file:
            self.output_file_path = file.name
            self.output_path_label.config(text= f'"{self.output_file_path}"', font=('Arial 10 italic'))


    def run(self):
        self.win.mainloop()
        job_info = {
        'Project:': str(self.project.get()),
        'Job No.:': str(self.job_num.get()),
        'Date:': str(datetime.now().strftime("%m-%d-%Y")),
        'By': str(self.author.get())
    }
        return self.input_file_path, self.output_file_path, self.lsw_model_version.get(), job_info

def create_file_selector_window():
    gui = FileSelectorGUI()
    return gui.run()




def create_output_alert_window(output_file_folder):
   win = Tk()
   win.title("LSW Holdown Report Generator - Success")
   Label(win, text='Analysis Successfull!' ,font=('Arial 13 bold')).grid(row=0,padx=50,pady=10)
   Label(win, text=f'See "{output_file_folder}" for report ',font=('Arial 13')).grid(row=1,padx=50,pady=10)
   Button(win,text="Exit", command=win.destroy).grid(row=2)
   win.mainloop()
   return win



if __name__ == "__main__":
    create_file_selector_window()
