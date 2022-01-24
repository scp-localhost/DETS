import sys
from flask import g
from webapp import app
host = '127.0.0.1'
port = '8080'
if __name__ == "__main__":
   if len(sys.argv) > 2:
      host = sys.argv[1]
      port = sys.argv[2]
app.run(debug=False, host=host, port=port)
