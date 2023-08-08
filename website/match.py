from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
import requests
import json
from datetime import datetime


match = Blueprint('match', __name__)

@match.route('/match',methods=['GET','POST'])
@login_required
def Matchs():
    actual_number = 0
    date = []
    home_team = []
    visitor_team = []
    id = []
    apiresponse = requests.get("https://www.balldontlie.io/api/v1/games?per_page=50")
    jsonapi = apiresponse.json()
    dumpapi = json.dumps(jsonapi)
    dumpapi_dict = json.loads(dumpapi)
    totalpages = dumpapi_dict['meta']['total_pages']
    totalpages = int(totalpages)
    if 'matchvalue' not in session:
        actual_number = 0
        date = []
        home_team = []
        visitor_team = []
        id=[]
        session['matchvalue'] = 1
        result = get_match_api_data(session['matchvalue'])
        while actual_number < 49:
            date.append(FormatDate(result['data'][actual_number]['date']))
            home_team.append(result['data'][actual_number]['home_team']['abbreviation'])
            visitor_team.append(result['data'][actual_number]['visitor_team']['abbreviation'])
            id.append(result['data'][actual_number]['id'])
            actual_number += 1
        return render_template("match.html", user=current_user, date =date,home_team=home_team,visitor_team=visitor_team,current_page=session['matchvalue'],ids=id)
        
    if request.method == 'POST':
        if 'next' in request.form and session['matchvalue'] < totalpages:
            actual_number = 0
            date = []
            home_team = []
            visitor_team = []
            id=[]
            session['matchvalue'] += 1
            result = get_match_api_data(session['matchvalue'])
            while actual_number < 49:
                date.append(FormatDate(result['data'][actual_number]['date']))
                home_team.append(result['data'][actual_number]['home_team']['abbreviation'])
                visitor_team.append(result['data'][actual_number]['visitor_team']['abbreviation'])
                id.append(result['data'][actual_number]['id'])
                actual_number += 1
            return render_template("match.html", user=current_user, date =date,home_team=home_team,visitor_team=visitor_team,current_page=session['matchvalue'],ids=id)
        elif 'precedent' in request.form and session['matchvalue'] > 1:
            actual_number = 0
            date = []
            home_team = []
            visitor_team = []
            id=[]
            session['matchvalue'] -= 1
            result = get_match_api_data(session['matchvalue'])
            while actual_number < 49:
                date.append(FormatDate(result['data'][actual_number]['date']))
                home_team.append(result['data'][actual_number]['home_team']['abbreviation'])
                visitor_team.append(result['data'][actual_number]['visitor_team']['abbreviation'])
                id.append(result['data'][actual_number]['id'])
                actual_number += 1
            return render_template("match.html", user=current_user, date =date,home_team=home_team,visitor_team=visitor_team,current_page=session['matchvalue'],ids=id)
        elif 'moreinfo' in request.form:
            idmatch = request.form.get('moreinfo')
            response_dict = get_api_data_matchinfo(idmatch)
            return render_template("matchinfo.html", user=current_user,date = response_dict['date'], home_team_score = response_dict['home_team_score'],period = response_dict['period'],status = response_dict['home_team_score'],time = response_dict['time'],postseason = response_dict['postseason'],season = response_dict['season'],visitor_team_score = response_dict['visitor_team_score']
                                    ,home_teamid = response_dict['home_team']['id'],home_teamname = response_dict['home_team']['full_name'],visitor_teamid = response_dict['visitor_team']['id'],visitor_teamname = response_dict['visitor_team']['full_name'],current_page=session['matchvalue'],ids=id)
        elif 'team' in request.form:
            if 'teaminfovalue' in session:
                session['teaminfovalue'] = 0
            idteam = request.form.get('team')
            response_dict = get_api_data_teaminfo(idteam)
            return render_template("teamsinfo.html",user=current_user,abbreviation = response_dict["abbreviation"],city = response_dict["city"],conference = response_dict["conference"],division = response_dict["division"],full_name = response_dict["full_name"],name = response_dict["name"],id = idteam  )
        elif 'seeplayer' in request.form:
            if 'teaminfovalue' not in session:
                session['teaminfovalue'] = 0
            actual_number = 0
            first_namesteaminfo=[]
            last_namesteaminfo=[]
            idteaminfo=[]
            idteams = request.form.get('seeplayer')
            session['teaminfovalue'] += 1
            result = get_api_data(session['teaminfovalue']).json()
            dumpresult = json.dumps(result)
            result_dict = json.loads(dumpresult)
            while actual_number < 49:
                if int(result_dict['data'][actual_number]['team']['id']) == int(idteams):
                    first_namesteaminfo.append(result_dict['data'][actual_number]['first_name'])
                    last_namesteaminfo.append(result_dict['data'][actual_number]['last_name'])
                    idteaminfo.append(result_dict['data'][actual_number]['id'])
                actual_number += 1
            response_dict = get_api_data_teaminfo(idteams)
            return render_template("teamsinfo.html",user=current_user,page = session['teaminfovalue'],abbreviation = response_dict["abbreviation"],city = response_dict["city"],conference = response_dict["conference"],division = response_dict["division"],full_name = response_dict["full_name"],name = response_dict["name"],firstnames = first_namesteaminfo,lastnames = last_namesteaminfo,idplayer = idteaminfo,id=idteams)
        else :
            actual_number = 0
            date = []
            home_team = []
            visitor_team = []
            id=[]
            session['matchvalue'] = 1
            result = get_match_api_data(session['matchvalue'])
            while actual_number < 49:
                date.append(FormatDate(result['data'][actual_number]['date']))
                home_team.append(result['data'][actual_number]['home_team']['abbreviation'])
                visitor_team.append(result['data'][actual_number]['visitor_team']['abbreviation'])
                id.append(result['data'][actual_number]['id'])
                actual_number += 1
            return render_template("match.html", user=current_user, date =date,home_team=home_team,visitor_team=visitor_team,current_page=session['matchvalue'],ids=id)
    elif 'matchvalue' in session:
        actual_number = 0
        date = []
        home_team = []
        visitor_team = []
        id=[]
        session['matchvalue'] = 1
        result = get_match_api_data(session['matchvalue'])
        while actual_number < 49:
            date.append(FormatDate(result['data'][actual_number]['date']))
            home_team.append(result['data'][actual_number]['home_team']['abbreviation'])
            visitor_team.append(result['data'][actual_number]['visitor_team']['abbreviation'])
            id.append(result['data'][actual_number]['id'])
            actual_number += 1
        return render_template("match.html", user=current_user, date =date,home_team=home_team,visitor_team=visitor_team,current_page=session['matchvalue'],ids=id)
    return render_template("match.html", user=current_user, date =date,home_team=home_team,visitor_team=visitor_team,current_page=session['matchvalue'],ids=id)

