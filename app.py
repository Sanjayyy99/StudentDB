from flask import Flask, request, jsonify
import sqlite3

DB_PATH = "students.db"
app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            grade TEXT
        );
    """)
    conn.commit()
    conn.close()

@app.route("/students", methods=["GET"])
def list_students():
    conn = get_db()
    rows = conn.execute("SELECT id, name, age, grade FROM students").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows]), 200

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_db()
    row = conn.execute(
        "SELECT id, name, age, grade FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(row)), 200

@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    age = data.get("age")
    grade = data.get("grade")
    if not name:
        return jsonify({"error": "name is required"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
        (name, age, grade)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"message": "created", "id": new_id}), 201

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    age = data.get("age")
    grade = data.get("grade")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?",
        (name, age, grade, student_id)
    )
    conn.commit()
    changed = cur.rowcount
    conn.close()

    if changed == 0:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "updated"}), 200

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    changed = cur.rowcount
    conn.close()

    if changed == 0:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "deleted"}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
