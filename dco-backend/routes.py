# routes.py

from flask import Flask, jsonify, request, render_template, Response
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from models import db
from resources import BusinessDomainResource, DatasetResource, DataAssetResource, ColumnInfoResource, StreamContentResource
from config import Config
from flask_cors import CORS  # Import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    api = Api(app)
    # Initialize CORS
    CORS(app)  # Apply CORS to the app

    # Swagger setup
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "My App"}
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Routes
    api.add_resource(BusinessDomainResource, '/api/business_domain', '/api/business_domain/<int:id>')
    api.add_resource(DatasetResource, '/api/business_domain/<int:business_domain_id>/dataset', '/api/business_domain/<int:business_domain_id>/dataset/<int:dataset_id>')
    api.add_resource(DataAssetResource, '/api/business_domain/<int:business_domain_id>/dataset/<int:dataset_id>/data_asset', '/api/business_domain/<int:business_domain_id>/dataset/<int:dataset_id>/data_asset/<int:data_asset_id>')
    api.add_resource(ColumnInfoResource, '/api/business_domain/<int:business_domain_id>/dataset/<int:dataset_id>/data_asset/<int:data_asset_id>/column', '/api/business_domain/<int:business_domain_id>/dataset/<int:dataset_id>/data_asset/<int:data_asset_id>/column/<int:column_id>')
    api.add_resource(StreamContentResource, '/api/stream-content')

    @app.route('/')
    def home():
        return jsonify({'message': 'Hello, World!'})


    @app.route('/ts')
    def test_stream():
        return render_template('test-stream.html')

    @app.route('/swagger.json')
    def swagger_spec():
        with open('swagger/swagger.json') as f:
            return Response(f.read(), mimetype='application/json')

    return app
