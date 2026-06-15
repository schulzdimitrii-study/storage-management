import os
import requests
from flask import Blueprint, render_template, current_app

dashboard_bp = Blueprint("dashboard", __name__)

BACKEND_URL = os.getenv("BACKEND_URL", "")

@dashboard_bp.route("/")
def index():
    try:
        products_res = requests.get(f"{BACKEND_URL}/products/")
        categories_res = requests.get(f"{BACKEND_URL}/categories/")
        suppliers_res = requests.get(f"{BACKEND_URL}/suppliers/")
        
        products = products_res.json() if products_res.status_code == 200 else []
        categories = categories_res.json() if categories_res.status_code == 200 else []
        suppliers = suppliers_res.json() if suppliers_res.status_code == 200 else []
        
        total_products = len(products)
        total_categories = len(categories)
        total_suppliers = len(suppliers)
        
        low_stock_products = [p for p in products if p.get("quantity", 0) <= p.get("min_quantity", 0)]
        
        all_movements = []
        product_names = {p["id"]: p["name"] for p in products}
        
        for p in products:
            mov_res = requests.get(f"{BACKEND_URL}/movements/{p['id']}")
            if mov_res.status_code == 200:
                movs = mov_res.json()
                for m in movs:
                    m["product_name"] = product_names.get(m["product_id"], "Unknown Product")
                    all_movements.append(m)
        
        all_movements.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        recent_movements = all_movements[:5]
        
        return render_template(
            "dashboard.html",
            total_products=total_products,
            total_categories=total_categories,
            total_suppliers=total_suppliers,
            low_stock_products=low_stock_products,
            recent_movements=recent_movements,
            active_page="dashboard"
        )
    except requests.exceptions.ConnectionError:
        return render_template("500.html", error="Não foi possível conectar à API do Backend. Certifique-se de que o serviço backend está rodando."), 500
    except Exception as e:
        return render_template("500.html", error=str(e)), 500
