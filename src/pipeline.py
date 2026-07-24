import pandas as pd
import numpy as np
import os

RAW = "data/raw/"
PROCESSED = "data/processed/"
os.makedirs(PROCESSED, exist_ok=True)

def load_raw():
    print("📂 Loading all datasets...")
    orders    = pd.read_csv(f"{RAW}olist_orders_dataset.csv",
                            parse_dates=["order_purchase_timestamp",
                                        "order_delivered_customer_date",
                                        "order_estimated_delivery_date"])
    items     = pd.read_csv(f"{RAW}olist_order_items_dataset.csv")
    customers = pd.read_csv(f"{RAW}olist_customers_dataset.csv")
    payments  = pd.read_csv(f"{RAW}olist_order_payments_dataset.csv")
    products  = pd.read_csv(f"{RAW}olist_products_dataset.csv")
    sellers   = pd.read_csv(f"{RAW}olist_sellers_dataset.csv")
    reviews   = pd.read_csv(f"{RAW}olist_order_reviews_dataset.csv")
    category  = pd.read_csv(f"{RAW}product_category_name_translation.csv")

    print(f"  orders:    {orders.shape}")
    print(f"  items:     {items.shape}")
    print(f"  customers: {customers.shape}")
    print(f"  payments:  {payments.shape}")
    print(f"  products:  {products.shape}")
    print(f"  sellers:   {sellers.shape}")
    print(f"  reviews:   {reviews.shape}")
    print(f"  category:  {category.shape}")

    return orders, items, customers, payments, products, sellers, reviews, category

def clean_orders(orders):
    print("\n🧹 Cleaning orders...")
    before = len(orders)
    # Keep only delivered orders
    orders = orders[orders["order_status"] == "delivered"]
    # Drop nulls in key date column
    orders = orders.dropna(subset=["order_purchase_timestamp",
                                   "order_delivered_customer_date"])
    orders = orders.drop_duplicates(subset=["order_id"])
    print(f"  Rows: {before} → {len(orders)}")
    return orders

def clean_items(items):
    print("\n🧹 Cleaning order items...")
    items = items[items["price"] > 0]
    items = items[items["quantity"] if "quantity" in items.columns
                  else items.index >= 0]
    items = items.drop_duplicates()
    print(f"  Shape: {items.shape}")
    return items

def build_master(orders, items, customers,
                 payments, products, category):
    print("\n🔗 Building master dataset...")

    # Merge items + orders
    df = items.merge(orders[["order_id",
                              "customer_id",
                              "order_purchase_timestamp",
                              "order_delivered_customer_date"]],
                     on="order_id", how="inner")

    # Merge customers
    df = df.merge(customers[["customer_id",
                              "customer_unique_id",
                              "customer_state"]],
                  on="customer_id", how="left")

    # Merge payments (total payment per order)
    pay_agg = (payments.groupby("order_id")["payment_value"]
                       .sum().reset_index()
                       .rename(columns={"payment_value":"order_payment"}))
    df = df.merge(pay_agg, on="order_id", how="left")

    # Merge products + category translation
    products = products.merge(category,
                              on="product_category_name",
                              how="left")
    df = df.merge(products[["product_id",
                             "product_category_name_english"]],
                  on="product_id", how="left")

    # Rename for clarity
    df = df.rename(columns={
        "order_purchase_timestamp": "order_date",
        "product_category_name_english": "category",
        "customer_unique_id": "customer_id_unique"
    })

    # Add useful time columns
    df["year"]    = df["order_date"].dt.year
    df["month"]   = df["order_date"].dt.month
    df["week"]    = df["order_date"].dt.isocalendar().week.astype(int)
    df["revenue"] = df["price"] + df["freight_value"]

    print(f"  Final master shape: {df.shape}")
    print(f"  Date range: {df['order_date'].min()} "
          f"→ {df['order_date'].max()}")
    print(f"  Unique customers: {df['customer_id_unique'].nunique()}")
    print(f"  Unique products:  {df['product_id'].nunique()}")
    print(f"  Categories:       {df['category'].nunique()}")

    return df

def validate(df):
    print("\n✅ Validating...")
    checks = {
        "No null order_date":
            df["order_date"].isnull().sum() == 0,
        "No null customer":
            df["customer_id_unique"].isnull().sum() == 0,
        "No negative revenue":
            (df["revenue"] >= 0).all(),
        "Has category data":
            df["category"].notnull().sum() > len(df) * 0.7,
    }
    for check, result in checks.items():
        print(f"  {'✅' if result else '❌'} {check}")

def run_pipeline():
    print("🚀 Starting RetailPulse Pipeline...\n")

    (orders, items, customers, payments,
     products, sellers, reviews, category) = load_raw()

    orders = clean_orders(orders)
    items  = clean_items(items)

    df = build_master(orders, items, customers,
                      payments, products, category)

    validate(df)

    df.to_csv(f"{PROCESSED}master.csv", index=False)
    print(f"\n💾 Saved to {PROCESSED}master.csv")
    print("✅ Pipeline complete!")
    return df

if __name__ == "__main__":
    run_pipeline()