import pandas as pd
import helper_functions as hf


def general_excel_csv_bulk_parse(df, studentIdColumnName, essayColumnName):
    """
      Extract student ID column and all essay columns into a new dataframe.

      Args:
          df: DataFrame containing the quiz data
          studentIDPattern: Regex pattern to match the student ID column
          essayPattern: Regex pattern to match essay columns

      Returns:
          DataFrame with student ID and all matched essay columns
      """
    print("finding student ID column...")
    studentIdColumnName = hf.find_column_by_pattern(df, studentIdColumnName)
    print(f"Found student ID column: {studentIdColumnName}")
    print("finding essay column...")
    essayColumnName = hf.find_column_by_pattern(df, essayColumnName)
    print(f"Found essay column: {essayColumnName}")
    # Find the student ID column using regex
    print(f"Student ID pattern: {studentIdColumnName}")
    studentIDColumn = hf.find_column_by_pattern(df, studentIdColumnName)

    if studentIDColumn is None:
        raise ValueError(f"Error: No column found matching student ID pattern")

    print(f"Matched Student ID column: {studentIDColumn}")

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
    columns_to_extract = [studentIDColumn] + essay_columns

    print(f"Extracting columns: {columns_to_extract}")
    print("\n" + "=" * 50 + "\n")

    # Extract the columns
    extracted_df = df[columns_to_extract].copy()

    # Optionally rename essay columns to Essay1, Essay2, etc.
    new_column_names = [studentIDColumn]
    for i in range(len(essay_columns)):
        new_column_names.append(f"Essay{i + 1}")

    extracted_df.columns = new_column_names
    cleaned_df = hf.remove_html_tags(extracted_df, hf.find_column_by_pattern(extracted_df,essayColumnName))

    print(f"Final DataFrame columns: {list(cleaned_df.columns)}")
    return cleaned_df