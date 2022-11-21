from waitress import serve
import pickle 
from flask import jsonify
import pandas as pd 
from flask import Flask,render_template, url_for,request,redirect

app = Flask(__name__)

modelOne = pickle.load(open('models/model1.pkl','rb'))
df_time_series = pd.read_pickle('models/model2.pkl')
def species(x):
	return {
    '0': lambda: "Species: Iris-setosa",
    '1': lambda: "Species: Iris-cersicolour",
    '2': lambda: "Species: Iris-virginica"
  }.get(x, lambda: "Invalid input")()



@app.route('/',methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else: 
		select = str(request.form.get('model'))
		if select == "log":
			return render_template('logreg.html', output='')
		else:
			return render_template('timeseries.html', output='')


@app.route('/logReg',methods=['GET','POST'])
def callModelOne():
	if request.method == 'GET':
		try:
			xValue = request.args.get('x',type=float)
			yValue = request.args.get('y',type=float)
			wValue = request.args.get('w',type=float)
			zValue = request.args.get('z',type=float)
			if xValue and xValue > 0 and yValue and yValue > 0 and wValue and wValue > 0 and zValue and zValue > 0:
				predict = modelOne.predict([[xValue, yValue, wValue, zValue]])[0]
				predict = species(str(predict))
				res = {
					'xValue':xValue,
					'yValue':yValue,
					'wValue':wValue,
					'zValue':zValue,
					'preValue': predict
				}
			else:
				res = {'preValue': 'Invalid input'}
		except:
			res = {'preValue': 'Invalid input'}
		finally:
			return jsonify(res)
	else:
		try:
			xValue = request.form.get('x',type=float)
			yValue = request.form.get('y',type=float)
			wValue = request.form.get('w',type=float)
			zValue = request.form.get('z', type=float)
			predict = modelOne.predict([[xValue, yValue, wValue, zValue]])[0]
			predict = species(str(predict))
		except:
			predict = 'Invalid input'
		finally:
			return render_template('logreg.html', output=predict)
	
		
@app.route('/timeSeries', methods=['GET','POST'])
def callModelTwo():
	if request.method == 'GET':
		try:
			xValue = request.args.get('x', type=int)
			if xValue and xValue >= 7:
				res = {
					'xValue':xValue,
					'preValue': 'Moving average: ' + str(df_time_series[xValue])
				}
			else:
				res = {'preValue': 'Invalid input'}
		except:
			res = {'preValue': 'Invalid input'}
		finally:
			return jsonify(res)
	else:
		try:
			xValue = request.form.get('x', type=int)
			predict = '7 Period Moving average: ' + str(df_time_series[xValue])
		except:
			predict = 'Invalid input'
		finally:
			return render_template('timeseries.html', output=predict)
	
		

@app.errorhandler(404)
def not_found(error):
	return render_template('error.html'), 404



if __name__ == "__main__":
	app.run(host="localhost",port=3000,debug=True)



