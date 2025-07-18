from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('terminal.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    script_path = request.json.get('script')
    if not script_path.endswith('.py'):
        return jsonify({"output": "Error: Please provide a Python file (.py)"})
    
    try:
        result = subprocess.run(['python', script_path], 
                               capture_output=True, text=True, timeout=30)
        return jsonify({
            "output": result.stdout,
            "error": result.stderr
        })
    except FileNotFoundError:
        return jsonify({"error": f"File '{script_path}' not found"})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)