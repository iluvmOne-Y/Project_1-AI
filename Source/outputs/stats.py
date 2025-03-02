import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os
import re
import glob

def parse_output_files():
    """Parse all output files and return a dataframe with the results."""
    data = []
    
    # Find all output files
    output_files = glob.glob("output-*.txt")
    
    for file_path in output_files:
        # Extract level number from filename
        level_match = re.search(r'output-(\d+)\.txt', file_path)
        if not level_match:
            continue
        
        level = int(level_match.group(1))
        
        # Read the file
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
        
        # Process each algorithm in the file
        i = 0
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                continue
                
            # Get algorithm name
            algorithm = lines[i].strip()
            
            # Process stats line
            if i + 1 < len(lines):
                stats_line = lines[i + 1]
                # Extract metrics using regular expressions
                steps_match = re.search(r'Steps: (\d+)', stats_line)
                weight_match = re.search(r'Weight: (\d+)', stats_line)
                node_match = re.search(r'Node: (\d+)', stats_line)
                time_match = re.search(r'Time \(ms\): ([\d\.]+)', stats_line)
                memory_match = re.search(r'Memory \(MB\): ([\d\.]+)', stats_line)
                
                steps = int(steps_match.group(1)) if steps_match else None
                weight = int(weight_match.group(1)) if weight_match else None
                node = int(node_match.group(1)) if node_match else None
                time_ms = float(time_match.group(1)) if time_match else None
                memory = float(memory_match.group(1)) if memory_match else None
                
                # Convert time to seconds for consistency with stats.py
                time_sec = time_ms / 1000 if time_ms is not None else None
                
                # Get solution path if available
                solution_path = lines[i + 2] if i + 2 < len(lines) else ""
                
                # Add to data
                data.append({
                    'level': level,
                    'algorithm': algorithm,
                    'steps': steps,
                    'weight': weight,
                    'nodes': node,
                    'time': time_sec,
                    'memory': memory,
                    'solution': solution_path
                })
                
            # Move to next algorithm
            i += 3
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.chart_path = "temp_charts"
        # Ensure the chart directory exists
        os.makedirs(self.chart_path, exist_ok=True)
        
    def generate_pdf(self, df):
        """Generate a PDF report with tables and charts comparing algorithm performance."""
        # Create a directory for results if it doesn't exist
        os.makedirs("results", exist_ok=True)
        
        pdf_path = f"results/algorithm_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        elements = []
        
        # Title
        elements.append(Paragraph("Sokoban Algorithm Performance Report", self.styles['Title']))
        elements.append(Spacer(1, 20))
        
        # Create a pivoted dataframe for easier comparison across levels
        pivot_df = pd.pivot_table(
            df, 
            values=['steps', 'weight', 'nodes', 'time', 'memory'],
            index=['level'],
            columns=['algorithm'],
            aggfunc='first'
        )
        
        # Get unique algorithms for table headers
        algorithms = df['algorithm'].unique().tolist()
        
        # Generate comparison table
        elements.append(Paragraph("Algorithm Performance Comparison by Level", self.styles['Heading1']))
        elements.append(Spacer(1, 10))
        
        # Create table for time comparison
        self._add_metric_table(elements, pivot_df, 'time', 'Time (s)', algorithms)
        elements.append(Spacer(1, 15))
        
        # Create table for node count comparison
        self._add_metric_table(elements, pivot_df, 'nodes', 'Nodes Expanded', algorithms)
        elements.append(Spacer(1, 15))
        
        # Create table for memory usage comparison
        self._add_metric_table(elements, pivot_df, 'memory', 'Memory Usage (MB)', algorithms)
        elements.append(Spacer(1, 15))
        
        # Create table for steps comparison
        self._add_metric_table(elements, pivot_df, 'steps', 'Solution Steps', algorithms)
        elements.append(Spacer(1, 15))
        
        # Create table for weight comparison
        self._add_metric_table(elements, pivot_df, 'weight', 'Total Weight', algorithms)
        elements.append(Spacer(1, 15))
        
        # Generate charts
        self._add_charts(elements, pivot_df, algorithms)
        
        # Generate statistical summary
        self._add_statistics_summary(elements, df, algorithms)
        
        # Build the PDF
        doc.build(elements)
        print(f"PDF report generated: {pdf_path}")
        
    def _add_metric_table(self, elements, pivot_df, metric, title, algorithms):
        """Add a table for a specific metric to the PDF."""
        elements.append(Paragraph(f"{title} Comparison", self.styles['Heading2']))
        elements.append(Spacer(1, 5))
        
        # Create table headers
        table_data = [['Level'] + algorithms]
        
        # Add data rows
        for level in sorted(pivot_df.index):
            row = [str(level)]
            for algo in algorithms:
                value = pivot_df.loc[level, (metric, algo)] if (metric, algo) in pivot_df.loc[level] else None
                if pd.isna(value):
                    row.append('N/A')
                elif metric == 'time':
                    row.append(f"{value:.2f}")
                elif metric in ['nodes', 'steps', 'weight']:
                    row.append(f"{int(value)}")
                else:  # memory
                    row.append(f"{value:.2f}")
            table_data.append(row)
        
        # Create table
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        
    def _add_charts(self, elements, pivot_df, algorithms):
        """Generate and add charts to the PDF."""
        elements.append(Paragraph("Performance Charts", self.styles['Heading1']))
        elements.append(Spacer(1, 10))
        
        # Time comparison chart
        self._create_chart(pivot_df, 'time', 'Processing Time (s)', algorithms)
        elements.append(Image(f"{self.chart_path}/time_comparison.png", width=450, height=280))
        elements.append(Spacer(1, 15))
        
        # Nodes comparison chart
        self._create_chart(pivot_df, 'nodes', 'Nodes Expanded', algorithms)
        elements.append(Image(f"{self.chart_path}/nodes_comparison.png", width=450, height=280))
        elements.append(Spacer(1, 15))
        
        # Memory comparison chart
        self._create_chart(pivot_df, 'memory', 'Memory Usage (MB)', algorithms)
        elements.append(Image(f"{self.chart_path}/memory_comparison.png", width=450, height=280))
        elements.append(Spacer(1, 15))
        
    def _create_chart(self, pivot_df, metric, title, algorithms):
        """Create a chart comparing algorithms by the given metric."""
        plt.figure(figsize=(10, 6))
        
        for algo in algorithms:
            if (metric, algo) in pivot_df.columns:
                plt.plot(
                    pivot_df.index, 
                    pivot_df[(metric, algo)], 
                    marker='o',
                    label=algo
                )
        
        plt.title(f'Algorithm Comparison: {title}')
        plt.xlabel('Level')
        plt.ylabel(title)
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{self.chart_path}/{metric}_comparison.png")
        plt.close()
        
    def _add_statistics_summary(self, elements, df, algorithms):
        """Add statistical summary of algorithm performance."""
        elements.append(Paragraph("Statistical Summary", self.styles['Heading1']))
        elements.append(Spacer(1, 10))
        
        # Calculate averages per algorithm
        summary_data = [['Metric'] + algorithms]
        
        metrics = {
            'Avg Time (s)': 'time',
            'Avg Nodes': 'nodes',
            'Avg Memory (MB)': 'memory',
            'Avg Steps': 'steps',
            'Avg Weight': 'weight'
        }
        
        for label, metric in metrics.items():
            row = [label]
            for algo in algorithms:
                values = df[df['algorithm'] == algo][metric]
                if len(values) > 0:
                    if metric in ['nodes', 'steps', 'weight']:
                        row.append(f"{int(values.mean())}")
                    else:
                        row.append(f"{values.mean():.2f}")
                else:
                    row.append('N/A')
            summary_data.append(row)
        
        # Create summary table
        t = Table(summary_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)

def main():
    # Parse output files
    df = parse_output_files()
    
    if df.empty:
        print("No data found in output files.")
        return
    
    # Generate PDF report
    report_generator = ReportGenerator()
    report_generator.generate_pdf(df)

if __name__ == "__main__":
    main()