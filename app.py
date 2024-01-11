from flask import Flask, request, render_template
from index import SearchEngineIndex  # Adjust the import if needed
import traceback

# Define Flask app
app = Flask(__name__)

# Initialize the search engine index
index = SearchEngineIndex(index_dir='indexdir', index_name='basic')  # Adjust parameters if needed

@app.route("/")
def welcome_page():
    # Renders the welcome page with a search bar.
    return render_template("welcome_page.html")

@app.route("/query")
def fetch_results():
    # Fetches search results based on the provided query.
    if 'keywords' not in request.args:
        return "Could not find a query"
    else:
        keywords = request.args['keywords']
        # Search the index for matching results
        results = index.search(keywords)
        # Render HTML document to present the results
        return render_template("results.html", results=results, keywords=keywords)

@app.errorhandler(500)
def handle_internal_error(exception):
    # Handles internal server errors and displays the traceback.
    return "<pre>" + traceback.format_exc() + "</pre>"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
