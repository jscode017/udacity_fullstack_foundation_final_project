from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app=Flask(__name__)

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)
    
@app.route("/")
@app.route("/restaurants/")
def show_all_restaurants():
    restaurants=session.query(Restaurant).all()
    return render_template('restaurants.html',items=restaurants)

@app.route("/restaurants/new/",methods=['GET','POST'])
def newrestaurants():
    if request.method=='POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('show_all_restaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route("/restaurants/<int:restaurant_id>/edit",methods=['GET','POST'])
def edit_restaurant(restaurant_id):

    edited_restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    
    if request.method=='POST':
        edited_restaurant.name=request.form['name']
        session.add(edited_restaurant)
        session.commit()
        return redirect(url_for('show_all_restaurants'))
    else:
        return render_template('editrestaurant.html',restaurant=edited_restaurant)

@app.route("/restaurants/<int:restaurant_id>/delete",methods=['GET','POST'])
def delete_restaurant(restaurant_id):
    deleted_restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method=='POST':
        session.delete(deleted_restaurant)
        session.commit()
        return redirect(url_for('show_all_restaurants'))
    else:
        return render_template('deleterestaurant.html',restaurant=deleted_restaurant)

@app.route("/restaurants/<int:restaurant_id>/")
@app.route("/restaurants/<int:restaurant_id>/show")
def show_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html',items=items,restaurant=restaurant)


@app.route("/restaurants/<int:restaurant_id>/new",methods=['GET','POST'])
def newmenu(restaurant_id):
    if request.method=='POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)

        session.commit()
        print newItem.name
        return redirect(url_for('show_menu',restaurant_id=restaurant_id))
    else:
        return render_template('newmenu.html',restaurant_id=restaurant_id)
    
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit",methods=['GET','POST'])
def edit_menu(restaurant_id,menu_id):

    edited_menu=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_menu.name = request.form['name']
        if request.form['description']:
            edited_menu.description = request.form['name']
        if request.form['price']:
            edited_menu.price = request.form['price']
        if request.form['course']:
            edited_menu.course = request.form['course']
        session.add(edited_menu)
        session.commit()
        return redirect(url_for('show_menu',restaurant_id=restaurant_id))
    else:
        return render_template('editmenu.html',item=edited_menu,restaurant_id=restaurant_id)
    


@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete",methods=['GET','POST'])
def delete_menu(restaurant_id,menu_id):
    delete_menu=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        session.delete(delete_menu)
        session.commit()
        return redirect(url_for('show_menu',restaurant_id=restaurant_id))
    else:
        return render_template('deletemenu.html',item=delete_menu,restaurant_id=restaurant_id)



if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=5000)