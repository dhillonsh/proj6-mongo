#from bson.objectid import ObjectId
from pymongo.objectid import ObjectId
import arrow

def humanize_arrow_date( date ):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case. 
    """
    try:
        then = arrow.get(arrow.get(date).format('YYYY-MM-DD'))
        now = arrow.get(arrow.utcnow().to('local').format('YYYY-MM-DD'))
        if then.date() == now.date():
            human = "Today"
        else: 
            human = then.humanize(now)
            if human == "in a day":
                human = "Tomorrow"
    except: 
        human = date
    return human


#############
#
# Functions available to the page code above
#
##############
def get_memos(collection):
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ):
        record['date'] = humanize_arrow_date(arrow.get(record['date']))
        #del record['_id']
        records.append(record)
    return records 

def add_memo(collection, date, memo):
    record = { "type": "dated_memo", "date":  arrow.get(date).naive.isoformat(), "text": memo }
    collection.insert(record)

def delete_memo(collection, _id):
    collection.remove({'_id': ObjectId(_id)})
