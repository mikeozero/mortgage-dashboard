from flask import Flask,render_template,jsonify
import time
from readdatabase import de,rde,ltv

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/time')
def get_time():
    return time.strftime("%Y-%m-%d %X")

@app.route('/l1')
def get_l1_fromcsv():
    df = de
    quarters = list(df.index)
    gt90 = list(df['gt90_rate'])
    gt30 = list(df['gt30_rate'])
    rpt = list(df['rpt_rate'])
    return jsonify({'quarters':quarters,'gt90':gt90,'gt30':gt30,'rpt':rpt})

@app.route('/c1')
def get_c1_fromcsv():
    df = rde
    regions = list(df.columns)
    quarters = list(df.index)
    values = []
    n = len(regions)
    for i in range(n):
        values.append(list(df.iloc[:,i]))
    return jsonify({"regions":regions,"quarters":quarters,"values":values})

@app.route('/r1')
def get_r1_data():
    df = ltv
    quarters = list(df.index)
    l5rt = list(df['l5rt'])
    b56rt = list(df['b56rt'])
    b67rt = list(df['b67rt'])
    b78rt = list(df['b78rt'])
    avg = list(df['avg'])
    return jsonify({'quarters':quarters,'l5rt':l5rt,'b56rt':b56rt,'b67rt':b67rt,'b78rt':b78rt,'avg':avg})



if __name__ == '__main__':
    app.run(host='0.0.0.0')
