import pandas as pd
import helper_functions as hf


def canvas_old_quiz_parse(df, studentIDColumn, studentNameColumn):
    """
    Parse Canvas Old Quiz export data by extracting student IDs, names, and essay answers following 'attempt' columns.

    This function processes Canvas old quiz export DataFrames that contain multiple 'attempt' columns,
    extracting the student ID column, student name column, and the column immediately following each
    'attempt' column (which typically contains the student's essay answer). The answer columns are
    renamed to 'Essay1', 'Essay2', etc. for clarity.

    Args:
        df (pandas.DataFrame): The Canvas old quiz export DataFrame containing 'attempt' columns
        studentIDColumn (str): The name or pattern of the column containing student IDs
        studentNameColumn (str): The name or pattern of the column containing student names

    Returns:
        pandas.DataFrame: A DataFrame with:
            - The student ID column
            - The student name column
            - Renamed essay answer columns (Essay1, Essay2, Essay3, etc.)

    Raises:
        ValueError: If no columns named 'attempt' are found in the DataFrame

    Notes:
        - This function is specifically designed for Canvas Classic Quiz exports
        - Each 'attempt' column is expected to be followed by an answer column
        - Prints diagnostic information about columns being extracted
        - Uses iloc to properly handle DataFrames with duplicate column names

    """
    # Find all columns named 'attempt'
    print(f"Student ID: {studentIDColumn}")
    studentIDColumn = hf.find_column_by_pattern(df, studentIDColumn)
    studentNameColumn = hf.find_column_by_pattern(df, studentNameColumn)
    print(f"Student ID: {studentIDColumn}")
    print(f"Student Name: {studentNameColumn}")

    itemtype_indices = [
        i
        for i, col in enumerate(df.columns)
        if col == "attempt"
    ]
    if not itemtype_indices:
        raise ValueError(
            "Error: No columns named 'attempt' found."
        )

    print(
        f"Found {len(itemtype_indices)} columns named 'attempt' at positions: {itemtype_indices}"
    )
    print("\n" + "=" * 50 + "\n")

    # Extract ID, Name, and the columns after each attempt
    columns_to_extract = [studentIDColumn, studentNameColumn]
    column_positions = [df.columns.get_loc(studentIDColumn), df.columns.get_loc(studentNameColumn)]

    for idx in itemtype_indices:
        if idx + 1 < len(df.columns):
            columns_to_extract.append(df.columns[idx + 1])
            column_positions.append(idx + 1)
        else:
            print(f"Warning: No column after 'attempt' at position {idx}")

    print(f"Extracting columns at positions {column_positions}:")
    for pos, col in zip(column_positions, columns_to_extract):
        print(f"  Position {pos}: {col}")
    print("\n" + "=" * 50 + "\n")

    # Extract using iloc to handle duplicate column names properly
    extracted_df = df.iloc[:, column_positions]

    # Rename columns to be clear about which is which
    new_column_names = [studentIDColumn, studentNameColumn]
    for i, idx in enumerate(itemtype_indices, 1):
        if idx + 1 < len(df.columns):
            # rename columns
            new_column_names.append(f"Essay{i}")

    extracted_df.columns = new_column_names
    return extracted_df