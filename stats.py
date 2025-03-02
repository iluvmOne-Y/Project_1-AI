import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os

class StatsVisualizer:
    def __init__(self, data):
        self.styles = getSampleStyleSheet()
        self.chart_path = "results/temp_charts"
        self.data = data
        self.df = self.parse_data()
        
        # Ensure the chart directory exists
        os.makedirs(self.chart_path, exist_ok=True)
        print("DataFrame after parsing:", self.df)  # Debug: Print the DataFrame to verify Level 1

    def parse_data(self):
        """Parse the input data into a DataFrame with four algorithms: BFS, DFS, UCS, A*."""
        lines = self.data.strip().split('\n')[2:]  # Skip header lines (adjusted to 2 based on your success)
        parsed_data = []
        for i, line in enumerate(lines, 1):  # Enumerate all lines for debugging
            if line.strip():
                try:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    print(f"Line {i}, Raw parts: {parts}")  # Debug: Print raw parts
                    if len(parts) < 13:  # Ensure we have enough columns
                        print(f"Warning: Skipping line {i} due to insufficient parts: {parts}")
                        continue
                    level = int(parts[0])
                    print(f"Processing Level: {level}, Parts: {parts}")  # Debug: Check each level
                    row = {
                        'level': level,
                        'BFS_storage': float(parts[1].replace(',', '.')) if parts[1].strip() != 'NULL' else None,
                        'BFS_states': int(parts[2]) if parts[2].strip() != 'NULL' else None,
                        'BFS_time': float(parts[3].replace(',', '.')) if parts[3].strip() != 'NULL' else None,
                        'DFS_storage': float(parts[4].replace(',', '.')) if parts[4].strip() != 'NULL' else None,
                        'DFS_states': int(parts[5]) if parts[5].strip() != 'NULL' else None,
                        'DFS_time': float(parts[6].replace(',', '.')) if parts[6].strip() != 'NULL' else None,
                        'UCS_storage': float(parts[7].replace(',', '.')) if parts[7].strip() != 'NULL' else None,
                        'UCS_states': int(parts[8]) if parts[8].strip() != 'NULL' else None,
                        'UCS_time': float(parts[9].replace(',', '.')) if parts[9].strip() != 'NULL' else None,
                        'AStar_storage': float(parts[10].replace(',', '.')) if parts[10].strip() != 'NULL' else None,
                        'AStar_states': int(parts[11]) if parts[11].strip() != 'NULL' else None,
                        'AStar_time': float(parts[12].replace(',', '.')) if parts[12].strip() != 'NULL' else None
                    }
                    parsed_data.append(row)
                except (ValueError, IndexError) as e:
                    print(f"Error parsing line {i}: {e}, Line content: {line}")
                    continue
        df = pd.DataFrame(parsed_data)
        if not df.empty:
            print("Sorted DataFrame by level:", df.sort_values('level'))  # Debug: Verify levels are sorted
        return df

    def generate_pdf(self):
        """Generate a PDF report with a restructured table, charts, and statistical summary."""
        pdf_path = f"results/algorithm_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)  # Keep portrait orientation
        elements = []

        # Title (slightly smaller)
        self.styles['Title'].fontSize = 13  # Reduced from 14
        elements.append(Paragraph("Sokoban Algorithm Performance Report", self.styles['Title']))
        elements.append(Spacer(1, 14))  # Slightly reduced spacing

        # Restructured Data Table
        self.styles['Heading1'].fontSize = 11  # Reduced from 12
        elements.append(Paragraph("BFS vs DFS vs UCS vs A* Comparison on 10 Maps", self.styles['Heading1']))
        elements.append(Spacer(1, 7))  # Slightly reduced spacing

        # Prepare the pivoted table
        df = self.df
        print("DataFrame for table generation:", df)  # Debug: Verify DataFrame before table creation
        if df.empty:
            print("Warning: DataFrame is empty, no data to display!")
            return

        # Ensure all levels (1-10) are included, even if missing, by filling with NULL if necessary
        all_levels = range(1, 11)  # Ensure levels 1 through 10
        table_data = [['Algorithm', 'Metric'] + [f"Level {i}" for i in all_levels]]
        algorithms = ['BFS', 'DFS', 'UCS', 'AStar']
        metrics = ['storage', 'states', 'time']
        metric_labels = ['Storage (MB)', 'States', 'Time (s)']

        for algo in algorithms:
            for metric, label in zip(metrics, metric_labels):
                row = [algo, label]
                for level in all_levels:
                    if level in df['level'].values:
                        value = df.loc[df['level'] == level, f'{algo}_{metric}'].values[0] if not df.loc[df['level'] == level, f'{algo}_{metric}'].empty else None
                    else:
                        value = None  # Fill missing levels with None (will display as NULL)
                    row.append(f"{value:.2f}" if pd.notna(value) and metric != 'states' else str(int(value)) if pd.notna(value) and metric == 'states' else 'NULL')
                table_data.append(row)

        # Slightly reduce column widths and adjust font sizes to make table smaller
        total_width = 595  # Width of A4 portrait (accounting for margins, roughly 595 points)
        num_cols = 12 + 2  # Algorithm, Metric, and 10 levels
        base_col_width = total_width / num_cols  # Distribute width evenly
        col_widths = [int(base_col_width * 0.9)] * 2 + [int(base_col_width * 0.7)] * 10  # Slightly narrower

        data_table = Table(table_data, colWidths=col_widths)
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),  # Reduced from 10
            ('BOTTOMPADDING', (0, 0), (-1, 0), 7),  # Slightly reduced padding
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),  # Reduced from 8
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(data_table)
        elements.append(Spacer(1, 14))  # Slightly reduced spacing

        # Charts (slightly smaller)
        # Time comparison chart
        plt.figure(figsize=(9, 5))  # Slightly reduced from (10, 6)
        plt.plot(df['level'], df['BFS_time'], marker='o', label='BFS')
        plt.plot(df['level'], df['DFS_time'], marker='o', label='DFS')
        plt.plot(df['level'], df['UCS_time'], marker='o', label='UCS')
        plt.plot(df['level'], df['AStar_time'], marker='o', label='A*')
        plt.title('BFS vs DFS vs UCS vs A* Processing Time on 10 Maps', fontsize=9)  # Reduced from 10
        plt.xlabel('Level', fontsize=7)  # Reduced from 8
        plt.ylabel('Time (seconds)', fontsize=7)  # Reduced from 8
        plt.legend(fontsize=7)  # Reduced from 8
        plt.grid(True)
        time_chart = f'{self.chart_path}/time_comparison.png'
        plt.savefig(time_chart)
        plt.close()

        # Storage comparison chart
        plt.figure(figsize=(9, 5))  # Slightly reduced from (10, 6)
        plt.plot(df['level'], df['BFS_storage'], marker='o', label='BFS')
        plt.plot(df['level'], df['DFS_storage'], marker='o', label='DFS')
        plt.plot(df['level'], df['UCS_storage'], marker='o', label='UCS')
        plt.plot(df['level'], df['AStar_storage'], marker='o', label='A*')
        plt.title('BFS vs DFS vs UCS vs A* Storage Usage on 10 Maps', fontsize=9)
        plt.xlabel('Level', fontsize=7)
        plt.ylabel('Storage (MB)', fontsize=7)
        plt.legend(fontsize=7)
        plt.grid(True)
        storage_chart = f'{self.chart_path}/storage_comparison.png'
        plt.savefig(storage_chart)
        plt.close()

        # States comparison chart
        plt.figure(figsize=(9, 5))  # Slightly reduced from (10, 6)
        plt.plot(df['level'], df['BFS_states'], marker='o', label='BFS')
        plt.plot(df['level'], df['DFS_states'], marker='o', label='DFS')
        plt.plot(df['level'], df['UCS_states'], marker='o', label='UCS')
        plt.plot(df['level'], df['AStar_states'], marker='o', label='A*')
        plt.title('BFS vs DFS vs UCS vs A* States Explored on 10 Maps', fontsize=9)
        plt.xlabel('Level', fontsize=7)
        plt.ylabel('Number of States', fontsize=7)
        plt.legend(fontsize=7)
        plt.grid(True)
        states_chart = f'{self.chart_path}/states_comparison.png'
        plt.savefig(states_chart)
        plt.close()

        # Add charts to PDF (slightly smaller)
        for chart in [time_chart, storage_chart, states_chart]:
            if os.path.exists(chart):
                elements.append(Image(chart, width=380, height=230))  # Slightly reduced from 400, 250
                elements.append(Spacer(1, 14))  # Slightly reduced spacing

        # Statistical Summary Table (slightly smaller)
        self.styles['Heading1'].fontSize = 11  # Reduced from 12
        elements.append(Paragraph("Statistical Summary", self.styles['Heading1']))
        elements.append(Spacer(1, 7))  # Slightly reduced spacing
        stats_data = [
            ['Metric', 'BFS', 'DFS', 'UCS', 'A*'],
            ['Avg Time (s)', f"{df['BFS_time'].mean():.2f}", f"{df['DFS_time'].mean():.2f}", f"{df['UCS_time'].mean():.2f}", f"{df['AStar_time'].mean():.2f}"],
            ['Avg States', f"{int(df['BFS_states'].mean())}", f"{int(df['DFS_states'].mean())}", f"{int(df['UCS_states'].mean())}", f"{int(df['AStar_states'].mean())}"],
            ['Avg Storage (MB)', f"{df['BFS_storage'].mean():.2f}", f"{df['DFS_storage'].mean():.2f}", f"{df['UCS_storage'].mean():.2f}", f"{df['AStar_storage'].mean():.2f}"]
        ]
        stats_table = Table(stats_data, colWidths=[65] * 5)  # Slightly reduced from 70
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),  # Reduced from 10
            ('BOTTOMPADDING', (0, 0), (-1, 0), 7),  # Slightly reduced padding
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),  # Reduced from 8
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(stats_table)

        # Build the PDF
        doc.build(elements)
        print(f"PDF report generated: {pdf_path}")

