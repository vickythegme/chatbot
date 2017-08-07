import json
import urllib
import os
import os.path
import sys
import requests
from flask import render_template
from flask import request, url_for, make_response
from watson_developer_cloud import ConversationV1
from os.path import join, dirname
from flask import Flask
import time
from requests.auth import HTTPProxyAuth



conversation = ConversationV1(
    username='8f852f62-ded3-4c89-b696-f6999670f391',
    # username='8b39e53f-697e-4c3a-aee7-efc78061bce0',
    password='wMCxakn17KSZ',
    # password='SehjL5SoP2wl',
    version='2017-02-03')
print("inside global app")
# conv_workspace_id = '63426865-ec68-48db-a233-3d58e03ffe67'
# conv_workspace_id = 'f79fd521-3494-4bc0-8344-6ef6f984c064'
conv_workspace_id = '5e685fd6-a971-47f1-af9b-ab409f4c5a36'

app = Flask(__name__, static_url_path='/static')


@app.route("/", methods=['GET', 'POST'])
def main_page():
	print("inside main")
	if request.method == 'GET':
		return render_template("index.html")
		

	elif request.method == 'POST':
		data = request.form['message']
		context = {}
		if os.path.getsize('static/doc/file.txt') > 0:
			file = open('static/doc/file.txt','r')
			context = json.loads(file.read())
			file.close()
		else:
			print('file is empty')
		
#		response = response_file.response_fun(conv_workspace_id,data,context)
		response = conversation.message(workspace_id = conv_workspace_id, message_input={'text' : data },context = context)
		print("***********"+json.dumps(response,indent=2)+"***************")
			
		
		file = open('static/doc/file.txt','w+')
#		print("Writing " + str(json.dumps(response['context'])) + "to file........")
		file.write(str(json.dumps(response['context'])))
		file.close()
		
		json_data = {}
		script3 = """<html></html>"""
		url=""
		print(response['output']['nodes_visited'][0])	
		if str(response['output']['nodes_visited'][0]) == 'customer_detail' or str(response['output']['nodes_visited'][0]) == 'customer_detail2':
			try:
				print(response['entities'][0]['value']);
				cust_detail = str(response['entities'][0]['value'])
				print("customer details="+cust_detail)
				url = 'https://ehnsarmecmpre01.extnet.ibm.com/api.php?query=%s'%cust_detail
			except:
				print("customer details not provided!!")
				script3 = """<html></html>"""
			
			try:
				return_val = requests.get(url,verify = False, proxies = {
						'http': '',
						'https': ''
				})
				json_data = return_val.json()
				print(json_data)
				script3 = """
				<html>
				<body><hr>
				<table border=0.2px>
				<tr>
				<th style="padding:2px;color:white;">NAME</th>
				<th style="padding:2px;color:white;">IMT</th>
				<th style="padding:2px;color:white;">COUNTRY</th>
				<th style="padding:2px;color:white;">COUNTRY_INV</th>
				<th style="padding:2px;color:white;">CUSTOMER_ID_IHD</th>
				<th style="padding:2px;color:white;">INV_SOURCE</th>
				<th style="padding:2px;color:white;">SECTOR</th>
				</tr>
				<tr>
				<td style="padding:2px;color:white;">{name}</td>
				<td style="padding:2px;color:white;">{imt}</td>
				<td style="padding:2px;color:white;">{country}</td>
				<td style="padding:2px;color:white;">{country_inv}</td>
				<td style="padding:2px;color:white;">{customer_id_ihd}</td>
				<td style="padding:2px;color:white;">{inv_source}</td>
				<td style="padding:2px;color:white;">{sector}</td>
				</tr>
				</table>
				</body>
				</html>""".format(name=str(json_data['NAME']),imt=str(json_data['IMT']),country=str(json_data['COUNTRY']),country_inv=str(json_data['COUNTRY_INV']),customer_id_ihd=str(json_data['CUSTOMER_ID_IHD']),inv_source=str(json_data['INV_SOURCE']),sector=str(json_data['SECTOR']))
				print("Connection established!!!!")
			except Exception as e:
				print("error occured!!")
				print(str(e))
		script1 = """"""
#		script2 = """<html>
#			<p style='visibility:hidden;' id='context' name='context'>{code}</p>
#			</html>""".format(code=str(json.dumps(response['context'])))
	

		response = str(response['output']['text'][0]) + script3 + script1
		print("leaving post method")
		return str(response)

if __name__ == "__main__":
	port = int(os.getenv('PORT', 5000))
	print("Starting app on port %d" % port)
	app.run(debug=True, port=port, host='0.0.0.0')
	
	

