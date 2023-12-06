from flask import Flask, render_template, request, redirect, url_for
import zelda_functions as utl
import json
import plotly.express as px
import plotly

app = Flask(__name__)
cache = utl.create_cache(utl.CACHE_FILEPATH)

@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        response = request.form['initial_choice']
        if response.lower() == 'yes':
            return redirect(url_for('search_item'))
        elif response.lower() == 'no':
            return redirect(url_for('analysis_question'))
        else:
            return render_template('welcome.html', error="Please enter yes or no.")
    return render_template('welcome.html')

@app.route('/search_item', methods=['GET', 'POST'])
def search_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_data = utl.fetch_item_details(item_name, cache, utl.CACHE_FILEPATH)

        if item_data:
            return render_template('item_result.html', item=item_data)
        else:
            return render_template('search_item.html', error="Item not found.")
    return render_template('search_item.html')

@app.route('/analysis_question', methods=['GET', 'POST'])
def analysis_question():
    if request.method == 'POST':
        response = request.form['response']  # yes or no
        if response.lower() == 'yes':
            return redirect(url_for('heart_recovery_input'))
        else:
            return redirect(url_for('go_back_or_exit'))
    return render_template('analysis_question.html')


@app.route('/go_back_or_exit', methods=['GET', 'POST'])
def go_back_or_exit():
    if request.method == 'POST':
        response = request.form['response']
        if response.lower() == 'go back':
            return redirect(url_for('welcome'))
        else:
            return "Thank you for using the project. See you next time!"
    return render_template('go_back_or_exit.html')

@app.route('/analysis_options', methods=['GET', 'POST'])
def analysis_options():
    if request.method == 'POST':
        # Handle the user's choice here
        return redirect(url_for('heart_recovery_input'))
    return render_template('analysis_options.html')

@app.route('/heart_recovery_input', methods=['GET', 'POST'])
def heart_recovery_input():
    if request.method == 'POST':
        hearts_needed_str = request.form.get('hearts_needed')
        if hearts_needed_str:
            try:
                hearts_needed = float(hearts_needed_str)
                # Directly call the analysis function here instead of redirecting
                combo_str, best_combo = utl.perform_local_analysis(hearts_needed)
                if best_combo:
                    return render_template('analysis_results.html', combo_str=combo_str, items=best_combo)
                else:
                    return render_template('error.html', message="No combination found.")
            except ValueError:
                return render_template('heart_recovery_input.html', error="Please enter a valid number.")
        else:
            return render_template('heart_recovery_input.html', error="Please enter the number of hearts.")
    # Display the form on a GET request
    return render_template('heart_recovery_input.html')


@app.route('/perform_analysis', methods=['POST'])
def perform_analysis():
    hearts_needed_str = request.form.get('hearts_needed')
    try:
        hearts_needed = float(hearts_needed_str)
        combo_str, best_combo = utl.perform_local_analysis(hearts_needed)
        if best_combo:
            # Prepare data for the pie chart
            labels = [item['name'] for item in best_combo]
            values = [item['hearts_recovered'] for item in best_combo]

            # Create a pie chart
            fig = px.pie(names=labels, values=values, title=f"Heart Recovery Items Distribution for {hearts_needed} Hearts")
            graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            return render_template('analysis_results.html', combo_str=combo_str, items=best_combo, graph_json=graph_json)
        else:
            return render_template('error.html', message="No combination found.")
    except ValueError:
        return render_template('heart_recovery_input.html', error="Please enter a valid number.")


if __name__ == '__main__':
    app.run(debug=True)
