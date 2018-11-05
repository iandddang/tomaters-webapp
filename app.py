from flask import Flask, request, jsonify, render_template

# flask config
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', page='home')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)