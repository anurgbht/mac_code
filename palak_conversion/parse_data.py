# uv run python palak_conversion/parse_data.py

import os
from tqdm import tqdm

file_name = os.path.join("palak_conversion", "Galaxy61-[S Replace Text on dataset 58].tabular")
parsed_file_name = os.path.join("palak_conversion", "parsed_data.txt")

with open(file_name, 'r') as f:
    total_lines = sum(1 for _ in f)

with open(file_name, 'r') as file:
    count = 0
    line = file.readline()  # Read the first line
    pbar = tqdm(total=total_lines, unit="lines")
    while len(line) > 0:  # Read lines until the end of the file
        split_line = line.split()

        if len(split_line) >= 2:
            first_value = split_line[0]
            second_value = split_line[1]
        else:
            second_value = split_line[0] if len(split_line) > 0 else None

        with open(parsed_file_name, 'a') as parsed_file:
            parsed_file.write(f"{first_value} {second_value}\n")

        line = file.readline()  # Read the next line for the next iteration
        count += 1
        pbar.update(1)
        # if count > 160:  # Limit to reading 10 lines for demonstration
        #     break
    pbar.close()