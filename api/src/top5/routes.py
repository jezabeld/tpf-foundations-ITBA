from flask import Blueprint
from . import model
from errors import Top5NotFound

bp = Blueprint('top5',__name__, url_prefix='/top5')


@bp.route('/casespermillon')
def get_top5cases():
    report = model.find_topcases()
    if (report == None):
        raise Top5NotFound()

    return report , 200 

@bp.route('/peoplevaccinated')
def get_top5vaccinated():
    report = model.find_topvaccinated()
    if (report == None):
        raise Top5NotFound()

    return report , 200 

@bp.route('/vaccines')
def get_top5vaccines():
    report = model.find_topvaccines()
    if (report == None):
        raise Top5NotFound()

    return report , 200 

@bp.route('/inmunity')
def get_top5inmunity():
    report = model.find_topkpi()
    if (report == None):
        raise Top5NotFound()

    return report , 200 