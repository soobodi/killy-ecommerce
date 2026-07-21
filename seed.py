from app import create_app, db
from app.models import Usuario, Categoria, Producto

app = create_app()

with app.app_context():
    # Evita insertar los mismos datos varias veces
    if Categoria.query.first():
        print("La base de datos ya contiene información.")
    else:
        # Categorías de Killy
        cat1 = Categoria(
            nombre="Regalos personalizados",
            descripcion="Detalles personalizados con nombres, frases y fotografías."
        )
        cat2 = Categoria(
            nombre="Cajas sorpresa",
            descripcion="Cajas preparadas para cumpleaños, aniversarios y ocasiones especiales."
        )
        cat3 = Categoria(
            nombre="Ramos de gomitas",
            descripcion="Detalles personalizados para una persona especial."
        )

        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()

        # Productos iniciales
        p1 = Producto(
            nombre="Taza personalizada",
            precio=12.00,
            stock=20,
            categoria_id=cat1.id
        )

        p2 = Producto(
            nombre="Caja sorpresa de cumpleaños",
            precio=25.00,
            stock=15,
            categoria_id=cat2.id
        )

        p3 = Producto(
            nombre="Kit corporativo personalizado",
            precio=35.00,
            stock=10,
            categoria_id=cat3.id
        )

        db.session.add_all([p1, p2, p3])

        # Usuario administrador
        admin = Usuario(
            nombre="Administración Killy",
            email="admin@killy.com",
            rol="admin"
        )
        admin.set_password("admin123")

        # Cliente de prueba
        cliente = Usuario(
            nombre="Cliente Killy",
            email="cliente@killy.com",
            rol="cliente"
        )
        cliente.set_password("cliente123")

        db.session.add_all([admin, cliente])
        db.session.commit()

        print("Datos iniciales de Killy insertados correctamente.")