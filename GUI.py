# Import the required Libraries
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os



# Set the geometry of tkinter frame
# win.geometry("700x350")

def get_input_file_path(win):
   global input_file_path
   file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
   input_file_path = os.path.abspath(file.name)
   Label(win, text= f'"{input_file_path}"', font=('Arial 13 italic')).grid(row=0,column=1, ipadx=50, ipady=10)
   print(input_file_path)

def get_output_file_path(win):
   global  output_file_path
   file = filedialog.askopenfile(mode='r', filetypes=[('PDF Files', '*.pdf')])
   output_file_path = os.path.abspath(file.name)
   Label(win, text= f'"{output_file_path}"', font=('Arial 13 italic')).grid(row=1,column=1, ipadx=50, ipady=10)
   print(output_file_path)
      

def close_window(win):
   win.destroy()

# Add a Label widget
def create_input_files_window():
    # Create an instance of tkinter frame
    win = Tk()
    win.title("LSW Holdown Report Generator")
    Label(win, text="Please select LSW .txt input file:", font=('Arial 13 bold')).grid(row=0,column=0, ipadx=50, ipady=10)
    ttk.Button(win, text="Browse", command= lambda: get_input_file_path(win)).grid(row=0, column=2)

    Label(win, text="Please select LSW .pdf output file:", font=('Arial 13 bold')).grid(row=1,column=0, ipadx=50, ipady=10)
    ttk.Button(win, text="Browse", command=lambda: get_output_file_path(win)).grid(row=1, column=2)

    ttk.Button(win,text="Submit", command=lambda: close_window(win)).grid(row=2, column=0)
    return win

def create_output_alert_window():
   win = Tk()
   win.title("LSW Holdown Report Generator")
   Label(win, text='Analysis Successfull!' ,font=('Arial 13 bold')).grid(row=0,padx=50,pady=10)
   Label(win, text='See "output.xlsx" for report ',font=('Arial 13')).grid(row=1,padx=50,pady=10)
   Button(win,text="Exit", command=lambda:close_window(win)).grid(row=2)
   return win


if __name__ == "__main__":
   win = create_input_files_window()
   win.mainloop()