@match.route('/matchinfo',methods=['GET','POST'])
@login_required
def Teamsinfo(idmatch):
    return render_template("matchinfo.html",user=current_user,ids = idmatch)


def get_match_api_data(page_num) :
    result = requests.get("https://www.balldontlie.io/api/v1/games?per_page=50&page=" + str(page_num))
    jsonresult = result.json()
    dumpresult = json.dumps(jsonresult)
    return json.loads(dumpresult)

def get_api_data_matchinfo(idmatch) :
    apiresponse = requests.get("https://www.balldontlie.io/api/v1/games/" + str(idmatch))
    jsonresponse = apiresponse.json()
    dumpresponse = json.dumps(jsonresponse)
    return json.loads(dumpresponse)

def get_api_data_teaminfo(idteams) :
    apiresponse = requests.get("https://www.balldontlie.io/api/v1/teams/" + str(idteams))
    jsonresponse = apiresponse.json()
    dumpresponse = json.dumps(jsonresponse)
    return json.loads(dumpresponse)

def get_api_data(page_num) :
    return requests.get("https://www.balldontlie.io/api/v1/players?per_page=100&page=" + str(page_num))

def FormatDate(dateIso) :
    iso_date = datetime.strptime(dateIso, "%Y-%m-%dT%H:%M:%S.%fZ")
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    day = iso_date.day
    month = iso_date.month
    year = iso_date.year
    
    formatted_date = f"{day} {month_names[month - 1]} {year}"
    return formatted_date