import asyncio
import aiohttp
import ssl
from threading import Thread
from flask import Flask, request, jsonify
from description_eval import evaluate_description, regenerate_description
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

products_api = os.getenv("PRODUCTS_API")

app = Flask(__name__)

products_cache = {}
# In-memory storage for feedback
feedback_storage = []


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_data = request.json
    feedback_storage.append(feedback_data)
    
    # Start a new thread to handle the asynchronous task
    def run_async_task():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(handle_regeneration(feedback_data['product_id']))
        loop.close()

    thread = Thread(target=run_async_task)
    thread.start()

    return jsonify({"status": "success", "message": "Feedback received and processing"})

async def handle_regeneration(product_id):
    # Convert product_id to string if it's numeric, to match cache keys
    product_key = str(product_id)
    if product_key in products_cache:
        product = products_cache[product_key]
        if 'description' in product:
            new_description = await regenerate_description(product['description'])
            product['description'] = new_description
            print(f"Regenerated Description for Product {product_id}: {new_description}")
        else:
            print(f"No description available for Product ID {product_id}")
    else:
        print(f"Product ID {product_id} not found in cache.")



async def fetch_products(products_api, limit=2):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.get(products_api) as response:
            products = await response.json()
            for product in products:
                # Ensure that each product has an 'id' and 'description'
                if 'id' in product and 'description' in product:
                    # Use str(product['id']) if ID is numeric
                    products_cache[str(product['id'])] = product
            return products[:limit]



# Main function to orchestrate the fetching and evaluation process
async def main():
    products = await fetch_products(products_api)
    for product in products:
        description = product['description']
        improvements = await evaluate_description(description)
        print(f"Original Description: {description}")
        print(f"Suggested Improvements: {improvements}")

# Flask application does not automatically run with asyncio,
# need to use this approach for asynchronous handling
if __name__ == "__main__":
    from aiohttp import web

    # Function to kick off the asyncio part when Flask app starts
    async def start_async_operations():
        asyncio.create_task(main())

    # Run the Flask app in a background thread
    import threading
    threading.Thread(target=lambda: app.run(use_reloader=False)).start()

    # Start asyncio operations
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_async_operations())
    loop.run_forever()
