# can-log-merger
When working with vehicle data, you often end up with multiple CAN log files where the timestamp resets in each one. This script solves that problem by intelligently merging multiple .asc files into a single, cohesive log. It automatically recalculates and adjusts the timestamps to be sequential across all files, making subsequent data analysis seamless.
在处理车辆CAN报文数据时，我们经常会得到多个由CANalyzer、CANoe等工具导出的.asc日志文件。这些文件各自的时间戳都是从零开始，给连续性分析带来了极大的不便。
本工具通过一个简单的Python脚本，能够智能地将这些分散的.asc文件合并为一个，并自动累加、校正时间戳，确保最终生成的单个文件具有完美连续的时间序列，让你的数据分析工作流更加顺畅。
