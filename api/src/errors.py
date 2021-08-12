from werkzeug.exceptions import HTTPException

class ReportNotFound(HTTPException):
    def __init__(self, date, region='global'):
        self.code = 404
        self.type = "ReportNotFound"
        self.description = f"Report for {region} for {date} not found"

class VaccinesNotFound(HTTPException):
    def __init__(self):
        self.code = 404
        self.type = "VaccinesNotFound"
        self.description = f"Vaccines report not found"

class Top5NotFound(HTTPException):
    def __init__(self, purchase_id):
        self.code = 404
        self.type = "Top5NotFound"
        self.description = f"Requested top 5 not found"

