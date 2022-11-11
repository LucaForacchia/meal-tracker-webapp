import requests


class BackendIntegration:
    def __init__(self, config):
        self.backend_url = config["backend_url"]

    def require_weekly_meal_list(self, week_number = None):
        params = {
            "week-number": week_number
        } if week_number is not None else {}

        res = requests.get(self.backend_url + "/meal/week", params=params)

        if res.status_code != 200:
            raise Exception("Il backend non è d'accordo!")

        return res.json()

    def require_frequencies(self):
        res = requests.get(self.backend_url + "/meal/counts")

        if res.status_code != 200:
            raise Exception("Il backend non è d'accordo!")
        
        return res.json()

    def require_meals_list(self):
        res = requests.get(self.backend_url + "/meal/names")

        if res.status_code != 200:
            raise Exception("Error requiring meal list! Check backend status")
        
        return res.json()["list"]

    def get_replacement_list(self):
        res = requests.get(self.backend_url + "/meal/replacement")

        if res.status_code != 200:
            raise Exception("Error requiring replacement table! Check backend status")
        
        print(res.json())
        return res.json()
