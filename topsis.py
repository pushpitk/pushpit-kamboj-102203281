# topsis_shyam_10155792/topsis.py

import sys
import pandas as pd
import numpy as np

def topsis(input_file, weights, impacts, output_file):
    """
    Perform TOPSIS on the given input file and produce the result file.
    """
    # 1. Read data (assuming input_file is CSV)
    df = pd.read_csv(input_file)
    
    # Basic validations
    if df.shape[1] < 3:
        raise Exception("Input file must contain three or more columns.")
    # The first column is object name, from second to last are numeric columns
    numeric_data = df.iloc[:, 1:].values
    if not np.issubdtype(numeric_data.dtype, np.number):
        raise Exception("From 2nd to last columns must contain numeric values only.")
    
    # Parse weights
    weights_list = [float(w.strip()) for w in weights.split(",")]
    # Parse impacts
    impacts_list = [i.strip() for i in impacts.split(",")]
    
    # More validations
    if len(weights_list) != len(impacts_list):
        raise Exception("Number of weights and number of impacts must be the same.")
    if len(weights_list) != (df.shape[1] - 1):
        raise Exception("Number of weights, impacts, and numeric columns must match.")
    for i in impacts_list:
        if i not in ['+', '-']:
            raise Exception("Impacts must be '+' or '-'.")
    
    # 2. Normalize the decision matrix
    #    Excluding the first column (names)
    R = numeric_data / np.sqrt((numeric_data**2).sum(axis=0))
    
    # 3. Multiply by weights
    for col in range(R.shape[1]):
        R[:, col] = R[:, col] * weights_list[col]
    
    # 4. Determine ideal best and ideal worst
    ideal_best = []
    ideal_worst = []
    for col in range(R.shape[1]):
        if impacts_list[col] == '+':
            ideal_best.append(R[:, col].max())
            ideal_worst.append(R[:, col].min())
        else:
            ideal_best.append(R[:, col].min())
            ideal_worst.append(R[:, col].max())
    
    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)
    
    # 5. Calculate Euclidean distance from ideal best and ideal worst
    dist_best = np.sqrt(((R - ideal_best)**2).sum(axis=1))
    dist_worst = np.sqrt(((R - ideal_worst)**2).sum(axis=1))
    
    # 6. Calculate the TOPSIS score
    score = dist_worst / (dist_best + dist_worst)
    
    # 7. Rank
    rank = score.argsort()[::-1]  # indices of scores sorted descending
    # Create an array of ranks (1 = highest score)
    ranks = np.empty_like(rank)
    ranks[rank] = np.arange(1, len(score)+1)
    
    # 8. Append to original df
    df['Topsis Score'] = score.round(3)
    df['Rank'] = ranks
    
    # 9. Save to CSV
    df.to_csv(output_file, index=False)
    print(f"File saved successfully as {output_file}")

def main():
    """
    Entry point for console_scripts. 
    This function parses command line arguments, calls the topsis function, etc.
    """
    if len(sys.argv) != 5:
        print("Usage: python <script> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        print('Example: topsis 101556-data.csv "1,1,1,2" "+,+,-,+" 101556-result.csv')
        sys.exit(1)
    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]
    
    try:
        topsis(input_file, weights, impacts, output_file)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
