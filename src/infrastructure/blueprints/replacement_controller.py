from flask import Blueprint, render_template

from infrastructure.config import get_backend_integration

replacement = Blueprint("replacement", __name__)

@replacement.route("/")
def home():
    # Visualizza ed elimina replacement
    try:
        replacement_list = get_backend_integration().get_replacement_list()
    except:
        replacement_list = [] # Require to backend! Until unavailable, insert it manually
        replacement_list.append([0, "Example", "Values"])
        replacement_list.append([0, "Unable to retrieve", "Data from backend"])
        replacement_list.append([1, "Feta Avocado Pomodorini", "Avocado Feta Pomodorini"])
        replacement_list.append([2, "Tomini in sfoglia", "Tomini in pasta sfoglia"])
    # # Inserisci nuovo replacement
    return render_template("replacement.html", replacement_list=replacement_list)