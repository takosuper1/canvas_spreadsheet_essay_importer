import helper_functions as hf


def canvas_new_quiz_parse(df, studentIDColumn, studentNameColumn):
    """
    Parse Canvas New Quiz export data by extracting student IDs, names, and answers following ItemType columns.

    This function processes Canvas quiz export DataFrames that contain multiple 'ItemType' columns,
    extracting the student ID column, student name column, and the column immediately following
    each ItemType column (which typically contains the student's answer). All answer columns are
    then combined into a single column with HTML tags removed.

    Args:
        df (pandas.DataFrame): The Canvas quiz export DataFrame containing ItemType columns
        studentIDColumn (str): The name or pattern of the column containing student IDs
        studentNameColumn (str): The name or pattern of the column containing student names

    Returns:
        pandas.DataFrame: A cleaned DataFrame with:
            - The student ID column
            - The student name column
            - A 'Combined_ItemType' column containing all answers with HTML tags removed

    Raises:
        ValueError: If no columns named 'ItemType' or starting with 'ItemType.' are found

    """
    # Find all columns named 'ItemType'
    print(f"Student ID: {studentIDColumn}")
    studentIDColumn = hf.find_column_by_pattern(df, studentIDColumn)
    studentNameColumn = hf.find_column_by_pattern(df, studentNameColumn)
    print(f"Student ID: {studentIDColumn}")
    print(f"Student Name: {studentNameColumn}")

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

    # Extract ID, Name, and the columns after each ItemType
    columns_to_extract = [studentIDColumn, studentNameColumn]
    column_positions = [df.columns.get_loc(studentIDColumn), df.columns.get_loc(studentNameColumn)]

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
    new_column_names = [studentIDColumn, studentNameColumn]
    for i, idx in enumerate(itemtype_indices, 1):
        if idx + 1 < len(df.columns):
            # rename columns
            new_column_names.append(f"ItemType{i}")

    extracted_df.columns = new_column_names
    combined_extracted_columns = combine_same_name_columns(extracted_df)
    cleaned_df = hf.remove_html_tags(combined_extracted_columns, "Combined_ItemType")
    return cleaned_df


def combine_same_name_columns(df, columnName="ItemType"):
    """
    Combine all columns starting with a specified name into a single column.

    This function finds all columns that start with the given columnName prefix,
    combines them by taking the first non-NaN value across each row, and creates
    a new 'Combined_ItemType' column. The original matching columns are then removed.

    Args:
        df (pandas.DataFrame): The DataFrame containing columns to combine
        columnName (str, optional): The prefix of column names to combine.
            Defaults to "ItemType".

    Returns:
        pandas.DataFrame: DataFrame with combined column added and original columns removed.
            The new column is named 'Combined_ItemType' and contains the first non-NaN
            value from each row across all matching columns.

    Notes:
        - If no matching columns are found, returns the original DataFrame unchanged
        - Uses backward fill (bfill) to find the first non-NaN value across rows
        - Prints diagnostic information about the columns being combined

    """
    same_name_columns = []
    for idx, col in enumerate(df.columns):
        # Find all after_ItemType columns
        same_name_columns = [col for col in df.columns if col.startswith(columnName)]

    if len(same_name_columns) == 0:
        print("No after_ItemType columns found to combine.")
        return df

    print(f"Combining {len(same_name_columns)} columns: {same_name_columns}")

    # Create combined column by taking first non-NaN value across the row
    df["Combined_ItemType"] = df[same_name_columns].bfill(axis=1).iloc[:, 0]

    # Drop the original after_ItemType columns
    df = df.drop(columns=same_name_columns)

    return df