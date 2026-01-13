import os
import json
from flask import Flask, render_template, send_file, abort
from data_pipeline import load_and_prepare, build_figures, generate_insights, generate_recommendations

app = Flask(__name__)

# Resolve dataset path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'Dataset', 'Aadhar Enrolment Dataset.csv')
REPORT_PATH = os.path.join(BASE_DIR, 'UIDAI_Aadhaar_Analytics_Report.pdf')

@app.route('/')
def index():
    data = load_and_prepare(DATASET_PATH, state_filter='Maharashtra')
    figures = build_figures(data)
    insights = generate_insights(data)
    recommendations = generate_recommendations(data)

    figures_json = {k: v.to_json() for k, v in figures.items()}
    return render_template('index.html', figures_json=figures_json, insights=insights, recommendations=recommendations)

@app.route('/download/dataset')
def download_dataset():
    try:
        return send_file(DATASET_PATH, as_attachment=True, download_name='Aadhar_Enrolment_Dataset.csv')
    except FileNotFoundError:
        abort(404)


@app.route('/download/report')
def download_report():
    try:
        return send_file(REPORT_PATH, as_attachment=True, download_name='UIDAI_Aadhaar_Analytics_Report.pdf')
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
