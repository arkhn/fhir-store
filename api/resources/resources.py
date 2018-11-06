from flask import jsonify, send_from_directory
# note: prefer send_from_directory to send_file  as send_file is not secured.
# From the official documentation : "Please never pass filenames to this function from user sources;
# you should use send_from_directory() instead."
from flask_restful import Resource, reqparse
import os
import yaml

from api.common.utils import fhir_resource_path


class Store(Resource):
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('output_format', required=True, type=str, choices=('json', 'yml'))
        parser.add_argument('fhir_resource_name', required=True, type=str)

        args = parser.parse_args()

        file_path = fhir_resource_path(args['fhir_resource_name'], parent_folder=args['output_format'])
        if not file_path:
            return jsonify(
                {"message": "Fhir resource not found."}
            )

        folder = os.path.dirname(file_path)
        file = os.path.basename(file_path)
        if args['output_format'] == 'json':
            return jsonify(yaml.load(open(file_path)))

        elif args['output_format'] == 'yml':
            return send_from_directory(folder, file)


class Mapping(Resource):
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('output_format', required=True, type=str, choices=('json', 'yml'))
        parser.add_argument('fhir_resource_name', required=True, type=str)
        parser.add_argument('database', required=True, type=str)

        args = parser.args()

        file_path = fhir_resource_path(args['fhir_resource_name'], parent_folder=args['database'])
        if not file_path:
            return jsonify(
                {"message": "Fhir resource not found."}
            )

        folder = os.path.dirname(file_path)
        file = os.path.basename(file_path)

        if args['output_format'] == 'json':
            return jsonify(yaml.load(open(file_path)))

        elif args['output_format'] == 'yml':
            return send_from_directory(folder, file)
