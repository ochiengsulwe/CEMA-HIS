template = {
    "swagger": "2.0.0",
    "info": {
        "title": "CEMA-HIS Restful APIs",
        "description": "This is test version of CEMA-HIS System, "
                       "designed to provide robust and scalable health information "
                       "management solutions.",
        "contact": {
            "responsibleDeveloper": "Ochieng' Sulwe Odongo",
            "email": "kodongohieng@gmail.com",
            "url": "https://github.com/ochiengsulwe",
        },
        "version": "1.0.0"
    },
    # "basePath": "/api/v1/views",  # base bash for blueprint registration
    "schemes": [
        "https",
        "http"
    ],
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Bearer <JWT_TOKEN>"
        }
    }
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
