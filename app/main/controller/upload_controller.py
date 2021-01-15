from werkzeug.datastructures import FileStorage

from flask_restplus import Namespace, fields, reqparse,Resource
from ..service.upload_service import *

api = Namespace('upload', description='User related operation')

uploadParser = reqparse.RequestParser()
uploadParser.add_argument('publicId', type=str, required=True)
uploadParser.add_argument('file1', location="files", type=FileStorage, required=True)


@api.route("/profile")
class UploadImage(Resource):

    @api.expect(uploadParser, validate=True)
    def put(self):
        """ upload profile Image"""
        data = uploadParser.parse_args()
        return upload_profile_image(data=data)

@api.route('/post')
class UploadPostImage(Resource):
    @api.expect(uploadParser)
    def put(self):
        data = uploadParser.parse_args()
        return uplaod_post_image(data=data)


