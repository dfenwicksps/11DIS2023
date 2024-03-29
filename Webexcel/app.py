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
        </style>
                <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Your name</th>
                    <th>Your Position</th>
                    <th>Teachers</th>
                    <th>Current work</th>
                    <th>Challenges</th>
                    <th>Help</th>
                </tr>
            </thead>
            <tbody>
            {% for row in data %}
                <tr>
                    <td>{{ row['ID'] }}</td>
                    <td>{{ row['Your_name'] }}</td>
                    <td>{{ row['Your_Position'] }}</td>
                    <td>{{ row['Teachers'] }}</td>
                    <td>{{ row['Current_work'] }}</td>
                    <td>{{ row['Challenges'] }}</td>
                    <td>{{ row['Help'] }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    ''', data=data_list)

if __name__ == '__main__':
    app.run(debug=True)
