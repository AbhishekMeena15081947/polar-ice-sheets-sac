#!/usr/bin/env python3
"""
Flask Backend for Real-Time Polar Ice Sheet Monitoring
Provides REST API endpoints for live sea ice data and dashboard
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import fetch_ice_data
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_ice_data import PolarIceDataFetcher

app = Flask(__name__)
CORS(app)  # Enable CORS for API access

# Initialize data fetcher
fetcher = PolarIceDataFetcher()

# Cache for storing latest data
data_cache = {
    'last_update': None,
    'data': None,
    'cache_duration': timedelta(hours=6)  # Refresh every 6 hours
}


def get_cached_data():
    """Get data from cache or fetch new data if expired"""
    now = datetime.now()
    
    if (data_cache['last_update'] is None or 
        data_cache['data'] is None or
        now - data_cache['last_update'] > data_cache['cache_duration']):
        
        # Fetch fresh data
        data_cache['data'] = fetcher.get_ice_sheet_status()
        data_cache['last_update'] = now
        print(f"[{now}] Data cache refreshed")
    
    return data_cache['data']


@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')


@app.route('/api/status')
def api_status():
    """Get current polar ice sheet status"""
    try:
        data = get_cached_data()
        return jsonify({
            'status': 'success',
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/current')
def api_current():
    """Get current sea ice extent for both hemispheres"""
    try:
        arctic = fetcher.fetch_current_sea_ice_extent('north')
        antarctic = fetcher.fetch_current_sea_ice_extent('south')
        
        return jsonify({
            'status': 'success',
            'data': {
                'arctic': arctic,
                'antarctic': antarctic
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/monthly/<hemisphere>')
def api_monthly(hemisphere):
    """Get monthly sea ice data for specified hemisphere"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        
        data = fetcher.fetch_monthly_data(hemisphere, year, month)
        
        return jsonify({
            'status': 'success',
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/historical/<hemisphere>')
def api_historical(hemisphere):
    """Get historical comparison data"""
    try:
        years = request.args.get('years', '2020,2021,2022,2023,2024')
        year_list = [int(y.strip()) for y in years.split(',')]
        
        data = fetcher.fetch_historical_comparison(hemisphere, year_list)
        
        return jsonify({
            'status': 'success',
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Polar Ice Sheet Monitor',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/refresh')
def refresh_cache():
    """Force refresh of data cache"""
    try:
        data_cache['last_update'] = None
        data = get_cached_data()
        
        return jsonify({
            'status': 'success',
            'message': 'Cache refreshed successfully',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"""\n    ╔════════════════════════════════════════════════════════╗
    ║   Polar Ice Sheet Real-Time Monitoring System         ║
    ║   Flask Backend Server                                 ║
    ╚════════════════════════════════════════════════════════╝
    
    🌍 Server starting on http://0.0.0.0:{port}
    📊 API endpoints available:
       - GET /api/status          (Full ice sheet status)
       - GET /api/current         (Current extent both hemispheres)
       - GET /api/monthly/<hem>   (Monthly data)
       - GET /api/historical/<hem> (Historical comparison)
       - GET /api/health          (Health check)
       - GET /api/refresh         (Force cache refresh)
    
    🔄 Data refresh interval: 6 hours
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
