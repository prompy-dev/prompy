from flask import Flask, jsonify, abort, g
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from controllers.openai_controller import openai_chat
from controllers.user_query_controller import check_user_query
from controllers.openai_parser_controller import openai_parser
load_dotenv()

# create app factory
def create_app(config_class=None):
  app = Flask(__name__, instance_relative_config=False)
  app.config.from_object(config_class)
  CORS(app)

  @app.get('/')
  @cross_origin()
  def index():
    return jsonify({ 'success': True })
  

  @app.post('/api/chat')
  @cross_origin()
  @check_user_query
  @openai_parser
  def prompy_entry():
    return jsonify({ 
      'success': True,
      'parsed_user_query': g.parsed_user_query
    })
  
  @app.get('/error')
  def spoof_error():
    abort(500)

  @app.errorhandler(500)
  def server_errror(error):
    return error_response(
      message="There was an error processing the request",
      status_code=500,
      error_type="Server Error"
    )
  
  def error_response(message, status_code=400, error_type="Bad Request"):
    return jsonify({
      "sucess": False,
      "message": message,
      "error": error_type
    }), status_code
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  return app
