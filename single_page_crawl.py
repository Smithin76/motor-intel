import json
from threading import Thread
from scrapper import DumpHtml
from flask import Flask, jsonify, request
from flask_cors import CORS
from scrapper_logger import getScrapperLogger

dump_html = DumpHtml()
logger = getScrapperLogger()


class processPage:
    def __init__(self, req):
        self.req = req
        logger.debug(f"REQUEST RECEIVED | {req}")
        self.url = self.req.get('url')
        self.timeout = self.req.get('timeout', 100)
        self.response = {}

    def fetch_page(self):
        html = dump_html.fetch_html_scraperapi(url=self.url)
        self.add_to_response(field='html', data=str(html))
        return

    def add_to_response(self, field, data):
        self.response[field] = data
        return

    def get_response(self):
        return self.response


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/health')
    def version():
        return f"PAGE SCRAPPER"

    @app.route('/scrapePage', methods=['POST'])
    def store_request():
        payload = request.json
        page = processPage(req=payload)
        page.fetch_page()
        return page.get_response()

    @app.after_request
    def apply_caching(response):
        response.headers["Content-Type"] = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_invalid_usage(error):
        pass

    return app


if __name__ == '__main__':
    port = 6000
    logger.info('App listening on %s' % str(port))
    app = create_app()
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True, use_reloader=True)
