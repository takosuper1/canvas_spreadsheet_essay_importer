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


def load_file(file_path):
    """
    Load a spreadsheet file (CSV or XLSX) into a pandas DataFrame.

    This function validates the file exists, determines its type using MIME type detection,
    and loads it into a DataFrame using the appropriate pandas reader.

    Args:
        file_path (str): Path to the spreadsheet file to load

    Returns:
        pandas.DataFrame: The loaded spreadsheet data

    Raises:
        FileNotFoundError: If the specified file does not exist
        ValueError: If there's an error reading the CSV or Excel file

    Notes:
        - Supports CSV and XLSX file formats
        - Uses helper_functions.check_file_type() for MIME type detection
        - File type detection is case-insensitive

    """
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


def check_essay_format(df):
    """
    Determine the essay file format and apply the appropriate parser.

    This function analyzes the DataFrame's column structure to identify whether it's from:
    - Canvas New Quiz (contains 'ItemType' columns)
    - Canvas Old Quiz (contains 'attempt' columns)
    - General essay format (contains essay and ID columns with regex-matched names)

    Then applies the corresponding parser to extract and clean the data.

    Args:
        df (pandas.DataFrame): The DataFrame to analyze and parse

    Returns:
        pandas.DataFrame: Parsed DataFrame with student IDs and essay responses extracted

    Raises:
        SpreadSheetColumnFormatError: If the DataFrame doesn't match any supported format

    Notes:
        - Checks formats in order: New Quiz → Old Quiz → General format
        - Uses regex patterns defined at module level for ID and essay column matching
        - Each parser handles format-specific column extraction and cleaning

    """
    if hf.check_essay_file_format(df, new_quiz_columns):
        return canvas_new_quiz_parse(df, regexID, regexStudent)
    elif hf.check_essay_file_format(df, old_quiz_columns):
        return canvas_old_quiz_parse(df, regexID, regexStudent)
    elif hf.check_essay_file_format(df, [regexEssay, regexID]):
        return general_excel_csv_bulk_parse(df, regexID, regexEssay, regexStudent)
    else:
        raise hf.SpreadSheetColumnFormatError

# MAIN FUNCTION
def run_extract_clean_essays(DATA_FILE_PATH):
    """
    Main pipeline function to load, parse, and clean essay data from a file.

    This is the primary entry point for processing essay files. It orchestrates the complete
    workflow: loading the file, detecting its format, extracting student IDs and essays,
    and cleaning the data (including HTML tag removal).

    Args:
        DATA_FILE_PATH (str): Path to the essay data file (CSV or XLSX)

    Returns:
        pandas.DataFrame: Cleaned DataFrame containing:
            - Student ID column
            - Essay response column(s) with HTML tags removed

    Raises:
        FileNotFoundError: If the specified file does not exist
        ValueError: If there's an error reading the file
        SpreadSheetColumnFormatError: If the file format is not supported

    Notes:
        - Automatically detects file type (CSV or XLSX)
        - Automatically detects essay format (Canvas New/Old Quiz or general format)
        - Removes HTML tags from essay responses
        - Combines multiple essay columns into a single column where applicable


    """
    # load_csv
    df = load_file(DATA_FILE_PATH)
    # extract IDs and Essays
    verified_and_parsed_df = check_essay_format(df)
    # Remove HTML tags from the combined column
    return verified_and_parsed_df


# Print the final result
print("Final Data (After Combining and Cleaning):")
print(run_extract_clean_essays(DATA_FILE_PATH))
print("\n" + "=" * 50 + "\n")