from flask import Flask
from ngrok import LabeledListenerBuilder
import ngrok

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # Set up ngrok to forward traffic to Flask app with a label
    ngrok.kill()
    ngrok.set_auth_token('2lnTGm9M2hGJrojyb7uHHdkM1OP_2SxMmJmTDnjgCZd3GPPWZ')
    ngrok.forward(
        addr=5000,
        labels='edge:edghts_2lnTTHwUtP6DU9BIGjYw9fjKKTa',
        proto="labeled",
    )

    # Start the Flask app
    app.run(debug=True, port=5000)
