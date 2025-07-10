A simple yet powerful tool to merge multiple CAN/CAN-FD .asc log files with automatic timestamp correction.

Overview
When working with vehicle data, you often end up with multiple CAN log files where the timestamp resets in each one. This script solves that problem by intelligently merging multiple .asc files into a single, cohesive log. It automatically recalculates and adjusts the timestamps to be sequential across all files, making subsequent data analysis seamless.

项目简介
在处理车辆CAN报文数据时，我们经常会得到多个由CANalyzer、CANoe等工具导出的.asc日志文件。这些文件各自的时间戳都是从零开始，给连续性分析带来了极大的不便。

本工具通过一个简单的Python脚本，能够智能地将这些分散的.asc文件合并为一个，并自动累ac、校正时间戳，确保最终生成的单个文件具有完美连续的时间序列，让你的数据分析工作流更加顺畅。

✨ Key Features
Smart Merging: Combines multiple .asc files into one.

Automatic Timestamp Correction: Ensures timestamps are continuous and sequential across all merged files.

Header Preservation: Uses the header from the first file and discards subsequent ones to maintain a valid file format.

Simple to Use: Just place your files in a folder and run the script.

Pure Python: No external libraries needed, runs out of the box with a standard Python installation.

🚀 How to Use
Save the script: Save the code as a Python file, for example, merge_logs.py.

Organize your files: Place all the .asc log files you want to merge into a single folder.

Update the script: Open merge_logs.py and modify the input_folder_path variable to the path of your folder.

# Change this line to your folder's path
input_folder_path = "C:/Users/YourName/Desktop/CAN_Logs"

Run the script: Execute the script from your terminal.

python merge_logs.py

Done!: A new file named merged_log.asc will be created in the same folder, containing all your merged data with corrected timestamps.
