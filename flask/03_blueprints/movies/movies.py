from flask import Blueprint
from flask import request, jsonify

movies_list = [
    {
        "name": "The Shawshank Redemption",
        "casts": [
            "Tim Robbins",
            "Morgan Freeman",
            "Bob Gunton",
            "William Sadler",
        ],
        "genres": ["Drama"],
        "budget": 25000000,
    },
    {
        "name": "The Godfather ",
        "casts": ["Marlon Brando", "Al Pacino", "James Caan", "Diane Keaton"],
        "genres": ["Crime", "Drama"],
        "budget": 6000000,
    },
    {
        "name": "The Avengers",
        "casts": ["Robert Downey Jr", "Scarlett Johansson", "Chris Evans"],
        "genres": ["Fiction", "Action"],
        "budget": 220000000,
    },
]

movies_bp = Blueprint('movies_bp', __name__)


@movies_bp.route('/')
@movies_bp.route('/movies')
def movies():
    if request.method == "GET":
        print("GET method listened.")

    if request.args:
        print("Args present!")

        if "budget_lt" in request.args:
            budget_max = int(request.args.get('budget_lt'))
            movies_list_filtered = [
                movie for movie in movies_list if movie['budget'] < budget_max
            ]
            return jsonify(movies_list_filtered), 200

    return jsonify(movies_list), 200


@movies_bp.route('/movies/genres')
def genres():
    genres = [{"genres": movie["genres"]} for movie in movies_list]
    return jsonify(genres), 200


@movies_bp.route('/movies/<int:index>/increase-budget')
def increase_budget(index):
    movies_list[index]['budget'] += 1
    return jsonify(movies_list[index]), 200


@movies_bp.route('/movies', methods=['POST'])
def add_movie():
    if request.method == "POST":
        print("POST method listened.")

    movie = request.get_json(force=True)
    movies_list.append(movie)
    return {'id': len(movies_list)}, 201


@movies_bp.route('/movies/<int:index>', methods=['PUT'])
def update_movie(index):
    movie = request.get_json()
    movies_list[index] = movie
    return jsonify(movies_list[index]), 200


@movies_bp.route('/movies/<int:index>', methods=['DELETE'])
def delete_movie(index):
    movies_list.pop(index)
    return {}, 204
