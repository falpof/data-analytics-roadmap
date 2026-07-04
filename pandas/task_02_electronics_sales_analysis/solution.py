import pandas as pd

orders = pd.read_csv("orders_electronics_dirty_150.csv")

orders["category"] = orders["category"].str.strip().str.title()
orders["product"] = orders["product"].str.strip().str.title()

# Normalize product names by correcting capitalization and official brand/model naming.
orders["product"] = (
    orders["product"]
    .replace(
        {
            "Macbook Air M3":"MacBook Air M3",
            "Lg Ultrafine":"LG UltraFine",
            "Airpods Pro":"AirPods Pro",
            "Asus Proart":"ASUS ProArt",
            "Asus Zenbook":"ASUS Zenbook",
            "Bose Qc":"Bose QC",
            "Dell Ultrasharp":"Dell UltraSharp",
            "Dell Xps 13":"Dell XPS 13",
            "Iphone 16":"iPhone 16",
            "Logitech Mx Keys":"Logitech MX Keys",
            "Nuphy Air75":"NuPhy Air75",
            "Sony Wh-1000Xm6":"Sony WH-1000XM6",
            "Thinkpad X1":"ThinkPad X1"
        }
    )
)



median_in_orders = orders["price"].median()
total_revenue = orders["price"].sum()
total_sales = orders["product"].count()
total_avg_price = orders["price"].mean()


electronics_analysis = (
    orders
    .groupby("category")
    .agg(
        sales=("product", "count"),
        revenue=("price", "sum"),
        avg_price=("price", "mean"),
        unique_products=("product", "nunique"),
    )
    .reset_index()
)
electronics_analysis["avg_price"] = electronics_analysis["avg_price"].round(2)

electronics_analysis["segment"] = "Regular"
electronics_analysis.loc[
    electronics_analysis["avg_price"] > median_in_orders,
    "segment"
] = "Premium"

electronics_analysis["revenue_share_percent"] = (
    electronics_analysis["revenue"]
    * 100
    / total_revenue
).round(2)

electronics_analysis["sales_share_percent"] = (
    electronics_analysis["sales"]
    * 100
    / total_sales
).round(2)

# Additional metric for identifying the higher-priced category
electronics_analysis["above_avg_price"] = "No"
electronics_analysis.loc[
    electronics_analysis["avg_price"] > total_avg_price,
    "above_avg_price"
] = "Yes"


# This table is for finding out the most expensive product in the category
most_expensive = ( 
    orders
    .groupby(["category", "product", "price"])
    .agg(
        sales_per_product=("product", "count")
    )
    .reset_index()
    .sort_values(
        ["category", "price", "product", "sales_per_product"],
        ascending=[True, False, True, False]
    )
    .drop_duplicates(
        subset="category"
    )
)
most_expensive = most_expensive.rename(columns={"product":"most_expensive_product"})

# This table is for finding out the cheapest product in the category
cheapest = ( 
    orders
    .groupby(["category", "product", "price"])
    .agg(
        sales_per_product=("product", "count")
    )
    .reset_index()
    .sort_values(
        ["category", "price", "product", "sales_per_product"],
        ascending=[True, True, True, False]
    )
    .drop_duplicates(
        subset="category"
    )
)
cheapest = cheapest.rename(columns={"product":"cheapest_product"})


merging_tables = (
    electronics_analysis
    .merge(
        most_expensive,
        on="category"
    )
    .merge(
        cheapest,
        on="category"
    )
)


report = (
    merging_tables[
        [
            "category",
            "unique_products",
            "sales",
            "sales_share_percent",
            "revenue",
            "revenue_share_percent",
            "avg_price",
            "above_avg_price",
            "segment",
            "most_expensive_product",
            "cheapest_product"
        ]
    ]
    .sort_values(
        ["segment", "above_avg_price", "revenue",  "sales"],
        ascending=[True, False, False, False]
    )
)



report.to_csv(
    "report.csv",
    index=False
)