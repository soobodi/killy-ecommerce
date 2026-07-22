import os
import uuid

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db
from app.models import Categoria, Pedido, Producto, Usuario
from . import admin_bp
from .decorators import admin_requerido


# =========================================================
# FUNCIONES PARA LA SUBIDA DE IMÁGENES
# =========================================================

def archivo_permitido(nombre_archivo):
    """Comprueba que el archivo tenga una extensión permitida."""

    if '.' not in nombre_archivo:
        return False

    extension = nombre_archivo.rsplit('.', 1)[1].lower()

    return extension in current_app.config['ALLOWED_EXTENSIONS']


def guardar_imagen(archivo):
    """Guarda una imagen con un nombre único."""

    if not archivo or not archivo.filename:
        return None

    if not archivo_permitido(archivo.filename):
        raise ValueError(
            'Formato no permitido. Utilice imágenes JPG, JPEG o WEBP.'
        )

    nombre_seguro = secure_filename(archivo.filename)
    extension = nombre_seguro.rsplit('.', 1)[1].lower()

    nombre_unico = f'{uuid.uuid4().hex}.{extension}'

    carpeta_destino = current_app.config['UPLOAD_FOLDER']
    os.makedirs(carpeta_destino, exist_ok=True)

    ruta_completa = os.path.join(
        carpeta_destino,
        nombre_unico
    )

    archivo.save(ruta_completa)

    return f'productos/{nombre_unico}'


def eliminar_imagen(nombre_imagen):
    """Elimina una imagen anterior del servidor."""

    if not nombre_imagen:
        return

    ruta_imagen = os.path.join(
        current_app.static_folder,
        'img',
        nombre_imagen
    )

    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)


# =========================================================
# DASHBOARD
# =========================================================

@admin_bp.route('/dashboard')
@login_required
@admin_requerido
def dashboard():
    total_productos = Producto.query.filter_by(
        activo=True
    ).count()

    total_categorias = Categoria.query.filter_by(
        activa=True
    ).count()

    total_clientes = Usuario.query.filter_by(
        rol='cliente',
        activo=True
    ).count()

    total_pedidos = Pedido.query.count()

    productos_bajo_stock = Producto.query.filter(
        Producto.activo.is_(True),
        Producto.stock <= 5
    ).order_by(
        Producto.stock.asc()
    ).all()

    return render_template(
        'admin/home.html',
        total_productos=total_productos,
        total_categorias=total_categorias,
        total_clientes=total_clientes,
        total_pedidos=total_pedidos,
        productos_bajo_stock=productos_bajo_stock
    )


# =========================================================
# CRUD DE CATEGORÍAS
# =========================================================

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


@admin_bp.route(
    '/categorias/crear',
    methods=['GET', 'POST']
)
@login_required
@admin_requerido
def crear_categoria():
    if request.method == 'POST':
        nombre = request.form.get(
            'nombre',
            ''
        ).strip()

        descripcion = request.form.get(
            'descripcion',
            ''
        ).strip()

        if not nombre:
            flash(
                'El nombre de la categoría es obligatorio.',
                'danger'
            )

            return render_template(
                'admin/categoria_form.html',
                categoria=None
            )

        categoria_existente = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre.lower()
        ).first()

        if categoria_existente:
            flash(
                'Ya existe una categoría con ese nombre.',
                'warning'
            )

            return render_template(
                'admin/categoria_form.html',
                categoria=None
            )

        nueva_categoria = Categoria(
            nombre=nombre,
            descripcion=descripcion,
            activa=True
        )

        db.session.add(nueva_categoria)
        db.session.commit()

        flash(
            'Categoría creada correctamente.',
            'success'
        )

        return redirect(
            url_for('admin.categorias')
        )

    return render_template(
        'admin/categoria_form.html',
        categoria=None
    )


@admin_bp.route(
    '/categorias/<int:id>/editar',
    methods=['GET', 'POST']
)
@login_required
@admin_requerido
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        nombre = request.form.get(
            'nombre',
            ''
        ).strip()

        descripcion = request.form.get(
            'descripcion',
            ''
        ).strip()

        if not nombre:
            flash(
                'El nombre de la categoría es obligatorio.',
                'danger'
            )

            return render_template(
                'admin/categoria_form.html',
                categoria=categoria
            )

        categoria_repetida = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre.lower(),
            Categoria.id != categoria.id
        ).first()

        if categoria_repetida:
            flash(
                'Ya existe otra categoría con ese nombre.',
                'warning'
            )

            return render_template(
                'admin/categoria_form.html',
                categoria=categoria
            )

        categoria.nombre = nombre
        categoria.descripcion = descripcion

        db.session.commit()

        flash(
            'Categoría actualizada correctamente.',
            'success'
        )

        return redirect(
            url_for('admin.categorias')
        )

    return render_template(
        'admin/categoria_form.html',
        categoria=categoria
    )


