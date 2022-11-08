from flask import Flask, render_template, request, redirect, url_for
from Model.models import DroneModel, db
from flask_sqlalchemy import SQLAlchemy
from djitellopy.swarm import TelloSwarm



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drone_DB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

drone_commands = []

db.init_app(app)


@app.route('/', methods=["POST","GET"])
def index():
    drone_list = DroneModel.query.all()
    print(drone_list)
    # drone_list.append(drone)
    return render_template('index.html', drone_list=drone_list, drone_commands=drone_commands)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/add_drone', methods=["POST","GET"])
def add_drone():
    if request.method == 'GET':
        return render_template('add_drone.html')
    if request.method == 'POST':
        drone = DroneModel(request.form.get("id"), request.form.get("name"), request.form.get("ip"))
        db.session.add(drone)
        db.session.commit()
        return redirect(url_for("index"))


@app.route('/delete_drone', methods=["POST", "GET"])
def delete_drone():
    if request.method == 'GET':
        return render_template("delete_drone.html")
    if request.method == 'POST':
        id = request.form.get("ID")
        drone = DroneModel.query.filter_by(drone_id=id).first()
        if drone is not None:
            db.session.delete(drone)
            db.session.commit()
        return redirect(url_for("index"))


@app.route('/command_added')
def command_added():
    return render_template('command_added.html')


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
    drone_list = DroneModel.query.all()

    for i in drone_list:
        drone_ips.append(i.drone_ip)
    print(drone_ips)
    if len(drone_ips) != 0:
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

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run()
