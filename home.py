from flask import Flask, render_template, request  
import pandas as pd
from datetime import date

app = Flask(__name__)

cpi_df = pd.read_csv('..\\Price Predictor\\clean_forecasted_cpi.csv')

prodname = cpi_df['product_name'].drop_duplicates()

@app.route('/', methods=['GET', 'POST'])
def home():
    dates = []
    quantity = []
    price = []
    L4list = request.form.get('productname')
    predicted_price_list = []
    predicted_price = 0

    if request.method == "POST":
        L4list = request.form.get('productname')
        
        prod_list = cpi_df[['product_name', 
                            'quantity',
                            'price', 
                            'ds', 
                            'yhat']]

        groupitem = prod_list.groupby('product_name')

        G = groupitem.get_group(L4list)
        
        #dates = list(G['ds'].dt.strftime("%x"))
        dates = list(G['ds'])
        quantity = list(G['quantity'])
        price = list(G['price'])
        predicted_price_list = list(G['yhat'])
        predicted_price = round(abs(float(predicted_price_list[27])),6)
       
    return render_template('home.html', 
                           Fourthlist = prodname, 
                           dates = dates, 
                           quantity = quantity, 
                           price = price, 
                           predicted_price = predicted_price,        
                           itemname = L4list)


if __name__ == "__main__":
    app.run(debug=True)