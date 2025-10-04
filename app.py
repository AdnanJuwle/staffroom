# StaffRoom Flask Application Entry Point
# This file exists to satisfy Render's default expectations

from web_app import app

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
