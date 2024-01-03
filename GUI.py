# Import the required Libraries
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os


from tkinter import Tk, Label, Button, filedialog

class FileSelectorGUI:
    def __init__(self):
        self.win = Tk()
        self.win.title("File Selector")

        self.input_file_path = None
        self.output_file_path = None

        Label(self.win, text="Select a LSW input file (.txt):",font=('Arial 13 bold')).grid(row=0, column=0,padx=30,pady=10)
        Button(self.win, text="Browse", command=self.select_input_file).grid(row=0, column=2, ipadx=10,ipady=3, padx=30)
        self.input_path_label = Label(self.win, text="")
        self.input_path_label.grid(row=0, column=1)

        Label(self.win, text="Select a LSW output file (.pdf):", font=('Arial 13 bold')).grid(row=1, column=0,padx=30)
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

def create_file_selector():
    gui = FileSelectorGUI()
    return gui.run()


# # Set the geometry of tkinter frame
# # win.geometry("700x350")

# def get_input_file_path(win):
#    global LSW_input_file_path
#    file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
#    LSW_input_file_path = os.path.abspath(file.name)
#    Label(win, text= f'"{LSW_input_file_path}"', font=('Arial 13 italic')).grid(row=0,column=1, ipadx=50, ipady=10)
#    print(LSW_input_file_path)
#    return LSW_input_file_path

# def get_output_file_path(win):
#    global  LSW_output_file_path
#    file = filedialog.askopenfile(mode='r', filetypes=[('PDF Files', '*.pdf')])
#    LSW_output_file_path = os.path.abspath(file.name)
#    Label(win, text= f'"{LSW_output_file_path}"', font=('Arial 13 italic')).grid(row=1,column=1, ipadx=50, ipady=10)
#    print(LSW_output_file_path)
#    return LSW_output_file_path
      

# def close_window(win):
#    win.destroy()

# # Add a Label widget
# def create_input_files_window():
#     # Create an instance of tkinter frame
#     win = Tk()
#     win.title("LSW Holdown Report Generator")
#     Label(win, text="Please select LSW .txt input file:", font=('Arial 13 bold')).grid(row=0,column=0, ipadx=50, ipady=10)
#     ttk.Button(win, text="Browse", command= lambda: get_input_file_path(win)).grid(row=0, column=2)

#     Label(win, text="Please select LSW .pdf output file:", font=('Arial 13 bold')).grid(row=1,column=0, ipadx=50, ipady=10)
#     ttk.Button(win, text="Browse", command=lambda: get_output_file_path(win)).grid(row=1, column=2)

#     ttk.Button(win,text="Submit", command=lambda: close_window(win)).grid(row=2, column=0)
#     return win

def create_output_alert():
   win = Tk()
   win.title("LSW Holdown Report Generator")
   Label(win, text='Analysis Successfull!' ,font=('Arial 13 bold')).grid(row=0,padx=50,pady=10)
   Label(win, text='See "output.xlsx" for report ',font=('Arial 13')).grid(row=1,padx=50,pady=10)
   Button(win,text="Exit", command=win.destroy).grid(row=2)
   win.mainloop()
   return win


if __name__ == "__main__":
   create_file_selector()