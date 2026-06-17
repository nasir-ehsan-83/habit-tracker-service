import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

def setup_offline_docs(app: FastAPI):
    # مسیر واقعی فولدر static
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, "static")  # fastapi_offline_docs/static

    # mount کردن
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # ReDoc
    @app.get("/redoc", include_in_schema=False)
    def redoc_docs():
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head><title>API ReDoc</title></head>
        <body>
            <redoc spec-url="/openapi.json"></redoc>
            <script src="/static/redoc/redoc.standalone.js"></script>
        </body>
        </html>
        """)

    # Swagger UI
    @app.get("/swagger", include_in_schema=False)
    def swagger_docs():
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="/static/swagger/swagger-ui.css">
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="/static/swagger/swagger-ui-bundle.js"></script>
            <script src="/static/swagger/swagger-ui-standalone-preset.js"></script>
            <script>
            SwaggerUIBundle({{
                url: "/openapi.json",
                dom_id: "#swagger-ui",
            }});
            </script>
        </body>
        </html>
        """)
