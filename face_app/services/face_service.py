import json
from face_app.db_connection import get_connection

def upsert_visitor(visitor_id, embedding):
    embedding_json = json.dumps(embedding)
    conn = get_connection()
    cursor = conn.cursor()
    # check if user exists
    cursor.execute("""
        SELECT visitor_id FROM visitor_master WHERE visitor_id = ?
    """, (visitor_id,))
    
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE visitor_master
            SET embading_data = ?
            WHERE visitor_id = ?
        """, (embedding_json, visitor_id))
    conn.commit()
    conn.close()
    return {"message": "upload  successful"}

def get_all_visitor():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT visitor_id, visitor_name, embading_data,visitor_number,visitor_address
        FROM visitor_master
        WHERE embading_data IS NOT NULL
    """)

    rows = cursor.fetchall()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "embedding": row[2],
            "mobile":row[3],
            "address":row[4]
        })
    conn.close()
    return users

def getCheckVisitor(checkBy, checkType, visitor):
    
    visitor_id = visitor.get("id")

    # 👉 CALL YOUR STORED PROCEDURE HERE
    # example:
    # call_checkin_sp(visitor_id, checkBy, checkType)

    if checkType == "checkIn":
        return {
            "status": 1,
            "message": "Visitor Check In Successfully",
            "visitor": visitor
        }
    else:
        return {
            "status": 1,
            "message": "Visitor Check Out Successfully",
            "visitor": visitor
        }


def get_single_visitor(visitor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT visitor_id, visitor_name, embading_data, visitor_number, visitor_address
        FROM visitor_master
        WHERE visitor_id = ?
    """, (visitor_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "embedding": row[2],
        "mobile": row[3],
        "address": row[4]
    }