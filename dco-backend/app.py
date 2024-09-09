from flask import Flask, jsonify, request,abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime

from flask_cors import CORS  # Import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/mydb'
db = SQLAlchemy(app)
api = Api(app)

# Initialize CORS
CORS(app)  # Apply CORS to the app

# Swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask API"
    }
)
app.register_blueprint(swagger_ui_bp, url_prefix=SWAGGER_URL)

# Models
class BusinessDomain(db.Model):
    __tablename__ = 'business_domain'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    db_name = db.Column(db.String(255))
    custom_fields = db.Column(db.JSON)

class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    business_domain_id = db.Column(db.Integer, db.ForeignKey('business_domain.id'))
    owner = db.Column(db.String(255))
    last_updated = db.Column(db.Date)
    number_of_records = db.Column(db.Integer)
    access_level = db.Column(db.String(50))
    recent_views = db.Column(db.Integer, default=0)
    custom_fields = db.Column(db.JSON)

class DataAsset(db.Model):
    __tablename__ = 'data_asset'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    asset_type = db.Column(db.String(50), nullable=False)
    storage_location = db.Column(db.String(255))
    constraints = db.Column(db.Text)
    update_frequency = db.Column(db.String(50))
    estimated_size = db.Column(db.Integer)
    row_doc_count = db.Column(db.Integer)
    processing_instruction = db.Column(db.String(50))
    custom_fields = db.Column(db.JSON)

class ColumnInfo(db.Model):
    __tablename__ = 'column_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    genai_description = db.Column(db.Text)
    sample_values = db.Column(db.Text)
    data_type = db.Column(db.String(50))
    is_required = db.Column(db.Boolean, default=False)
    data_asset_id = db.Column(db.Integer, db.ForeignKey('data_asset.id'))
    custom_fields = db.Column(db.JSON)

# Home Page Route
@app.route('/', methods=['GET'])
def home():
    print("Request Headers:")
    for header, value in request.headers.items():
        print(f'{header}: {value}')

    return jsonify({'message': 'Welcome to the Business Domain API!'})


@app.before_request
def limit_remote_addr():
    print(f'Request received from - {request.remote_addr}')
    if request.remote_addr not in ['10.20.30.40' , '127.0.0.1']:
        abort(403)  # Forbidden

# Resources

class BusinessDomainResource(Resource):
    def get(self, id=None):
        query = BusinessDomain.query
        if id:
            domain = query.get(id)
            if not domain:
                return {'message': 'Business Domain not found'}, 404
            return jsonify({
                'id': domain.id,
                'name': domain.name,
                'description': domain.description,
                'db_name': domain.db_name,
                'custom_fields': domain.custom_fields
            })
        # Search functionality
        name = request.args.get('name')
        if name:
            query = query.filter(BusinessDomain.name.ilike(f'%{name}%'))
        domains = query.all()
        return jsonify([{
            'id': domain.id,
            'name': domain.name,
            'description': domain.description,
            'db_name': domain.db_name,
            'custom_fields': domain.custom_fields
        } for domain in domains])

class DatasetResource(Resource):
    def get(self, business_domain_id, dataset_id=None):
        query = Dataset.query.filter_by(business_domain_id=business_domain_id)

        # If a specific dataset ID is provided, retrieve that dataset
        if dataset_id:
            dataset = query.filter_by(id=dataset_id).first()
            if not dataset:
                return {'message': 'Dataset not found'}, 404

            return jsonify({
                'id': dataset.id,
                'name': dataset.name,
                'description': dataset.description,
                'business_domain_id': dataset.business_domain_id,
                'owner': dataset.owner,
                'last_updated': dataset.last_updated,
                'number_of_records': dataset.number_of_records,
                'access_level': dataset.access_level,
                'recent_views': dataset.recent_views,
                'custom_fields': dataset.custom_fields
            })

        # Filtering
        name = request.args.get('name')
        owner = request.args.get('owner')
        if name:
            query = query.filter(Dataset.name.ilike(f'%{name}%'))
        if owner:
            query = query.filter(Dataset.owner.ilike(f'%{owner}%'))

        datasets = query.all()
        return jsonify([{
            'id': dataset.id,
            'name': dataset.name,
            'description': dataset.description,
            'business_domain_id': dataset.business_domain_id,
            'owner': dataset.owner,
            'last_updated': dataset.last_updated,
            'number_of_records': dataset.number_of_records,
            'access_level': dataset.access_level,
            'recent_views': dataset.recent_views,
            'custom_fields': dataset.custom_fields
        } for dataset in datasets])

