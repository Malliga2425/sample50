from flask import Flask, request, render_template, jsonify, session, Blueprint
import json
import os, time, shutil,  requests
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import re
from flask_sqlalchemy import SQLAlchemy
from bl import get_product_details,get_proposer_details,get_translations,get_user_details,insert_all_details,get_all_details
from model import db
from flasgger import Swagger,swag_from
from swagger import template,swagger_config

app = Flask(__name__)
front_prefix = Blueprint("Api", __name__,  url_prefix="/Data")
app.secret_key = 'KSV'
# Use your actual database URI here
app.config.from_mapping(
           # SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://ksvadmin:KaizenAdmin%40275@150.230.166.29/AdityaBirlaPIVC',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
       
            SWAGGER={
                'title': "Flasgger",
                'uiversion': 3
            }
        )

swagger_config['swagger_ui_bundle_js'] = 'static/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = 'static/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = 'static/jquery.min.js'
swagger_config['swagger_ui_css'] = 'static/swagger-ui.css'


db.init_app(app)
# Set up logging
logging.basicConfig(level=logging.INFO)
 
# Set up file handler for logging
file_handler = RotatingFileHandler('api.log', maxBytes=1024*1024*10, backupCount=5)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
 
 
@front_prefix.route('/get_translations', methods=['GET'])
def api_get_translations():
    language = request.args.get('language')
    page_name = request.args.get('page_name')
    return jsonify(get_translations(language, page_name))
 
@front_prefix.route('/get_user_details', methods=['GET'])
def api_get_user_details():
    dob = request.args.get('dob')
    mobile_number = request.args.get('mobile_number')
    return jsonify(get_user_details(dob, mobile_number))
 
@front_prefix.route('/get_proposer_details', methods=['GET'])
def api_get_proposer_details():
    application_id = request.args.get('application_ID')  # Adjust parameter name
    return jsonify(get_proposer_details(application_id))  # Adjust parameter name
 
@front_prefix.route('/get_product_details', methods=['GET'])
def api_get_product_details():
    application_id = request.args.get('application_id')
    return jsonify(get_product_details(application_id))
 
    
@front_prefix.route('/insert_data', methods=['POST'])
@swag_from('insert_all_details.yaml')
def insert_data():

    user_data = {
        "application_id": request.args.get('application_id'),
        "dob": request.args.get('dob'),
        "consent": 0,
        "mobile_number": request.args.get('mobile_number'),
        "language": request.args.get('language'),
        "enrolment_photo": request.args.get('enrolment_photo'),
        "verification_link": request.args.get('verification_link'),
    }
 
    proposer_data = {
        "application_id": request.args.get('application_id'),
        "owner_name": request.args.get('owner_name'),
        "owner_dob": request.args.get('dob'),
        "address": request.args.get('address'),
        "pincode": request.args.get('pincode'),
        "mail_id": request.args.get('mail_id'),
        "insured_name": request.args.get('insured_name'),
        "insured_dob": request.args.get('insured_dob'),
        "city_state": request.args.get('city_state'),
        "mobile_number": request.args.get('mobile_number'),
    }
 
    product_data = {
        "application_id": request.args.get('application_id'),
        "plan_name": request.args.get('plan_name'),
        "sum_assured": request.args.get('sum_assured'),
        "premium_term": request.args.get('premium_term'),
        "frequency": request.args.get('frequency'),
        "plan_type": request.args.get('plan_type'),
        "policy_term": request.args.get('policy_term'),
        "premium_amount": request.args.get('premium_amount'),
        "purpose_insurance": request.args.get('purpose_insurance'),
    }
 
    return insert_all_details(user_data, proposer_data, product_data)
 
    
@front_prefix.route('/get_all_details', methods=['GET'])
@swag_from('get_all_details.yaml')
def api_get_all_details():
   
    application_id = request.args.get('application_id')

    return jsonify(get_all_details(application_id))

app.register_blueprint(front_prefix)
Swagger(app, config=swagger_config, template=template)

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8088)