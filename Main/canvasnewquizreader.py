import pandas as pd
import re
import os
import typing


# CONSTANTS
studentIDColumn = "ID"


def check_file_type(file_path) -> str:
    # logic for checking if csv or excel file
    return "Unreadable file type"


# Legend's script needs to call this script to start the import
def load_file(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")
    file_type = check_file_type(file_path)
    # Try loading the CSV
    if file_type == "csv":
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")
    # Try loading the excel file
    if file_type == "excel":
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            raise ValueError(f"Error reading excel file: {e}")


def extract_desired_dfs(df):
    # Check if 'ID' column exists
    if studentIDColumn not in df.columns:
        raise KeyError("Error: The CSV file does not contain an 'ID' column.")

    # Find all columns named 'ItemType'
    itemtype_indices = [
        i
        for i, col in enumerate(df.columns)
        if col == "ItemType" or col.startswith("ItemType.")
    ]
    if not itemtype_indices:
        raise ValueError(
            "Error: No columns named 'ItemType' or starting with 'ItemType.' found."
        )

    print(
        f"Found {len(itemtype_indices)} columns named 'ItemType' at positions: {itemtype_indices}"
    )
    print("\n" + "=" * 50 + "\n")

    # Extract ID and the columns after each ItemType
    columns_to_extract = [studentIDColumn]
    column_positions = [df.columns.get_loc(studentIDColumn)]

    for idx in itemtype_indices:
        if idx + 1 < len(df.columns):
            columns_to_extract.append(df.columns[idx + 1])
            column_positions.append(idx + 1)
        else:
            print(f"Warning: No column after ItemType at position {idx}")

    print(f"Extracting columns at positions {column_positions}:")
    for pos, col in zip(column_positions, columns_to_extract):
        print(f"  Position {pos}: {col}")
    print("\n" + "=" * 50 + "\n")

    # Extract using iloc to handle duplicate column names properly
    extracted_df = df.iloc[:, column_positions]

    # Rename columns to be clear about which is which
    new_column_names = [studentIDColumn]
    for i, idx in enumerate(itemtype_indices, 1):
        if idx + 1 < len(df.columns):
            # get rubric
            rubric.append(df.columns[idx + 1])
            # rename columns
            new_column_names.append(f"ItemType{i}")

    extracted_df.columns = new_column_names
    return extracted_df


def get_rubric(rubric):
    return ". ".join(rubric)


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
    df = load_csv()
    # extract IDs and Essays
    extracted_df = extract_desired_dfs(df)
    # Apply the combining function
    combined_columns_extracted_df = combine_itemtype_columns(extracted_df)
    # Remove HTML tags from the combined column
    print(f"rubric: {get_rubric(rubric)}")
    return remove_html_tags(combined_columns_extracted_df, "Combined_ItemType")


# Print the final result
print("Final Data (After Combining and Cleaning):")
print(run_extract_clean_essays())
print("\n" + "=" * 50 + "\n")
