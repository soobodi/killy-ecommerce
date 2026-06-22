from flask import Blueprint

admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='../../template_folder/admin'
)

from . import routes