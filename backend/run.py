from backend.app.__init__ import create_app

flask_app = create_app()


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5555, debug=True)