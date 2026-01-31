import pandas as pd
import helper_functions as hf


def canvas_old_quiz_parse(df, studentIDColumn):
    # Find all columns named 'ItemType'
    print(f"Student ID: {studentIDColumn}")
    studentIDColumn = hf.find_column_by_pattern(df, studentIDColumn)
    print(f"Student ID: {studentIDColumn}")
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

    # Extract ID and the columns after each ItemType
    columns_to_extract = [studentIDColumn]
    column_positions = [df.columns.get_loc(studentIDColumn)]

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
    new_column_names = [studentIDColumn]
    for i, idx in enumerate(itemtype_indices, 1):
        if idx + 1 < len(df.columns):
            # rename columns
            new_column_names.append(f"Essay{i}")

    extracted_df.columns = new_column_names
    return extracted_df
