from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

from cupcakes import get_cupcakes, find_cupcake, add_cupcake_dictionary, write_new_csv

@app.route("/")
def home():
    cupcakes = get_cupcakes("cupcakes.csv")
    order = get_cupcakes("orders.csv")
    order_total = round(sum([float(x["price"]) for x in order]), 2)
    return render_template("index.html", cupcakes=cupcakes, items_num=len(order), order_total=order_total)

@app.route("/cupcakes")
def all_cupcakes():
    cupcakes = get_cupcakes("cupcakes.csv")
    return render_template("cupcakes.html", cupcakes=cupcakes)

@app.route("/add-cupcake/<name>")
def add_cupcake(name):
    cupcake = find_cupcake("cupcakes.csv", name)

    if cupcake:
        add_cupcake_dictionary("orders.csv", cupcake=cupcake)
        return redirect(url_for("home"))
    else:
        return "Sorry cupcake not found."


@app.route("/individual-cupcake/<name>")
def individual_cupcake(name):
    cupcake = find_cupcake("cupcakes.csv", name)
    
    if cupcake:
        return render_template("individual-cupcake.html", cupcake=cupcake)
    else:
        return "Sorry cupcake not found."

@app.route("/order")
def order():
    cupcakes=get_cupcakes("orders.csv")

    cupcakes_counted = []
    cupcake_set = set()

    for cupcake in cupcakes:
        cupcake_set.add((cupcake["name"], cupcake["price"], cupcakes.count(cupcake)))


    return render_template("order.html", cupcakes=cupcake_set)

#tried to get this to work nothing I could find online really helped me out, will try to get it to work in the future
@app.route("/order/<name>", methods=["DELETE"])
def delete_cupcake(name):
    cupcakes = get_cupcakes("orders.csv")
    for cupcake in cupcakes:
        if cupcake["name"] == name:
            cupcakes.remove(cupcake)
            break
    write_new_csv("orders.csv", cupcakes)
    return "Cupcake deleted", 200


if __name__ == "__main__":
    app.env = "development"
    app.run(debug = True)





