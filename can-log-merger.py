import os
import glob


def merge_asc_files(input_folder, output_file):
    """
    Merges all .asc log files in a specified folder and automatically corrects the timestamps.

    This function will:
    1. Use the header of the first file as the header for the merged file.
    2. Automatically accumulate the timestamps of subsequent files to ensure continuity.
    3. Ignore the header sections of subsequent files.

    Args:
        input_folder (str): The path to the folder containing the .asc files.
        output_file (str): The full path and filename for the merged output file.
    """
    # Get the paths of all .asc files in the folder and sort them by name
    file_paths = sorted(glob.glob(os.path.join(input_folder, '*.asc')))

    if not file_paths:
        print(f"No .asc files found in the folder '{input_folder}'.")
        return

    print(f"Found {len(file_paths)} files. Starting merge process...")

    last_global_timestamp = 0.0  # Used to record the final timestamp at the end of the previous file
    header_written = False  # Flag to track if the header has been written

    # Open the output file
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
        # Iterate through each found file
        for file_path in file_paths:
            print(f"  -> Processing: {os.path.basename(file_path)}")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:

                # Flag to indicate if the data section has started
                is_data_section = False

                for line in infile:
                    stripped_line = line.strip()

                    # Check if it is a data line (usually starts with a floating-point timestamp)
                    is_data_line = False
                    if stripped_line:
                        try:
                            float(stripped_line.split()[0])
                            is_data_line = True
                        except (ValueError, IndexError):
                            is_data_line = False

                    # --- Header Processing ---
                    if not is_data_section:
                        # For the first file, copy its header
                        if not header_written:
                            outfile.write(line)
                        # The "base hex" line is the end marker for the header
                        if stripped_line.lower().startswith('base hex'):
                            is_data_section = True
                            # The header of the first file is written, no more headers will be written
                            if not header_written:
                                header_written = True
                        continue  # Continue to the next line until the data section begins

                    # --- Data Row Processing ---
                    if is_data_line:
                        parts = line.split(maxsplit=1)
                        if len(parts) < 2:
                            continue  # Skip incorrectly formatted or empty lines

                        original_ts_str, rest_of_line = parts

                        try:
                            # Calculate the new timestamp
                            original_ts = float(original_ts_str)
                            new_ts = original_ts + last_global_timestamp

                            # Maintain the same decimal precision as the original timestamp
                            if '.' in original_ts_str:
                                precision = len(original_ts_str.split('.')[1])
                                new_ts_str = f"{new_ts:.{precision}f}"
                            else:
                                new_ts_str = str(int(new_ts))

                            # Maintain original column alignment and write to file
                            outfile.write(f"{new_ts_str.rjust(len(original_ts_str))} {rest_of_line}")
                        except ValueError:
                            # If conversion fails, write the line as is
                            outfile.write(line)

                # After reading a file, record the timestamp of its last line for the next file's accumulation
                # Note: The 'new_ts' variable here holds the latest timestamp from the current file's last line
                if 'new_ts' in locals():
                    last_global_timestamp = new_ts

    print(f"\nMerge complete! All files have been merged into: {output_file}")


# --- Usage Instructions ---
if __name__ == "__main__":
    # 1. Please place all your .asc files in a single folder.
    # 2. Modify the 'input_folder_path' below to the path of your folder.
    input_folder_path = "F:/6.26-6.28/6.26/776#/CAN"  # Example: "C:/Users/YourName/Desktop/CAN_Logs"

    # 3. Modify the 'output_file_name' below to your desired merged filename.
    output_file_name = ("merged_log_6.26_776.asc")

    # Check if the path exists
    if not os.path.isdir(input_folder_path):
        print(f"Error: The folder '{input_folder_path}' does not exist. Please modify the path in the script.")
    else:
        # Construct the full output file path
        output_file_path = os.path.join(input_folder_path, output_file_name)

        # Execute the merge function
        merge_asc_files(input_folder_path, output_file_path)
