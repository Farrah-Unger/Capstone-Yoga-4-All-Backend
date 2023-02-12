from flask import Blueprint, jsonify, request
from app import db
from app.models.reflex import Reflex
from app.models.diary import Diary
from app.routes.routes_helper import validate_reflex

reflex_bp = Blueprint("reflex", __name__, url_prefix="/reflex")

#get all reflex /category
@reflex_bp.route("", methods=["GET"])
def get_all_reflexes():
    reflexes = Reflex.query.all()
    reflex_response = []

    for reflex in reflexes:
        reflex_response.append(
            {
            "reflex_id": reflex.reflex_id,
            "title": reflex.title,
            "image": reflex.image
            }
        )

    return jsonify(reflex_response)

#get one reflex /category/reflex
@reflex_bp.route("/<reflex_id>", methods=["GET"]) #is it category/reflex_id? or reflex/id
def get_one_reflex(reflex_id):
    reflex = validate_reflex(reflex_id)
    
    return {
        "reflex": {
            "reflex_id": reflex.reflex_id,
            "title": reflex.title,
            "videos": reflex.videos,
            "image": reflex.image,
            "education": reflex.education
        }
    }

    # query on the id for the urls #
    # q = Reflex.query(videos).filter(reflex_id == id)
    #check for session syntax #


    # SELECT address.* FROM user
    # JOIN address ON user.id=address.user_id
    # WHERE user.name = :name_1
    
            # "education": reflex.education,
            # "videos": reflex.videos
    
# Create a New Reflex for testing purposes
@reflex_bp.route("", methods=["POST"])
def create_reflex():
    request_body = request.get_json()

    try:
        new_reflex = Reflex(
            reflex_id=request_body["reflex_id"], 
            title=request_body["title"],
            education=request_body["education"],
            image=request_body["image"],
            videos=request_body["videos"]
        )
    except KeyError:
        return {"details": "Missing Entry Description"}, 400

    db.session.add(new_reflex)
    db.session.commit()

    return {
        "reflex" : {
            "reflex_id": new_reflex.reflex_id,
            "title": new_reflex.title,
            "education": new_reflex.education,
            "image" : new_reflex.image,
            "videos": new_reflex.videos

        }
    }, 201

# Delete a reflex
@reflex_bp.route("/<reflex_id>", methods=["DELETE"])
def delete_reflex(reflex_id):
    reflex = validate_reflex(reflex_id)

    db.session.delete(reflex)
    db.session.commit()


    return {
        "details": f'Reflex {reflex.reflex_id} successfully deleted'
    }

# update one reflex (education and or videos update)
@reflex_bp.route("/<reflex_id>", methods=["PUT"])
def update_reflex(reflex_id):
    reflex = validate_reflex(reflex_id)

    request_body =request.get_json()
    reflex.education = request_body["education"]
    reflex.videos = request_body["videos"]
    reflex.image = request_body["image"]

    reflex.reflex_id = int(reflex.reflex_id) 
    
    db.session.commit()
    
    return {
        "reflex": {
            "reflex_id": reflex.reflex_id,
            "title": reflex.title,
            "education": reflex.education,
            "image" : reflex.image,
            "videos": reflex.videos,
        }
    }