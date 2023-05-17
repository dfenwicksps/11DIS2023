from flask import Flask, render_template_string
import openpyxl

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
    file_path = "/Users/d.fenwick/Downloads/pcc.xlsx"  # Replace with your file path
    sheet_name = "Sheet1"  # Replace with your sheet name
    data = read_excel(file_path, sheet_name)
    return render_template_string('''
        {% for paragraph in data %}
            <p>{{ paragraph }}</p>
        {% endfor %}
    ''', data=data)

if __name__ == '__main__':
    app.run(debug=True)
