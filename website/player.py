from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
import requests
import json


player = Blueprint('player', __name__)

@player.route('/player',methods=['GET','POST'])
@login_required
def Player():

    actual_number = 0
    id = []
    first_names = []
    last_names = []
    apiresponse = requests.get(" https://www.balldontlie.io/api/v1/players?per_page=50")
    jsonapi = apiresponse.json()
    dumpapi = json.dumps(jsonapi)
    dumpapi_dict = json.loads(dumpapi)
    totalpages = dumpapi_dict['meta']['total_pages']
    totalpages = int(totalpages)

    if 'value' not in session:
        actual_number = 0
        first_names = []
        last_names = []
        id=[]
        session['value'] = 1
        result = get_api_data(session['value']).json()
        dumpresult = json.dumps(result)
        result_dict = json.loads(dumpresult)
        while actual_number < 49:
            first_names.append(result_dict['data'][actual_number]['first_name'])
            last_names.append(result_dict['data'][actual_number]['last_name'])
            id.append(result_dict['data'][actual_number]['id'])
            actual_number += 1
        return render_template("player.html",user=current_user, first_names = first_names, last_names = last_names,current_page=session['value'],ids=id)
    
    if request.method == 'POST':
        if 'next' in request.form and session['value'] < totalpages:
            actual_number = 0
            first_names = []
            last_names = []
            id = []
            session['value'] += 1
            result = get_api_data(session['value']).json()
            dumpresult = json.dumps(result)
            result_dict = json.loads(dumpresult)
            while actual_number < 49:
                first_names.append(result_dict['data'][actual_number]['first_name'])
                last_names.append(result_dict['data'][actual_number]['last_name'])
                id.append(result_dict['data'][actual_number]['id'])
                actual_number += 1
            return render_template("player.html",user=current_user, first_names = first_names, last_names = last_names,current_page=session['value'],ids=id)
        
        elif 'precedent' in request.form and session['value'] > 1:
            actual_number = 0
            first_names = []
            last_names = []
            id = []
            session['value'] -= 1
            result = get_api_data(session['value']).json()
            dumpresult = json.dumps(result)
            result_dict = json.loads(dumpresult)
            while actual_number < 49:
                first_names.append(result_dict['data'][actual_number]['first_name'])
                last_names.append(result_dict['data'][actual_number]['last_name'])
                id.append(result_dict['data'][actual_number]['id'])
                actual_number += 1
            return render_template("player.html",user=current_user, first_names = first_names, last_names = last_names,current_page=session['value'],ids=id)
        elif 'moreinfo' in request.form:
            idplayer = request.form.get('moreinfo')
            response_dict = get_api_data_playerinfo(idplayer)
            return render_template("playerinfo.html",user=current_user,firstname = response_dict["first_name"],lastname = response_dict["last_name"],position = response_dict["position"],
                                   height_feet= response_dict["height_feet"],height_inches=response_dict["height_inches"],weight_pounds=response_dict["weight_pounds"],teamid = response_dict["team"]["id"] )
        elif 'team' in request.form:
            idteam = request.form.get('team')
            response_dict = get_api_data_teaminfo(idteam)
            return render_template("teamsinfo.html",user=current_user,abbreviation = response_dict["abbreviation"],city = response_dict["city"],conference = response_dict["conference"],division = response_dict["division"],full_name = response_dict["full_name"],name = response_dict["name"],id=idteam )
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
            first_names = []
            last_names = []
            id = []
            result = get_api_data(session['value']).json()
            dumpresult = json.dumps(result)
            result_dict = json.loads(dumpresult)
            while actual_number < 49:
                first_names.append(result_dict['data'][actual_number]['first_name'])
                last_names.append(result_dict['data'][actual_number]['last_name'])
                id.append(result_dict['data'][actual_number]['id'])
                actual_number += 1
            return render_template("player.html",user=current_user, first_names = first_names, last_names = last_names,current_page=session['value'],ids=id)
            
    elif 'value' in session :
        actual_number = 0
        first_names = []
        last_names = []
        id = []
        session['value'] = 1
        result = get_api_data(session['value']).json()
        dumpresult = json.dumps(result)
        result_dict = json.loads(dumpresult)
        while actual_number < 49:
            first_names.append(result_dict['data'][actual_number]['first_name'])
            last_names.append(result_dict['data'][actual_number]['last_name'])
            id.append(result_dict['data'][actual_number]['id'])
            actual_number += 1
        return render_template("player.html",user=current_user, first_names = first_names, last_names = last_names,current_page=session['value'],ids=id)

    
    return render_template("player.html", user=current_user, firstnames = first_names, lastnames = last_names,current_page=session['value'],ids=id)


@player.route('/playerinfo',methods=['GET','POST'])
@login_required
def Playerinfo(idplayer):
    

    return render_template("playerinfo.html",user=current_user,ids = idplayer)


def get_api_data(page_num) :
    return requests.get("https://www.balldontlie.io/api/v1/players?per_page=100&page=" + str(page_num))

def get_api_data_playerinfo(idplayer) :
    apiresponse = requests.get("https://www.balldontlie.io/api/v1/players/" + str(idplayer))
    jsonresponse = apiresponse.json()
    dumpresponse = json.dumps(jsonresponse)
    return json.loads(dumpresponse)

def get_api_data_teaminfo(idteams) :
    apiresponse = requests.get("https://www.balldontlie.io/api/v1/teams/" + str(idteams))
    jsonresponse = apiresponse.json()
    dumpresponse = json.dumps(jsonresponse)
    return json.loads(dumpresponse)