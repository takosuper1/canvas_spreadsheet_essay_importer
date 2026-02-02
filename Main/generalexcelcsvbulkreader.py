import pandas as pd
import helper_functions as hf


def general_excel_csv_bulk_parse(df, studentIdColumnName, essayColumnName, studentNamePattern):
    """
    Extract student ID, student name, and all essay columns into a new dataframe.

    This function processes general CSV/Excel quiz files by extracting student identification
    columns and essay response columns using regex pattern matching. Essay columns are renamed
    for consistency and HTML tags are removed from essay content.

    Args:
        df (pandas.DataFrame): DataFrame containing the quiz data
        studentIdColumnName (str): Regex pattern to match the student ID column
        essayColumnName (str): Regex pattern to match essay columns
        studentNamePattern (str): Regex pattern to match the student name column

    Returns:
        pandas.DataFrame: A DataFrame with:
            - The student ID column
            - The student name column
            - Renamed essay columns (Essay1, Essay2, etc.) with HTML tags removed

    Raises:
        ValueError: If no column matching the student ID pattern is found
        ValueError: If no columns matching the essay pattern are found
        ValueError: If no column matching the student name pattern is found
    """
    print("Finding student ID column...")
    studentIdColumnName = hf.find_column_by_pattern(df, studentIdColumnName)
    print(f"Found student ID column: {studentIdColumnName}")

    print("Finding student name column...")
    studentNamePattern = hf.find_column_by_pattern(df, studentNamePattern)
    print(f"Found student name column: {studentNamePattern}")

    print("Finding essay column...")
    essayColumnName = hf.find_column_by_pattern(df, essayColumnName)
    print(f"Found essay column: {essayColumnName}")

    # Find the student ID column using regex
    print(f"Student ID pattern: {studentIdColumnName}")
    studentIDColumn = hf.find_column_by_pattern(df, studentIdColumnName)

    if studentIDColumn is None:
        raise ValueError(f"Error: No column found matching student ID pattern")

    print(f"Matched Student ID column: {studentIDColumn}")

    # Find the student name column using regex
    print(f"\nStudent Name pattern: {studentNamePattern}")
    studentNameColumn = hf.find_column_by_pattern(df, studentNamePattern)

    if studentNameColumn is None:
        raise ValueError(f"Error: No column found matching student name pattern")

    print(f"Matched Student Name column: {studentNameColumn}")

    # Find all essay columns using regex
    print(f"\nEssay pattern: {essayColumnName}")

    essay_columns = []
    for col in df.columns:
        if essayColumnName == col:
            essay_columns.append(col)

    if not essay_columns:
        raise ValueError("Error: No columns found matching essay pattern")

    print(f"Found {len(essay_columns)} essay column(s): {essay_columns}")
    print("\n" + "=" * 50 + "\n")

    # Build list of columns to extract
    columns_to_extract = [studentIDColumn, studentNameColumn] + essay_columns

    print(f"Extracting columns: {columns_to_extract}")
    print("\n" + "=" * 50 + "\n")

    # Extract the columns
    extracted_df = df[columns_to_extract].copy()

    # Rename columns: keep ID and Name, rename essays to Essay1, Essay2, etc.
    new_column_names = [studentIDColumn, studentNameColumn]
    for i in range(len(essay_columns)):
        new_column_names.append(f"Essay{i + 1}")

    extracted_df.columns = new_column_names
    cleaned_df = hf.remove_html_tags(extracted_df, hf.find_column_by_pattern(extracted_df, essayColumnName))

    print(f"Final DataFrame columns: {list(cleaned_df.columns)}")
    return cleaned_df