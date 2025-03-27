from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'  # Sử dụng SQLite, có thể đổi sang PostgreSQL/MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://phuongvv:Phuongvv@123@/hotel_db?host=/cloudsql/mineral-style-252402:us-central1:hotel-db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model CSDL
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{ "id": r.id, "name": r.name, "price": r.price, "available": r.available } for r in rooms])

@app.route('/api/book', methods=['POST'])
def book_room():
    data = request.json
    room = Room.query.get(data.get("room_id"))
    if room and room.available:
        room.available = False
        booking = Booking(room_id=room.id, name=data["name"], email=data["email"])
        db.session.add(booking)
        db.session.commit()
        return jsonify({"message": "Đặt phòng thành công!", "room": {"id": room.id, "name": room.name, "price": room.price}})
    return jsonify({"message": "Phòng không khả dụng."}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    response = {"reply": f"Bạn đã nói: {user_message}. Tôi có thể giúp gì?"}
    return jsonify(response)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
