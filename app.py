from flask import Flask, render_template, request, redirect, url_for
import zelda_functions as utl


app = Flask(__name__)
cache = utl.create_cache(utl.CACHE_FILEPATH)

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        pass
    return render_template('analysis.html')


@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        response = request.form['initial_choice']
        if response.lower() == 'yes':
            return redirect(url_for('search_item'))
        elif response.lower() == 'no':
            return redirect(url_for('analysis'))
        else:
            return render_template('welcome.html', error="Please enter yes or no.")
    return render_template('welcome.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
@app.route('/search', methods=['POST'])
@app.route('/search', methods=['POST'])
def search():
    user_response = request.form['find_item'].strip().lower()
    if user_response == 'yes':
        return render_template('item_search.html')
    elif user_response == 'no':
        return render_template('analysis.html')
    else:
        return render_template('index.html', error="Invalid response. Please enter yes or no.")


@app.route('/search_item', methods=['GET', 'POST'])
def search_item():
    if request.method == 'POST':
        item_name = request.form['item_name']

        item_data = utl.fetch_item_details(item_name, cache, utl.CACHE_FILEPATH)

        if item_data:
            return render_template('item_result.html', item_data=item_data)
        else:
            return render_template('search_item.html', error="Item not found.")
    return render_template('search_item.html')


@app.route('/item_result', methods=['POST'])
def item_result():
    item_name = request.form['item_name']
    item_data = utl.fetch_and_display_item(item_name)  # Assuming this function exists in zelda_functions.py
    return render_template('item_result.html', item_data=item_data)


@app.route('/perform_analysis', methods=['POST'])
def perform_analysis():
    user_response = request.form['do_analysis'].strip().lower()
    if user_response == 'yes':
        return render_template('analysis_results.html', results=analysis_results)
    else:
        return render_template('index.html', message="Returning to main menu.")

if __name__ == '__main__':
    app.run(debug=True)