@admin_bp.route(
    '/categorias/<int:id>/estado',
    methods=['POST']
)
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
                'No puede desactivar una categoría que todavía '
                'tiene productos activos.',
                'warning'
            )

            return redirect(
                url_for('admin.categorias')
            )

        categoria.activa = False
        mensaje = 'Categoría desactivada correctamente.'

    else:
        categoria.activa = True
        mensaje = 'Categoría activada correctamente.'

    db.session.commit()

    flash(mensaje, 'success')

    return redirect(
        url_for('admin.categorias')
    )


# =========================================================
# CRUD DE PRODUCTOS
# =========================================================

@admin_bp.route('/productos')
@login_required
@admin_requerido
def productos():
    busqueda = request.args.get(
        'q',
        ''
    ).strip()

    categoria_id = request.args.get(
        'categoria',
        type=int
    )

    query = Producto.query

    if busqueda:
        query = query.filter(
            Producto.nombre.ilike(
                f'%{busqueda}%'
            )
        )

    if categoria_id:
        query = query.filter_by(
            categoria_id=categoria_id
        )

    listado_productos = query.order_by(
        Producto.activo.desc(),
        Producto.creado_en.desc()
    ).all()

    categorias_activas = Categoria.query.filter_by(
        activa=True
    ).order_by(
        Categoria.nombre.asc()
    ).all()

    return render_template(
        'admin/productos.html',
        productos=listado_productos,
        categorias=categorias_activas,
        busqueda=busqueda,
        categoria_id=categoria_id
    )


@admin_bp.route(
    '/productos/crear',
    methods=['GET', 'POST']
)
@login_required
@admin_requerido
def crear_producto():
    categorias = Categoria.query.filter_by(
        activa=True
    ).order_by(
        Categoria.nombre.asc()
    ).all()

    if request.method == 'POST':
        nombre = request.form.get(
            'nombre',
            ''
        ).strip()

        descripcion = request.form.get(
            'descripcion',
            ''
        ).strip()

        precio = request.form.get(
            'precio',
            type=float
        )

        stock = request.form.get(
            'stock',
            type=int
        )

        categoria_id = request.form.get(
            'categoria_id',
            type=int
        )

        if not nombre:
            flash(
                'El nombre del producto es obligatorio.',
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=None,
                categorias=categorias
            )

        if precio is None or precio < 0:
            flash(
                'Ingrese un precio válido.',
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=None,
                categorias=categorias
            )

        if stock is None or stock < 0:
            flash(
                'Ingrese una cantidad de stock válida.',
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=None,
                categorias=categorias
            )

        categoria = Categoria.query.filter_by(
            id=categoria_id,
            activa=True
        ).first()

        if not categoria:
            flash(
                'Seleccione una categoría válida.',
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=None,
                categorias=categorias
            )

        imagen = request.files.get('imagen')
        nombre_imagen = None

        try:
            if imagen and imagen.filename:
                nombre_imagen = guardar_imagen(imagen)

        except ValueError as error:
            flash(
                str(error),
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=None,
                categorias=categorias
            )

        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen=nombre_imagen,
            categoria_id=categoria.id,
            activo=True
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        flash(
            'Producto creado correctamente.',
            'success'
        )

        return redirect(
            url_for('admin.productos')
        )

    return render_template(
        'admin/producto_form.html',
        producto=None,
        categorias=categorias
    )


@admin_bp.route(
    '/productos/<int:id>/editar',
    methods=['GET', 'POST']
)
@login_required
@admin_requerido
def editar_producto(id):
    producto = Producto.query.get_or_404(id)

    categorias = Categoria.query.filter_by(
        activa=True
    ).order_by(
        Categoria.nombre.asc()
    ).all()

    if request.method == 'POST':
        nombre = request.form.get(
            'nombre',
            ''
        ).strip()

        descripcion = request.form.get(
            'descripcion',
            ''
        ).strip()

        precio = request.form.get(
            'precio',
            type=float
        )

        stock = request.form.get(
            'stock',
            type=int
        )

        categoria_id = request.form.get(
            'categoria_id',
            type=int
        )

        if not nombre:
            flash(
                'El nombre del producto es obligatorio.',
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=producto,
                categorias=categorias
            )

        if precio is None or precio < 0:
            flash(
                'Ingrese un precio válido.',
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=producto,
                categorias=categorias
            )

        if stock is None or stock < 0:
            flash(
                'Ingrese una cantidad de stock válida.',
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=producto,
                categorias=categorias
            )

        categoria = Categoria.query.filter_by(
            id=categoria_id,
            activa=True
        ).first()

        if not categoria:
            flash(
                'Seleccione una categoría válida.',
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=producto,
                categorias=categorias
            )

        imagen = request.files.get('imagen')

        try:
            if imagen and imagen.filename:
                nueva_imagen = guardar_imagen(imagen)

                if producto.imagen:
                    eliminar_imagen(producto.imagen)

                producto.imagen = nueva_imagen

        except ValueError as error:
            flash(
                str(error),
                'danger'
            )

            return render_template(
                'admin/producto_form.html',
                producto=producto,
                categorias=categorias
            )

        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock = stock
        producto.categoria_id = categoria.id

        db.session.commit()

        flash(
            'Producto actualizado correctamente.',
            'success'
        )

        return redirect(
            url_for('admin.productos')
        )

    return render_template(
        'admin/producto_form.html',
        producto=producto,
        categorias=categorias
    )


