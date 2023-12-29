from PyPDF2 import PdfReader
from icecream import ic
import re
import pandas as pd
import math
from sklearn.cluster import DBSCAN
import numpy as np




def read_full_pdf(file_path):
    # Open the PDF file
    with open(file_path, 'rb') as file:
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

def extract_lateral_load_cases(text):
    # Regular expression to find all lateral load cases
    pattern = r"Lateral Load = (.*?)'"
    lateral_load_cases = re.findall(pattern, text)
    return [load_case.replace(" ","") for load_case in lateral_load_cases]

def find_sections(text):
    # Splitting the text at each occurrence of the break text
    break_text = "Handle"
    sections = re.split(break_text, text)
    sections_w_entries = [section for section in sections if check_for_entries(section)]
    return sections_w_entries

def extract_entries_from_section(text):
    pattern = r"(\d+) (SW\d+) ([a-zA-Z]+\d+-?[a-zA-Z]*) (\d+\*?) (T[\w_]*\d+) (\d{1,3}(?:,\d{3})* [a-zA-Z]+) (T[\w_]*\d+) (\d{1,3}(?:,\d{3})* [a-zA-Z]+)"
    lines = re.findall(pattern, text) # finds all cpatures groups and creates list of tuples
    return lines

def extract_entries_from_input(text):
    #pattern = r"(\d+) (D\d+) (SW\d+) (\d+) (-?\d+\.?\d*\s+[a-zA-Z]+,\s*-?\d+\.?\d*\s+[a-zA-Z]+) (-?\d+\.?\d*\s+[a-zA-Z]+,\s*-?\d+\s*\d*\.?\d*\s+[a-zA-Z]+) (T[\w_]*\d+) (T[\w_]*\d+) "
    #pattern = r"(\d+)\s+([a-zA-Z]+\d+-?[a-zA-Z]*)\s+(SW\d+)\s+(\d+)\s+(-?\d+\.?\d*\s+[a-zA-Z]+,-?\s*(?:-?\d+\.?\d*)?\s*[a-zA-Z]*\s*)\s*(-?\d+\.?\d*\s+[a-zA-Z]+,-?\s*(?:-?\d+\.?\d*)?\s*[a-zA-Z]*\s*)\s+(T[\w_]*\d+)\s+(T[\w_]*\d+)"
    pattern = "(\d+)\s+([a-zA-Z]+\d+-?[a-zA-Z]*)\s+(SW\d+)\s+(\d+)\s+\[([-\d.]+),\s+([-\d.]+)\]\s+\[([-\d.]+),\s+([-\d.]+)\]\s+([A-Za-z]\d+[A-Za-z]?)_([A-Za-z]\d+)\s+([A-Za-z]\d+[A-Za-z]?)_([A-Za-z]\d+)"

    lines = re.findall(pattern, text) # finds all cpatures groups and creates list of tuples
    return lines

def check_for_entries(text: str) -> bool:
    pattern = r"(\d+) (SW\d+) ([a-zA-Z]+\d+-?[a-zA-Z]*) (\d+\*?) (T[\w_]*\d+) (\d{1,3}(?:,\d{3})* [a-zA-Z]+) (T[\w_]*\d+) (\d{1,3}(?:,\d{3})* [a-zA-Z]+)"
    return bool(re.search(pattern,text))


# def label_close_points(df, handle_column, coord_col, out_label="label",tolerance=3):
#     # use 3" for any model per Tamara
#     # Sort the DataFrame based on x-coordinates
#     sorted_df = df.sort_values(by=coord_col)
#     # Initialize label and a list to store the labels
#     label = 0
#     labels = [None] * len(sorted_df)
#     # Iterate through the DataFrame rows
#     for i in range(len(sorted_df)):
#         if labels[i] is not None:
#             continue

#         labels[i] = label
#         current_x = sorted_df.iloc[i][coord_col]

#         # Check the next points in the sorted DataFrame
#         for j in range(i+1, len(sorted_df)):
#             if math.isclose(current_x, sorted_df.iloc[j][coord_col], abs_tol=tolerance):
#                 if labels[j] is None:
#                     labels[j] = label
#                     print(f"l: {j} || Current x: {current_x} || Next x: {sorted_df.iloc[j][coord_col]}")
#             else:
#                 print(f"Breaking at {j}: Current x = {current_x}, Next x = {sorted_df.iloc[j][coord_col]}, Label = {label}")
#                 print("__________________________________________________________________")
#                 break
#         label += 1

#     # Map the labels back to the original DataFrame order
#     sorted_df[out_label] = labels
#     return df.merge(sorted_df[[out_label]], left_index=True, right_index=True, how='left')

def convert_coord_pair_to_float(coord):
    if not type(coord) == str:
        coord = coord.str
    coord = coord.strip()
    coord = coord.strip("[]")
    x,y = coord.split(",")
    x = float(x)
    y = float(y)
    return x,y

def label_close_points_with_dbscan(df, handle_column, coord_cols: list, out_label="label", eps=3):
    X = df[coord_cols].values
    clustering = DBSCAN(eps=eps, min_samples=2).fit(X)
    df[out_label] = clustering.labels_
    return df

def create_location_key(label_l, label_r):
    return f"{str(label_l)}_{str(label_r)}"

####################### Key variables #####################################
output_file_path = "test_files/Thornton SW Output.pdf"
input_file_path = "test_files/Thornton Input.txt"
eps = 2


# # ############### Read output pdf and store as DF #################
output_text = read_full_pdf(output_file_path)
print(output_text)
### read output file
load_cases = extract_lateral_load_cases(output_text)
print(load_cases)
sections = find_sections(output_text)
print(extract_entries_from_section("2638 SW122 L5-E 22 T7_x6 0 lbs T7_x6 0 lbs "))
output_dict = {}
# create output dict in folowing format {laod_case: [entry as tuple]}
print(f"Length Sections: {len(sections)}")
print(f"Length load cases: {len(load_cases)}")
assert len(sections) == len(load_cases)
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

