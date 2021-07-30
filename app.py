from flask import Flask,render_template,jsonify
import time
from readdatabase import de,rde,ltv,decc,rdecc,lmt,cri,amr

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/time')
def get_time():
    return time.strftime("%Y-%m-%d %X")

@app.route('/l1')
def get_l1_data():
    df = de
    quarters = list(df.index)
    gt90 = list(df['gt90_rate'])
    gt30 = list(df['gt30_rate'])
    rpt = list(df['rpt_rate'])
    return jsonify({'quarters':quarters,'gt90':gt90,'gt30':gt30,'rpt':rpt})

@app.route('/c1')
def get_c1_data():
    df = rde
    regions = list(df.columns)
    quarters = list(df.index)
    values = []
    n = len(regions)
    for i in range(n):
        values.append(list(df.iloc[:,i]))
    return jsonify({"regions":regions,"quarters":quarters,"values":values})

@app.route('/c2')
def get_c2_data():
    df = amr
    quarters = list(df.index)
    lt20 = list(df['lt20rt'])
    lt25 = list(df['lt25rt'])
    gt25 = list(df['gt25rt'])
    return jsonify({"quarters":quarters,"lt20":lt20,"lt25":lt25,"gt25": gt25})

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

@app.route('/lt')
def get_lt_data():
    df = decc
    quarters = list(df.index)
    gt90 = list(df['gt90_rate'])
    gt30 = list(df['gt30_rate'])
    rpt = list(df['rpt_rate'])
    return jsonify({'quarters':quarters,'gt90':gt90,'gt30':gt30,'rpt':rpt})

@app.route('/rt')
def get_rt_data():
    df = lmt
    quarters = list(df.index)
    visa = list(df['VISA'])
    amex = list(df['AMEX'])
    return jsonify({'quarters':quarters,'visa':visa,'amex':amex})

@app.route('/lb')
def get_lb_data():
    df = cri
    quarters = list(df.index)
    abrt = list(df['abrt'])
    crt = list(df['crt'])
    dert = list(df['dert'])
    return jsonify({'quarters':quarters,'abrt':abrt,'crt':crt,'dert':dert})


@app.route('/rb')
def get_rb_data():
    df = rdecc
    regions = list(df.columns)
    quarters = list(df.index)
    values = []
    n = len(regions)
    for i in range(n):
        values.append(list(df.iloc[:,i]))
    return jsonify({"regions":regions,"quarters":quarters,"values":values})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
