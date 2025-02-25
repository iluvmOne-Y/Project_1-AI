import json
import glob
import os
from datetime import datetime

def load_json_files(results_dir='.'):
    """Load all JSON files from results directory"""
    data = {}
    for filename in glob.glob(os.path.join(results_dir, '*.json')):
        with open(filename, 'r') as f:
            level_data = json.load(f)
            for entry in level_data:
                level = entry['level']
                algo = entry['algorithm']
                if level not in data:
                    data[level] = {}
                if algo not in data[level]:
                    data[level][algo] = entry
    return data

def format_table(data):
    """Convert data to formatted table string"""
    # Header
    table = "| Timeout : 1800s |  |  |  |  |  |  |  |  |  |  |  |  |\n"
    table += "| Số thư tự | BFS |  |  | DFS |  |  | UCS |  |  | $A^*$ |  |  |\n"
    table += "|  | Storage (MB) | States (state) | Time (s) | Storage (MB) | States (state) | Time (s) | Storage (MB) | States (state) | Time (s) | Storage (MB) | States (state) | Time (s) |\n"

    # Data rows
    max_level = max(data.keys()) if data else 5
    for level in range(1, max_level + 1):
        row = [str(level)]
        algo_names = {
            'BFS': 'BFS',
            'DFS': 'DFS', 
            'UCS': 'UCS',
            'A*': 'AStar'  # This maps display name 'A*' to JSON name 'AStar'
        }
        for algo in ['BFS', 'DFS', 'UCS', 'AStar']:
            if level in data and algo in data[level]:
                entry = data[level][algo]
                # Convert memory from "1.70MB" to "1,70"
                memory = entry['memory'].replace('.', ',').rstrip('MB')
                # Convert time from "0.16s" to "0,16"
                time = entry['time'].replace('.', ',').rstrip('s')
                row.extend([
                    memory,
                    entry['nodes'],
                    time
                ])
            else:
                row.extend(['NULL', 'NULL', 'NULL'])
        table += f"| {' | '.join(row)} |\n"

    return table

def main():
    # Load JSON data
    data = load_json_files()
    
    # Convert to table format
    table = format_table(data)
    
    # Save to file
    output_file = 'algorithm_comparison.txt'
    with open(output_file, 'w') as f:
        f.write(table)
    
    print(f"Table has been generated and saved to {output_file}")
    print("\nGenerated Table:")
    print(table)

if __name__ == "__main__":
    main()