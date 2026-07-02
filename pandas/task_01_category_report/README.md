# Task 01 - Category Sales Report
The first Pandas project focused on data cleaning, transformation and aggregation

## Dataset
- `orders_dirty_100.csv`
The dataset contains coffee shop orders with drink names, prices and barista IDs
Some drink names contain formatting issues that need to be cleaned before analysis

## My task
- Clean inconsistent drink names
- Create drink categories
- Keep only drinks that cost more than 35 AED
- Calculate:
  - total sales
  - total revenue
  - average check
  - number of unique drinks in each category
- Mark premium categories based on the average check
- Export the final report as a CSV file

## What I practiced
- String cleaning
- `replace()`
- `map()`
- `query()`
- `groupby()`
- `agg()`
- `nunique()`
- `loc`
- `sort_values()`
- `to_csv()`

## Files
- `solution.py` – my solution
- `orders_dirty_100.csv` – dataset
- `report.csv` – generated report

## Status
✅ Completed