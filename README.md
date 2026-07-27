# Killy E-Commerce
Regalos personalizados creados para sorprender, celebrar y expresar emociones.
## Descripción
Killy es un proyecto de tienda en línea desarrollado con Flask y MariaDB. Permite a los usuarios navegar por diferentes colecciones de productos, agregarlos al carrito, gestionar pedidos y actualizar su cuenta. El panel de administración permite gestionar productos, categorías, pedidos y clientes.
## Tecnologías
- Python 3.14
- Flask
- MariaDB
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Bootstrap 5
- jQuery
# Killy - E-commerce de Regalos Personalizados

Killy es una tienda en línea de regalos personalizados, creada para sorprender, celebrar y expresar emociones. Los usuarios pueden explorar productos, agregarlos al carrito, realizar pedidos y gestionar su cuenta.

---

## Funcionalidades principales

### 1. Panel de Administración
- Dashboard con métricas de ventas, pedidos y productos con bajo stock.
- CRUD de categorías: listar, crear, editar y eliminar.
- CRUD de productos: listar, crear, editar, eliminar y subir imágenes.
- Gestión de clientes: listar, activar o desactivar cuentas.
- Gestión de pedidos: listar todos los pedidos y cambiar su estado (pendiente → pagado → enviado → entregado).

### 2. Subida de imágenes
- Carpeta configurada: `app/static/img/`
- Lógica de subida de imágenes en formularios de productos (admin).
- Validación de tipo de archivo: JPG, JPEG, WEBP.
- Validación de tamaño máximo: 3 MB.

### 3. Frontend
- Estilos propios derivados de Bootstrap (`static/css/style.css`).
- Página principal (`home.html`) con Hero, colecciones y productos destacados.
- Página de catálogo (`tienda.html`) con búsqueda, filtrado por categorías y productos.
- Footer con nombre de los integrantes.
- Página "Sobre nosotros" (`sobre_nosotros.html`) con descripción del proyecto y año.
- Página "Contacto" (`contacto.html`) con formulario de contacto.
- Sistema de carrito de compras, pago y confirmación de pedidos.
- Gestión de cuenta de usuario: actualizar información y cambiar contraseña (`mi_cuenta.html`).

### 4. Despliegue y entorno
- Archivo `.env` con configuración de la base de datos y secret key.
- Archivo `.gitignore` configurado para ignorar archivos sensibles.
- Archivo `requirements.txt` actualizado con todas las dependencias.
- Configuración lista para modo producción (`FLASK_ENV=production`).
- Variables de entorno definidas en `.env`.
- Gunicorn como servidor WSGI (se implementará en producción).
- README con instrucciones completas de instalación y uso.

---