from flask import make_response, abort
from app.models.diary import Diary
from app.models.reflex import Reflex

# # Validate reflex helper function
def validate_reflex(reflex_id):
    try:
        reflex_id = int(reflex_id)
    except:
        abort(make_response({"details": "Invalid Data, id must be a number"}, 400))
    
    reflex = Reflex.query.get(reflex_id)
    # print("reflex test print", reflex)
    if not reflex:
        abort(make_response({"details": f"There is no existing reflex {reflex_id}"}, 400))
    
    return reflex

## Validate diary entry helper function
def validate_entry(diary_id):
    try:
        diary_id = int(diary_id)
    except:
        abort(make_response({"message": f"diary {diary_id} invalid"}, 400))

    entry = Diary.query.get(diary_id)

    if not entry:
        abort(make_response({"message":f"diary {diary_id} not found"}, 404))

    return entry