from flask import Flask, request, jsonify
import sqlite3
import logging

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('daily_activity.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/initial_state', methods=['GET'])
def get_initial_state():
    conn = get_db_connection()
    state = conn.execute("SELECT state FROM states WHERE is_initial=1").fetchone()
    conn.close()
    return jsonify(state=state['state'] if state else 'None')


@app.route('/user_feedback', methods=['POST'])
def get_user_feedback():
    data = request.get_json()
    predicted_activity = data.get('predicted_activity')
    conn = get_db_connection()
    feedback = conn.execute("SELECT feedback FROM feedback WHERE activity=?", (predicted_activity,)).fetchone()
    conn.close()
    return jsonify(feedback=feedback['feedback'] if feedback else 'No')


@app.route('/update_state', methods=['POST'])
def update_state_with_feedback():
    data = request.get_json()
    user_feedback = data.get('user_feedback')
    current_state = data.get('current_state')
    conn = get_db_connection()
    conn.execute("UPDATE states SET feedback=? WHERE state=?", (user_feedback, current_state))
    conn.commit()
    next_state = conn.execute("SELECT state FROM states WHERE state=?", (current_state,)).fetchone()
    conn.close()
    return jsonify(next_state=next_state['state'] if next_state else current_state)


@app.route('/check_day_end', methods=['GET'])
def check_if_day_ends():
    conn = get_db_connection()
    status = conn.execute("SELECT day_end FROM daily_status ORDER BY created_at DESC LIMIT 1").fetchone()
    conn.close()
    return jsonify(day_ends=bool(status['day_end']) if status else False)


@app.route('/initial_location', methods=['GET'])
def get_initial_location():
    conn = get_db_connection()
    initial_state = conn.execute("SELECT state FROM states WHERE is_initial=1").fetchone()
    location = conn.execute("SELECT location FROM locations WHERE state=?", (initial_state['state'],)).fetchone()
    conn.close()
    return jsonify(location=location['location'] if location else 'location_1')


@app.route('/location', methods=['GET'])
def get_location_from_database():
    state = request.args.get('state')
    conn = get_db_connection()
    location = conn.execute("SELECT location FROM locations WHERE state=?", (state,)).fetchone()
    conn.close()
    return jsonify(location=location['location'] if location else 'location_1')


@app.route('/activity', methods=['GET'])
def get_activity_from_database():
    activity_id = int(request.args.get('activity_id'))
    conn = get_db_connection()
    activity = conn.execute("SELECT activity FROM activities WHERE id=?", (activity_id,)).fetchone()
    conn.close()
    return jsonify(activity=activity['activity'] if activity else 'unknown_activity')


@app.route('/activities', methods=['GET'])
def get_all_activities():
    conn = get_db_connection()
    activities = conn.execute("SELECT id, activity FROM activities").fetchall()
    conn.close()
    return jsonify(activities=[dict(activity) for activity in activities])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000)
