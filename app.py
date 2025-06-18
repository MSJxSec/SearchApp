from flask import Flask, render_template, request
import os

app = Flask(__name__)

def search_files(keyword, folders):
    results = []
    for folder in folders:
        for root, _, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines, 1):
                        if keyword.lower() in line.lower():
                            highlighted = line.replace(
                                keyword, f"<span class='highlight'>{keyword}</span>")
                            results.append({
                                'file': file,
                                'line_number': i,
                                'content': highlighted.strip()
                            })
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        folders = ['Database', 'ExtraData']
        results = search_files(keyword, folders)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)