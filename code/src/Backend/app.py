from flask import Flask, request, jsonify, render_template
import backend as bk

app = Flask(__name__, template_folder='../Frontend', static_folder='../Frontend')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    files = request.files.getlist('files')
    if not files or not files[0]:
        return jsonify({"error": "No file uploaded"}), 400
    file = files[0]  # Process only the first file
    result = bk.analyze_file(file)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)