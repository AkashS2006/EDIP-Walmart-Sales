# Walmart Sales Analysis

Team project analyzing the Walmart Sales Forecasting dataset (Store, Department,
and Weekly Sales data, combined with store features like weather, fuel price,
CPI, unemployment, and holiday flags).

## Team

| Name | GitHub Handle | Role (Week 1) |
|------|---------------|---------------|
| A    | @handle       | SQLite schema + data load |
| B    | @handle       | Individual EDA |
| C    | @handle       | Individual EDA |

## Project Structure

```
walmart-sales-analysis/
├── data/
│   ├── raw/            # Original downloaded CSVs (gitignored, not committed)
│   └── processed/      # Cleaned data exports (gitignored, not committed)
├── notebooks/
│   └── eda_shared.ipynb   # Combined team EDA notebook
├── db/
│   └── walmart.db      # SQLite database (gitignored if large, or use Git LFS)
├── src/
│   ├── schema.py        # Creates SQLite tables
│   └── load_data.py      # Cleans raw data and loads into SQLite
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/yourteam/walmart-sales-analysis.git
   cd walmart-sales-analysis
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Download the dataset (Walmart Sales Forecasting, Kaggle) and place these
   files in `data/raw/`:
   - `stores.csv`
   - `features.csv`
   - `train.csv`

4. Run the schema + load scripts:
   ```bash
   python src/schema.py
   python src/load_data.py
   ```

5. Open `notebooks/eda_shared.ipynb` in VS Code or Jupyter to explore.

## Week 1 Deliverables

- [ ] Cleaned data loaded into `db/walmart.db`
- [ ] Shared EDA notebook with combined findings from all teammates

## Branching Convention

- `main` — always working/stable
- `feature/<name>` — individual work, merged via pull request
- Commit early, commit often, write clear messages
