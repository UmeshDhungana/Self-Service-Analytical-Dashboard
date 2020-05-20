from flask import Flask, jsonify, request, redirect
from flask import render_template
from datetime import time
from lib import description
import json

app = Flask(__name__)

@app.route("/")
def index():
    settings = description.get_all_settings()
    table_name = settings[0][1]
    config = json.loads(settings[0][3])
    legend = table_name
    print(table_name)
    labels, values = description.get_time_graph(table_name)
    graph_type = config["graph"]

    return render_template('index.html', values=values, labels=labels, legend=legend, graph_type=graph_type)



@app.route("/simple_chart")
def chart():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('chart.html', values=values, labels=labels, legend=legend)


@app.route("/line_chart")
def line_chart():
    legend = 'Temperatures'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
             '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
             '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']
    return render_template('line_chart.html', values=temperatures, labels=times, legend=legend)


@app.route("/time_chart")
def time_chart():
    legend = 'Temperatures'
    # temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
    #                 61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
    #                 70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    # times = [time(hour=11, minute=14, second=15),
    #          time(hour=11, minute=14, second=30),
    #          time(hour=11, minute=14, second=45),
    #          time(hour=11, minute=15, second=00),
    #          time(hour=11, minute=15, second=15),
    #          time(hour=11, minute=15, second=30),
    #          time(hour=11, minute=15, second=45),
    #          time(hour=11, minute=16, second=00),
    #          time(hour=11, minute=16, second=15),
    #          time(hour=11, minute=16, second=30),
    #          time(hour=11, minute=16, second=45),
    #          time(hour=11, minute=17, second=00),
    #          time(hour=11, minute=17, second=15),
    #          time(hour=11, minute=17, second=30),
    #          time(hour=11, minute=17, second=45),
    #          time(hour=11, minute=18, second=00),
    #          time(hour=11, minute=18, second=15),
    #          time(hour=11, minute=18, second=30)]
    labels, values = description.get_verification_time_graph()
    print(labels)
    print(values)
    return render_template('time_chart.html', values=values, labels=labels, legend=legend)

@app.route("/settings")
def settings():
    available_table = ["registration","verification"]
    settings = description.get_all_settings()
    return render_template('settings.html', tables=available_table, settings=settings )

@app.route("/getTabledetails")
def getTableDetails():
    table_name = request.args.get("table_name")
    details = description.get_columns_names(table_name)
    return jsonify(details)

@app.route("/storesettings", methods=['POST','GET'])
def storesettings():
    table_name = request.args.get('table')
    column_name = request.args.get('columns')
    graph = request.args.get('graph')

    json_string = json.dumps({'column': column_name, 'graph': graph})

    description.store_settings(table_name, json_string)
    return redirect("/settings")

@app.route("/delete", methods=["GET"])
def delete():
    id = request.args.get('id')
    description.delete(id)
    return jsonify({'status': 200})

if __name__ == "__main__":
    app.run(debug=True)
