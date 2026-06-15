function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('open');
        document.body.style.overflow = '';
    }
}

window.addEventListener('click', function (event) {
    if (event.target.classList.contains('modal-overlay')) {
        closeModal(event.target.id);
    }
});

window.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal-overlay.open');
        openModals.forEach(modal => {
            closeModal(modal.id);
        });
    }
});

function openMovementModal(productId, productName) {
    document.getElementById('mov_product_id').value = productId;
    document.getElementById('mov_product_name').innerText = productName;
    openModal('movementModal');
}

function openEditModal(id, name, description, sku, price, quantity, minQuantity, supplierId, categoryIdsStr) {
    const form = document.getElementById('editProductForm');
    form.action = `/products/update/${id}`;

    document.getElementById('edit_title_name').innerText = name;
    document.getElementById('edit_name').value = name;
    document.getElementById('edit_description').value = description;
    document.getElementById('edit_sku').value = sku;
    document.getElementById('edit_price').value = price;
    document.getElementById('edit_quantity').value = quantity;
    document.getElementById('edit_min_quantity').value = minQuantity;
    document.getElementById('edit_supplier_id').value = supplierId;

    const checkboxes = document.querySelectorAll('#editProductModal input[name="category_ids"]');
    checkboxes.forEach(cb => cb.checked = false);

    if (categoryIdsStr) {
        const activeIds = categoryIdsStr.split(',');
        activeIds.forEach(catId => {
            const cb = document.getElementById(`edit_cat_${catId}`);
            if (cb) {
                cb.checked = true;
            }
        });
    }

    openModal('editProductModal');
}

function openEditSupplierModal(id, name, email, phone, address) {
    const form = document.getElementById('editSupplierForm');
    form.action = `/management/suppliers/update/${id}`;

    document.getElementById('edit_sup_title_name').innerText = name;
    document.getElementById('edit_sup_name').value = name;
    document.getElementById('edit_sup_email').value = email || '';
    document.getElementById('edit_sup_phone').value = phone || '';
    document.getElementById('edit_sup_address').value = address || '';

    openModal('editSupplierModal');
}

function openEditCategoryModal(id, name, description) {
    const form = document.getElementById('editCategoryForm');
    form.action = `/management/categories/update/${id}`;

    document.getElementById('edit_cat_title_name').innerText = name;
    document.getElementById('edit_cat_name').value = name;
    document.getElementById('edit_cat_description').value = description || '';

    openModal('editCategoryModal');
}


document.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                toast.remove();
            }, 500);
        }, 5000);
    });

    const themeToggleBtn = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');

    if (document.body.classList.contains('light-theme')) {
        if (themeIcon) {
            themeIcon.className = 'fa-solid fa-sun';
        }
    } else {
        if (themeIcon) {
            themeIcon.className = 'fa-solid fa-moon';
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const isLight = document.body.classList.toggle('light-theme');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');

            if (themeIcon) {
                themeIcon.className = isLight ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
            }
        });
    }

    const editSupplierBtns = document.querySelectorAll('.edit-supplier-btn');
    editSupplierBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const name = btn.getAttribute('data-name');
            const email = btn.getAttribute('data-email');
            const phone = btn.getAttribute('data-phone');
            const address = btn.getAttribute('data-address');
            openEditSupplierModal(id, name, email, phone, address);
        });
    });

    const editCategoryBtns = document.querySelectorAll('.edit-category-btn');
    editCategoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const name = btn.getAttribute('data-name');
            const description = btn.getAttribute('data-description');
            openEditCategoryModal(id, name, description);
        });
    });

    const editProductBtns = document.querySelectorAll('.edit-product-btn');
    editProductBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const name = btn.getAttribute('data-name');
            const description = btn.getAttribute('data-description');
            const sku = btn.getAttribute('data-sku');
            const price = btn.getAttribute('data-price');
            const quantity = btn.getAttribute('data-quantity');
            const minQuantity = btn.getAttribute('data-min-quantity');
            const supplierId = btn.getAttribute('data-supplier-id');
            const categoryIdsStr = btn.getAttribute('data-category-ids');
            openEditModal(id, name, description, sku, price, quantity, minQuantity, supplierId, categoryIdsStr);
        });
    });
});
