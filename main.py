import pandas as pd
import matplotlib.pyplot as plt
import os

# Create directories for GitHub submission if they don't exist
os.makedirs('visualizations', exist_ok=True)
os.makedirs('report', exist_ok=True)

def main():
    print("Starting Weather Data Analysis...")

    # 1. DATA LOADING & CLEANING (With smart path checking)
    file_path = 'data/weather_data.csv'
    if not os.path.exists(file_path):
        file_path = 'weather_data.csv' # Fallback if it's in the same folder

    try:
        df = pd.read_csv(file_path)
        # Convert Date column to actual datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        # Handle any missing values
        df.fillna(0, inplace=True)
        print(f"Data loaded and cleaned successfully from '{file_path}'.")
    except FileNotFoundError:
        print("Error: weather_data.csv not found. Please ensure the file is in your folder.")
        return

    # 2. BASIC ANALYSIS
    avg_temp = df['Temperature_C'].mean()
    max_temp = df['Temperature_C'].max()
    total_precip = df['Precipitation_mm'].sum()
    
    print("\n--- Key Metrics ---")
    print(f"Average Temperature: {avg_temp:.2f}°C")
    print(f"Maximum Temperature: {max_temp}°C")
    print(f"Total Precipitation (100 Days): {total_precip}mm")

    # 3. VISUALIZATION 1: Line Chart (Daily Temperature Trends)
    # Using matplotlib to plot daily data over the 100 days
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Temperature_C'], color='crimson', linewidth=2)
    plt.title('Daily Temperature Changes Over 100 Days', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45) # Tilt the dates so they don't overlap
    plt.tight_layout()
    plt.savefig('visualizations/temperature_trend.png')
    plt.show() # Displays the chart in Spyder's Plot pane
    print("Saved and displayed Line Chart.")

    # 4. VISUALIZATION 2: Bar Chart (Total Precipitation by Month)
    # Group the daily data into monthly totals for a clean bar chart
    df['Month'] = df['Date'].dt.strftime('%B')
    monthly_precip = df.groupby('Month')['Precipitation_mm'].sum().reset_index()
    
    # Sort months chronologically rather than alphabetically
    month_order = ['January', 'February', 'March', 'April']
    monthly_precip['Month'] = pd.Categorical(monthly_precip['Month'], categories=month_order, ordered=True)
    monthly_precip = monthly_precip.sort_values('Month')

    plt.figure(figsize=(10, 6))
    plt.bar(monthly_precip['Month'], monthly_precip['Precipitation_mm'], color='dodgerblue', edgecolor='black')
    plt.title('Total Precipitation by Month', fontsize=14, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Precipitation (mm)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('visualizations/precipitation_bar.png')
    plt.show() # Displays the chart in Spyder's Plot pane
    print("Saved and displayed Bar Chart.")

    # 5. GENERATE REPORT
    report_content = f"""# Weather Data Analysis Report

## 1. Project Overview
This project analyzes daily weather patterns, specifically focusing on temperature trends and precipitation levels over a 100-day period.

## 2. Key Metrics
* **Average Temperature:** {avg_temp:.2f}°C
* **Highest Temperature:** {max_temp}°C
* **Total Precipitation:** {total_precip}mm

## 3. Meaningful Insights
* **Temperature Trends:** The line chart reveals a gradual upward trend in temperature from January to April, peaking at {max_temp}°C.
* **Precipitation Patterns:** The bar chart indicates varying levels of rainfall across the early months of the year, tracking a total of {total_precip}mm.
"""

    with open('report/analysis_report.md', 'w') as f:
        f.write(report_content)
    print("Saved Written Insights: report/analysis_report.md")
    print("\nProject execution complete! Check your folders for the outputs.")

if __name__ == "__main__":
    main()
    
