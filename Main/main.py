import pandas as pd
import os
import re
from canvasnewquizreader import canvas_new_quiz_parse
from canvasoldquizreader import canvas_old_quiz_parse
from generalexcelcsvbulkreader import general_excel_csv_bulk_parse
import helper_functions as hf

DATA_FILE_PATH = "../Tests/Sample_Data/generaluploadsample.csv"
regexEssay = r'^.*essay.*$'
regexID = r'^(?:student[_\s]?id|id)$'
regexStudent = r'^(?:student[_\s]?name|name)$'
new_quiz_columns = ["ItemType"]
old_quiz_columns = ["attempt"]

# Legend's script needs to call this script to start the import
def load_file(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")
    file_type = hf.check_file_type(file_path)
    # Try loading the CSV
    if file_type == "CSV":
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")
    # Try loading the excel file
    if file_type == "XLXS":
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            raise ValueError(f"Error reading excel file: {e}")

# insert logic for choosing which parser to use
def check_essay_format(df):
    if hf.check_essay_file_format(df, new_quiz_columns):
        return canvas_new_quiz_parse(df, regexID)
    elif hf.check_essay_file_format(df, old_quiz_columns):
        return canvas_old_quiz_parse(df, regexID)
    elif hf.check_essay_file_format(df, [regexEssay, regexID]):
        return general_excel_csv_bulk_parse(df, regexID, regexEssay)
    else:
        raise hf.SpreadSheetColumnFormatError


def run_extract_clean_essays():
    # load_csv
    df = load_file(DATA_FILE_PATH)
    # extract IDs and Essays
    verified_and_parsed_df = check_essay_format(df)
    # Remove HTML tags from the combined column
    return verified_and_parsed_df



# Print the final result
print("Final Data (After Combining and Cleaning):")
print(run_extract_clean_essays())
print("\n" + "=" * 50 + "\n")
