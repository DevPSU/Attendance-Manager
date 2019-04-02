from app.app import application

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True, port=80, threaded=True)
