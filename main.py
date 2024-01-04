from PyPDF2 import PdfReader
from icecream import ic
import re
import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
import openpyxl
from openpyxl.drawing.image import Image
from GUI import create_file_selector_window, create_output_alert_window
from datetime import datetime
import os
import sys



################### functions ############################
##### fucntions for reading pdf #####
def read_full_pdf(pdf_file_path: str):
    """
    Reads all pages of a pdf and returns contents as a string
    """
    # Open the PDF file
    with open(pdf_file_path, 'rb') as file:
        reader = PdfReader(file)
        # Initialize an empty string to hold all text
        full_text = ""
        # Iterate over all the pages
        for page_num in range(0,len(reader.pages)):
            # Extract text from the page
            page = reader.pages[page_num]
            text = page.extract_text()
            # Add the text to the full text
            full_text += text
        return full_text

def extract_lateral_load_cases(text: str):
    """
    Uses regex to find lateral load cases in a string and returns them as a list
    """
    pattern = r"Lateral Load = (.*?)'"
    lateral_load_cases = re.findall(pattern, text)
    return [load_case.replace(" ","") for load_case in lateral_load_cases]

def find_sections(text: str):
    """
    Uses break text to divide long string into sections and returns sections as list
    Sections are checked to see if they contain entries which is row in our pdf table
    """
    # Splitting the text at each occurrence of the break text
    break_text = "Handle"
    sections = re.split(break_text, text)
    sections_w_entries = [section for section in sections if check_for_entries(section)]
    return sections_w_entries

def extract_entries_from_section(text: str):
    """
    Uses regex to find entries (row of data in pdf text) in text and returns each row as list of tuples
    """
    pattern = r"(\d+) (SW\d+) ([a-zA-Z]+\d+-?[a-zA-Z]*) (\d+\*?) (T[\w_]*\d+) (\d{1,3}(?:,\d{3})* [a-zA-Z]+) (T[\w_]*\d+) (\d{1,3}(?:,\d{3})* [a-zA-Z]+)"
    lines = re.findall(pattern, text) # finds all cpatures groups and creates list of tuples
    return lines


def check_for_entries(text: str) -> bool:
    """
    Uses regex to check for entry (row of data) and returns boolean
    """
    pattern = r"(\d+) (SW\d+) ([a-zA-Z]+\d+-?[a-zA-Z]*) (\d+\*?) (T[\w_]*\d+) (\d{1,3}(?:,\d{3})* [a-zA-Z]+) (T[\w_]*\d+) (\d{1,3}(?:,\d{3})* [a-zA-Z]+)"
    return bool(re.search(pattern,text))

def ensure_df_in_list_same_length(df_list: list):
    """
    Checks that each dataframe in list is the same length
    """
    assert all([len(df)==len(df_list[0]) for df in df_list])


##### functions for manipulating dataframes #####
def convert_coord_pair_to_float(coord):
    """
    Takes string in following format: [1234.2, -134] and returns each number as a float 1234.1, -134"""
    if not type(coord) == str:
        coord = coord.str
    coord = coord.strip()
    coord = coord.strip("[]")
    x,y = coord.split(",")
    x = float(x)
    y = float(y)
    return x,y

def remove_comma_convert_to_float(x):
    """
    Takes a string with expected format "12,3423 lb" and converts number to float
    """
    number,unit = x.split(" ")  # TO DO create fucntion that takes unti and appends to column title
    number = number.replace(",","")
    number = float(number)
    return number

def label_close_points_with_dbscan(df, coord_cols: list, out_label="label", eps=3):
    """
    Use sklearn DBSCAN alogrithm to create a label column from x,y coordiante colummns
    
    Inputs:
    df (pandas.DataFrame): dataframe contianing coord columns
    coord_cols (list): name of columns containing coordinates
    out_label (str): name for new label column
    eps (int): DBSCAN algorithm paramter; maximum distance between two samples for one to be considered
          as in the neighborhood of the other. 
    """
    X = df[coord_cols].values
    clustering = DBSCAN(eps=eps, min_samples=2).fit(X)
    df[out_label] = clustering.labels_
    return df

def create_location_key(label_l, label_r):
    """
    Applied to a datframe via lambda fucntion; 
    Combines two strings with an "_"
    """
    return f"{str(label_l)}_{str(label_r)}"

def extract_level(diaphragm_label):
    """
    Extract digits from diaphragm string and returns them as integer
    """
    assert isinstance(diaphragm_label,str)
    digit_list = [character for character in diaphragm_label if character.isdigit()]
    level = "".join([digit for digit in digit_list])
    return int(level)

