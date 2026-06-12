import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import pickle

# To fix the import issue, add backend to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.features import load_and_engineer, FEATURES
from config import RAW_CSV

# Presentation plots directory (saving directly to notebooks for easy access, and frontend)
PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frontend', 'public', 'assets')
DS_PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'notebooks', 'presentation_plots')

os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(DS_PLOTS_DIR, exist_ok=True)

def generate():
    print("Generating demo & presentation plots...")
    df = load_and_engineer(RAW_CSV)

    # Calculate simulated times for analysis if not present
    base = df['Travel Time Index'] * 20
    df['car_time']   = (base * (1 + (df['Congestion Level']/100.0) * 0.8)).round(1)
    df['bus_time']   = (base * (1 + (df['Congestion Level']/100.0) * 1.1)).round(1)
    df['metro_time'] = (base * (1 + (df['Congestion Level']/100.0) * 0.2)).round(1)

    # 1. Congestion Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Congestion Level'], bins=30, kde=True, color='teal')
    plt.title('Bangalore Congestion Level Distribution')
    plt.savefig(os.path.join(PLOTS_DIR, 'congestion_dist.png'))
    plt.close()

    # 2. Travel Time Comparison
    plt.figure(figsize=(10, 6))
    modes = ['car_time', 'bus_time', 'metro_time']
    data_to_plot = [df[m].mean() for m in modes]
    plt.bar(['Car', 'Bus', 'Metro'], data_to_plot, color=['#ff6b6b', '#feca57', '#48dbfb'])
    plt.title('Average Predicted Travel Times across Bengaluru')
    plt.ylabel('Minutes')
    plt.savefig(os.path.join(PLOTS_DIR, 'mode_comparison.png'))
    plt.close()

    # --- DATA SCIENCE PRESENTATION PLOTS ---

    # 3. Model Feature Importance
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'rf_car.pkl')
        with open(model_path, 'rb') as f:
            rf_model = pickle.load(f)
        
        importances = rf_model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=importances[indices], y=[FEATURES[i] for i in indices], palette='viridis')
        plt.title('Random Forest Feature Importance (Car Time Prediction)')
        plt.xlabel('Relative Importance')
        plt.tight_layout()
        plt.savefig(os.path.join(DS_PLOTS_DIR, 'feature_importance.png'))
        plt.close()
        print("Feature importance plot generated.")
    except Exception as e:
        print(f"Could not generate feature importance: {e}")

    # 4. Time of Day Impact on Travel Modes
    plt.figure(figsize=(12, 6))
    hourly_avg = df.groupby('hour')[['car_time', 'bus_time', 'metro_time']].mean()
    plt.plot(hourly_avg.index, hourly_avg['car_time'], marker='o', label='Car', color='#ff6b6b', linewidth=2)
    plt.plot(hourly_avg.index, hourly_avg['bus_time'], marker='s', label='Bus', color='#feca57', linewidth=2)
    plt.plot(hourly_avg.index, hourly_avg['metro_time'], marker='^', label='Metro', color='#48dbfb', linewidth=2)
    plt.title('Impact of Time of Day on Commute Durations (The Peak Hour Effect)')
    plt.xlabel('Hour of Day (24H format)')
    plt.ylabel('Average Travel Time (minutes)')
    plt.axvspan(8, 10, color='red', alpha=0.1, label='Morning Peak')
    plt.axvspan(17, 20, color='red', alpha=0.1, label='Evening Peak')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DS_PLOTS_DIR, 'time_of_day_impact.png'))
    plt.close()

    # 5. Congestion vs Travel Time
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df.sample(min(1000, len(df))), x='Congestion Level', y='car_time', alpha=0.5, label='Car', color='#ff6b6b')
    sns.scatterplot(data=df.sample(min(1000, len(df))), x='Congestion Level', y='metro_time', alpha=0.5, label='Metro', color='#48dbfb')
    plt.title('Congestion Vulnerability: Car vs Metro')
    plt.xlabel('Congestion Level (%)')
    plt.ylabel('Travel Time (minutes)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(DS_PLOTS_DIR, 'congestion_vulnerability.png'))
    plt.close()

    print(f"Successfully generated new Data Science presentation plots in {DS_PLOTS_DIR}")

if __name__ == "__main__":
    generate()
