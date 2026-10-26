# 📈 Stock Prediction Algorithm

ML-based trading strategy for the Brazilian stock market (B3), developed as an undergraduate thesis at UNESP (2024).

Three machine learning models — Random Forest, XGBoost, and SVM — were used to classify stock movements (buy / hold / sell) based on technical indicators, and to build portfolios evaluated against the Ibovespa benchmark.

---

## 🏆 Results (Jan 2022 – Oct 2024)

| Model | Cumulative Return | Sharpe Ratio |
|---|---|---|
| **XGBoost** | **254.4%** | **1.731** |
| SVM | 229.7% | 1.357 |
| Random Forest | 157.6% | 1.018 |
| Ibovespa (benchmark) | 20.9% | 0.340 |

All three models significantly outperformed the Ibovespa benchmark in both return and risk-adjusted performance. XGBoost achieved the highest Sharpe Ratio (1.731), while Random Forest delivered the most stable equity curve with controlled drawdown.

## ⚠️ Limitations

- Results come from a historical backtest (Jan 2022 to Oct 2024), not from live trading.
- The test window covers a single period of the Brazilian market, so performance may not hold in other market conditions.
- Assets were selected using validation-period Sharpe Ratio (2020 to 2021), which can favor assets that simply performed well in that window.
- The Ibovespa is a broad index, while the strategy holds a selected subset of assets, so the comparison is not like for like.

## 🔭 Next steps

- Walk-forward validation across several test periods to check how stable the results are.
- Paper trading to compare live signals against the backtest.


---

## 🧠 How it works

Stock price movement was framed as a 3-class classification problem:

- **-1** → Sell signal (expected price drop)
- **0** → Hold (sideways movement within a threshold)
- **1** → Buy signal (expected price rise)

Models were trained on 10 years of historical data (2010–2019), validated on 2020–2021, and tested on 2022–2024 — strict temporal splits to prevent data leakage.

### Features used

Technical indicators computed from OHLCV data:

`RSI` · `MACD` · `Volatility` · `Z-Score` · `VWAP` · `CCI` · `SOSC` · `Detrend` · `Lag features` · `Price direction (Dir / Dir_p)`

### Portfolio selection strategy

For each model, assets were selected from the top 25% Sharpe Ratio performers on the validation set, filtered by Maximum Drawdown (MDD). This strategy was then applied to the test set with no lookahead bias.

---

## 🗂️ Project Structure

```
stock-prediction-algorithm/
├── Project_stock prediction algorithm/
│   ├── src/               # Feature engineering, training, evaluation
│   ├── models/            # Trained models and reports per asset
│   ├── data/              # Raw and processed stock data
│   ├── indicadores/       # Financial indicators implementation
│   ├── utils/             # Utility functions
│   ├── setups_run.ipynb   # Model training and grid search orchestration
│   ├── summary.ipynb      # Performance summary
│   └── summary_return.ipynb  # Return and risk analysis
├── Monograph-final-work.pdf  # Full undergraduate thesis (Portuguese)
└── README.md
```

---

## 🚀 How to Run

```bash
git clone https://github.com/Lucasyuki01/stock-prediction-algorithm.git
cd stock-prediction-algorithm
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Then open and run the notebooks in order:
1. `setups_run.ipynb` — trains models with grid search
2. `summary.ipynb` — evaluates Sharpe and MDD per asset
3. `summary_return.ipynb` — cumulative return analysis

> Data is fetched automatically via `yfinance`. Place any local CSVs in `data/`.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-189ABF?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)

---

## 👨‍💻 Author

**Lucas Yuki Nishimoto**
Undergraduate thesis in Computer Science — UNESP, Bauru, Brazil (2024)

**Advisor:** Prof. Dr. Mateus Roder
**Co-advisor:** Prof. Dr. André Debiaso Rossi

📄 [Full thesis (PDF)](./Monograph-final-work.pdf)
