#!/usr/bin/env python3
import os
from api.v1 import create_app

app = create_app(os.getenv('CEMA_HIS_CONFIG') or 'default')


if __name__ == "__main__":
    host = os.getenv('CEMA_HIS_API_HOST', '0.0.0.0')
    port = int(os.getenv('CEMA_HIS_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
