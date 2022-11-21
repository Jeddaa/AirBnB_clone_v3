#!/usr/bin/python3
"""view for Place objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.user import User
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review(place_id):
    """retrieves the list of reviews object of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """retrieves a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """deletes an instance of review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """creates a review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, decription="Missing user_id")

    user_id = data['user_id']
    if not storage.get(User, user_id):
        abort(404)
    if 'text' not in data:
        abort(400, description="Missing text")

    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """update the review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