for load_case, entries in output_dict.items():
    entries_w_load_case = [entry + (load_case,) for entry in entries ]
    df = pd.DataFrame(entries_w_load_case, columns=output_cols)
    output_dfs.append(df)


# key output_dfs are same length befoe combining
for df in output_dfs:
    print(len(df))
output_df = pd.concat(output_dfs, ignore_index=True)

def remove_comma_convert_to_float(x):
    number,unit = x.split(" ")  # TO DO create fucntion that takes unti and appends to column title
    number = number.replace(",","")
    number = float(number)
    return number

output_df["left_tension"] = output_df.apply(lambda row: remove_comma_convert_to_float(row["left_tension"]), axis=1)
output_df["right_tension"] = output_df.apply(lambda row: remove_comma_convert_to_float(row["right_tension"]), axis=1)

print(output_df)
# breakpoint()
# #convert remove commas and convert right, left tension values to int 
# def convert_to_float_add_unit_to_title(df, cols_to_convert):
#     for col in cols_to_convert:
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
input_df = pd.read_table(input_file_path, header=None)
input_df = input_df.iloc[:,:-1]
input_df.columns = input_cols


############## create location keys for input df to determine stacked shear walls
# remove repetiive columns and only keep necessary info for input_df for merge
input_df = input_df[["handle","left_location", "right_location", "diaphragm"]]



input_df[["x_left","y_left"]] = input_df.apply(lambda row: convert_coord_pair_to_float(row["left_location"]), axis=1, result_type="expand")
input_df[["x_right","y_right"]] = input_df.apply(lambda row: convert_coord_pair_to_float(row["right_location"]), axis=1, result_type="expand")

input_df = label_close_points_with_dbscan(input_df, "handle", ['x_left','y_left'], out_label="label_l",eps=2)
input_df = label_close_points_with_dbscan(input_df, "handle", ['x_right','y_right'], out_label="label_r",eps=2)

input_df["location_key"] = input_df.apply(lambda row: create_location_key(row["label_l"], row["label_r"]), axis=1)

grouped_sw_df = input_df.groupby("location_key", as_index=False)

bad_walls = 0
#check that allsw w same location tag are four levels
for shearwall,frame in grouped_sw_df:
    # print(f"Shearwall: {shearwall}")
    # print(frame)
    if not len(frame) == 4:
        bad_walls+=1
        print("_____________________________________________________________________________")
        print(f"Shearwall: {shearwall}")
        # print(frame.head())
        print(frame[['handle','x_left','xl_label','y_left','yl_label','x_right','xr_label','y_right','yr_label']])
        print("_____________________________________________________________________________")
    
print(f"bad walls{ bad_walls}")

def extract_level(diaphragm_label):
    assert isinstance(diaphragm_label,str)
    digit_list = [character for character in diaphragm_label if character.isdigit()]
    level = "".join([digit for digit in digit_list])
    return int(level)

input_df["level"] = input_df.apply(lambda row: extract_level(row["diaphragm"]), axis=1)


########################### Merge Coordinate Keys to Output df
output_df["handle"] = output_df["handle"].astype("str")  # convert from numpy to string for merge
input_df["handle"] = input_df["handle"].astype("str")  # convert from numpy to string for merge
df = pd.merge(output_df, input_df, on="handle", how="left")





########################### group by load case and shear wall and find delta forces 
grouped_df = df.groupby(["load_case","location_key"])#.sort_values("level")

# this code is done in the function bellow
# for shearwall,frame in  grouped_df:
#     print(shearwall)
#     print(frame.sort_values("level"))
#     frame["delta_l_tension"] = frame["left_tension_float"]-frame["left_tension_float"].shift(-1)
#     frame["delta_l_tension"] = frame["delta_l_tension"].fillna(frame["left_tension"])
#     print(frame)


def find_delta_forces(frame, force_cols: list):
    # Sort the group if needed
    frame = frame.sort_values("level")
    # Calculate the difference between consecutive rows for 'left_tension_float'
    for force_col in force_cols:
        frame[f"delta_{force_col}"] = frame[force_col] - frame[force_col].shift(-1)
        frame[f"delta_{force_col}"] = frame[f"delta_{force_col}"].fillna(frame[force_col])
    return frame

result_df = grouped_df.apply(find_delta_forces, force_cols=["left_tension","right_tension"])
print(result_df["load_case"])
result_df = result_df.reset_index(drop=True) # convert multi-index back to cols
print(result_df["load_case"])
print(result_df)
result_df["max_delta"] = result_df[["delta_left_tension","delta_right_tension"]].max(axis=1) #find max delta between right and left holddowns
print(result_df["load_case"])
print(result_df)

# Group by 'handle' and calculate the max force for each group
max_delta_force_id = result_df.groupby('handle')['max_delta'].idxmax()

# Retain only the rows where the force equals the maximum force in its group
final_output_df = result_df.loc[max_delta_force_id]
print(final_output_df["load_case"])
print(final_output_df)

# print(final_output_df)
final_output_df = final_output_df.groupby("location_key").apply(lambda frame: frame.sort_values("level")) #group by location key to see stacked walls

final_output_df = final_output_df[["handle","name","load_case","level","left_tension", 'delta_left_tension', "right_tension", 'delta_right_tension','max_delta']]

# print(len(final_output_df))
# print(len(input_df))
final_output_df.to_csv("final_output.csv", index=False) #set index to true bc handle was used in groupby and is now index
