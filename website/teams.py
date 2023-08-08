from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
import requests
import json

teams = Blueprint('teams', __name__)

@teams.route('/teams',methods=['GET','POST'])
@login_required
def Teams():
    actual_number = 0
    full_name = []
    id=[]
    first_namesteaminfo=[]
    last_namesteaminfo=[]
    idteaminfo=[]
    apiresponse = requests.get("https://www.balldontlie.io/api/v1/teams?per_page=15")
    jsonapi = apiresponse.json()
    dumpapi = json.dumps(jsonapi)
    dumpapi_dict = json.loads(dumpapi)
    totalpages = dumpapi_dict['meta']['total_pages']
    totalpages = int(totalpages)

    if 'teamvalue' not in session:
        actual_number = 0
        full_name = []
        id=[]
        session['teamvalue'] = 1
        result = get_team_api_data(session['teamvalue'])
        while actual_number < 14:
            full_name.append(result['data'][actual_number]['full_name'])
            id.append(result['data'][actual_number]['id'])
            actual_number += 1
        return render_template("teams.html", user=current_user,full_names = full_name,current_page=session['teamvalue'],ids=id)
    

    if request.method == 'POST':
        if 'next' in request.form and session['teamvalue'] < totalpages:
            actual_number = 0
            full_name = []
            id=[]
            session['teamvalue'] += 1
            result = get_team_api_data(session['teamvalue'])
            while actual_number < 14:
                full_name.append(result['data'][actual_number]['full_name'])
                id.append(result['data'][actual_number]['id'])
                actual_number += 1
            return render_template("teams.html", user=current_user,full_names = full_name,current_page=session['teamvalue'],ids=id)
        elif 'precedent' in request.form and session['teamvalue'] > 1:
            actual_number = 0
            full_name = []
            id=[]
            session['teamvalue'] -= 1
            result = get_team_api_data(session['teamvalue'])
            while actual_number < 14:
                full_name.append(result['data'][actual_number]['full_name'])
                id.append(result['data'][actual_number]['id'])
                actual_number += 1
            return render_template("teams.html", user=current_user,full_names = full_name,current_page=session['teamvalue'],ids=id)
        elif 'moreinfo' in request.form:
            if 'teaminfovalue' in session:
                session['teaminfovalue'] = 0
            idteams = request.form.get('moreinfo')
            response_dict = get_api_data_teaminfo(idteams)
            return render_template("teamsinfo.html",user=current_user,abbreviation = response_dict["abbreviation"],city = response_dict["city"],conference = response_dict["conference"],division = response_dict["division"],full_name = response_dict["full_name"],name = response_dict["name"],id = idteams )
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
                if  int(result_dict['data'][actual_number]['team']['id']) == int(idteams):
                    first_namesteaminfo.append(result_dict['data'][actual_number]['first_name'])
                    last_namesteaminfo.append(result_dict['data'][actual_number]['last_name'])
                    idteaminfo.append(result_dict['data'][actual_number]['id'])

                actual_number += 1
            response_dict = get_api_data_teaminfo(idteams)
            return render_template("teamsinfo.html",user=current_user,page = session['teaminfovalue'],abbreviation = response_dict["abbreviation"],city = response_dict["city"],conference = response_dict["conference"],division = response_dict["division"],full_name = response_dict["full_name"],name = response_dict["name"],firstnames = first_namesteaminfo,lastnames = last_namesteaminfo,idplayer = idteaminfo,id=idteams)
        elif 'playerinfo' in request.form:
            idplayer = request.form.get('playerinfo')
            response_dict = get_api_data_playerinfo(idplayer)
            return render_template("playerinfo.html",user=current_user,firstname = response_dict["first_name"],lastname = response_dict["last_name"],position = response_dict["position"],
                                   height_feet= response_dict["height_feet"],height_inches=response_dict["height_inches"],weight_pounds=response_dict["weight_pounds"],teamid = response_dict["team"]["id"] )
        else :
            actual_number = 0
            full_name = []
            id=[]
            result = get_team_api_data(session['teamvalue'])
            while actual_number < 14:
                full_name.append(result['data'][actual_number]['full_name'])
                id.append(result['data'][actual_number]['id'])
                actual_number += 1
            return render_template("teams.html", user=current_user,full_names = full_name,current_page=session['teamvalue'],ids=id)
    elif 'teamvalue' in session:
            actual_number = 0
            full_name = []
            id=[]
            session['teamvalue'] = 1
            result = get_team_api_data(session['teamvalue'])
            while actual_number < 14:
                full_name.append(result['data'][actual_number]['full_name'])
                id.append(result['data'][actual_number]['id'])
                actual_number += 1
            return render_template("teams.html", user=current_user,full_names = full_name,current_page=session['teamvalue'],ids=id)

    return render_template("teams.html", user=current_user,full_names = full_name,current_page=session['teamvalue'],ids=id)


@teams.route('/teamsinfo',methods=['GET','POST'])
@login_required
def Teamsinfo(idteams):
    return render_template("teamsinfo.html",user=current_user,ids = idteams)

def get_api_data(page_num) :
    return requests.get("https://www.balldontlie.io/api/v1/players?per_page=100&page=" + str(page_num))

def get_team_api_data(page_num) :
    result = requests.get("https://www.balldontlie.io/api/v1/teams?per_page=15&page=" + str(page_num))
    jsonresult = result.json()
    dumpresult = json.dumps(jsonresult)
    return json.loads(dumpresult)

def get_api_data_teaminfo(idteams) :
    apiresponse = requests.get("https://www.balldontlie.io/api/v1/teams/" + str(idteams))
    jsonresponse = apiresponse.json()
    dumpresponse = json.dumps(jsonresponse)
    return json.loads(dumpresponse)

def get_api_data_playerinfo(idplayer) :
    apiresponse = requests.get("https://www.balldontlie.io/api/v1/players/" + str(idplayer))
    jsonresponse = apiresponse.json()
    dumpresponse = json.dumps(jsonresponse)
    return json.loads(dumpresponse)