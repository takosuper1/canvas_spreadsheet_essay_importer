import pandas as pd
import os
import re

from Main.canvasnewquizreader import canvas_new_quiz_parse
from helper_functions import check_file_type

data_file_path = ""
is_canvas_new_quiz = False
is_canvas_old_quiz = False
is_general_essay_file = False
regexID = ""
regexStudent = ""
# Legend's script needs to call this script to start the import
def load_file(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")
    file_type = check_file_type(file_path)
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

# Combine all after_ItemType columns
def combine_itemtype_columns(df):
    """
    Combines all columns that start with 'ItemType' into a single column.
    Takes the non-NaN value when only one column has data.
    """
    # Find all after_ItemType columns
    itemtype_cols = [col for col in df.columns if col.startswith("ItemType")]

    if len(itemtype_cols) == 0:
        print("No after_ItemType columns found to combine.")
        return df

    print(f"Combining {len(itemtype_cols)} columns: {itemtype_cols}")

    # Create combined column by taking first non-NaN value across the row
    df["Combined_ItemType"] = df[itemtype_cols].bfill(axis=1).iloc[:, 0]

    # Drop the original after_ItemType columns
    df = df.drop(columns=itemtype_cols)

    return df


# Remove HTML tags from a column
def remove_html_tags(df, column_name):
    """
    Removes HTML tags from the specified column.
    """
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in dataframe.")
        return df

    print(f"Removing HTML tags from column: {column_name}")

    # Function to strip HTML tags
    def strip_tags(text):
        if pd.isna(text):
            return text
        # Remove HTML tags using regex
        clean_text = re.sub(r"<[^>]+>", "", str(text))
        # Also remove extra whitespace that might be left over
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        return clean_text

    df[column_name] = df[column_name].apply(strip_tags)

    return df


def run_extract_clean_essays():
    # load_csv
    df = load_file(data_file_path)
    # extract IDs and Essays
    extracted_df = extract_desired_dfs(df)
    # Apply the combining function
    combined_columns_extracted_df = combine_itemtype_columns(extracted_df)
    # Remove HTML tags from the combined column

    return remove_html_tags(combined_columns_extracted_df, "Combined_ItemType")


# Print the final result
print("Final Data (After Combining and Cleaning):")
print(run_extract_clean_essays())
print("\n" + "=" * 50 + "\n")
