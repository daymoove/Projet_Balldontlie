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
                                   height_feet= response_dict["height_feet"],height_inches=response_dict["height_inches"],weight_pounds=response_dict["weight_pounds"] )
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


@player.route('/playerinfo/<idplayer>',methods=['GET','POST'])
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