from fastapi.responses import HTMLResponse
from fastapi import APIRouter

welcome_router = APIRouter()

@welcome_router.get("/", response_class=HTMLResponse)
async def home_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to the Movie Listing API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    text-align: center;
                }
                header {
                    background-color: #333;
                    color: #fff;
                    padding: 20px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                h1 {
                    margin: 0;
                    font-size: 2.5em;
                }
                main {
                    padding: 20px;
                }
                p {
                    font-size: 1.2em;
                    line-height: 1.6;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    font-size: 1.1em;
                    margin: 10px 0;
                }
                a {
                    color: #007BFF;
                    text-decoration: none;
                    font-weight: bold;
                }
                a:hover {
                    text-decoration: underline;
                }
                footer {
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #333;
                    color: #fff;
                    box-shadow: 0 -4px 6px rgba(0,0,0,0.1);
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Welcome to the Movie Listing API</h1>
            </header>
            <main>
                <p>This API offers a comprehensive solution for managing movies. With this API, you can:</p>
                <ul>
                    <li><strong>Add movies</strong> - Create new entries in your movie catalog.</li>
                    <li><strong>View movies</strong> - Browse and explore all the movies in the catalog.</li>
                    <li><strong>Update movies</strong> - Edit the details of existing movies that you added.</li>
                    <li><strong>Delete movies</strong> - Remove movies from the catalog that you added.</li>
                    <li><strong>Rate movies</strong> - Provide ratings for movies you’ve watched.</li>
                    <li><strong>Comment on movies</strong> - Share your thoughts and feedback on movies.</li>
                </ul>
                <p>To explore the available endpoints and interact with the API, visit:</p>
                <ul>
                    <li><a href="/docs">API Documentation (Swagger UI)</a></li>
                    <li><a href="/redoc">API Documentation (ReDoc)</a></li>
                </ul>
                <p>For a detailed description of the API and its specifications, you can access:</p>
                <ul>
                    <li><a href="/openapi.json">OpenAPI JSON Specification</a></li>
                </ul>
            </main>
            <footer>
                <p>&copy; 2024 Movie Listing API. All rights reserved.</p>
            </footer>
        </body>
    </html>
    """
