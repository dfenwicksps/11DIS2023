from flask import Flask, render_template_string
import openpyxl
import pandas as pd

app = Flask(__name__)

def read_excel(file_path, sheet_name):
    workbook = openpyxl.load_workbook(filename=file_path)
    sheet = workbook[sheet_name]
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(" ".join(str(cell) for cell in row))
    return data

@app.route('/')
def home():
    file_path = "/Users/d.fenwick/Downloads/leaders.xlsx"  # Replace with your file path
    #sheet_name = "Sheet1"  # Replace with your sheet name
    #data = read_excel(file_path, sheet_name)
    #data_list = [paragraph.split() for paragraph in data]
    #data_list = [dict(ID=i, Start_time='...', Completion_time='...', Email='...', Name='...', Last_modified_time='...', Your_name='...', Your_Position='...', Teachers='...', Current_work='...', Challenges='...', Help='...') for i in range(14)]
    #pandas
    data = pd.read_excel(file_path, sheet_name='Sheet1')
    data.columns = ['ID', 'Start_time', 'Completion_time', 'Email', 'Name', 'Last_modified_time', 'Your_name',
                    'Your_Position', 'Teachers', 'Current_work', 'Challenges', 'Help']

    data_list = data.to_dict('records')

    return render_template_string('''
                <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                padding: 8px;
                text-align: left;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .question {
                font-weight: bold;
            }
        </style>
                 {% for row in data %}
            <div class="qa-block">
                <div class="question">Your name: </div><div>{{ row.Your_name }}</div>
                <div class="question">Your Position: </div><div>{{ row.Your_Position }}</div>
                <div class="question">Teachers you mostly work with: </div><div>{{ row.Teachers }}</div>
                <div class="question">What are you currently working on? </div><div>{{ row.Current_work }}</div>
                <div class="question">What has been the biggest challenge in your role? </div><div>{{ row.Challenges }}</div>
                <div class="question">What has helped you the most in your role? </div><div>{{ row.Help }}</div>
                <hr>
            </div>
        {% endfor %}
    ''', data=data_list)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
