from flask import Flask, current_app, json
from daily_report import routes as dailyRoutes
from vaccines import routes as vaccRoutes
from top5 import routes as top5Routes
from werkzeug.exceptions import HTTPException
import traceback
import decimal
import datetime 

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def ping():
    return {
        'message':'Willcommen! Service is working.'
    }, 200

app.register_blueprint(dailyRoutes.bp)
app.register_blueprint(vaccRoutes.bp)
app.register_blueprint(top5Routes.bp)

@app.errorhandler(Exception)
def handle_exception(e):
    current_app.logger.error(e)
    traceback.print_tb(e.__traceback__)

    # pass through HTTP errors
    if isinstance(e, HTTPException):
        current_app.logger.error(e)
        return {
            'type': e.name if not hasattr(e,'type') else e.name,
            'message': e.description
        }, e.code

    # non HTTP errors
    return {"message": "Internal server error"}, 500

class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        return super(MyJSONEncoder, self).default(obj)

with app.app_context():  
    app.json_encoder = MyJSONEncoder