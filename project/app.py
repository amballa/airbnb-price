from flask import Flask, render_template, request
from flask_assets import Bundle, Environment


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

    # app routesc

    @app.route('/')
    def root():
        return render_template('index.html')

    return app
