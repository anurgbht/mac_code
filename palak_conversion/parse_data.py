# uv run python palak_conversion/parse_data.py

import os
from tqdm import tqdm

def process_file(file_name, parsed_file_name):

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


if __name__ == "__main__":

    input_dir = os.path.join("palak_conversion", "data/input")
    output_dir = os.path.join("palak_conversion", "data/parsed")

    for file in os.listdir(input_dir):
        if file.endswith(".tabular"):
            file_name = os.path.join(input_dir, file)
            parsed_file_name = file_name.replace("data/input", "data/parsed").replace(".tabular", "_parsed.txt")
            process_file(file_name, parsed_file_name)
    