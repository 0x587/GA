from flask import Blueprint

uniapp = Blueprint('uniapp', __name__, url_prefix='/uniapp')

import UniApp.routes
