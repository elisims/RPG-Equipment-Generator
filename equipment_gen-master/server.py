"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template, Flask

# local modules
import config

import logging
import sys

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")
# connex_app.add_api("swagger_dmg_types.yml")


# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return render_template("home.html")

@connex_app.route("/loadouts")
def loadouts():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "loadouts.html"
    """
    return render_template("loadouts.html")

@connex_app.route("/base_weapons")
def base_weapons():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "base_weapons.html"
    """
    return render_template("base_weapons.html")

@connex_app.route("/damage_types")
def damage_types():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "damage_types.html"
    """
    return render_template("damage_types.html")

@connex_app.route("/cultures")
def cultures():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "cultures.html"
    """
    return render_template("cultures.html")

@connex_app.route("/element_types")
def element_types():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "element_types.html"
    """
    return render_template("element_types.html")

@connex_app.route("/owners")
def owners():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "owners.html"
    """
    return render_template("owners.html")

@connex_app.route("/status_effects")
def status_effects():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "status_effects.html"
    """
    return render_template("status_effects.html")

@connex_app.route("/dynamic")
def dynamic():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "dynamic.html"
    """
    return render_template("dynamic.html")

@connex_app.route("/generate_unique_weapon")
def generate_unique_weapon():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "generate_unique_weapon.html"
    """
    return render_template("generate_unique_weapon.html")

@connex_app.route("/login")
def login():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "login.html"
    """
    return render_template("login.html")

@connex_app.route("/signup")
def signup():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "login.html"
    """
    return render_template("signup.html")

if __name__ == "__main__":
    connex_app.run(debug=True)
