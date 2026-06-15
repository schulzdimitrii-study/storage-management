import os
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.utils import get_error_message

management_bp = Blueprint("management", __name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

@management_bp.route("/management")
def index():
    try:
        categories_res = requests.get(f"{BACKEND_URL}/categories/")
        suppliers_res = requests.get(f"{BACKEND_URL}/suppliers/")
        
        categories = categories_res.json() if categories_res.status_code == 200 else []
        suppliers = suppliers_res.json() if suppliers_res.status_code == 200 else []
        
        return render_template(
            "management.html",
            categories=categories,
            suppliers=suppliers,
            active_page="management"
        )
    except Exception as e:
        flash(f"Erro ao carregar dados: {str(e)}", "danger")
        return render_template("management.html", categories=[], suppliers=[], active_page="management")

@management_bp.route("/management/suppliers/create", methods=["POST"])
def create_supplier():
    try:
        name = request.form.get("name")
        email = request.form.get("email") or None
        phone = request.form.get("phone") or None
        address = request.form.get("address") or None

        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address
        }

        res = requests.post(f"{BACKEND_URL}/suppliers/", json=payload)
        if res.status_code == 201:
            flash("Fornecedor criado com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao criar fornecedor")
            flash(f"Falha ao criar fornecedor: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("management.index"))

@management_bp.route("/management/suppliers/update/<int:supplier_id>", methods=["POST"])
def update_supplier(supplier_id):
    try:
        name = request.form.get("name")
        email = request.form.get("email") or None
        phone = request.form.get("phone") or None
        address = request.form.get("address") or None

        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address
        }

        res = requests.put(f"{BACKEND_URL}/suppliers/{supplier_id}", json=payload)
        if res.status_code == 200:
            flash("Fornecedor atualizado com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao atualizar fornecedor")
            flash(f"Falha ao atualizar fornecedor: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("management.index"))

@management_bp.route("/management/suppliers/delete/<int:supplier_id>", methods=["POST"])
def delete_supplier(supplier_id):
    try:
        res = requests.delete(f"{BACKEND_URL}/suppliers/{supplier_id}")
        if res.status_code == 200:
            flash("Fornecedor excluído com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao excluir fornecedor")
            flash(f"Falha ao excluir fornecedor: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("management.index"))

@management_bp.route("/management/categories/create", methods=["POST"])
def create_category():
    try:
        name = request.form.get("name")
        description = request.form.get("description") or None

        payload = {
            "name": name,
            "description": description
        }

        res = requests.post(f"{BACKEND_URL}/categories/", json=payload)
        if res.status_code == 201:
            flash("Categoria criada com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao criar categoria")
            flash(f"Falha ao criar categoria: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("management.index"))

@management_bp.route("/management/categories/update/<int:category_id>", methods=["POST"])
def update_category(category_id):
    try:
        name = request.form.get("name")
        description = request.form.get("description") or None

        payload = {
            "name": name,
            "description": description
        }

        res = requests.put(f"{BACKEND_URL}/categories/{category_id}", json=payload)
        if res.status_code == 200:
            flash("Categoria atualizada com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao atualizar categoria")
            flash(f"Falha ao atualizar categoria: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("management.index"))

@management_bp.route("/management/categories/delete/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    try:
        res = requests.delete(f"{BACKEND_URL}/categories/{category_id}")
        if res.status_code == 200:
            flash("Categoria excluída com sucesso!", "success")
        else:
            error_msg = get_error_message(res, "Erro ao excluir categoria")
            flash(f"Falha ao excluir categoria: {error_msg}", "danger")
    except Exception as e:
        flash(f"Erro: {str(e)}", "danger")
        
    return redirect(url_for("management.index"))
