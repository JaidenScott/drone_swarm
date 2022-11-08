import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#DroneModel(db.Models)
class DroneModel():
    __tablename__ = "drones"

    #drone_id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String)
    #ip = db.Column(db.String)
    drone_id = ""
    name = ""
    ip = ""

    def __init__(self, drone_id, name, ip):
        self.drone_id = drone_id
        self.name = name
        self.drone_ip = ip

    def __repr__(self):
        return f"{self.drone_id}:{self.name}:{self.drone_ip}"

    def create_drone(self):
        pass

    def read_drone(self):
        pass

    def delete_drone(self):
        pass



