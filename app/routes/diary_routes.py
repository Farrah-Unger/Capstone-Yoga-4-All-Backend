from flask import Blueprint, request, jsonify
from app import db
from app.models.diary import Diary
from app.routes.routes_helper import validate_entry
# from datetime import date

diary_bp = Blueprint("diary", __name__, url_prefix="/diary")

# Create a New Entry
@diary_bp.route("", methods=["POST"])
def create_entry():
    request_body = request.get_json()

    try:
        new_entry = Diary(
            # diary_id=request_body["diary_id"], 
            entry=request_body["entry"],
            posted_at=request_body["posted_at"]
        )
    except KeyError:
        return {"details": "Missing Entry Description"}, 400

    db.session.add(new_entry)
    db.session.commit()

    return {
        "entry" : {
            # "diary_id": new_entry.diary_id,
            "entry": new_entry.entry,
            "posted at": new_entry.posted_at
        }
    }, 201

# Get all diary entries
@diary_bp.route("", methods=["GET"])
def read_all_entries():
    
        entries = Diary.query.all()
        entries_response = []
    
        for entry in entries:
            entries_response.append(
                {
                    "diary_id": entry.diary_id,
                    "posted_at": entry.posted_at,
                    "entry": entry.entry
                }
            )
        return jsonify(entries_response)

# Get ONE diary entry
@diary_bp.route("/<diary_id>", methods=["GET"])
def read_one_entry(diary_id):
    entry = validate_entry(diary_id)

    return {
        "entry": {
            "id": entry.diary_id,
            "posted_at": entry.posted_at,
            "entry": entry.entry
        }
    }
    
# Update a diary entry
@diary_bp.route("/<diary_id>", methods=["PUT"])
def update_entry(diary_id):
    entry = validate_entry(diary_id)

    request_body =request.get_json()
    entry.entry = request_body["entry"]

    entry.diary_id = int(entry.diary_id) 
    
    db.session.commit()
    
    return {
        "entry": {
            "diary_id": entry.diary_id,
            "entry": entry.entry,
            "posted_at": entry.posted_at
        }
    }

# Delete a diary entry
@diary_bp.route("/<diary_id>", methods=["DELETE"])
def delete_diary(diary_id):
    entry = validate_entry(diary_id)

    db.session.delete(entry)
    db.session.commit()


    return {
        "details": f'Diary entry {entry.diary_id} successfully deleted'
    }

    # testing