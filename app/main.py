
from flask import Flask, jsonify, request, redirect, url_for, abort
from .models import store
from .utils import generate_short_code, is_valid_url


app = Flask(__name__)


@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })


@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })


# Shorten URL Endpoint
@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing url in request body'}), 400
    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({'error': 'Invalid URL'}), 400
    # Generate unique short code
    for _ in range(5):
        short_code = generate_short_code()
        if not store.get_url(short_code):
            break
    else:
        return jsonify({'error': 'Could not generate unique short code'}), 500
    store.add_url(short_code, long_url)
    short_url = request.host_url.rstrip('/') + '/' + short_code
    return jsonify({'short_code': short_code, 'short_url': short_url}), 201


# Redirect Endpoint
@app.route('/<short_code>', methods=['GET'])
def redirect_short_url(short_code):
    entry = store.get_url(short_code)
    if not entry:
        abort(404, description="Short code not found")
    store.increment_click(short_code)
    return redirect(entry['url'])


# Analytics Endpoint
@app.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    stats = store.get_stats(short_code)
    if not stats:
        return jsonify({'error': 'Short code not found'}), 404
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)