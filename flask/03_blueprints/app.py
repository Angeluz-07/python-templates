from flask import Flask
from movies.movies import movies_bp

app = Flask(__name__)

app.register_blueprint(movies_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run()
