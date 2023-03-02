import time
import requests
from flask import Blueprint, render_template, request

from infrastructure.config import load_config, get_backend_integration

meals = Blueprint("meals", __name__)

config = load_config()

@meals.route("/", methods=['GET', 'POST'])
def meal_insertion():
    if request.method == 'POST':
        print(request.form)

        meal_form = {
            "date": request.form.get('dateMeal'),
            "start_week": True if "Start week" in request.form.keys() else False,
            "meal_type": request.form.get('meal_type'),
            "participants": request.form.get('participants'),
            "meal": request.form.get('meal'),
            "notes": request.form.get('notes')
        }

        if "dessert" in request.form.keys():
            if (dessert:=request.form.get("dessert")) != "":
                meal_form["dessert"] = dessert


        # QUI FACCIO LE COSE!
        # APRO UNA MODALE (SE CI RIESCO)
        # FACCIO LA MIA CHIAMATA AL BACKEND (SE CI RIESCO)
        # TODO: QUESTO VA NEL BACKEND INTEGRATION, NON QUI! E DOVREBBE RESTITUIRE ERRORI QUANDO USATO IN DEBUG
        print(meal_form)
        res = requests.post(config["backend_url"] + "/meal/", json=meal_form)
        if res.status_code != 201:
            raise Exception("Unexpected status code!")
        # E VERIFICO CHE MI RISPONDA 201. IN CASO CONTRARIO, APRO ERRORI A MANETTA
        time.sleep(0.5)

    meal_list = get_backend_integration().require_meals_list()
    return render_template("insertion.html", meal_list=meal_list)    

@meals.route("/week")
def week_meals():
    week_number = int(request.args["week-number"]) if "week-number" in request.args else None
    
    try:
        meals_list = get_backend_integration().require_weekly_meal_list(week_number)
        for meal in meals_list["meals"]:
            meal["dessert"] = meal["dessert"] if meal["dessert"] is not None else "-"
            
        return render_template("week_view.html", meals = meals_list["meals"], week_number = meals_list["week_number"])
    except:
        return render_template("week_view.html", error = True, week_number = week_number)

@meals.route("/frequencies")
def frequencies():
    meals_list = get_backend_integration().require_frequencies()[:50]

    for i in range(0, len(meals_list)):
        meals_list[i].append(i+1)
    return render_template("frequencies.html", meals = meals_list)