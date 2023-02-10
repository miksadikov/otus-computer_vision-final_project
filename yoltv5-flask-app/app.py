import os
import sys
import shutil
from pathlib import Path

from flask import Flask, render_template, request, redirect

from detect import run

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 6000 * 4000

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return
            
        shutil.rmtree(ROOT / 'runs/detect/exp')
        dir = ROOT / 'data/images'
        for F in os.listdir(dir):
            os.remove(os.path.join(dir, F))

        img_bytes = file.read()    
        with open(ROOT / 'data/images/image.jpg', 'wb') as f:
            f.write(img_bytes)        
        run()
        shutil.move(ROOT / 'runs/detect/exp/image.jpg', ROOT / 'static/image.jpg')
        return render_template('result.html', class_id=1,
                               class_name='class_name')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
