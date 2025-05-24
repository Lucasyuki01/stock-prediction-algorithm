
# 📈 Stock Prediction Algorithm

This project is part of my **undergraduate thesis (TCC)** in Computer Science and focuses on using **Machine Learning** techniques to forecast the behavior of financial assets in the Brazilian stock market (B3).

## 🎯 Objective

To evaluate the performance of different machine learning models in predicting stock movement (buy, hold, sell) based on technical indicators, and to compare the resulting portfolios in terms of **Sharpe Ratio** and **Maximum Drawdown (MDD)**.

## 🧠 Technologies and Techniques Used

- **Machine Learning Models**:
  - Random Forest
  - XGBoost
  - Support Vector Machines (SVM)

- **Indicators and Features**:
  - RSI (Relative Strength Index)
  - MACD
  - Volatility
  - Z-score

- **Backtesting Strategy**:
  - Portfolio selection based on classification results
  - Evaluation using Sharpe Ratio and MDD
  - Data split: ~10 years total; last 3 for testing, 1 for validation, rest for training

- **Tools and Libraries**:
  - Python
  - scikit-learn
  - pandas, numpy
  - matplotlib, seaborn

## 🗂️ Project Structure

```
stock-prediction-algorithm/
├── data/                     # Raw and processed stock data
├── models/                   # Trained models and reports by asset
├── src/                      # Source code (feature engineering, training, evaluation)
├── utils/                    # Utility functions
├── indicadores/              # Financial indicators implementation
├── setups_run.ipynb          # Orchestration of model setups
├── summary.ipynb             # Final performance summary
├── summary_return.ipynb      # Return and risk analysis
└── README.md
```

## 📊 Results

The final section compares the strategies built from each algorithm using:
- Sharpe Ratio
- Maximum Drawdown
- Return distribution
- Asset selection frequency

Graphs and tables were generated to support discussion and performance comparison.

## 🧪 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Lucasyuki01/stock-prediction-algorithm.git
   cd stock-prediction-algorithm
   ```

2. (Optional) Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. Run the main notebooks:
   - `setups_run.ipynb`
   - `summary.ipynb`
   - `summary_return.ipynb`

Ensure the data is correctly placed in the `data/` folder and the models in `models/`.

## 👨‍💻 Author

Developed by **Lucas Yuki**  
Final undergraduate thesis (TCC) in Computer Science – UNESP (2024)

**Advisor**: Prof. Dr. Mateus Roder  
**Co-advisor**: Prof. Dr. André Debiaso

## 📜 License

This project is licensed under the MIT License.
