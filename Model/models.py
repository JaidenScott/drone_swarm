import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#DroneModel(db.Model)


class DroneModel(db.Model):
    __tablename__ = "drones"

    drone_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    drone_ip = db.Column(db.String)
    drone_battery = db.Column(db.String)
    #drone_id = ""
    #name = ""
    #ip = ""

    def __init__(self, drone_id, name, drone_ip):
        self.drone_id = drone_id
        self.name = name
        self.drone_ip = drone_ip
        self.drone_battery = "Unknown"





