# Task 02 - Electronics Sales Analysis
The second Pandas project focused on data cleaning, business metrics and report generation.

## Dataset
- `orders_electronics_dirty_150.csv`

The dataset contains electronics store orders with product names, categories, prices, cities and payment methods.
Some product and category names contain inconsistent formatting that must be cleaned before analysis.

## My task
- Clean inconsistent product and category names
- Normalize product names
- Calculate sales metrics for each category
- Calculate:
  - total sales
  - sales share (%)
  - total revenue
  - revenue share (%)
  - average product price
  - number of unique products
- Classify categories into Premium and Regular segments
- Identify categories with an above-average product price
- Find the most expensive and cheapest product in every category
- Export the final report as a CSV file

## Business decisions
- Categories with an average price above the global median price are classified as **Premium**
- Categories with an average price above the overall average price are marked as **Above Average**

## What I practiced
- String cleaning
- `replace()`
- `groupby()`
- `agg()`
- `median()`
- `mean()`
- `sum()`
- `count()`
- `nunique()`
- `loc`
- `merge()`
- `sort_values()`
- `drop_duplicates()`
- `rename()`
- `to_csv()`

## Files
- `solution.py`
- `orders_electronics_dirty_150.csv`
- `report.csv`
- `dashboard_preview,png` 

## Status
✅ Completed