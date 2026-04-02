import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# To fix the import issue, add backend to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.features import load_and_engineer
from config import RAW_CSV

# Create public directory for frontend if it doesn't exist
# Or just save to local ml/plots folder for now
# We'll save to frontend/public/assets so it can be shown in demo if needed
PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frontend', 'public', 'assets')
os.makedirs(PLOTS_DIR, exist_ok=True)

def generate():
    print("Generating demo plots...")
    df = load_and_engineer(RAW_CSV)

    # 1. Congestion Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Congestion Level'], bins=30, kde=True, color='teal')
    plt.title('CommuteIQ — Bangalore Congestion Levels')
    plt.savefig(os.path.join(PLOTS_DIR, 'congestion_dist.png'))
    plt.close()

    # 2. Travel Time Comparison
    base = df['Travel Time Index'] * 20
    df['car_time']   = (base * (1 + (df['Congestion Level']/100.0) * 0.8)).round(1)
    df['bus_time']   = (base * (1 + (df['Congestion Level']/100.0) * 1.1)).round(1)
    df['metro_time'] = (base * (1 + (df['Congestion Level']/100.0) * 0.2)).round(1)

    plt.figure(figsize=(10, 6))
    modes = ['car_time', 'bus_time', 'metro_time']
    data_to_plot = [df[m].mean() for m in modes]
    plt.bar(['Car', 'Bus', 'Metro'], data_to_plot, color=['#ff6b6b', '#feca57', '#48dbfb'])
    plt.title('Average Predicted Travel Times across Bengaluru (Phase 1)')
    plt.ylabel('Minutes')
    plt.savefig(os.path.join(PLOTS_DIR, 'mode_comparison.png'))
    plt.close()

    print(f"Successfully generated 2 plots in {PLOTS_DIR}")

if __name__ == "__main__":
    generate()
