import os
import magic
import re
import pandas as pd


# ERRORS/EXCEPTIONS
class UnsupportedFileTypeError(Exception):
    """Raised when the file type is not supported"""
    pass


class FileNotFoundError(Exception):
    """Raised when the file does not exist"""
    pass


class SpreadSheetColumnFormatError(Exception):
    """Raised when the formatting of the spreadsheet is not supported"""
    pass


def check_file_type(file_path):
    """
    Check if a file is CSV, XLSX, or ODS.

    Args:
        file_path (str): Path to the file to check

    Returns:
        str: One of "CSV", "XLSX", or "ODS"

    Raises:
        FileNotFoundError: If the file does not exist (built-in exception)
        UnsupportedFileTypeError: If the file is not CSV, XLSX, or ODS
        IOError: If there's an error reading the file
    """
    # Check if the file exists (raises built-in FileNotFoundError)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")
    # Check if it's actually a file (not a directory)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Path is not a file: {file_path}")

    try:
        # Initialize the magic library
        mime = magic.Magic(mime=True)

        # Get the MIME type of the file
        mime_type = mime.from_file(file_path)

        # Check for XLSX
        if mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            return "XLSX"

        # Check for ODS
        elif mime_type == "application/vnd.oasis.opendocument.spreadsheet":
            return "ODS"

        # Check for CSV (text/csv or text/plain)
        elif mime_type in ["text/csv", "text/plain"]:
            # Try to verify it's actually CSV by checking for delimiters
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    first_line = file.readline()

                    # If file is empty, raise error
                    if not first_line:
                        raise UnsupportedFileTypeError(
                            f"File appears to be empty: {file_path}"
                        )

                    # Check if it contains comma delimiters (CSV characteristic)
                    # We're being lenient here - you might want stricter validation
                    if "," in first_line or mime_type == "text/csv":
                        return "CSV"
                    else:
                        raise UnsupportedFileTypeError(
                            f"File does not appear to be a valid CSV. "
                            f"Detected MIME type: {mime_type}"
                        )

            except UnicodeDecodeError as e:
                raise IOError(
                    f"Unable to read file with UTF-8 encoding: {file_path}. "
                    f"Error: {str(e)}"
                )
            except IOError as e:
                # Re-raise IOError with more context
                raise IOError(f"Error reading file {file_path}: {str(e)}")

        # Any other MIME type is unsupported
        else:
            raise UnsupportedFileTypeError(
                f"Unsupported file type. Only CSV, XLSX, and ODS files are accepted. "
                f"Detected MIME type: {mime_type}"
            )

    except magic.MagicException as e:
        raise IOError(f"Error detecting file type for {file_path}: {str(e)}")


def check_essay_file_format(df, column_names_list):
    """
    Validate that a DataFrame contains all required columns and detect extra columns.

    This function checks if the provided DataFrame has columns matching all the required
    regex patterns and reports whether there are additional columns beyond those required.
    Uses case-insensitive regex matching to find columns.

    Args:
        df (pandas.DataFrame): The DataFrame to validate
        column_names_list (list of str): List of regex patterns to match against column names.
            Each pattern should match at least one column in the DataFrame.

    Returns:
        bool: True if there are extra columns beyond the required matches, False otherwise.
            Also returns False if any required pattern is not found (with error message printed).

    Notes:
        - Uses case-insensitive regex matching
        - Each pattern is matched only once (first match wins)
        - Prints error message if required columns are missing
        - Prints warning message if extra columns are detected


    """
    # Compile regex patterns (case-insensitive)
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in column_names_list]

    # Find matches for each pattern
    matched_columns = []
    for pattern in compiled_patterns:
        match_found = False
        for col in df.columns:
            if pattern.match(col):
                matched_columns.append(col)
                match_found = True
                break  # Only match each pattern once

        if not match_found:
            print(f"Error: No column found matching pattern: {pattern.pattern}")
            print(f"Found columns: {list(df.columns)}")
            return False

    # Check if there are more columns than the ones we matched
    has_extra_columns = len(df.columns) > len(matched_columns)

    if has_extra_columns:
        extra_cols = set(df.columns) - set(matched_columns)
        print(f"Warning: Found {len(extra_cols)} extra column(s): {extra_cols}")
        return True

    return False


def remove_html_tags(df, column_name):
    """
    Remove all HTML tags from a specified column in a DataFrame.

    This function strips HTML tags from text data and normalizes whitespace in the
    specified column. It preserves the original DataFrame structure and handles
    NaN values appropriately.

    Args:
        df (pandas.DataFrame): The DataFrame containing the column to clean
        column_name (str): The name of the column from which to remove HTML tags

    Returns:
        pandas.DataFrame: The DataFrame with HTML tags removed from the specified column.
            Returns the original DataFrame unchanged if the column is not found.

    Notes:
        - Uses regex to remove all HTML tags (anything between < and >)
        - Collapses multiple whitespace characters into single spaces
        - Strips leading and trailing whitespace
        - Preserves NaN values without modification
        - Prints a message if the specified column is not found

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


def find_column_by_pattern(df, pattern):
    """
    Find the first column in a DataFrame that matches a given regex pattern.

    This function performs case-insensitive regex matching against all column names
    in the DataFrame and returns the first match found.

    Args:
        df (pandas.DataFrame): The DataFrame to search
        pattern (str): A regex pattern string to match against column names

    Returns:
        str or None: The actual column name that matches the pattern, or None if no match is found

    Notes:
        - Matching is case-insensitive
        - Returns only the first match if multiple columns match the pattern
        - The pattern is treated as a regex, not a literal string


    """
    compiled_pattern = re.compile(pattern, re.IGNORECASE)
    for col in df.columns:
        if compiled_pattern.match(col):
            return col
    return None