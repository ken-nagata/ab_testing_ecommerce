# E-commerce A/B Testing

A hands-on A/B testing project based on the [Kaggle e-commerce dataset](https://www.kaggle.com/datasets/ahmedmohameddawoud/ecommerce-ab-testing).

## Goal
Test whether a new landing page drives a statistically significant lift in conversion rate vs the old page.

## Methods
- Frequentist hypothesis testing (z-test for proportions)
- Power analysis and sample size calculation
- Logistic regression for covariate analysis

## Project Structure
```
ab_testing/
├── data/
│   ├── raw/          # original dataset (not tracked)
│   └── processed/    # cleaned data (not tracked)
├── notebooks/        # EDA and analysis notebooks
├── src/              # reusable Python modules
├── tests/            # unit tests
├── pyproject.toml
└── README.md
```

## Setup
```bash
poetry install
poetry run jupyter notebook
```