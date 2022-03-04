from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from .model import user_desc
import pickle
import pandas as pd
import numpy as np
import keras
import tensorflow as tf


def build_app():

    app = Flask(__name__)

    js = Bundle('breakpoints.min.js', 'browser.min.js', 'jquery.dropotron.min.js',
                'jquery.min.js', 'jquery.scrollex.min.js', 'main.js', 'util.js',
                output='gen/all.js')

    css = Bundle('main.css', output='gen/all.css')

    assets = Environment(app)

    assets.register('all_js', js)
    assets.register('all_css', css)

    @app.route('/')
    def root():
        return render_template('index.html')

    @app.route('/#')
    def return_to_home():
        return render_template('index.html')
    
    @app.route('/results', methods=['POST'])
    def display_results():
        capacity = int(request.values['capacity'])
        bedrooms = int(request.values['bedrooms'])
        beds = int(request.values['beds'])
        baths = int(request.values['baths'])
        min_nights = int(request.values['minimum_nights'])
        max_nights = int(request.values['maximum_nights'])
        amnt_amenities = int(request.values['amnt_amenities'])
        room_type = request.values['room_type']
        desc = request.values['desc']

        user_arr = np.array([room_type, capacity, bedrooms,
                            beds, min_nights, max_nights, amnt_amenities, baths])

        df_nlp = user_desc(desc)
        arr_nlp = df_nlp.to_numpy().flatten()

        user_arr = np.concatenate((user_arr, arr_nlp))
        user_arr_reshaped = user_arr.reshape(1, len(user_arr))

        # Model
        #model = pickle.load(open('project/best_regressor', 'rb'))

        graph = tf.compat.v1.get_default_graph()

        with graph.as_default():
            model = keras.models.load_model("project/keras_model")
            result = model.predict(user_arr_reshaped)

        price = round(result[0][0])

        return render_template('results.html', price=price)

    return app
