#!/usr/bin/python3
""" API actions for user object """
from flask import jsonify, make_response, abort, request, Blueprint
from api.v1.views import app_views
from models import storage
from models import Review, Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """gets list of all review objects by specific place_id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    review_save = storage.all("Review")
    reviews = []
    for value in review_save.values():
        reviews.append(value_to_dict())
    return jsonify(reviews)


@app_views.route('/review/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """fetches review from storage"""
    try:
        review = storage.get('Review', review_id)
        return jsonify(review.to_dict())
    except Exception:
            abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """fetches review obj from storage and deletes it.
    returns empty json response with status code 200"""
    try:
        reviewObj = storage.get('Review', review_id)
        reviewObj.delete()
        return jsonify({}), 200
    except Exception:
            abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review():
    """handles creation for new review for specific place"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400

    newReview = Review(user_id=request.get_json()["user_id"])

    for key, value in request.get_json().items():
        setattr(newReview, key, value)

    newReview.save()

    return (jsonify(newReview.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """updates review object by specific id"""
    review = storage.get('Review', review_id)

    if review is None:
        abort(404)

    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    update_fields = ['id', 'created_at', 'user_id', 'updated_at']
    for key, value in request.get_json().items():
        if key not in update_fields:
            setattr(review, key, value)

    review.save()

    return (jsonify(review.to_dict()), 200)