@admin_bp.route(
    '/productos/<int:id>/estado',
    methods=['POST']
)
@login_required
@admin_requerido
def cambiar_estado_producto(id):
    producto = Producto.query.get_or_404(id)

    producto.activo = not producto.activo

    db.session.commit()

    if producto.activo:
        mensaje = 'Producto activado correctamente.'
    else:
        mensaje = 'Producto desactivado correctamente.'

    flash(mensaje, 'success')

    return redirect(
        url_for('admin.productos')
    )


# =========================================================
# MÓDULOS PENDIENTES
# =========================================================

# =========================================================
# ADMINISTRACIÓN DE CLIENTES
# =========================================================

@admin_bp.route('/clientes')
@login_required
@admin_requerido
def clientes():
    busqueda = request.args.get(
        'q',
        ''
    ).strip()

    query = Usuario.query.filter_by(
        rol='cliente'
    )

    if busqueda:
        termino = f'%{busqueda}%'

        query = query.filter(
            db.or_(
                Usuario.nombre.ilike(termino),
                Usuario.email.ilike(termino)
            )
        )

    listado_clientes = query.order_by(
        Usuario.activo.desc(),
        Usuario.creado_en.desc()
    ).all()

    return render_template(
        'admin/clientes.html',
        clientes=listado_clientes,
        busqueda=busqueda
    )


@admin_bp.route(
    '/clientes/<int:id>/estado',
    methods=['POST']
)
@login_required
@admin_requerido
def cambiar_estado_cliente(id):
    cliente = Usuario.query.filter_by(
        id=id,
        rol='cliente'
    ).first_or_404()

    cliente.activo = not cliente.activo

    db.session.commit()

    if cliente.activo:
        mensaje = 'Cliente activado correctamente.'
    else:
        mensaje = 'Cliente desactivado correctamente.'

    flash(mensaje, 'success')

    return redirect(
        url_for('admin.clientes')
    )


# =========================================================
# ADMINISTRACIÓN DE PEDIDOS
# =========================================================

@admin_bp.route('/pedidos')
@login_required
@admin_requerido
def pedidos():
    busqueda = request.args.get(
        'q',
        ''
    ).strip()

    estado = request.args.get(
        'estado',
        ''
    ).strip()

    query = Pedido.query.join(
        Usuario,
        Pedido.usuario_id == Usuario.id
    )

    if busqueda:
        termino = f'%{busqueda}%'

        filtros = [
            Usuario.nombre.ilike(termino),
            Usuario.email.ilike(termino)
        ]

        if busqueda.isdigit():
            filtros.append(
                Pedido.id == int(busqueda)
            )

        query = query.filter(
            db.or_(*filtros)
        )

    estados_permitidos = {
        'pendiente',
        'pagado',
        'enviado',
        'entregado',
        'cancelado'
    }

    if estado in estados_permitidos:
        query = query.filter(
            Pedido.estado == estado
        )

    listado_pedidos = query.order_by(
        Pedido.fecha.desc()
    ).all()

    return render_template(
        'admin/pedidos.html',
        pedidos=listado_pedidos,
        busqueda=busqueda,
        estado=estado
    )


@admin_bp.route('/pedidos/<int:id>')
@login_required
@admin_requerido
def detalle_pedido(id):
    pedido = Pedido.query.get_or_404(id)

    return render_template(
        'admin/pedido_detalle.html',
        pedido=pedido
    )


@admin_bp.route(
    '/pedidos/<int:id>/estado',
    methods=['POST']
)
@login_required
@admin_requerido
def cambiar_estado_pedido(id):
    pedido = Pedido.query.get_or_404(id)

    nuevo_estado = request.form.get(
        'estado',
        ''
    ).strip()

    estados_permitidos = {
        'pendiente',
        'pagado',
        'enviado',
        'entregado',
        'cancelado'
    }

    if nuevo_estado not in estados_permitidos:
        flash(
            'El estado seleccionado no es válido.',
            'danger'
        )

        return redirect(
            url_for(
                'admin.detalle_pedido',
                id=pedido.id
            )
        )

    pedido.estado = nuevo_estado

    db.session.commit()

    flash(
        'Estado del pedido actualizado correctamente.',
        'success'
    )

    return redirect(
        url_for(
            'admin.detalle_pedido',
            id=pedido.id
        )
    )