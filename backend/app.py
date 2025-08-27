from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection, init_db

app = Flask(__name__)
CORS(app)

# Initialize DB if not exists
init_db()

@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos ORDER BY id ASC;")
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    task = data.get("task", "").strip()
    if not task:
        return jsonify({"error": "Task cannot be empty"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (task) VALUES (%s) RETURNING *;", (task,))
    new_todo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_todo)

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s RETURNING *;", (todo_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({"message": "Todo deleted"})
    else:
        return jsonify({"error": "Todo not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
