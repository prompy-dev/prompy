from flask import Flask, current_app, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from flask_talisman import Talisman
load_dotenv()

# Pipeline steps
from steps import (
  clean_user_query, 
  parse_query, 
  embed_query, 
  chat_llm, 
  score_query,
  pinecone_query,
  summarize_query,
  run_query
)


# create app factory
def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    CORS(app)

    # Configure Talisman with security headers
    Talisman(
        app,
        force_https=True,
        strict_transport_security=True,
        session_cookie_secure=True,
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self'",
            'style-src': "'self'",
            'img-src': "'self'",
            'connect-src': "'self'"
        }
    )

    @app.post("/api/chat")
    @cross_origin()
    def recommendation():
        try:
            data = request.get_json()
            query = data["prompt"]

            pipeline_chain = (
                clean_user_query()
                | parse_query()
                | summarize_query()
                | score_query()
                | run_query()
                | embed_query()
                | pinecone_query()
                | chat_llm()
            )

            result = pipeline_chain.invoke({"input": query})

        except Exception as e:
            current_app.logger.exception(e)
            return error_response(
                message="Error running pipeline chain " + str(e),
                error_type="Failed Pipeline",
                status_code=500,
            )
        else:
            return jsonify({"success": True, "feedback": result})

    def error_response(message, status_code=400, error_type="Bad Request"):
        return (
            jsonify({"sucess": False, "message": message, "error": error_type}),
            status_code,
        )

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    return app
