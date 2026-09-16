import re

from app.schemas.analysis import ProjectAnalysis


def analyze_project(description: str) -> ProjectAnalysis:
    """
    تحلیل توضیحات پروژه به صورت دستی و بدون نیاز به API
    """

    text = description.lower()

    result = {
        "project_type": "unknown",
        "features": [],
        "estimated_complexity": "low",
        "product_count": None,
    }

    # -------------------------
    # نوع پروژه
    # -------------------------

    if any(word in text for word in [
        "فروشگاه",
        "فروشگاهی",
        "فروش",
        "محصول",
        "فروش آنلاین",
        "فروشگاه اینترنتی",
    ]):
        result["project_type"] = "ecommerce"

    elif any(word in text for word in [
        "شرکتی",
        "شرکت",
        "معرفی شرکت",
        "سازمانی",
    ]):
        result["project_type"] = "corporate"

    elif any(word in text for word in [
        "شخصی",
        "رزومه",
        "پورتفولیو",
        "نمونه کار",
    ]):
        result["project_type"] = "portfolio"

    # -------------------------
    # طراحی سایت
    # -------------------------

    if any(word in text for word in [
        "طراحی سایت",
        "سایت می‌خواهم",
        "سایت میخوام",
        "سایت می خواهم",
        "یک سایت",
        "یه سایت",
        "سایت شرکتی",
        "سایت فروشگاهی",
        "فروشگاه اینترنتی",
        "وب‌سایت",
        "وب سایت",
    ]):
        result["features"].append("website_design")

    # -------------------------
    # Elementor
    # -------------------------

    if any(word in text for word in [
        "المنتور",
        "elementor",
    ]):
        result["features"].append("elementor_design")

    # -------------------------
    # WooCommerce
    # -------------------------

    if any(word in text for word in [
        "ووکامرس",
        "woocommerce",
        "فروشگاه",
        "فروشگاهی",
    ]):
        result["features"].append("woocommerce")

    # -------------------------
    # پرداخت آنلاین
    # -------------------------

    if any(word in text for word in [
        "درگاه",
        "درگاه پرداخت",
        "پرداخت آنلاین",
        "پرداخت اینترنتی",
        "زرین پال",
        "زرین‌پال",
    ]):
        result["features"].append("online_payment")

    # -------------------------
    # ورود محصولات
    # -------------------------

    if any(word in text for word in [
        "ورود محصولات",
        "ثبت محصولات",
        "اضافه کردن محصولات",
        "افزودن محصولات",
        "محصولات را وارد",
    ]):
        result["features"].append("product_entry")

    # -------------------------
    # سئو
    # -------------------------

    if any(word in text for word in [
        "سئو",
        "seo",
        "بهینه سازی",
        "بهینه‌سازی",
    ]):
        result["features"].append("initial_seo")

    # -------------------------
    # پشتیبانی
    # -------------------------

    if any(word in text for word in [
        "پشتیبانی",
        "نگهداری سایت",
        "نگهداری",
        "ساپورت",
        "support",
    ]):
        result["features"].append("support")

    # -------------------------
    # طراحی اختصاصی
    # -------------------------

    if any(word in text for word in [
        "اختصاصی",
        "طراحی اختصاصی",
        "طراحی سفارشی",
        "کاملاً اختصاصی",
        "کاملا اختصاصی",
    ]):
        result["features"].append("custom_design")

    # -------------------------
    # چند شعبه
    # -------------------------

    if any(word in text for word in [
        "شعبه",
        "شعب",
        "نمایندگی",
        "چند شعبه",
    ]):
        result["features"].append("multi_branch")

    # -------------------------
    # استخراج تعداد محصولات
    # -------------------------

    match = re.search(
        r"(\d+)\s*(?:محصول|محصولات)",
        text
    )

    if match:
        result["product_count"] = int(match.group(1))

    # -------------------------
    # تعیین پیچیدگی
    # -------------------------

    complexity_score = 0

    if "website_design" in result["features"]:
        complexity_score += 1

    if "woocommerce" in result["features"]:
        complexity_score += 1

    if "online_payment" in result["features"]:
        complexity_score += 1

    if "initial_seo" in result["features"]:
        complexity_score += 1

    if "custom_design" in result["features"]:
        complexity_score += 2

    if "support" in result["features"]:
        complexity_score += 1

    if "multi_branch" in result["features"]:
        complexity_score += 3

    # -------------------------
    # تأثیر تعداد محصولات
    # -------------------------

    if result["product_count"] is not None:

        count = result["product_count"]

        if count <= 20:
            complexity_score += 0

        elif count <= 100:
            complexity_score += 1

        elif count <= 500:
            complexity_score += 2

        elif count <= 1000:
            complexity_score += 3

        else:
            complexity_score += 4

    # -------------------------
    # سطح نهایی پیچیدگی
    # -------------------------

    if complexity_score >= 7:
        result["estimated_complexity"] = "high"

    elif complexity_score >= 3:
        result["estimated_complexity"] = "medium"

    else:
        result["estimated_complexity"] = "low"

    return ProjectAnalysis(**result)