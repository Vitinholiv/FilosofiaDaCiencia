import json, os, shutil
from app import visualization_data
from render import build_timeline_elements

OUT_DIR = 'docs'

def main():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    data = visualization_data()
    result = build_timeline_elements(data)
    with open(f'{OUT_DIR}/timeline.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)

    shutil.copy('templates/index.html', f'{OUT_DIR}/index.html')
    shutil.copytree('static/css', f'{OUT_DIR}/css')
    shutil.copytree('static/js', f'{OUT_DIR}/js')
    shutil.copytree('static', f'{OUT_DIR}/static')
    shutil.copy('sw.js', f'{OUT_DIR}/sw.js')

    images = []
    for root, _, files in os.walk(f'{OUT_DIR}/static/img'):
        for fname in files:
            rel = os.path.relpath(os.path.join(root, fname), OUT_DIR)
            images.append('./' + rel.replace(os.sep, '/'))
    with open(f'{OUT_DIR}/img-manifest.json', 'w') as f:
        json.dump(images, f)

    print(f'Site estático gerado em ./{OUT_DIR} ({len(images)} imagens)')

if __name__ == '__main__':
    main()