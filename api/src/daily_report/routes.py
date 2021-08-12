from flask import Blueprint
from . import model
from errors import ReportNotFound

bp = Blueprint('dailyreport',__name__, url_prefix='/dailyreport')

@bp.route('/<region>')
def get_regionreport(region):
    if(region=='global'):
        report = model.find_global()
        if (report == None):
            raise ReportNotFound(date='today', region='global')
    else:
        region = region.replace("_", " ")
        report = model.find_region(date=None, region=region)
        if (report == None):
            raise ReportNotFound(date='today', region=region)

    return report , 200 

@bp.route('/<region>/<date>')
def get_regionreport_bydate(date, region):
    if(region=='global'):
        report = model.find_global(date)
        if (report == None):
            raise ReportNotFound(date=date, region='global')
    else:
        report = model.find_region(date, region)
        if (report == None):
            raise ReportNotFound(date, region)

    return report , 200 

