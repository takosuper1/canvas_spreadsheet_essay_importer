import helper_functions as hf


def canvas_new_quiz_parse(df, studentIDColumn):
    # Find all columns named 'ItemType'
    print(f"Student ID: {studentIDColumn}")
    studentIDColumn = hf.find_column_by_pattern(df, studentIDColumn)
    print(f"Student ID: {studentIDColumn}")
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
            # rename columns
            new_column_names.append(f"ItemType{i}")

    extracted_df.columns = new_column_names
    combined_extracted_columns = combine_same_name_columns(extracted_df)
    cleaned_df = hf.remove_html_tags(combined_extracted_columns, "Combined_ItemType")
    return cleaned_df


# Combine all after_ItemType columns
def combine_same_name_columns(df,columnName = "ItemType"):
    """
      Combines all columns that start with  into a single column.
      Takes the non-NaN value when only one column has data.
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




