from flask import Blueprint
from . import model
from errors import VaccinesNotFound

bp = Blueprint('vaccines',__name__, url_prefix='/vaccines')

@bp.route('/')
def get_vaccines():
    report = model.find_global()
    if (report == None):
        raise VaccinesNotFound()

    return report , 200 

