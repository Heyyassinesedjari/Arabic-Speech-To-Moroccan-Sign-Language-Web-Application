from asr_to_sign import app
import logging
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    app.run(debug=True)