def find_delta_forces(frame, force_cols: list):
    """
    This function is intended to be applied to each dataframe that is grouped by load case and shear wall.
    It returns the elta force between the wall at current level and the wall above it.
    The top wall returns Nan (no wall above it) and it is given its on force value as the delta force
    """
    # Sort the group if needed
    frame = frame.sort_values("level")
    # Calculate the difference between consecutive rows for 'left_tension_float'
    for force_col in force_cols:
        frame[f"delta_{force_col}"] = frame[force_col] - frame[force_col].shift(-1)
        frame[f"delta_{force_col}"] = frame[f"delta_{force_col}"].fillna(frame[force_col])
    return frame



##### Output Related Functions #####
def append_date_and_time(prefix):
    """
    Appends current date to the prefix string
    """
    date = datetime.now()
    formated_date = date.strftime("%m-%d-%Y")
    return f"{prefix}_{formated_date}"

# create folder for report using current date and time
def create_output_folder_path(name):
    """
    Finds CWD and returns output folder path inside desktop dir
    """
    # date = datetime.now()
    # formated_date = date.strftime("%d-%m-%Y_%H:%M:%S")
    output_folder_name = append_date_and_time(name)
    current_folder = os.getcwd() # get Home directory
    output_folder_path = os.path.join(current_folder, output_folder_name)
    return output_folder_path

def resource_path(relative_path):
    """ 
    Get absolute path to resource, works for dev and for PyInstaller 
    Note: sys._MEIPASS is a temporary folder for PyInstaller, necessary to load images folder into bundled app
    """
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


####################### Key variables #####################################
eps = 2
logo_path = resource_path(r"images/MSD Full Logo.jpg")

LSW_input_file_path, LSW_output_file_path = create_file_selector_window()


# # ############### Read output pdf and store as DF #################
output_text = read_full_pdf(LSW_output_file_path)

##### parse output file to output dict in folowing format {load_case: [entry: tuple]} #####
load_cases = extract_lateral_load_cases(output_text)
sections = find_sections(output_text)
output_dict = {}

assert len(sections) == len(load_cases) # if assertion fails, there was an error readig the output_pdf
# extract entries from section and pair entries with assocaited laod case in output_dict
for i,section in enumerate(sections):
    lines = extract_entries_from_section(section)
    if not load_cases[i] in output_dict.keys():
        output_dict[load_cases[i]] = []
        print(f"added {load_cases[i]} to ouput dict")
    output_dict[load_cases[i]].extend(lines)

output_cols = [
    'handle',
    'name',
    'diaphragm',
    'shearwall_type',
    'LHD',
    'left_tension',
    'RHD',
    'right_tension',
    'load_case'
]

output_dfs = []

# add load case to each tuple entry from extraction and create dataframe for each load case
for load_case, entries in output_dict.items():
    entries_w_load_case = [entry + (load_case,) for entry in entries ]
    df = pd.DataFrame(entries_w_load_case, columns=output_cols)
    output_dfs.append(df)


ensure_df_in_list_same_length(output_dfs)  #after creating datframes, each load case df should have same length
output_df = pd.concat(output_dfs, ignore_index=True)
output_raw_df = output_df #save raw output for report later

output_df["left_tension"] = output_df.apply(lambda row: remove_comma_convert_to_float(row["left_tension"]), axis=1)
output_df["right_tension"] = output_df.apply(lambda row: remove_comma_convert_to_float(row["right_tension"]), axis=1)

############### Read Input Text and Store as Df ###################
input_cols = [
    "handle",
    "diaphragm",
    "name",
    "shearwall_type",
    "left_location",
    "right_location",
    "LHD",
    "RHD"
]

input_df = pd.read_table(LSW_input_file_path, header=None)
input_df = input_df.iloc[:,:-1] # drops last column which is filled with Nan values
input_df.columns = input_cols
input_raw_df = input_df # save initial input_df for logging purposes

############## create location keys for input df to determine stacked shear walls
# remove only keep necessary columns for input_df for merge
input_df = input_df[["handle","left_location", "right_location", "diaphragm"]]

input_df[["x_left","y_left"]] = input_df.apply(lambda row: convert_coord_pair_to_float(row["left_location"]), axis=1, result_type="expand")
input_df[["x_right","y_right"]] = input_df.apply(lambda row: convert_coord_pair_to_float(row["right_location"]), axis=1, result_type="expand")

print(input_df)
input_df = label_close_points_with_dbscan(input_df, ['x_left','y_left'], out_label="label_l",eps=2) #create unqiue lable for similar left coord
input_df = label_close_points_with_dbscan(input_df, ['x_right','y_right'], out_label="label_r",eps=2) #create unqiue lable for similar right coord

input_df["location_key"] = input_df.apply(lambda row: create_location_key(row["label_l"], row["label_r"]), axis=1)

grouped_sw_df = input_df.groupby("location_key", as_index=False)

