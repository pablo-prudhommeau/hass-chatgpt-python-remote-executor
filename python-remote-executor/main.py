from flask import Flask, request, jsonify
import sys
import subprocess
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/run_script', methods=['POST'])
def run_script():
    data = request.json
    script = data['script']
    requirements = data.get('requirements', '')

    if requirements:
        with open('requirements.txt', 'w') as f:
            f.write(requirements)

        install_result = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], capture_output=True, text=True)
        print("------------------")
        print(requirements)
        print("***")
        print(install_result.stdout.replace('\\n', '\n').replace('\\t', '\t'))
        print("***")
        print(install_result.stderr.replace('\\n', '\n').replace('\\t', '\t'))
        print("***")
        print(install_result)
        print("------------------")

        if install_result.returncode == 1:
            return jsonify({
                'stdout': install_result.stdout,
                'stderr': install_result.stderr,
                'returncode': install_result.returncode
            }), 400

    script_result = subprocess.run(["python3", "-c", script], capture_output=True, text=True)

    print(">>>>>>>>>>>>>>>>>>")
    print(script)
    print("***")
    print(script_result.stdout.replace('\\n', '\n').replace('\\t', '\t'))
    print("***")
    print(script_result.stderr.replace('\\n', '\n').replace('\\t', '\t'))
    print("***")
    print("Return code : " + str(script_result.returncode))
    print(">>>>>>>>>>>>>>>>>>")

    sys.stdout.flush()

    return jsonify({
        'stdout': script_result.stdout,
        'stderr': script_result.stderr,
        'returncode': script_result.returncode
    })

if __name__ == '__main__':
    app.run(host='::', port=6000)
