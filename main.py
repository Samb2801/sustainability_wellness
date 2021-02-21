#main.py

# Import the Flask module that has been installed.
from flask import Flask, jsonify, request
import simplejson as json
from functools import partial

# Creating a new "app" by using the Flask constructor. Passes __name__ as a parameter.
app = Flask(__name__)

# Annotation that allows the function to be hit at the specific URL.
@app.route("/")
# Generic Python function that returns "Hello world!"
def index():
	return "Hello world!"

# Annotation that allows the function to be hit at the specific URL. Indicates a POST HTTP method.
@app.route("/fitness/v1.0/data", methods=["POST"])
def get_Fitenessdata():
    data=request.get_data()
    parsed_json = (json.loads(data))
    unconsious_Persons=ProcessData1(parsed_json)
    if len(unconsious_Persons['Criticaltemparature'])==0 and len(unconsious_Persons['CriticalHeartRate'])==0 and len(unconsious_Persons['CritcalOxygen'])==0:
        return "All Are Consious",200
    print(unconsious_Persons)
    return unconsious_Persons,200

# def ProcessData(data):
#     oxygenRange=range(95,98)
#     unconsious= {'unconsious': []}
#     temp = unconsious['unconsious'] 
#     fitnessdatas = data.get('fitnessdata')
#     for fitnessdata in fitnessdatas:
#         res = bytes(json.dumps(fitnessdata), 'utf-8') 
#         parsed_json = (json.loads(res))
#         print( "averageHeartRate",type(parsed_json['averageHeartRate']))
#         # if int(fitnessdata['averageHeartRate']) >= 95 or int(fitnessdata['tempareture']) >= 95 or int(fitnessdata['oxygen']) <= 98 or int(fitnessdata['suger']) >= 140:
#         if int(fitnessdata['averageHeartRate']) >= 95 or int(fitnessdata['tempareture']) >= 100 or int(fitnessdata['oxygen']) in oxygenRange:
#             temp.append(fitnessdata)
#     return unconsious
 
def ProcessData1(data):
    # oxygenRange=range(95,98)
    # criticalTemp = {'Criticaltemparature': []} 
    # temp = unconsious['unconsious'] 
    fitnessdatas = data.get('fitnessdata')
    # Creating Directory of Unconsious persons according to category
    Unconsious= {'Criticaltemparature': [],'CriticalHeartRate':[],'CritcalOxygen':[]}
    for fitnessdata in fitnessdatas:
        res = bytes(json.dumps(fitnessdata), 'utf-8') 
        parsed_json = (json.loads(res))
        print( "averageHeartRate",type(parsed_json['averageHeartRate']))
        if int(fitnessdata['averageHeartRate']) >= 95 :
            print(ProcessDataParameterWie(1,fitnessdata,Unconsious))
        elif  int(fitnessdata['tempareture']) >= 95 :
            print(ProcessDataParameterWie(2,fitnessdata,Unconsious))
        elif  int(fitnessdata['oxygen']) >= 95 :
            print(ProcessDataParameterWie(3,fitnessdata,Unconsious))
    return Unconsious   	

def temparature(data,Unconsious):
    temp = Unconsious['Criticaltemparature']
    temp.append(data) 
    return Unconsious
 
def oxygen(data,Unconsious):
    temp = Unconsious['CritcalOxygen']
    temp.append(data)
    return Unconsious
 
def heartRate(data,Unconsious):
    temp = Unconsious['CriticalHeartRate']
    temp.append(data)
    return Unconsious

def ProcessDataParameterWie(argument,data,Unconsious):
    switcher = {
        1: partial(heartRate, data,Unconsious),
        2: partial(temparature,data,Unconsious),
        3: partial(oxygen,data,Unconsious)
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "Invalid month")
    # Execute the function
    print(func())

# Checks to see if the name of the package is the run as the main package.
if __name__ == "__main__":
	# Runs the Flask application only if the main.py file is being run.
	app.run()
