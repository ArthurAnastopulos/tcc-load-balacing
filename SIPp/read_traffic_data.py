import pandas as pd
import argparse
from datetime import datetime
import matplotlib.pyplot as plt

def calculate_jitter_and_latency(df):
    # Convert the Timestamp column to datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Calculate inter-packet time differences
    df['Inter-Arrival Time'] = df['Timestamp'].diff().dt.total_seconds()
    
    # Calculate jitter using RTP formula: mean of absolute differences of inter-arrival times
    df['Jitter'] = df['Inter-Arrival Time'].rolling(window=2).apply(lambda x: abs(x[1] - x[0]), raw=True)
    
    # Fill NaN values that result from rolling window with the previous value
    df['Jitter'] = df['Jitter'].fillna(method='bfill')
    
    # Calculate cumulative sum of jitter and the average jitter
    df['Cumulative Jitter'] = df['Jitter'].cumsum()
    df['Average Jitter'] = df['Cumulative Jitter'] / (df.index + 1)
    
    # Calculate latency (assuming we have a reference timestamp for calculating latency)
    reference_time = df['Timestamp'].iloc[0]
    df['Latency'] = (df['Timestamp'] - reference_time).dt.total_seconds()
    
    return df

def plot_jitter(df):
    # Ensure no NaN values in Jitter column for plotting
    df = df.dropna(subset=['Jitter'])

    # Resample data for better visualization (e.g., plot every 100th point)
    sample_df = df.iloc[::100]

    # Convert columns to numpy arrays
    timestamps = sample_df['Timestamp'].values
    jitter = sample_df['Jitter'].values

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, jitter, marker='o', linestyle='-', color='b')
    plt.title('Jitter Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Jitter (seconds)')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to make room for rotated labels
    plt.show()

def plot_average_jitter(df):
    # Ensure no NaN values in Average Jitter column for plotting
    df = df.dropna(subset=['Average Jitter'])

    # Convert columns to numpy arrays
    timestamps = df['Timestamp'].values
    average_jitter = df['Average Jitter'].values

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, average_jitter, marker='o', linestyle='-', color='r')
    plt.title('Average Jitter Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Average Jitter (seconds)')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to make room for rotated labels
    plt.show()

def plot_latency(df):
    # Ensure no NaN values in Latency column for plotting
    df = df.dropna(subset=['Latency'])

    # Convert columns to numpy arrays
    timestamps = df['Timestamp'].values
    latency = df['Latency'].values

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, latency, marker='o', linestyle='-', color='g')
    plt.title('Latency Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Latency (seconds)')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to make room for rotated labels
    plt.show()

def main():
    # Argument parser for command line arguments
    parser = argparse.ArgumentParser(description='Process network traffic CSV file to calculate jitter and latency.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file.')
    args = parser.parse_args()
    
    # Read the CSV file
    df = pd.read_csv(args.csv_file)
    
    # Calculate jitter and latency
    df = calculate_jitter_and_latency(df)
    
    # Print the resulting dataframe
    print(df)
    
    # Plot jitter, average jitter, and latency
    plot_jitter(df)
    plot_average_jitter(df)
    plot_latency(df)
    
    # Optionally, save the dataframe to a new CSV file
    output_file = 'output_with_jitter_latency.csv'
    df.to_csv(output_file, index=False)
    print(f'Results saved to {output_file}')

if __name__ == "__main__":
    main()
