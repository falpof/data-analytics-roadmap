import pandas as pd


orders = pd.read_csv("orders_dirty_100.csv")
drink_category = {
    "Latte": "Milk Coffee",
    "Flat White": "Milk Coffee",
    "Espresso": "Classic Coffee",
    "Signature Coffee": "Signature",
    "Matcha": "Tea"
}



orders["drink"] = (
    orders["drink"]
    .str.strip()
    .str.title()
)
orders["drink"] = (
    orders["drink"]
    .replace(
        {
            "Mccoffee": "Signature Coffee"
        }
    )
)

orders = orders.query(
    "35 < price"
)
orders["category"] = (
    orders["drink"]
    .map(drink_category)
)


categories_analysis = (
    orders
    .groupby("category")
    .agg(
        sales=("drink", "count"),
        revenue=("price", "sum"),
        avg_check=("price", "mean"),
        unique_drinks=("drink", "nunique")
    )
    .reset_index()
)
categories_analysis["avg_check"] = categories_analysis["avg_check"].round(2)

categories_analysis["premium_category"] = "No"
categories_analysis.loc[
    categories_analysis["avg_check"] > 45,
    "premium_category"
] = "Yes"

report = (
    categories_analysis
    .sort_values(
        ["premium_category", "revenue"],
        ascending=[False, False]
    )
)


report.to_csv(
    "report.csv",
    index=False
)