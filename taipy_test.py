import pandas as pd
import numpy as np
from taipy import Gui
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load the dataset
def load_dataset(file_path):
    return pd.read_csv(file_path)

# Group the data by category and item
def prepare_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    grouped_data = df.groupby(['Category', 'Item'])
    return grouped_data

# Plot graphs for all categories and items
def plot_graphs(grouped_data):
    plots = {}
    for (category, item), group in grouped_data:
        plt.figure(figsize=(10, 6))
        plt.plot(group['Date'], group['Value'], marker='o', label=f"{item}")
        plt.title(f"Category: {category} | Item: {item}")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid()
        plot_path = f"plot_{category}_{item}.png"
        plt.savefig(plot_path)
        plt.close()
        plots[(category, item)] = plot_path
    return plots

# Predict future values
def predict_future_values(grouped_data, forecast_days=30):
    predictions = {}
    for (category, item), group in grouped_data:
        group = group.sort_values('Date')
        dates = group['Date'].map(datetime.toordinal).values.reshape(-1, 1)
        values = group['Value'].values.reshape(-1, 1)
        
        # Train a simple Linear Regression model
        model = LinearRegression()
        model.fit(dates, values)
        
        # Predict future values
        last_date = group['Date'].max()
        future_dates = [(last_date + timedelta(days=i)).toordinal() for i in range(1, forecast_days + 1)]
        future_values = model.predict(np.array(future_dates).reshape(-1, 1)).flatten()
        
        predictions[(category, item)] = {
            "dates": [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)],
            "values": future_values.tolist()
        }
    return predictions

# Taipy GUI integration
def create_dashboard(df, predictions, plots):
    categories = df['Category'].unique().tolist()
    selected_category = categories[0]
    
    def update_selected_category(category):
        return category

    gui_content = f"""
    <|layout|columns=1 1 1 1|
    <|{categories}|selector|value={selected_category}|on_change=update_selected_category|label=Select Category|>
    |>
    <|table|columns=Date, Item, Value|rows={df[df['Category'] == selected_category].to_dict('records')}|>
    <|{plots}|plot|height=400px|width=600px|>
    """
    
    Gui(page=gui_content).run()

# Main program
if __name__ == "__main__":
    dataset_path = "your_dataset.csv"  # Replace with the path to your dataset
    df = load_dataset(dataset_path)
    
    grouped_data = prepare_data(df)
    plots = plot_graphs(grouped_data)
    predictions = predict_future_values(grouped_data)
    
    # Create Taipy Dashboard
    create_dashboard(df, predictions, plots)