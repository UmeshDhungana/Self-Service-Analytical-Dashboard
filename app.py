from flask import Flask, jsonify, request, redirect, flash
from flask import render_template
from werkzeug.utils import secure_filename
import os
import pandas as pd
from datetime import time
from lib import description
from DBUtils import engine
import json

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)

@app.route("/")
def index():
    settings = description.get_all_settings()
    value_list = []
    label_list = []
    legend_list = []
    graph_type_list = []
    description_list = []
    ids = []


    for setting in settings:
        table_name = setting[1]
        config = json.loads(setting[3])
        legend = table_name
        date = config["date"]
        end_date = config["end_date"]
        if table_name == "registration & verification":
            labels, values = description.get_reg_vs_verif_count(date, end_date)
        elif(config["column"] =="date"):
            labels, values = description.get_time_graph(table_name, date, end_date)
        else:
            labels, values = description.get_count(table_name, config["column"], date, end_date)
        graph_type = config["graph"]
        description_list.append(config["description"])
        value_list.append(values)
        label_list.append(labels)
        legend_list.append(legend)
        graph_type_list.append(graph_type)
        ids.append(setting[0])

    return render_template('index.html', values=value_list, labels=label_list, legend=legend_list, graph_type=graph_type_list, description=description_list, ids=ids)



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
    available_table = ["registration","verification", "registration & verification"]
    settings = description.get_all_settings()
    edit_id = request.args.get("edit")
    print("-------------", edit_id)
    config = []
    for setting in settings:
        conf = json.loads(setting[3])
        config.append(conf)
    return render_template('settings.html', tables=available_table, settings=settings, config = zip(settings, config), edit_id=edit_id)

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
    desc = request.args.get('desc')
    date = request.args.get('date')
    end_date = request.args.get('end_date')

    json_string = json.dumps({'column': column_name, 'graph': graph, 'description': desc, 'date': date, 'end_date': end_date})

    description.store_settings(table_name, json_string)
    flash("New figure added")
    return redirect("/settings")

@app.route("/delete", methods=["GET"])
def delete():
    id = request.args.get('id')
    description.delete(id)
    return jsonify({'status': 200})

@app.route("/upload-csv", methods=["GET","POST"])
def upload_csv():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        table = request.form.get("table")
        # if user does not select file, browser also
        # submit an empty part without filename
        if file:
            filename = secure_filename(file.filename)

            full_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(full_path)
            df = pd.read_csv(full_path)
            df.to_sql(name=table, con=engine, index=False, if_exists='append')
            flash("Upload successful")
        else:
            flash("file not found")
    return render_template('uploadcsv.html')

@app.route("/edit", methods=["POST","GET"])
def edit():
    graph = request.args.get('graph')
    desc = request.args.get('desc')
    id = request.args.get('id')
    date = request.args.get('date')
    end_date = request.args.get('end_date')
    description.update(graph, desc, id, date, end_date)
    flash("Edit successful")
    return redirect("/settings")


if __name__ == "__main__":
    app.secret_key = 'jbsdakjsdbu73847364'
    app.run(debug=True)
