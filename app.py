from flask import Flask , render_template , request , render_template_string , jsonify , url_for
from CRS import CropProduction
from CYP import yeildPrediction
import numpy as np
# from weather import weather_forcast
from weather import weather

app = Flask('__name__')

@app.route("/")
def func():
    return render_template('home.html' , res="")

@app.route("/details" , methods = ['GET' , 'POST'])
def details():
    if request.method == 'POST':
        N  = request.form['N']
        P  = request.form['P']
        K  = request.form['K']
        temprature  = request.form['temperature']
        humidity  = request.form['humidity']
        ph  = request.form['ph']
        rainfall  = request.form['rainfall']
        result = CropProduction(N,P,K,temprature,humidity,ph,rainfall)
        return render_template('home.html' , res=result)
    return "<h1>N</h1>"


@app.route("/yieldpred")
def yield_pre():
    return render_template('CYP_Details.html' , res="")

@app.route("/yield" , methods = ['GET' , 'POST'])
def yield_prediction():
    year = request.form['year']
    rain = request.form['rain']
    pest = request.form['pest']
    temp = request.form['temp']
    area = request.form['area']
    item = request.form['item']
    
    res = yeildPrediction(year,rain,pest,temp,area,item)
    return render_template('CYP_Details.html' , res=res)

@app.route("/city" )
def weatherForecastCity():
    return render_template('weatherpredic.html')





@app.route("/cityforecast" , methods = ['GET' , 'POST'])
def forecast():
    city = request.form['city']
    print(city)
    return weatherForecast(city)







@app.route("/<city>")
def weatherForecast(city):
    df = weather(city)
    weather_images = {
        "clear sky":url_for('static', filename='clearsky.png'),
        "overcast clouds":url_for('static', filename='overcastjpeg.jpeg'),
        "broken clouds": url_for('static', filename='brokencloud.jpeg'),
        "light rain": url_for('static', filename='lightrainjpeg.jpeg'),
        "few clouds":url_for('static', filename='few-clouds.png'),
        "scattered clouds":url_for('static', filename='scattercloud.jpeg'),
        "light snow": url_for('static' ,filename='lightsnow.jpeg' ),
        "moderate rain": url_for('static' ,filename='moderaterain.png' ),
        "heavy intensity rain":url_for('static' ,filename='heavyrain.jpeg' ),
    }

    # Add a new column for images
    df['Temperature (°C)'] = df['Temperature (°C)'].astype(np.dtype('int64'))
    df['Image'] = df['Weather'].map(weather_images).apply(lambda x: f'<img src="{x}" width="100" height="80">')
    if df is not None:
        table_html = df.to_html(classes='table table-striped', index=False, escape=False)
        return render_template("weather.html" , city=city, table_html=table_html)
    else:
        return f"<h1>Weather data for {city} could not be retrieved</h1>"


if __name__ == '__main__':
    app.run(debug=True)