from datetime import date
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash

from infrastructure.config import load_config, get_backend_integration
from infrastructure.integrations.backend_integration import WeekNotFound

meals = Blueprint("meals", __name__)

config = load_config()

@meals.route("/", methods=['GET', 'POST'])
def meal_insertion():
    if request.method == 'POST':
        print(request.form)

        meal_form = {
            "date": request.form.get('dateMeal'),
            "start_week": request.form.get("Start week") == "on",
            "meal_type": request.form.get('meal_type'),
            "participants": request.form.get('participants'),
            "meal": request.form.get('meal'),
            "notes": request.form.get('notes')
        }

        if "dessert" in request.form.keys():
            if (dessert:=request.form.get("dessert")) != "":
                meal_form["dessert"] = dessert


        res = requests.post(config["backend_url"] + "/meal/", json=meal_form)
        if res.status_code == 201:
            flash("Pasto inserito ✓", "success")
        else:
            flash("Errore durante l'inserimento — riprova", "error")

        return redirect(url_for('meals.meal_insertion'))

    meal_list = get_backend_integration().require_meals_list()
    return render_template("insertion.html", meal_list=meal_list, today=date.today().isoformat())    

@meals.route("/week")
def week_meals():
    week_number = None
    meal_date = request.args.get("date")

    try:
        if meal_date:
            meals_list = get_backend_integration().require_weekly_meal_list_by_date(meal_date)
        else:
            week_number = int(request.args["week-number"]) if "week-number" in request.args else None
            meals_list = get_backend_integration().require_weekly_meal_list(week_number)
        for meal in meals_list["meals"]:
            meal["dessert"] = meal["dessert"] if meal["dessert"] is not None else "-"
            
        return render_template("week_view.html", meals = meals_list["meals"], week_number = meals_list["week_number"], meal_date = meal_date)
    except WeekNotFound as err:
        return render_template("week_view.html", error = str(err), week_number = None, meal_date = meal_date)
    except:
        return render_template("week_view.html", error = "Il backend non è d'accordo", week_number = week_number, meal_date = meal_date)

@meals.route("/frequencies")
def frequencies():
     # Get the query parameter from the request
    who = request.args.get('who')

    meals_list = get_backend_integration().require_frequencies(who)[:100]

    for i in range(0, len(meals_list)):
        meals_list[i].append(i+1)
    return render_template("frequencies.html", meals = meals_list)

@meals.route("/deletion")
def confirm_deletion():
    meal = {
        "date": request.args["date"],
        "type": request.args["meal_type"],
        "participants": request.args["participants"]
    }

    return render_template("deletion.html", meal = meal)

@meals.route("/deletion-confirmed")
def delete_meal():
    meal = {
        "date": request.args["date"],
        "meal_type": request.args["meal_type"],
        "participants": request.args["participants"]
    }

    get_backend_integration().delete_meal(meal)

    return redirect(url_for('meals.week_meals'))