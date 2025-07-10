import os
import glob


def merge_asc_files(input_folder, output_file):
    """
    合并指定文件夹中的所有 .asc 日志文件，并自动校正时间戳。

    该函数会:
    1. 使用第一个文件的文件头作为合并后文件的文件头。
    2. 自动累加后续文件的时间戳，确保其连续性。
    3. 忽略后续文件的文件头部分。

    Args:
        input_folder (str): 包含 .asc 文件的文件夹路径。
        output_file (str): 合并后输出文件的完整路径和文件名。
    """
    # 获取文件夹内所有 .asc 文件的路径，并按名称排序
    file_paths = sorted(glob.glob(os.path.join(input_folder, '*.asc')))

    if not file_paths:
        print(f"在文件夹 '{input_folder}' 中没有找到 .asc 文件。")
        return

    print(f"找到了 {len(file_paths)} 个文件，将开始合并...")

    last_global_timestamp = 0.0  # 用于记录上一个文件结束时的最终时间戳
    header_written = False  # 标记是否已经写入了文件头

    # 打开输出文件
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
        # 遍历每一个找到的文件
        for file_path in file_paths:
            print(f"  -> 正在处理: {os.path.basename(file_path)}")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:

                # 标记数据行是否开始
                is_data_section = False

                for line in infile:
                    stripped_line = line.strip()

                    # 检查是否为数据行（通常以浮点数时间戳开头）
                    is_data_line = False
                    if stripped_line:
                        try:
                            float(stripped_line.split()[0])
                            is_data_line = True
                        except (ValueError, IndexError):
                            is_data_line = False

                    # --- 文件头处理 ---
                    if not is_data_section:
                        # 对于第一个文件，复制其文件头
                        if not header_written:
                            outfile.write(line)
                        # "base hex" 行是文件头的结束标志
                        if stripped_line.lower().startswith('base hex'):
                            is_data_section = True
                            # 第一个文件的头已经写完，后续不再写头
                            if not header_written:
                                header_written = True
                        continue  # 继续读取下一行，直到数据行开始

                    # --- 数据行处理 ---
                    if is_data_line:
                        parts = line.split(maxsplit=1)
                        if len(parts) < 2:
                            continue  # 跳过格式不正确或空的行

                        original_ts_str, rest_of_line = parts

                        try:
                            # 计算新的时间戳
                            original_ts = float(original_ts_str)
                            new_ts = original_ts + last_global_timestamp

                            # 保持与原始时间戳相同的小数位数精度
                            if '.' in original_ts_str:
                                precision = len(original_ts_str.split('.')[1])
                                new_ts_str = f"{new_ts:.{precision}f}"
                            else:
                                new_ts_str = str(int(new_ts))

                            # 保持原始的列对齐格式并写入文件
                            outfile.write(f"{new_ts_str.rjust(len(original_ts_str))} {rest_of_line}")
                        except ValueError:
                            # 如果转换失败，则按原样写入该行
                            outfile.write(line)

                # 读完一个文件后，记录这个文件最后一行的时间戳，用于下一个文件的累加
                # 注意：这里的 new_ts 变量恰好是当前文件最后一行的最新时间戳
                if 'new_ts' in locals():
                    last_global_timestamp = new_ts

    print(f"\n合并完成！所有文件已合并到: {output_file}")


# --- 使用说明 ---
if __name__ == "__main__":
    # 1. 请将你的 .asc 文件全部放在一个文件夹中。
    # 2. 修改下面的 input_folder_path 为你存放文件的文件夹路径。
    input_folder_path = "F:/S59耐久车试验数据搜集6.26-6.28/6.26/776#/CAN"  # 例如: "C:/Users/YourName/Desktop/CAN_Logs"

    # 3. 修改下面的 output_file_name 为你希望生成的合并文件名。
    output_file_name = ("merged_log_6.26_776.asc")

    # 检查路径是否存在
    if not os.path.isdir(input_folder_path):
        print(f"错误：文件夹 '{input_folder_path}' 不存在。请修改脚本中的路径。")
    else:
        # 拼接完整的输出文件路径
        output_file_path = os.path.join(input_folder_path, output_file_name)

        # 执行合并函数
        merge_asc_files(input_folder_path, output_file_path)