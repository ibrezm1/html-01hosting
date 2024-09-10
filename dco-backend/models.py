# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
