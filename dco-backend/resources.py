# resources.py

from flask_restful import Resource
from flask import jsonify, request, Response
from models import BusinessDomain, Dataset, DataAsset, ColumnInfo, db
import time 

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
    def get(self, dataset_id, data_asset_id=None):
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
    def get(self, data_asset_id, column_id=None):
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



class StreamContentResource(Resource):
    @staticmethod
    def stream_llm_responses(prompt):
        responses = [f"Response part {i+1}" for i in range(10)]
        for response in responses:
            yield f"data: {response}\n\n"
            time.sleep(1)  # Simulate delay

    def post(self):
        # Check if the Content-Type is application/json
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({"error": "Unsupported Media Type, expected 'application/json'"}), 415

        # Parse the JSON data from the request
        data = request.get_json()
        message = data.get("message")
        model = data.get("model")

        # Validate the presence of 'message' and 'model' parameters
        if not message or not model:
            return jsonify({"error": "Missing 'message' or 'model' parameter"}), 400

        # Handle fixed model response
        if model == 'fixed':
            response_text = "This is a fixed response. Oops! I can't help but laugh. Did you really just say that?"
            resp = Response(response_text)
            resp.headers.add('Content-Type', 'application/text')
            return resp

        # Handle other models (streaming response from LLM)
        else:
            resp = Response(self.stream_llm_responses(message), content_type='text/event-stream')
            return resp

        # Return method not allowed for other methods
        return jsonify({"error": "Method not allowed"}), 405