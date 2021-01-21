from werkzeug.datastructures import FileStorage

from flask_restplus import Namespace, fields, reqparse,Resource
from ..service.upload_service import *
from app.main.model.posts_model import *
from app.main.utils.middleware.route_guard import roles_required

api = Namespace('upload',authorizations=Const.authorizations, description='User related operation')

uploadParser = reqparse.RequestParser()
uploadParser.add_argument('publicId', type=str, required=True)
uploadParser.add_argument('file1', location="files", type=FileStorage, required=True)


@api.route("/profile")
class UploadImage(Resource):
    target = os.path.join(Const.APP_ROOT, 'files')  # folder path
    if not os.path.isdir(target):
        os.mkdir(target)
    # @api.doc(security='apikey')
    # @roles_required("ADMIN","DEVELOPER")
    @api.expect(uploadParser, validate=True)
    def put(self):
        """ upload profile Image"""
        data = uploadParser.parse_args()
        return upload_profile_image(data=data)

@api.route('/post')
class UploadPostImage(Resource):
    target = os.path.join(Const.APP_ROOT, 'files')  # folder path
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    # @api.doc(security="apikey")
    # @roles_required("ADMIN", "DEVELOPER")
    @api.expect(uploadParser)
    def put(self):
        data = uploadParser.parse_args()
        return uplaod_post_image(data=data)


