import pandas as pd
import matplotlib.pyplot as plt
import argparse

def read_csv_and_plot(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Convert the first column to datetime and set as index
    df['Date'] = pd.to_datetime(df.iloc[:, 0])
    df.set_index('Date', inplace=True)
    
    # Plotting Variable_A and Variable_B
    plt.figure(figsize=(10, 5))
    plt.plot(df['Variable_A'], label='Variable_A')
    plt.plot(df['Variable_B'], label='Variable_B')

    # Adding labels and title
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Graph of Variable_A and Variable_B over Time')
    plt.legend()

    # Save the plot to the same directory as the script
    plt.savefig('graph_Variable_A_B.png')
    
    # Show the plot
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='Path to the CSV file')

    args = parser.parse_args()

    read_csv_and_plot(args.file_path)