from flask_app.models.model_post import Post
from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_img

# API
@app.route('/img/create/<int:post_id>', methods=['post'])
@app.route('/img/create', methods=['post'])
def create_img(post_id=0):
    is_valid = model_img.Image.validate_images(request.form)
    if not is_valid:
        response = {
            'code': 400
        }
        return response

    img_id = model_img.Image.create(request.form)
    if img_id:
        print("img -> create -> if 1")
        if post_id != 0:
            print("img -> create -> if 2")
            model_img.Image.create_image_link({
                'post_id': post_id,
                'image_id': img_id,
            })
            response = {
                'msg': 'Upload successfull',
                'img_id': img_id,
                'code': 200
            }
            print(response)
            return jsonify(response)
    return jsonify(msg="image upload failed")

@app.route('/img/<int:id>')
def show_img(id):
    return 'show img'

@app.route('/img/<int:id>/delete')
def delete_img(id):
    img_id = model_img.Image.delete_one(id)
    if img_id:
        return jsonify(msg="Image delete successful")
    return jsonify(msg="unable to delete image")