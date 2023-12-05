from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = '2eccf75f911805e28fade73529d4b60e'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather = {
            'city': data['name'],
            'temperature': round(data['main']['temp'] - 273.15, 2),  # Kelvin to Celsius
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }
        return render_template('weather.html', weather=weather)
    except requests.exceptions.RequestException as e:
        return render_template('error.html',error=f'Request failed: {e}')
    except Exception as e:
        return render_template('error.html', error=str(e))
    
if __name__ == '__main__':
    app.run(debug=True)
