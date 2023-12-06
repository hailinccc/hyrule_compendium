# Hyrule Compendium Interactive Project

Explore and analyze data from "The Legend of Zelda: Breath of the Wild" with this interactive application. Leveraging the [Hyrule Compendium API](https://gadhagod.github.io/Hyrule-Compendium-API/#/), this project offers users an in-depth look at various game elements including monsters, equipment, materials, creatures, and treasures.

### Required Packages: 
- **Plotly**: For interactive data visualizations.
- **Flask**: To create a web-based user interface.
- **Requests**: To handle HTTP requests to the API.
- **JSON**: For parsing and handling JSON data.

### Project Structure

- **`final_project.py`**: Contains the main project code.
- **`zelda_function.py`**: Module for data retrieval functions.
- **`app.py`**: Manages the Flask web application.
- **`/templates`**: Folder containing Flask HTML templates.


## Data Source

**Source API:** https://gadhagod.github.io/Hyrule-Compendium-API/#/

### Access

In the Hyrule Compendium project, data is accessed from the Hyrule Compendium API, which provides detailed information about various elements from the world of Hyrule. This includes data on monsters, equipment, materials, and more. The Python application fetches this data using HTTP requests to specific API endpoints.

To organize the retrieved data, it's structured into a tree format using the TreeNode class, with each category (like monsters or equipment) forming a branch and its items as leaves.

Caching is employed to enhance efficiency. When data is first fetched, it's stored in a cache ('hyrule_retrieved.json'), managed through the create_cache function. Subsequent data requests first check this cache, reducing the need for additional API calls. This approach speeds up data retrieval and minimizes network usage, making the application more efficient and responsive. Also, when processing the Heart Restoration Analysis, a file is also cached ('hearts_recovered_entries.json') 

### Data Summary

The Hyrule Compendium project taps into the data provided by the Hyrule Compendium API, encompassing a total of 389 distinct items from the "Legend of Zelda: Breath of the Wild" game universe. This comprehensive dataset covers several categories such as Monsters, Equipment, Materials, Creatures, and Treasure, with all 389 records being retrieved for the project. Each record in the dataset is rich with details, featuring key attributes like name, category, common_locations, description, and image. For certain items, additional information like hearts_recovered is also provided. This extensive and detailed dataset is instrumental for the project’s objective of offering interactive and insightful analysis into various aspects of the game, enhancing understanding of character attributes, item utilities, and more.

## Data Structure

In the Hyrule Compendium project, a tree data structure is employed to organize data from the Hyrule Compendium API, which includes categories like Monsters, Equipment, Materials, Creatures, and Treasure. Each category is represented as a root node, with individual items or entities as child nodes. Nodes in this tree, created using the TreeNode class, store attributes like name, type, and optionally data, encompassing specific details from the API. This hierarchical structure facilitates efficient data organization, allowing for effective traversal and retrieval of information. The tree is also serialized into a JSON format for storage, ensuring the data's hierarchical integrity is maintained for later use. This tree data structure aligns with the project's goal to provide an organized and interactive exploration of the game's diverse elements. The tree structure is included in the JSON file called 'hyrule_tree.json'.

## User Interaction

### User Interaction and Options:

**Search or Analyze:** Users can choose to query specific items or perform heart recovery data analysis by responding to questions, and this is facilitated through interactive prompts or a web interface using Flask. In the searching section, the user can type the name of a particular item like a monster. The application presents detailed information about each queried item, such as its description, common locations, and related images. Additionally, users can perform statistical analyses, which can help user to determine the best combination of items for health recovery.

**Interactive Visualizations:** Using Plotly, the application offers interactive graphs, providing a visual representation of the data. For example, users can view pie charts showing the distribution of different item types or analyze health recovery options.

### How to Use:

1. Run the `final_project.py`.
2. Click the URL prompted. 
3. Choose between searching for items or performing analyses.
4. Interact with the data through the web interface or command line prompts.
5. View and interact with Plotly visualizations for graphical data insights.
