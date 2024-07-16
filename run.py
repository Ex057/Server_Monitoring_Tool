from app import create_app, db
from app.models import User, Server

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Server': Server}

if __name__ == '__main__':
    app.run(debug=True)