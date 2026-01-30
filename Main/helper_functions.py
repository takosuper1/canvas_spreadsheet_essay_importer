import os
import magic


def check_file_type(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        return "Error: File does not exist."

    # Initialize the magic library
    mime = magic.Magic(mime=True)

    # Get the MIME type of the file
    mime_type = mime.from_file(file_path)

    # Determine the file type based on MIME type
    if mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return "XLSX"
    elif mime_type == "application/vnd.oasis.opendocument.spreadsheet":
        return "ODS"
    elif mime_type == "text/csv" or mime_type == "text/plain":
        # Further check for CSV or TSV
        with open(file_path, "r", encoding="utf-8") as file:
            first_line = file.readline()
            if "\t" in first_line:
                return "TSV"
            else:
                return "CSV"
    else:
        return f"File is not a recognized spreadsheet or CSV/TSV file. Detected MIME type: {mime_type}"
