import json, os, shutil
from app import visualization_data
from render import build_timeline_elements

OUT_DIR = 'docs'

def main():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    shutil.copy('templates/index.html', f'{OUT_DIR}/index.html')
    shutil.copytree('static/css', f'{OUT_DIR}/css')
    shutil.copytree('static/js', f'{OUT_DIR}/js')
    shutil.copytree('static', f'{OUT_DIR}/static')
    shutil.copy('sw.js', f'{OUT_DIR}/sw.js')

    data = visualization_data()
    result = build_timeline_elements(data)
    
    json_str = json.dumps(result, ensure_ascii=False)
    data_js_content = f"export const timelineData = {json_str};\n"

    with open(f'{OUT_DIR}/js/data.js', 'w', encoding='utf-8') as f:
        f.write(data_js_content)

    with open(f'{OUT_DIR}/static/js/data.js', 'w', encoding='utf-8') as f:
        f.write(data_js_content)

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