class DataAssetResource(Resource):
    def get(self, business_domain_id, dataset_id, data_asset_id=None):
        query = DataAsset.query.filter_by(dataset_id=dataset_id)

        if data_asset_id:
            data_asset = query.filter_by(id=data_asset_id).first()
            if not data_asset:
                return {'message': 'Data Asset not found'}, 404
            return jsonify({
                'id': data_asset.id,
                'name': data_asset.name,
                'description': data_asset.description,
                'dataset_id': data_asset.dataset_id,
                'asset_type': data_asset.asset_type,
                'storage_location': data_asset.storage_location,
                'constraints': data_asset.constraints,
                'update_frequency': data_asset.update_frequency,
                'estimated_size': data_asset.estimated_size,
                'row_doc_count': data_asset.row_doc_count,
                'processing_instruction': data_asset.processing_instruction,
                'custom_fields': data_asset.custom_fields
            })

        # Search functionality
        name = request.args.get('name')
        asset_type = request.args.get('asset_type')
        if name:
            query = query.filter(DataAsset.name.ilike(f'%{name}%'))
        if asset_type:
            query = query.filter(DataAsset.asset_type.ilike(f'%{asset_type}%'))

        data_assets = query.all()
        return jsonify([{
            'id': data_asset.id,
            'name': data_asset.name,
            'description': data_asset.description,
            'dataset_id': data_asset.dataset_id,
            'asset_type': data_asset.asset_type,
            'storage_location': data_asset.storage_location,
            'constraints': data_asset.constraints,
            'update_frequency': data_asset.update_frequency,
            'estimated_size': data_asset.estimated_size,
            'row_doc_count': data_asset.row_doc_count,
            'processing_instruction': data_asset.processing_instruction,
            'custom_fields': data_asset.custom_fields
        } for data_asset in data_assets])

class ColumnInfoResource(Resource):
    def get(self, business_domain_id, dataset_id, data_asset_id, column_id=None):
        query = ColumnInfo.query.filter_by(data_asset_id=data_asset_id)
        
        if column_id:
            column = query.filter_by(id=column_id).first()
            if not column:
                return {'message': 'Column not found'}, 404
            return jsonify({
                'id': column.id,
                'name': column.name,
                'description': column.description,
                'genai_description': column.genai_description,
                'sample_values': column.sample_values,
                'data_type': column.data_type,
                'is_required': column.is_required,
                'data_asset_id': column.data_asset_id,
                'custom_fields': column.custom_fields
            })

        # Search functionality
        name = request.args.get('name')
        data_type = request.args.get('data_type')
        if name:
            query = query.filter(ColumnInfo.name.ilike(f'%{name}%'))
        if data_type:
            query = query.filter(ColumnInfo.data_type.ilike(f'%{data_type}%'))

        columns = query.all()
        return jsonify([{
            'id': column.id,
            'name': column.name,
            'description': column.description,
            'genai_description': column.genai_description,
            'sample_values': column.sample_values,
            'data_type': column.data_type,
            'is_required': column.is_required,
            'data_asset_id': column.data_asset_id,
            'custom_fields': column.custom_fields
        } for column in columns])

# Add resources to API
api.add_resource(BusinessDomainResource, '/business_domains', '/business_domains/<int:id>')
api.add_resource(DatasetResource, '/business_domains/<int:business_domain_id>/datasets', '/business_domains/<int:business_domain_id>/datasets/<int:dataset_id>')
api.add_resource(DataAssetResource, '/business_domains/<int:business_domain_id>/datasets/<int:dataset_id>/data_assets', '/business_domains/<int:business_domain_id>/datasets/<int:dataset_id>/data_assets/<int:data_asset_id>')
api.add_resource(ColumnInfoResource, '/business_domains/<int:business_domain_id>/datasets/<int:dataset_id>/data_assets/<int:data_asset_id>/columns', '/business_domains/<int:business_domain_id>/datasets/<int:dataset_id>/data_assets/<int:data_asset_id>/columns/<int:column_id>')

if __name__ == '__main__':
    app.run(debug=True)


#/business_domains
#/business_domains/<int:id>
#/business_domains/<int:id>/datasets
#/business_domains/<int:id>/datasets/<int:dataset_id>
#/business_domains/<int:id>/datasets/<int:dataset_id>/data_assets
#/business_domains/<int:id>/datasets/<int:dataset_id>/data_assets/<int:data_asset_id>
#/business_domains/<int:id>/datasets/<int:dataset_id>/data_assets/<int:data_asset_id>/columns
#/business_domains/<int:id>/datasets/<int:dataset_id>/data_assets/<int:data_asset_id>/columns/<int:column_id>

# http://127.0.0.1:5000/business_domains
# http://127.0.0.1:5000/business_domains/1/datasets
# http://127.0.0.1:5000/business_domains/1/datasets/1/data_assets
# http://127.0.0.1:5000/business_domains/1/datasets/1/data_assets/1/columns
# http://127.0.0.1:5000/business_domains/1/datasets/1/data_assets/1/columns/1
# http://127.0.0.1:5000/business_domains/1/datasets/1/data_assets/1/columns?name=date

# edghts_2lnTTHwUtP6DU9BIGjYw9fjKKTa
# https://equipped-crab-readily.ngrok-free.app/
# ngrok tunnel --label edge=edghts_2lnTTHwUtP6DU9BIGjYw9fjKKTa http://localhost:5000
# 
# $ cat /home/ibrez/.config/ngrok/ngrok.yml
# version: 3
# agent:
#   authtoken: xxxxxxXXXXXXXXXXXX_XXXXXXXXXXXXXXXXXXXX
# ngrok config check
# ngrok tunnel --label edge=edghts_2lnTTHwUtP6DU9BIGjYw9fjKKTa http://localhost:5000


