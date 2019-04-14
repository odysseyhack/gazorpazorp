from flask import Flask, json, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/projects")
def projects():
    # Read project database
    with app.open_resource('database.json', mode='r') as jsonfeed:
        projects = json.load(jsonfeed)
    return render_template("projects.html", projects=projects)

@app.route("/createproject")
def create():
    return render_template("create_project.html")

@app.route("/add_project", methods=['POST'])
def add_project():
    """
    Add project to the project database. Expects input from create_project.html
    """
    # Extract data from form
    name = request.form["name"]
    description = request.form['description']
    target = int(request.form['target'])
    address = request.form['address']
    etr = request.form['etr']

    # Update project database
    with app.open_resource('database.json', mode='r') as jsonfeed:
        projects = json.load(jsonfeed)
    with open('/var/www/FlaskApp/FlaskApp/database.json', mode="w") as jsonfeed:
        projects[address] = {"name": name, \
                             "description": description, \
                             "target": target, \
                             "etr": etr, \
                             'investors': {}}
        json.dump(projects, jsonfeed)

    return redirect("/projects/{}".format(address))

@app.route("/invest/")
@app.route("/invest/<address>")
def invest(address=None):
    return render_template("invest.html", address=address)

@app.route("/projects/<address>")
def show_project(address):
    """
    Show project page

    :param address: address of the project
    :type address: str
    """
    # Read project database
    with app.open_resource('database.json', mode='r') as jsonfeed:
        projects = json.load(jsonfeed)

    # Check if project exists
    if address in projects.keys():
        # Compute total collected Satoshis
        btc_collected = sum([int(value) for value 
                             in projects[address]['investors'].values()])

        # Return different pages depending on whether the target is reached
        if btc_collected < int(projects[address]['target']):
            return render_template("project_lfi.html", 
                                    project=projects[address], \
                                    collected=btc_collected, \
                                    address=address)
        else:
            return render_template("project.html",
                                    project=projects[address], \
                                    collected=btc_collected, \
                                    address=address)
    else:
        return render_template("no_project.html")

@app.route("/add_investor", methods=['POST'])
def add_investor():
    """
    Add investor to the project database. Expects input from invest.html
    """
    # Extract data from form
    target_address = request.form["target_address"]
    txid = request.form['txid']
    vout = request.form['vout']
    amount = request.form['amount']

    # Update project database
    with app.open_resource('database.json', mode='r') as jsonfeed:
        projects = json.load(jsonfeed)
    with open('/var/www/FlaskApp/FlaskApp/database.json', mode="w") as jsonfeed:
        projects[target_address]['investors'][txid] = amount
        json.dump(projects, jsonfeed)

    return redirect("/projects/{}".format(target_address)) 

if __name__ == "__main__":
    app.run(debug=True)