# bad_walls = 0
# #check that allsw w same location tag are four levels
# for shearwall,frame in grouped_sw_df:
#     if not len(frame) == 4:
#         bad_walls+=1
#         # print("_____________________________________________________________________________")
#         # print(f"Shearwall: {shearwall}")
#         # # print(frame.head())
#         # print(frame[['handle','x_left','xl_label','y_left','yl_label','x_right','xr_label','y_right','yr_label']])
#         # print("_____________________________________________________________________________")
    
# print(f"bad walls{ bad_walls}")


input_df["level"] = input_df.apply(lambda row: extract_level(row["diaphragm"]), axis=1)


########################### Merge Coordinate Keys to Output df
output_df["handle"] = output_df["handle"].astype("str")  # convert from numpy to string for merge
input_df["handle"] = input_df["handle"].astype("str")  # convert from numpy to string for merge
df = pd.merge(output_df, input_df, on="handle", how="left")


########################### group by load case and shear wall and find delta forces for each side
grouped_df = df.groupby(["load_case","location_key"])#.sort_values("level")

delta_df = grouped_df.apply(find_delta_forces, force_cols=["left_tension","right_tension"])

delta_df = delta_df.reset_index(drop=True) # convert multi-index back to cols

##### Group by 'handle' and calculate the max delta force for each holdown in shearwall #####
delta_grouped_df = delta_df.groupby("handle")

#obtain index of maximum values for left and right HD
delta_left_max_index = delta_grouped_df["delta_left_tension"].idxmax() 
delta_right_max_index = delta_grouped_df["delta_right_tension"].idxmax()

# filter for max delta vlaue based on index and pull releveant columns for output report
walls_max_delta_left_df = delta_df.loc[delta_left_max_index][["handle","name","delta_left_tension","LHD","load_case","left_location"]]
walls_max_delta_left_df.rename(columns={"load_case": "load_case_left"},inplace=True)
walls_max_delta_right_df = delta_df.loc[delta_right_max_index][["handle","delta_right_tension","RHD","load_case","right_location", "location_key", "level"]]
walls_max_delta_right_df.rename(columns={"load_case": "load_case_right"},inplace=True)

assert(len(walls_max_delta_left_df)==len(walls_max_delta_right_df)) #dfs should be same length
walls_max_delta_df = walls_max_delta_left_df.merge(walls_max_delta_right_df,how="outer", on="handle") 


# groupy by location key and sort by level for output report clarity
walls_max_delta_df = walls_max_delta_df.groupby("location_key",as_index=False).apply(lambda frame: frame.sort_values("level"))
walls_max_delta_df.drop(columns="location_key",inplace=True)


############################################## create tiedown schedule
# holdowns are not always same on left and right side for each hshearwall
# stack the holddown type and tension force for left and rght shearwalls
LHD_df = walls_max_delta_df[["LHD","delta_left_tension"]]
LHD_df.rename(columns={"LHD": "HD_type", "delta_left_tension": "tension"},inplace=True)
RHD_df = walls_max_delta_df[["RHD","delta_right_tension"]]
RHD_df.rename(columns={"RHD": "HD_type", "delta_right_tension": "tension"}, inplace=True)
HD_df = pd.concat([LHD_df,RHD_df],axis=0, ignore_index=True) # concatenat along rows

HD_max_df = HD_df.groupby("HD_type", as_index=False).max("tension").sort_values("tension",ascending=False) 


# ##################### Output Important dfs to different sheets in output.xlsx #######################
# create output folder path in CWD
output_folder_path = create_output_folder_path("LSW_HoldownReport")
print(f"- Output Folder: {output_folder_path}")
#create folder for output
if not os.path.exists(output_folder_path): 
    os.makedirs(output_folder_path)
    print(" * Output Folder created *")

xlsx_output_path = os.path.join(output_folder_path, "output.xlsx")

with pd.ExcelWriter(xlsx_output_path) as writer:
    HD_max_df.to_excel(writer, sheet_name="Holdown Summary", index=False, startrow=15) #leave room for MAR logo
    walls_max_delta_df.to_excel(writer, sheet_name='Wall Info', index=False, startrow=15) #leave room for MAR logo
    output_raw_df.to_excel(writer, sheet_name='LSW output data', index=False)
    input_raw_df.to_excel(writer, sheet_name='LSW input data', index=False)
    
 
######################### add mar logo to holdown summary, Wall info
wb = openpyxl.load_workbook(xlsx_output_path)
ws1 = wb["Holdown Summary"]
ws2 = wb["Wall Info"]
ws1.add_image(Image(logo_path), "A1")
ws2.add_image(Image(logo_path), "A1")
wb.save(xlsx_output_path)

#### display success message
create_output_alert_window(output_folder_path)



 