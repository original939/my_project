from flask import Flask, render_template, request, redirect, Response
from prometheus_client import Gauge, generate_latest

app = Flask(__name__)

todos = []

# Создайте метрику для количества запросов
requests_total = Gauge('my_website_requests_total', 'Total number of requests to my website')

# Создайте метрику для количества добавленных задач
todos_added_total = Gauge('my_website_todos_added_total', 'Total number of todos added')

@app.route('/')
def index():
    requests_total.inc()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    todo = request.form.get('todo')
    if todo:
        todos.append(todo)
        todos_added_total.inc()
    return redirect('/')

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
    return redirect('/')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

