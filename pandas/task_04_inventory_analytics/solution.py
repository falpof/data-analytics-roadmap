import pandas as pd

products = pd.read_csv("products.csv")
inventory = pd.read_csv("inventory.csv")
receipts = pd.read_csv("receipts.csv")
sales = pd.read_csv("sales.csv")

# if there's no price, the price is taken from products.csv
unit_cost_map = products.set_index("product_id")["unit_cost"]
receipts["unit_cost"] = receipts["unit_cost"].fillna(
    receipts["product_id"].map(unit_cost_map)
)
# finding revenue per day
sales["revenue"] = sales["quantity"] * sales["sale_price"]
sales_analytics = (
    sales
    .merge(
        products,
        on="product_id"
    )
)

# date filtering
sales_analytics["sale_datetime"] = pd.to_datetime(
    sales_analytics["sale_datetime"]
)
sales_analytics["date"] = sales_analytics["sale_datetime"].dt.date

# counter of days and average sales for the period
count_days = (
    sales_analytics["sale_datetime"].max().date()
    - sales_analytics["sale_datetime"].min().date()
).days + 1
table_of_avg_sales = (
    sales_analytics
    .groupby("product_name")
    .agg(
        unit_sold=("quantity", "sum")
    )
    .reset_index()
)
table_of_avg_sales["avg_sales_per_date"] = (
    table_of_avg_sales["unit_sold"] / count_days
)

# sales analytics
sales_analytics["COGS"] = sales_analytics["quantity"] * sales_analytics["unit_cost"]
sales_analytics = (
    sales_analytics
    .groupby("product_name")
    .agg(
        revenue=("revenue", "sum"),
        COGS=("COGS", "sum"),
        units_sold=("quantity", "sum")
    )
    .reset_index()
)
sales_analytics["profit"] = (
    sales_analytics["revenue"] - sales_analytics["COGS"]
)

#inventory analytics
inventory_analitycs = (
    inventory
    .merge(
        products,
        on="product_id"
    )
    .groupby("product_name")
    .agg(
        avg_inventory=("closing_stock", "mean"),
        min_leftover=("closing_stock", "min"),
        max_leftover=("closing_stock", "max")
    )
    .reset_index()
)
# finding the money spent on purchase
receipts["purchase_cost"] = (
    receipts["quantity_received"] * receipts["unit_cost"]
)
# supply analytics :)
supply_analytics = (
    receipts
    .merge(
        products,
        on="product_id"
    )
    .groupby("product_name")
    .agg(
        unit_received=("quantity_received", "sum"),
        purchase_cost=("purchase_cost", "sum")
    )
)

# finding initial stock of first day
initial_stock = (
    inventory
    .merge(
        products,
        on="product_id"
    )
    .reset_index()
    .sort_values(
        "date",
        ascending=True
    )
    .drop_duplicates(
        subset="product_id"
    )
)
# finding current leftover of last day after closing
current_leftover = (
    inventory
    .merge(
        products,
        on="product_id"
    )
    .reset_index()
    .sort_values(
        "date",
        ascending=False
    )
    .drop_duplicates(
        subset="product_id"

    )
)
# summary of all tables
common_metrics = (
    sales_analytics
    .merge(
        inventory_analitycs,
        on="product_name"
    )
    .merge(
        supply_analytics,
        on="product_name"
    )
    .merge(
        initial_stock[
            [
                "product_name",
                "opening_stock"
            ]
        ],
        on="product_name"
    )
    .merge(
        current_leftover[
            [
                "product_name",
                "closing_stock"
            ]
        ],
        on="product_name"
    )    
    .merge(
        table_of_avg_sales[
            [
                "product_name",
                "avg_sales_per_date"
            ]
        ],
        on="product_name"
    )
)
# measures how quickly inventory is sold and replaced over a given period
common_metrics["inventory_turnover"] = common_metrics["units_sold"] / common_metrics["avg_inventory"]
# measures the percentage of available inventory that was sold during the analyzed period
common_metrics["sell_through_rate"] = (
    common_metrics["units_sold"]
    /  
    (common_metrics["opening_stock"] + common_metrics["unit_received"])
    * 100
)

# low and high line of turnover
low_line = common_metrics["inventory_turnover"].quantile(0.25)
high_line = common_metrics["inventory_turnover"].quantile(0.65)
# distribution of classifications
common_metrics["movement_class"] = "medium_moving"
common_metrics.loc[
    high_line < common_metrics["inventory_turnover"],
    "movement_class"
] = "fast_moving"
common_metrics.loc[
    low_line > common_metrics["inventory_turnover"],
    "movement_class"
] = "slow_moving"

# estimates how many days the current inventory will last
common_metrics["days_of_inventory"] = (
    common_metrics["closing_stock"] / common_metrics["avg_sales_per_date"]
)

# indicates the risk of running out of stock
common_metrics["stockout_risk"] = "medium_risk"
common_metrics.loc[
    common_metrics["days_of_inventory"] < 7,
    "stockout_risk"
] = "high_risk"
common_metrics.loc[
    common_metrics["days_of_inventory"] > 14,
    "stockout_risk"
] = "low_risk"


# save as csv
common_metrics.to_csv(
    "common_metrics.csv",
    index=False
)