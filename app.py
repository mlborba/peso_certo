import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app

# Para Vercel
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

