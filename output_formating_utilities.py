import openpyxl
from openpyxl.drawing.image import Image as OpenpyxlImage
from PIL import Image
import io

def resize_and_convert_image(img_path: str, resize_factor: int) -> io.BytesIO:
    """
    Load and resize img then Convert to a io.BytesIO object
    Note: io.BytesIO object prefered because it can be read by openpyxl
    and the image does not need to be saved to disc
    """
    # Open and resize the imag
    img = Image.open(img_path)
    img_size = img.size
    new_size = tuple([int(pixel_qty / resize_factor) for pixel_qty in img_size])
    resized_img = img.resize(new_size)

    # Save resized image to BytesIO object
    img_byte_arr = io.BytesIO()
    resized_img.save(img_byte_arr, format=img.format)
    img_byte_arr.seek(0) #reset file opointer to begining
    return img_byte_arr

def write_dict_to_xlsx(
        info_dict:dict,
        worksheet:openpyxl.worksheet.worksheet.Worksheet, 
        start_row:int, 
        start_col:int):
    """
    Writes the contents of a dictionary to a specified worksheet starting from a given row and column.
    """
    for i, entry in enumerate(info_dict.items()):
        label_cell = worksheet.cell(start_row+i,start_col) 
        label_cell.value = entry[0]
        info_cell = worksheet.cell(start_row+i,start_col+1) 
        info_cell.value = entry[1]


def add_ImgByteArr_to_worksheet(
        img_byte_arr:io.BytesIO,
        worksheet:openpyxl.worksheet.worksheet.Worksheet,
        insert_cell="A1"
        ):
    """
    Add image byte array to worksheet using openpyxl at specifed location
    """
    openpyxl_img = OpenpyxlImage(img_byte_arr)
    # Add image to worksheet and save
    worksheet.add_image(openpyxl_img, insert_cell)

def scale_cols_to_max_width(worksheet:openpyxl.worksheet.worksheet.Worksheet):
    """
    Scale all columns in worksheet to the maximum cell width
    """
    dims = {}
    for row in worksheet.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))   
    for col, value in dims.items():
        worksheet.column_dimensions[col].width = value
