import os
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.utils import get_error_message

products_bp = Blueprint("products", __name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

@products_bp.route("/products")
def index():
    try:
        products_res = requests.get(f"{BACKEND_URL}/products/")
        categories_res = requests.get(f"{BACKEND_URL}/categories/")
        suppliers_res = requests.get(f"{BACKEND_URL}/suppliers/")
        
        products = products_res.json() if products_res.status_code == 200 else []
        categories = categories_res.json() if categories_res.status_code == 200 else []
        suppliers = suppliers_res.json() if suppliers_res.status_code == 200 else []
        
        supplier_names = {s["id"]: s["name"] for s in suppliers}
        category_names = {c["id"]: c["name"] for c in categories}
        
        for p in products:
            p["supplier_name"] = supplier_names.get(p.get("supplier_id"), "None")
            p["category_names"] = [category_names.get(cid, "Unknown") for cid in p.get("category_ids", [])]
            
        return render_template(
            "products.html",
            products=products,
            categories=categories,
            suppliers=suppliers,
            active_page="products"
        )
    except Exception as e:
        flash(f"Erro ao carregar produtos: {str(e)}", "danger")
        return render_template("products.html", products=[], categories=[], suppliers=[], active_page="products")

@products_bp.route("/products/create", methods=["POST"])
def create():
    try:
        name = request.form.get("name")
        description = request.form.get("description") or None
        sku = request.form.get("sku")
        price = float(request.form.get("price", 0.0))
        quantity = int(request.form.get("quantity", 0))
        min_quantity = int(request.form.get("min_quantity", 0))
        
        supplier_id_raw = request.form.get("supplier_id")
        supplier_id = int(supplier_id_raw) if supplier_id_raw else None
        
        category_ids = [int(cid) for cid in request.form.getlist("category_ids")]

        payload = {
            "name": name,
            "description": description,
            "sku": sku,
            "price": price,
            "quantity": quantity,
            "min_quantity": min_quantity,
            "supplier_id": supplier_id,
            "category_ids": category_ids
        }

        res = requests.post(f"{BACKEND_URL}/products/", json=payload)
        if res.status_code == 201:
            flash("Produto criado com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao criar produto")
            flash(f"Falha ao criar produto: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("products.index"))

@products_bp.route("/products/update/<int:product_id>", methods=["POST"])
def update(product_id):
    try:
        name = request.form.get("name")
        description = request.form.get("description") or None
        sku = request.form.get("sku")
        price = float(request.form.get("price", 0.0))
        quantity = int(request.form.get("quantity", 0))
        min_quantity = int(request.form.get("min_quantity", 0))
        
        supplier_id_raw = request.form.get("supplier_id")
        supplier_id = int(supplier_id_raw) if supplier_id_raw else None
        
        category_ids = [int(cid) for cid in request.form.getlist("category_ids")]

        payload = {
            "name": name,
            "description": description,
            "sku": sku,
            "price": price,
            "quantity": quantity,
            "min_quantity": min_quantity,
            "supplier_id": supplier_id,
            "category_ids": category_ids
        }

        res = requests.put(f"{BACKEND_URL}/products/{product_id}", json=payload)
        if res.status_code == 200:
            flash("Produto atualizado com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao atualizar produto")
            flash(f"Falha ao atualizar produto: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("products.index"))

@products_bp.route("/products/delete/<int:product_id>", methods=["POST"])
def delete(product_id):
    try:
        res = requests.delete(f"{BACKEND_URL}/products/{product_id}")
        if res.status_code == 200:
            flash("Produto excluído com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao excluir produto")
            flash(f"Falha ao excluir produto: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("products.index"))

@products_bp.route("/products/movement", methods=["POST"])
def movement():
    try:
        product_id = int(request.form.get("product_id"))
        movement_type = request.form.get("movement_type")
        quantity = int(request.form.get("quantity", 0))
        reason = request.form.get("reason") or None

        payload = {
            "product_id": product_id,
            "movement_type": movement_type,
            "quantity": quantity,
            "reason": reason
        }

        res = requests.post(f"{BACKEND_URL}/movements/", json=payload)
        if res.status_code == 201:
            flash(f"Movimentação de estoque registrada com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao registrar movimentação")
            flash(f"Falha ao registrar movimentação de estoque: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("products.index"))
