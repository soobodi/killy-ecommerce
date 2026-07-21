from app import create_app, db
from app.models import Usuario, Categoria, Producto

app = create_app()

with app.app_context():

    # Limpiar únicamente productos y categorías de prueba
    Producto.query.delete()
    Categoria.query.delete()
    db.session.commit()

    categorias = {
        "Ramos de Gomitas": Categoria(
            nombre="🌸 Ramos de Gomitas",
            descripcion="Ramos preparados con gomitas y dulces."
        ),
        "Llaveros Tejidos": Categoria(
            nombre="🧶 Llaveros Tejidos",
            descripcion="Llaveros tejidos sencillos y personalizados."
        ),
        "Amigurumis": Categoria(
            nombre="🧸 Amigurumis",
            descripcion="Amigurumis personalizados elaborados a mano."
        ),
        "Cajas de Dulces": Categoria(
            nombre="🍫 Cajas de Dulces",
            descripcion="Cajas de dulces en diferentes tamaños."
        ),
        "Botiquines": Categoria(
            nombre="🚑 Botiquines de Dulces",
            descripcion="Botiquines de emergencia llenos de dulces."
        ),
        "Globos": Categoria(
            nombre="🎈 Globos Personalizados",
            descripcion="Globos con nombres, frases y diseños."
        ),
        "Cajas Temáticas": Categoria(
            nombre="🎁 Cajas Temáticas",
            descripcion="Cajas para fechas y ocasiones especiales."
        ),
        "Cajas Sorpresa": Categoria(
            nombre="💝 Cajas Sorpresa",
            descripcion="Cajas sorpresa personalizadas."
        )
    }

    db.session.add_all(categorias.values())
    db.session.commit()

    productos = [
        Producto(
            nombre="Ramo pequeño",
            descripcion="Ramo elaborado con 15 gomitas.",
            precio=12.00,
            stock=20,
            categoria_id=categorias["Ramos de Gomitas"].id
        ),
        Producto(
            nombre="Ramo mediano",
            descripcion="Ramo elaborado con 20 gomitas.",
            precio=18.00,
            stock=20,
            categoria_id=categorias["Ramos de Gomitas"].id
        ),
        Producto(
            nombre="Ramo grande",
            descripcion="Ramo elaborado con 25 gomitas.",
            precio=24.00,
            stock=15,
            categoria_id=categorias["Ramos de Gomitas"].id
        ),

        Producto(
            nombre="Llavero tejido sencillo",
            descripcion="Llavero tejido artesanal con diseño sencillo.",
            precio=7.99,
            stock=20,
            categoria_id=categorias["Llaveros Tejidos"].id
        ),
        Producto(
            nombre="Llavero tejido personalizado",
            descripcion="Llavero personalizado según el diseño elegido.",
            precio=9.99,
            stock=15,
            categoria_id=categorias["Llaveros Tejidos"].id
        ),
        Producto(
            nombre="Llavero tejido para pareja",
            descripcion="Juego de dos llaveros tejidos para pareja.",
            precio=16.99,
            stock=10,
            categoria_id=categorias["Llaveros Tejidos"].id
        ),

        Producto(
            nombre="Amigurumi personalizado 20 cm",
            descripcion="Amigurumi personalizado elaborado a mano.",
            precio=28.99,
            stock=10,
            categoria_id=categorias["Amigurumis"].id
        ),
        Producto(
            nombre="Amigurumi para pareja",
            descripcion="Pareja de amigurumis personalizados.",
            precio=54.99,
            stock=8,
            categoria_id=categorias["Amigurumis"].id
        ),
        Producto(
            nombre="Amigurumi con accesorios",
            descripcion="Amigurumi personalizado con accesorios.",
            precio=34.99,
            stock=8,
            categoria_id=categorias["Amigurumis"].id
        ),

        Producto(
            nombre="Caja pequeña de dulces",
            descripcion="Caja pequeña con variedad de dulces.",
            precio=14.99,
            stock=20,
            categoria_id=categorias["Cajas de Dulces"].id
        ),
        Producto(
            nombre="Caja mediana de dulces",
            descripcion="Caja mediana con variedad de dulces.",
            precio=22.99,
            stock=15,
            categoria_id=categorias["Cajas de Dulces"].id
        ),
        Producto(
            nombre="Caja grande de dulces",
            descripcion="Caja grande con variedad de dulces.",
            precio=32.99,
            stock=10,
            categoria_id=categorias["Cajas de Dulces"].id
        ),

        Producto(
            nombre="Mini botiquín de dulces",
            descripcion="Mini botiquín con dulces seleccionados.",
            precio=16.99,
            stock=20,
            categoria_id=categorias["Botiquines"].id
        ),
        Producto(
            nombre="Botiquín clásico",
            descripcion="Botiquín clásico con variedad de dulces.",
            precio=24.99,
            stock=15,
            categoria_id=categorias["Botiquines"].id
        ),
        Producto(
            nombre="Botiquín premium",
            descripcion="Botiquín premium con dulces y decoración.",
            precio=34.99,
            stock=10,
            categoria_id=categorias["Botiquines"].id
        ),

        Producto(
            nombre="Globo con nombre",
            descripcion="Globo personalizado con nombre.",
            precio=10.99,
            stock=20,
            categoria_id=categorias["Globos"].id
        ),
        Producto(
            nombre="Globo con diseño personalizado",
            descripcion="Globo elaborado con un diseño personalizado.",
            precio=14.99,
            stock=15,
            categoria_id=categorias["Globos"].id
        ),
        Producto(
            nombre="Globo burbuja personalizado",
            descripcion="Globo burbuja decorado y personalizado.",
            precio=19.99,
            stock=12,
            categoria_id=categorias["Globos"].id
        ),
        Producto(
            nombre="Set de globos decorativos",
            descripcion="Set de globos para celebraciones.",
            precio=24.99,
            stock=10,
            categoria_id=categorias["Globos"].id
        ),

        Producto(
            nombre="Caja temática mini",
            descripcion="Caja temática pequeña para una ocasión especial.",
            precio=18.99,
            stock=20,
            categoria_id=categorias["Cajas Temáticas"].id
        ),
        Producto(
            nombre="Caja temática clásica",
            descripcion="Caja temática clásica personalizada.",
            precio=28.99,
            stock=15,
            categoria_id=categorias["Cajas Temáticas"].id
        ),
        Producto(
            nombre="Caja temática premium",
            descripcion="Caja temática premium con dulces y detalles.",
            precio=42.99,
            stock=10,
            categoria_id=categorias["Cajas Temáticas"].id
        ),
        Producto(
            nombre="Caja temática deluxe",
            descripcion="Caja temática deluxe completamente personalizada.",
            precio=58.99,
            stock=8,
            categoria_id=categorias["Cajas Temáticas"].id
        ),

        Producto(
            nombre="Caja sorpresa personalizada",
            descripcion="Caja sorpresa adaptada a la ocasión y persona.",
            precio=29.99,
            stock=12,
            categoria_id=categorias["Cajas Sorpresa"].id
        )
    ]

    db.session.add_all(productos)

    # Crear usuarios solo si no existen
    if not Usuario.query.filter_by(email="admin@killy.com").first():
        admin = Usuario(
            nombre="Administración Killy",
            email="admin@killy.com",
            rol="admin"
        )
        admin.set_password("admin123")
        db.session.add(admin)

    if not Usuario.query.filter_by(email="cliente@killy.com").first():
        cliente = Usuario(
            nombre="Cliente Killy",
            email="cliente@killy.com",
            rol="cliente"
        )
        cliente.set_password("cliente123")
        db.session.add(cliente)

    db.session.commit()

    print("Catálogo de Killy cargado correctamente.")