from src import app

@app.route('/login')
def login():
    return 'Hello from login'