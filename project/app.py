from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from tables import Description


def build_app():

    app = Flask(__name__)

    # To use the HTML5 template

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
        capacity = request.values['capacity']
        bedrooms = request.values['bedrooms']
        beds = request.values['beds']
        baths = request.values['baths']
        min_nights = request.values['minimum_nights']
        max_nights = request.values['maximum_nights']
        amnt_amenities = request.values['amnt_amenities']
        room_type = request.values['room_type']
        desc = request.values['desc']
        return render_template('results.html', 
                                capacity=capacity,
                                bedrooms=bedrooms,
                                beds=beds,
                                baths=baths,
                                min_nights=min_nights,
                                max_nights=max_nights,
                                amnt_amenities=amnt_amenities,
                                room_type=room_type,
                                desc=desc)
    return app
    # oeinef