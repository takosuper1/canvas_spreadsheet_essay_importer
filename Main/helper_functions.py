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

class SpreadSheetColumnFormatError (Exception):
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
    Check if the dataframe has all required columns (using regex matching)
    and return True if there are extra columns beyond the required ones.

    Args:
        df: pandas DataFrame
        column_names_list: list of regex patterns to match against column names

    Returns:
        True if there are more columns than matches found, False otherwise
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


def find_column_by_pattern(df, pattern):
    """
    Find the first column that matches the given regex pattern.

    Args:
        df: pandas DataFrame
        pattern: regex pattern string

    Returns:
        str: The actual column name that matches, or None if no match found
    """
    compiled_pattern = re.compile(pattern, re.IGNORECASE)
    for col in df.columns:
        if compiled_pattern.match(col):
            return col
    return None