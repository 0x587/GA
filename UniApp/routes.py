from UniApp.uniapp import uniapp
import json


@uniapp.errorhandler(500)
def server_error(error_code):
    result = {
        'code': str(error_code),
        'msg': 'This request triggered an internal server error.'
               ' Please check whether the request method or parameters are valid.',
        'data': None
    }
    return json.dumps(result), {'Content-Type': 'json'}
