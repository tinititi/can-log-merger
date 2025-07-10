# can-log-merger
When working with vehicle data, you often end up with multiple CAN log files where the timestamp resets in each one. This script solves that problem by intelligently merging multiple .asc files into a single, cohesive log. It automatically recalculates and adjusts the timestamps to be sequential across all files, making subsequent data analysis seamless.
