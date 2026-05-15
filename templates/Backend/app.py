from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
NOTES_FILE = 'notes.json'

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return[]
    with open(NOTES_FILE, 'r') as f:
        return json.load(f)
def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
         json.dump(notes,f)

@app.route('/')
def index():
    notes = load_notes()
    return render_template('index.html', notes = notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()
    if title or body:
        notes = load_notes()
        notes.insert(0, {'id': len(notes) + 1, 'title': title or 'Untitled', 'body': body})
        save_notes(notes)
        return redirect(url_for('index'))
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    notes = load_notes()
    notes = [n for n in notes if n['id'] != note_id]
    save_notes(notes)
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)

    