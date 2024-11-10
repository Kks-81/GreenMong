import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 데이터베이스 연결 함수
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'esg_survey.db')
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection

# 데이터베이스 초기화 함수 (처음에만 수동으로 실행)
def init_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS esg_survey')
    cursor.execute('''
        CREATE TABLE esg_survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            industry TEXT,
            question1_yes INTEGER,
            question1_no INTEGER,
            question2_yes INTEGER,
            question2_no INTEGER,
            question3_yes INTEGER,
            question3_no INTEGER,
            question4_yes INTEGER,
            question4_no INTEGER,
            question5_yes INTEGER,
            question5_no INTEGER
        )
    ''')
    connection.commit()
    connection.close()

# 초기 데이터베이스 설정
# init_db()  # 주석 처리하여 매번 초기화되지 않도록 함.

# 산업군 선택 페이지
@app.route('/')
def industry_selection():
    return render_template('industry_selection.html')

# 산업군 선택 후 해당 설문조사 페이지로 이동
@app.route('/select_industry', methods=['POST'])
def select_industry():
    industry = request.form.get('industry')

    # 선택한 산업군에 따라 해당 설문조사 페이지로 리다이렉트
    if industry == 'manufacturing':
        return redirect(url_for('manufacturing_survey'))
    elif industry == 'construction':
        return redirect(url_for('construction_survey'))
    elif industry == 'service':
        return redirect(url_for('service_survey'))
    elif industry == 'agriculture':
        return redirect(url_for('agriculture_survey'))
    elif industry == 'transport':
        return redirect(url_for('transport_survey'))
    elif industry == 'energy':
        return redirect(url_for('energy_survey'))
    else:
        return redirect(url_for('industry_selection'))

# 각 산업군 설문조사 페이지 라우팅
@app.route('/survey/manufacturing')
def manufacturing_survey():
    return render_template('manufacturing_survey.html', industry="manufacturing")

@app.route('/survey/construction')
def construction_survey():
    return render_template('construction_survey.html', industry="construction")

@app.route('/survey/service')
def service_survey():
    return render_template('service_survey.html', industry="service")

@app.route('/survey/agriculture')
def agriculture_survey():
    return render_template('agriculture_survey.html', industry="agriculture")

@app.route('/survey/transport')
def transport_survey():
    return render_template('transport_survey.html', industry="transport")

@app.route('/survey/energy')
def energy_survey():
    return render_template('energy_survey.html', industry="energy")

# 설문조사 제출 처리
@app.route('/submit', methods=['POST'])
def submit():
    industry = request.form.get('industry')
    
    # 각 질문에 대한 Yes/No 응답 수
    question1_yes = 1 if request.form.get('question1') == 'yes' else 0
    question1_no = 1 if request.form.get('question1') == 'no' else 0
    question2_yes = 1 if request.form.get('question2') == 'yes' else 0
    question2_no = 1 if request.form.get('question2') == 'no' else 0
    question3_yes = 1 if request.form.get('question3') == 'yes' else 0
    question3_no = 1 if request.form.get('question3') == 'no' else 0
    question4_yes = 1 if request.form.get('question4') == 'yes' else 0
    question4_no = 1 if request.form.get('question4') == 'no' else 0
    question5_yes = 1 if request.form.get('question5') == 'yes' else 0
    question5_no = 1 if request.form.get('question5') == 'no' else 0

    # 데이터베이스에 응답 저장
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO esg_survey (industry, question1_yes, question1_no, question2_yes, question2_no, question3_yes, question3_no, question4_yes, question4_no, question5_yes, question5_no)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (industry, question1_yes, question1_no, question2_yes, question2_no, question3_yes, question3_no, question4_yes, question4_no, question5_yes, question5_no))
    connection.commit()
    connection.close()

    # 결과 페이지로 리다이렉트
    return redirect(url_for('results', industry=industry))

# 결과 페이지
@app.route('/results')
def results():
    industry = request.args.get('industry')
    connection = get_db_connection()
    cursor = connection.cursor()

    # 가장 최근에 입력된 결과 가져오기
    cursor.execute("SELECT * FROM esg_survey ORDER BY id DESC LIMIT 1")
    latest_result = cursor.fetchone()
    connection.close()

    if latest_result is None:
        return "No results found. Please complete the survey first."

    # Row 객체를 dictionary로 변환
    latest_result = dict(latest_result)

    return render_template('results.html', result=latest_result, industry=industry)

if __name__ == '__main__':
    app.run(debug=True)  # 배포 환경에서는 gunicorn을 사용하여 실행

