from typing import Any

from app.database.database import SessionLocal
from app.database.models import Service
from app.schemas.analysis import ProjectAnalysis


def calculate_price(analysis: ProjectAnalysis) -> dict[str, Any]:
    """
    محاسبه قیمت پروژه بر اساس سرویس‌ها و تعداد محصولات.
    """

    features = analysis.features

    db = SessionLocal()

    items = []
    total = 0

    for feature in features:

        # کاتالوگ بزرگ محصولات را جداگانه محاسبه می‌کنیم
        if feature == "large_product_catalog":
            continue

        service = (
            db.query(Service)
            .filter(Service.code == feature)
            .first()
        )

        if service:
            items.append({
                "feature": service.code,
                "name": service.name,
                "price": service.price,
            })

            total += service.price

    # --------------------------------
    # قیمت ورود محصولات بر اساس تعداد
    # --------------------------------

    if analysis.product_count is not None:

        count = analysis.product_count

        if count <= 20:
            product_price = 2000000

        elif count <= 100:
            product_price = 4000000

        elif count <= 500:
            product_price = 7000000

        elif count <= 1000:
            product_price = 10000000

        else:
            product_price = 15000000

        items.append({
            "feature": "product_entry",
            "name": f"ورود {count} محصول",
            "price": product_price,
        })

        total += product_price

    # --------------------------------
    # تعیین بازه قیمت
    # --------------------------------

    if analysis.estimated_complexity == "low":
        min_price = round(total * 0.90)
        max_price = round(total * 1.05)

    elif analysis.estimated_complexity == "medium":
        min_price = round(total * 0.90)
        max_price = round(total * 1.15)

    else:
        min_price = round(total * 0.85)
        max_price = round(total * 1.30)

    db.close()

    return {
        "items": items,
        "total": total,
        "estimated_range": {
            "min": min_price,
            "max": max_price,
        },
    }