from flask import Flask, render_template, request, redirect, url_for, flash

import pygal

from pygal import graph

import psycopg2

from flask_sqlalchemy import SQLAlchemy

from config.config import Development,Production

app = Flask(__name__)
app.config.from_object(Production)
db = SQLAlchemy(app)

from models.inventories import Inventories
from models.sales import Sales


@app.before_first_request
def create_tables():
    db.create_all()
    # db.drop_all()


@app.route('/')
def hello_world():
    # x = 'Leon'
    records = Inventories.fetch_all_records()

    return render_template('index.html', records=records)


@app.route('/add_inventory', methods=['POST', 'GET'])
def add_inventory():
    if request.method == 'POST':
        # saving values in each field in their appropriate variables
        invName = request.form['inventory']
        type = request.form['type']
        buyingPrice = request.form['buyingPrice']
        stock = request.form['stock']
        sellingPrice = request.form['sellingPrice']

        print(invName)
        print(type)
        print(buyingPrice)
        print(sellingPrice)
        print(stock)

        # saving values from form ,per record,into the db
        record = Inventories(inv_name=invName, inv_type=type, buyingPrice=buyingPrice, stock=stock,
                             sellingPrice=sellingPrice)
        record.add_records()

    # return home page/route
    return redirect(url_for('hello_world'))


# create a route for making sales
@app.route('/salepro/<int:id>', methods=['POST', 'GET'])
def makeSales(id):
    # print(id)
    # fetch the exact line/record from db of the particular product to be sold
    record = Inventories.fetch_one_record(id)
    if record:
        if request.method == 'POST':
            # get record from form
            quantity = request.form['quantity']
            # calculating new stock,get current stock number and subtract the quantity requested during sale
            newStock = record.stock - int(quantity)
            # update the same record to the new stock number calculated above
            record.stock = newStock
            # print(quantity)
            db.session.commit()

            # sales = Sales(inv_id=id, quantity=quantity)
            # sales.add_records()
            # db.session.commit()

            flash('You have successfully made a sale', 'success')
            return redirect(url_for('hello_world'))
            # return render_template(url_for('makeSale.html',quantity=quantity,sales=sales))


# create a route for viewing sales
@app.route('/viewsale/<int:id>')
def viewSales(id):
    record = Inventories.fetch_one_record(id)

    return render_template('viewSale.html', record=record)


# @app.route('/test/<num1>/<num2>')
# def test(num1, num2):
#     return num1 + num2

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    record = Inventories.fetch_one_record(id)

    if request.method == 'POST':
        record.invName = request.form['inventory']
        record.type = request.form['type']
        record.buyingPrice = request.form['buyingPrice']
        record.stock = request.form['stock']
        record.sellingPrice = request.form['sellingPrice']

        db.session.commit()

        return redirect(url_for('hello_world'))

    return render_template('edit.html', record=record)


@app.route('/delete/<int:id>')
def delete(id):
    record = Inventories.fetch_one_record(id)
    print(record.id)
    print(record.inv_name)

    db.session.delete(record)
    db.session.commit()
    flash('You have successfully deleted the inventory', 'danger')

    return redirect('/')


@app.route('/dashboard')
def charts():
    conn = psycopg2.connect("dbname='abcDB' user='postgres' host='127.0.0.1' password='0000' ")

    # ratios = [('Gentlemen', 5), ('Ladies', 9)]
    # ratios[0][0]
    # # ratios1 = [{},{}]
    # pie_chart = pygal.Pie()
    # pie_chart.title = 'Browser usage in February 2012 (in %)'
    # pie_chart.add(ratios[0][0], ratios[0][1])
    # pie_chart.add(ratios[1][0], ratios[1][1])
    # # pie_chart.add('Chrome', 36.3)
    # # pie_chart.add('Safari', 4.5)
    # # pie_chart.add('Opera', 2.3)
    # pie_data = pie_chart.render_data_uri()

    # data = [
    #     {'month': 'January', 'total': 22},
    #     {'month': 'February', 'total': 27},
    #     {'month': 'March', 'total': 23},
    #     {'month': 'April', 'total': 20},
    #     {'month': 'May', 'total': 12},
    #     {'month': 'June', 'total': 32},
    #     {'month': 'July', 'total': 42},
    #     {'month': 'August', 'total': 72},
    #     {'month': 'September', 'total': 52},
    #     {'month': 'October', 'total': 42},
    #     {'month': 'November', 'total': 92},
    #     {'month': 'December', 'total': 102}
    # ]

    cur = conn.cursor()

    # cur.execute("""SELECT (sum(i.sellingPrice * s.quantity)) as salesTotal, EXTRACT(MONTH FROM s.created_at) as salesMonth
    # from sales as s
    # join inventories as i on s.inv_id = i.id
    # GROUP BY salesMonth
    # ORDER BY salesMonth""")

    cur.execute("""SELECT distinct inventories.inv_type as invType,(sum(sales.quantity)over (partition by inventories.inv_type)) as quantitySold
from sales join inventories on sales.inv_id = inventories.id""")

    rows = cur.fetchall()

    invType = []
    quantitySold = []

    for each in rows:
        invType.append(each[1])
        quantitySold.append(each[1])

    graph = pygal.Bar(title='View quantity sold with every inventory',x_title='Inventory Category',y_title='Quantity Sold')
    # graph.title = 'Inventory Category VS Quantity Sold'

    graph.x_labels = invType
    graph.add('Inventory Category', invType)

    graph.y_labels = quantitySold
    graph.y_labels = map(str, range(450, 800))
    graph.add('Quantity Sold', quantitySold)

    # graph.add('Java', [15, 45, 76, 80, 91, 95])
    # graph.add('C++', [5, 51, 54, 102, 150, 201])
    # graph.add('All others combined!', [5, 15, 21, 55, 92, 105])

    graph_data = graph.render_data_uri()

    # , pie_data = pie_data

    return render_template('dashboard.html', graph_data=graph_data)


if __name__ == '__main__':
    app.run()
