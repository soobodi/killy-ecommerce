from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import Categoria, Producto, Usuario, Pedido
from . import admin_bp
from .decorators import admin_requerido


# DASHBOARD
@admin_bp.route('/dashboard')
@login_required
@admin_requerido
def dashboard():
    total_productos = Producto.query.filter_by(activo=True).count()
    total_categorias = Categoria.query.filter_by(activa=True).count()
    total_clientes = Usuario.query.filter_by(
        rol='cliente',
        activo=True
    ).count()
    total_pedidos = Pedido.query.count()

    productos_bajo_stock = Producto.query.filter(
        Producto.activo.is_(True),
        Producto.stock <= 5
    ).order_by(Producto.stock.asc()).all()

    return render_template(
        'admin/home.html',
        total_productos=total_productos,
        total_categorias=total_categorias,
        total_clientes=total_clientes,
        total_pedidos=total_pedidos,
        productos_bajo_stock=productos_bajo_stock
    )


# LISTAR CATEGORÍAS
@admin_bp.route('/categorias')
@login_required
@admin_requerido
def categorias():
    listado = Categoria.query.order_by(
        Categoria.activa.desc(),
        Categoria.nombre.asc()
    ).all()

    return render_template(
        'admin/categorias.html',
        categorias=listado
    )


# CREAR CATEGORÍA
@admin_bp.route('/categorias/crear', methods=['GET', 'POST'])
@login_required
@admin_requerido
def crear_categoria():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre:
            flash('El nombre de la categoría es obligatorio.', 'danger')
            return render_template('admin/categoria_form.html')

        categoria_existente = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre.lower()
        ).first()

        if categoria_existente:
            flash('Ya existe una categoría con ese nombre.', 'warning')
            return render_template('admin/categoria_form.html')

        nueva_categoria = Categoria(
            nombre=nombre,
            descripcion=descripcion,
            activa=True
        )

        db.session.add(nueva_categoria)
        db.session.commit()

        flash('Categoría creada correctamente.', 'success')
        return redirect(url_for('admin.categorias'))

    return render_template(
        'admin/categoria_form.html',
        categoria=None
    )


# EDITAR CATEGORÍA
@admin_bp.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_requerido
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre:
            flash('El nombre de la categoría es obligatorio.', 'danger')
            return render_template(
                'admin/categoria_form.html',
                categoria=categoria
            )

        categoria_repetida = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre.lower(),
            Categoria.id != categoria.id
        ).first()

        if categoria_repetida:
            flash('Ya existe otra categoría con ese nombre.', 'warning')
            return render_template(
                'admin/categoria_form.html',
                categoria=categoria
            )

        categoria.nombre = nombre
        categoria.descripcion = descripcion

        db.session.commit()

        flash('Categoría actualizada correctamente.', 'success')
        return redirect(url_for('admin.categorias'))

    return render_template(
        'admin/categoria_form.html',
        categoria=categoria
    )


# ELIMINACIÓN LÓGICA / REACTIVACIÓN
@admin_bp.route('/categorias/<int:id>/estado', methods=['POST'])
@login_required
@admin_requerido
def cambiar_estado_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if categoria.activa:
        productos_activos = Producto.query.filter_by(
            categoria_id=categoria.id,
            activo=True
        ).count()

        if productos_activos > 0:
            flash(
                'No puede desactivar una categoría que todavía tiene '
                'productos activos.',
                'warning'
            )
            return redirect(url_for('admin.categorias'))

        categoria.activa = False
        mensaje = 'Categoría desactivada correctamente.'
    else:
        categoria.activa = True
        mensaje = 'Categoría activada correctamente.'

    db.session.commit()

    flash(mensaje, 'success')
    return redirect(url_for('admin.categorias'))


# RUTAS PARA LOS SIGUIENTES MÓDULOS
@admin_bp.route('/productos')
@login_required
@admin_requerido
def productos():
    return render_template('admin/productos.html')


@admin_bp.route('/clientes')
@login_required
@admin_requerido
def clientes():
    return render_template('admin/clientes.html')


@admin_bp.route('/pedidos')
@login_required
@admin_requerido
def pedidos():
    return render_template('admin/pedidos.html')