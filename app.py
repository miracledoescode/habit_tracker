from flask import Flask, render_template, request, jsonify, g
from database import get_db, close_db, init_db, query_db
import datetime
import os

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/habits', methods=['GET'])
def get_habits():
    # Get all habits
    habits = query_db('SELECT * FROM habits ORDER BY created_at DESC')
    
    habits_data = []
    today = datetime.date.today().isoformat()
    
    for habit in habits:
        habit_id = habit['id']
        
        # Get logs for this habit
        logs_rows = query_db('SELECT log_date FROM daily_logs WHERE habit_id = ? ORDER BY log_date DESC', (habit_id,))
        logs = [str(log['log_date']) for log in logs_rows] # Convert date objects to string for JSON serialization if needed
        
        # Calculate streak
        streak = 0
        current_date = datetime.date.today()
        
        check_date = current_date
        if today not in logs:
             check_date = current_date - datetime.timedelta(days=1)
             
        while check_date.isoformat() in logs:
            streak += 1
            check_date -= datetime.timedelta(days=1)
            
        habits_data.append({
            'id': habit['id'],
            'name': habit['name'],
            'completed_today': today in logs,
            'streak': streak,
            'logs': logs
        })
        
    return jsonify(habits_data)

@app.route('/api/habits', methods=['POST'])
def add_habit():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
        
    query_db('INSERT INTO habits (name) VALUES (?)', (name,))
    
    return jsonify({'success': True}), 201

@app.route('/api/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    query_db('DELETE FROM habits WHERE id = ?', (habit_id,))
    return jsonify({'success': True})

@app.route('/api/logs', methods=['POST'])
def toggle_log():
    data = request.get_json()
    habit_id = data.get('habit_id')
    date_str = data.get('date', datetime.date.today().isoformat())
    
    if not habit_id:
        return jsonify({'error': 'Habit ID is required'}), 400
        
    # Check if exists
    existing = query_db('SELECT 1 FROM daily_logs WHERE habit_id = ? AND log_date = ?', (habit_id, date_str), one=True)
    
    if existing:
        query_db('DELETE FROM daily_logs WHERE habit_id = ? AND log_date = ?', (habit_id, date_str))
        status = 'removed'
    else:
        query_db('INSERT INTO daily_logs (habit_id, log_date) VALUES (?, ?)', (habit_id, date_str))
        status = 'added'
        
    return jsonify({'status': status})

@app.route('/api/debug-db')
def debug_db():
    try:
        db = get_db()
        db.execute('SELECT 1')
        return jsonify({'status': 'ok', 'db_type': getattr(g, '_db_type', 'unknown')})
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

if __name__ == '__main__':
    # Initialize DB if locally and it doesn't exist
    if not os.environ.get('DATABASE_URL') and not os.path.exists('habits.db'):
        with app.app_context():
            init_db(app)
            
    app.run(debug=True)
