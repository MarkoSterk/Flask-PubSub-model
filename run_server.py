from app import create_app

DEBUG = False
PORT = 3000

app = create_app()

if __name__ == '__main__':
    app.run('0.0.0.0', port = PORT, debug = DEBUG)