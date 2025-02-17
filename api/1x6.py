from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# URL для отправки запроса к API
url = "https://dota1x6.com/api/game/get_item_builds"

# Заголовки для запроса
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Valve/Steam HTTP Client 1.0 (570)",
    "dedicated-key": "E7B1B91D62D7A2D785AA131F64EE9C9F236CDE43",
    "Accept": "text/html,*/*;q=0.9"
}

def get_item_builds(hero_name):
    # Данные для запроса
    data = {
        "matchId": "0",
        "matchKey": "OL8Uh56Gk7CTnJSKRz3aVL9FNDdiuuwJ",
        "heroName": f"npc_dota_hero_{hero_name}"
    }

    try:
        # Отправляем POST-запрос
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Если запрос успешен
        if response.status_code == 200:
            return response.json()  # Возвращаем JSON с данными
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Маршрут для главной страницы
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        hero_name = request.form["hero_name"].lower()  # Получаем имя героя из формы
        builds = get_item_builds(hero_name)  # Запрашиваем данные сборок
        return render_template("index.html", hero_name=hero_name.capitalize(), builds=builds)  # Отправляем данные на HTML-шаблон
    return render_template("index.html", hero_name=None, builds=None)

if __name__ == "__main__":
    app.run(debug=True)
