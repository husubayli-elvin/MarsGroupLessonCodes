from flask import request, jsonify, send_from_directory
from http import HTTPStatus
from post_service.app import app
from marshmallow.exceptions import ValidationError

from post_service.schemas.schmas import RecipeSchema
from post_service.config.base import MEDIA_ROOT

from post_service.utils.common import save_file


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(MEDIA_ROOT, filename)


@app.route('/recipes/', methods=['POST'])
def recipes():
    if request.method == 'POST':
        try:
            data = request.json or request.form
            image = request.files.get('image')
            serializer = RecipeSchema(exclude=['image', 'owner_id'])
            print('here')
            recipe = serializer.load(data)
            print(recipe)
            recipe.owner_id = 1
            recipe.image = save_file(image)
            recipe.save()
            print(recipe)
            return RecipeSchema().jsonify(recipe), HTTPStatus.CREATED
        except ValidationError as err:
            return jsonify(err.messages), HTTPStatus.BAD_REQUEST
