import pandas as pd
import re
import typing


# CONSTANTS
studentIDColumn = "ID"
studentNameColumn = "Name"





def canvas_new_quiz_parse(df):
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
    column_positions = [df.columns.get_loc(studentIDColumn.upper())]

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
    return extracted_df










