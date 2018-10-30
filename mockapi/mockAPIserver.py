#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify,request,abort
import json
from pprint import pprint
#from urllib.parse import urlsplit, parse_qs
usercheck=open('/home/mockapi/user.json','r')
menucheck=open('/home/mockapi/menu.json','r')
sacheck=open('/home/mockapi/sa.json','r')
devlopcheck=open('/home/mockapi/devlop.json','r')
sysopscheck=open('/home/mockapi/sysops.json','r')
jsonUser = json.load(usercheck)
jsonMenu = json.load(menucheck)
jsonSa = json.load(sacheck)
jsonDevlop = json.load(devlopcheck)
jsonSysops = json.load(sysopscheck)


# In[ ]:


app = Flask(__name__)

@app.route('/')
def welcome():
    return ' Hello! welcome to cc102 Mock APIserver'



@app.route('/user/<string:user_open_id>')
def get_single_user(user_open_id):
    for singleuser in jsonUser:
        if singleuser['user_open_id'] == user_open_id:
            return jsonify(singleuser)
    return jsonify ({'message': 'store not found'})



@app.route('/user' , methods=['POST'])
def create_user():
    request_data = request.get_json()
    new_user = {
       
        'user_img': request_data['user_img'], 
        'user_nick_name': request_data['user_nick_name'], 
        'user_open_id': request_data['user_open_id'], 
        'user_register_menu': request_data['user_register_menu'], 
        'user_status': request_data['user_status']
            }
    jsonUser.append(new_user)
    return jsonify(new_user)




@app.route('/user/<string:user_open_id>', methods=['PUT'])
def update_task(user_open_id):
    task = [task for task in jsonUser if task['user_open_id'] == user_open_id]
 #   if len(task) == 0:
 #      abort(404)
 #   if not request.json:
 #       abort(400)
 #  if 'user_nick_name' in request.json and type(request.json['user_nick_name']) != str:
 #       abort(400)
 #   if 'user_status' in request.json and type(request.json['user_status']) is not str:
 #       abort(400)
 #   if 'user_img' in request.json and type(request.json['user_img']) is not str:
 #       abort(400)
 #   if 'user_register_menu' in request.json and type(request.json['user_img']) is not str:
 #       abort(400)
    task[0]['user_nick_name'] = request.json.get('user_nick_name', task[0]['user_nick_name'])
    task[0]['user_status'] = request.json.get('user_status', task[0]['user_status'])
    task[0]['user_img'] = request.json.get('user_img', task[0]['user_img'])
    task[0]['user_register_menu'] = request.json.get('user_register_menu', task[0]['user_register_menu'])
    return jsonify({'task': task[0]})



  


@app.route('/users')
def get_users():
 
    user_open_id =request.args['user_open_id']
    a = user_open_id.split(",")
    b=len(a)
    c=[]
    for i in range(0,b):
        for searchuser in jsonUser:
            if searchuser['user_open_id'] == a[i]:
                c.append(searchuser)
                print(a[i])
    return jsonify(c)

        
        
        
        
        
        

    
    
@app.route('/menu',methods=['POST'])
def get_menu():
    request_data = request.get_json()
    new_menu = {
       
        'menu_id': request_data['menu_id'], 
        'menu_content': request_data['menu_content']
       
            }
    jsonMenu.append(new_menu)
    return jsonify({"status_describe":"success add menu"})
    
    
    
    
@app.route('/question/sa')
def get_sa():
    avalue=[]
    question_id =request.args.get("question_id")
    sa_id=int(question_id)
    for qsa in jsonSa:
        if qsa['question_id'] == sa_id:
            return jsonify(qsa)   
    
@app.route('/question/devlop')
def get_dv():
    avalue=[]
    question_id =request.args.get("question_id")
    dv_id=int(question_id)
    for qsa in jsonDevlop:
        if qsa['question_id'] == dv_id:
            return jsonify(qsa)   
        
        
@app.route('/question/sysops')
def get_sys():
    avalue=[]
    question_id =request.args.get("question_id")
    sys_id=int(question_id)
    for qsa in jsonSysops:
        if qsa['question_id'] == sys_id:
            return jsonify(qsa)     
    
    
    
    
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5005 )

