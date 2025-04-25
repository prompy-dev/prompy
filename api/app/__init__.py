from flask import Flask, jsonify, g, request
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

from steps.chat_llm import chat_llm
from steps.user_query import clean_user_query
from steps.parse_query import parse_query

# langchain
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
# from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_core.runnables import RunnableSequence

# from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# create app factory
def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    # initialize db extensions
    # db.init_app(app)

    CORS(app)

    @app.post("/api/chat")
    @cross_origin()
    def recommendation():
        try:
            data = request.get_json()
            query = data["prompt"]

            pipeline_chain = clean_user_query() | parse_query() | chat_llm()

            result = pipeline_chain.invoke({"input": query})

        except:
            return error_response()
        else:
            return jsonify({"success": True, "recommendation": result})

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
