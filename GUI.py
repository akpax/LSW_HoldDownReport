# Import the required Libraries
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os



# Set the geometry of tkinter frame
# win.geometry("700x350")

def get_file_path(file_type: str):
   global input_file_path, output_file_path
   if file_type == "input":
      file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
      input_file_path = os.path.abspath(file.name)
      print(input_file_path)
   elif file_type == "output":
      file = filedialog.askopenfile(mode='r', filetypes=[('PDF Files', '*.pdf')])
      output_file_path = os.path.abspath(file.name)
      print(output_file_path)
      

def close_window(win):
   win.destroy()

# Add a Label widget
def create_input_files_window():
    # Create an instance of tkinter frame
    win = Tk()
    win.title("LSW Holdown Report Generator")
    Label(win, text="Please select LSW .txt input file:", font=('Arial 13')).grid(row=0,column=0, ipadx=50, ipady=10)
    ttk.Button(win, text="Browse", command=lambda: get_file_path("input")).grid(row=0, column=1)

    Label(win, text="Please select LSW .pdf output file:", font=('Arial 13')).grid(row=1,column=0, ipadx=50, ipady=10)
    ttk.Button(win, text="Browse", command=lambda: get_file_path("output")).grid(row=1, column=1)

    ttk.Button(win,text="Submit", command=lambda: close_window(win)).grid(row=2, column=0)
    return win

if __name__ == "__main__":
   win = create_input_files_window()
   win.mainloop()