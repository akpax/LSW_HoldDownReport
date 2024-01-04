from tkinter import Tk, Label, Button, filedialog

class FileSelectorGUI:
    def __init__(self):
        self.win = Tk()
        self.win.title("LSW Holdown Report - File Selector")

        self.input_file_path = None
        self.output_file_path = None

        Label(self.win, text="Select a LSW shearwall input file (.txt):",font=('Arial 13 bold')).grid(row=0, column=0,padx=30,pady=10)
        Button(self.win, text="Browse", command=self.select_input_file).grid(row=0, column=2, ipadx=10,ipady=3, padx=30)
        self.input_path_label = Label(self.win, text="")
        self.input_path_label.grid(row=0, column=1)

        Label(self.win, text="Select a LSW tension force output file (.pdf):", font=('Arial 13 bold')).grid(row=1, column=0,padx=30)
        Button(self.win, text="Browse", command=self.select_output_file).grid(row=1, column=2,ipadx=10,ipady=3, padx=30)
        self.output_path_label = Label(self.win, text="")
        self.output_path_label.grid(row=1, column=1)

        Button(self.win, text="Submit", command=self.win.destroy).grid(row=3, column=1, columnspan=2, ipadx=25,ipady=3, pady=25)

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
        return self.input_file_path, self.output_file_path

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
