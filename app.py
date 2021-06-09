from flask import Flask, render_template, request, redirect
from urllib.request import urlopen
import json
app = Flask(__name__)


@app.route('/')
def index():
    try:
        url = "https://api.covid19india.org/data.json"
        response = urlopen(url)
        covid_data = json.loads(response.read())
    except:
        file = open('covid19data.json')
        covid_data = json.load(file)

    main_list = covid_data["cases_time_series"]

    total_cases = 0
    total_recovered = 0
    total_vaccinated = 0

    for i in range(len(main_list)):
        if 'dailyconfirmed' in main_list[i]:
            total_cases = total_cases + int(main_list[i]["dailyconfirmed"])
        if 'totalrecovered' in main_list[i]:
            total_recovered = total_recovered + int(main_list[i]["totalrecovered"])

    tested_list = covid_data["tested"]
    total_vaccinated = tested_list[-1]["totalindividualsvaccinated"]

    return_list = [str(total_cases), str(total_recovered), total_vaccinated]
    return render_template('index.html', return_list=return_list)


@app.route('/usefulLinks.html')
def useful_links():
    return render_template('usefulLinks.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/check_state_data', methods=['POST', 'GET'])
def check_state_data():
    if request.method == "POST":

        indian_state = request.form.get('state')

        try:
            url = "https://api.covid19india.org/data.json"
            response = urlopen(url)
            covid_data = json.loads(response.read())

        except:
            file = open('covid19data.json')

            covid_data = json.load(file)

        main_list = covid_data["cases_time_series"]

        state = indian_state.capitalize()
        total_cases = 0

        statewise_data = covid_data['statewise']

        for i in range(len(statewise_data)):
            if 'state' in statewise_data[i]:
                if statewise_data[i]["state"] == state:
                    total_case_state = int(statewise_data[i]['confirmed'])
                    total_recovered_state = int(statewise_data[i]['recovered'])
                    break

        total_cases = 0
        total_recovered = 0
        total_vaccinated = 0

        for i in range(len(main_list)):
            if 'dailyconfirmed' in main_list[i]:
                total_cases = total_cases + int(main_list[i]["dailyconfirmed"])
            if 'totalrecovered' in main_list[i]:
                total_recovered = total_recovered + int(main_list[i]["totalrecovered"])

        tested_list = covid_data["tested"]
        total_vaccinated = tested_list[-1]["totalindividualsvaccinated"]

        return_list = [str(total_cases), str(total_recovered), str(total_vaccinated), str(total_case_state), str(total_recovered_state), str(indian_state)]

    return render_template('stateData.html', return_list=return_list)


if __name__ == "__main__":
    app.run(debug=True)
