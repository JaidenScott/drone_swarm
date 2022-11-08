from flask import Flask, render_template, request, redirect, url_for
from Model.models import DroneModel
from flask_sqlalchemy import SQLAlchemy
from djitellopy.swarm import TelloSwarm



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drone_DB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

drone_list = []
drone_commands = []


@app.route('/', methods=["POST","GET"])
def index():
    if request.form:
        drone = DroneModel(request.form.get("id"), request.form.get("name"), request.form.get("ip"))
        drone_list.append(drone)
    return render_template('index.html', drone_list=drone_list, drone_commands=drone_commands)


@app.route('/add_drone', methods=["POST","GET"])
def add_drone():
    return render_template('add_drone.html')


@app.route('/command_added')
def command_added():
    return render_template('command_added.html')


@app.before_first_request
def create_table():
    pass
    #db.create_all()


@app.route('/move_left')
def move_left():
    drone_commands.append("left")
    return redirect(url_for("index"))


@app.route('/move_right')
def move_right():
    drone_commands.append("right")
    return redirect(url_for("index"))


@app.route('/move_forward')
def move_forward():
    drone_commands.append("forward")
    return redirect(url_for("index"))


@app.route('/clear_all_commands')
def clear_all_commands():
    drone_commands.clear()
    return redirect(url_for("index"))


@app.route('/start_operation')
def start_operation():
    drone_ips = []
    for i in drone_list:
        drone_ips.append(i.drone_ip)

    if len(drone_ips) != 0:
        operation_status = ""
        swarm = TelloSwarm.fromIps(drone_ips)

        swarm.connect()
        swarm.takeoff()

        for i in drone_commands:
            print(i)
            if i == "left":
                swarm.move_left(100)
            if i == "right":
                swarm.move_right(100)
            if i == "forward":
                swarm.move_forward(100)

        swarm.land()
        swarm.end()
    else:
        operation_status = "Cant start operation without drones"

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run()
