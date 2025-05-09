#!/usr/bin/env python3
from connexion import FlaskApp
#from openapi_server import encoder
import uvicorn

app = FlaskApp(__name__, specification_dir='./openapi/')
#app.json_encoder = encoder.JSONEncoder

if __name__ == '__main__':
    
    app.add_api('cloudinstance.yaml', arguments={'title': '5GMETA Cloud API'}, pythonic_params=True)
    config = uvicorn.Config("__main__:app", host='0.0.0.0', port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
    
