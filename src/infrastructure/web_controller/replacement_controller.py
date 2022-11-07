from flask import Blueprint, render_template

replacement = Blueprint("replacement", __name__)

@replacement.route("/")
def home():
    # Visualizza ed elimina replacement
    replacement_list = [] # Require to backend! Until unavailable, insert it manually
    replacement_list.append([1, "Feta Avocado Pomodorini", "Avocado Feta Pomodorini"])
    replacement_list.append([2, "Tomini in sfoglia", "Tomini in pasta sfoglia"])
    # Inserisci nuovo replacement
    return render_template("replacement.html", replacement_list=replacement_list)