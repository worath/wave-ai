from app.database.database import SessionLocal, engine, Base
from app.database.models import Service


# ساخت جدول‌ها
Base.metadata.create_all(bind=engine)


services = [
    {
        "name": "طراحی سایت",
        "code": "website_design",
        "category": "design",
        "price": 15_000_000,
    },
    {
        "name": "طراحی با Elementor",
        "code": "elementor_design",
        "category": "design",
        "price": 5_000_000,
    },
    {
        "name": "ووکامرس",
        "code": "woocommerce",
        "category": "ecommerce",
        "price": 7_000_000,
    },
    {
        "name": "درگاه پرداخت",
        "code": "online_payment",
        "category": "ecommerce",
        "price": 1_500_000,
    },
    {
        "name": "ورود محصولات",
        "code": "product_entry",
        "category": "ecommerce",
        "price": 2_000_000,
    },
    {
        "name": "سئو اولیه",
        "code": "initial_seo",
        "category": "seo",
        "price": 5_000_000,
    },
    {
        "name": "پشتیبانی",
        "code": "support",
        "category": "support",
        "price": 8_000_000,
    },
    {
        "name": "طراحی اختصاصی",
        "code": "custom_design",
        "category": "design",
        "price": 20_000_000,
    },
    {
        "name": "چند شعبه",
        "code": "multi_branch",
        "category": "advanced",
        "price": 8_000_000,
    },
    {
        "name": "کاتالوگ بزرگ محصولات",
        "code": "large_product_catalog",
        "category": "ecommerce",
        "price": 10_000_000,
    },
]


db = SessionLocal()

for service_data in services:
    service = Service(**service_data)
    db.add(service)

db.commit()
db.close()

print("Database initialized successfully.")
print("Services added successfully.")

