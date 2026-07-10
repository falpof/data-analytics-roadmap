import pandas as pd

customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")
payments = pd.read_csv("payments.csv")

# Cleaning every csv on wrong columns
payments = payments.dropna(subset=["amount"])
payments["payment_method"] = payments["payment_method"].str.title().str.strip()
customers["city"] = customers["city"].str.title().str.strip()
orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    format="mixed",
    dayfirst=True
)

report_date = orders["order_date"].max()

customer_orders = (
    orders
    .merge(
        customers,
        on="customer_id"
    )
    .merge(
        payments,
        on="order_id"
    )
)

customer_metrics = (
    customer_orders
    .groupby("customer_id")
    .agg(
        LTV=("amount", "sum"),
        orders_count=("order_id", "count"),
        avg_check=("amount", "mean"),
        first_purchase=("order_date", "min"),
        last_purchase=("order_date", "max")
    )
)
customer_metrics["avg_check"] = customer_metrics["avg_check"].round(2)
customer_metrics["days_since_last_purchase"] = (
    report_date - customer_metrics["last_purchase"]
)

# report for BI
customers_report = (
    customer_orders[
        [
            "customer_id",
            "customer_name",
            "city",
            "registration_date"
        ]
    ]
    .merge(
        customer_metrics,
        on="customer_id"
    )
    .drop_duplicates(
        subset="customer_id"
    )
    .sort_values(
        "LTV",
        ascending=False
    )
)

customers_report.to_csv(
    "customers_report.csv",
    index=False
)
customer_orders.to_csv(
    "customer_orders.csv",
    index=False
)