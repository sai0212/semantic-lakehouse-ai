from faker import Faker
import numpy as np
import pandas as pd

SEED = 42

CUSTOMER_COUNT = 100
PRODUCT_COUNT = 20
STORE_COUNT = 5

fake = Faker()
fake.seed_instance(SEED)

rng = np.random.default_rng(SEED)



def generate_customers():
    customers = []

    for i in range(1, CUSTOMER_COUNT + 1):
        customers.append({
            "customer_id": f"CUST-{i:06d}",
            "customer_name": fake.name(),
            "email": fake.email(),
            "region": rng.choice(["North", "South", "East", "West"]),
        })

    return pd.DataFrame(customers)

def generate_products():
    products = []

    categories = ["Electronics", "Home", "Clothing", "Books", "Sports"]

    for i in range(1, PRODUCT_COUNT + 1):
        products.append({
            "product_id": f"PROD-{i:06d}",
            "product_name": fake.word().title(),
            "category": rng.choice(categories),
            "current_unit_price": round(rng.uniform(10, 500), 2),
        })

    return pd.DataFrame(products)

def generate_stores():
    stores = []

    regions = ["North", "South", "East", "West"]

    for i in range(1, STORE_COUNT + 1):
        stores.append({
            "store_id": f"STORE-{i:06d}",
            "store_name": f"Store {i}",
            "region": rng.choice(regions),
        })

    return pd.DataFrame(stores)


def generate_dataset():
    customers = generate_customers()
    products = generate_products()
    stores = generate_stores()
    return stores
    # return customers, products, stores

if __name__ == "__main__":
    # customers, products, stores = generate_dataset()
    stores = generate_dataset()
    # print(customers.head())
    # print(products.head())
    print(stores.head())

