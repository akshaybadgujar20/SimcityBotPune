from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS

from simcity.bot.enums.material import Material
from simcity.bot.main import buy_items, sell_materials, collect_raw_materials, collect_produced_items_from_commercial_buildings, collect_sold_item_money, \
    add_commercial_material_to_production, add_raw_material_to_production, set_up, stop_buy_items, stop_sell_materials, stop_collect_sold_item_money, \
    stop_add_raw_material_to_production, stop_collect_raw_materials, stop_collect_produced_items_from_commercial_buildings, set_running_state
from simcity.bot.material_data_loader import load_material_info_data

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# Sample data (simulates a database)
data = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"},
]

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

# Get all items
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(data)

# Get a single item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# Add a new item
@app.route('/api/items', methods=['POST'])
def add_item():
    new_item = request.json
    new_item["id"] = len(data) + 1
    data.append(new_item)
    return jsonify(new_item), 201

# Update an existing item by ID
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    item.update(request.json)
    return jsonify(item )

# Delete an item by ID
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

# Add a new item
@app.route('/action-perform', methods=['POST'])
def perform_action():
    request_data = request.json
    material_priorities = {}
    select_material_list = []
    city_port = request_data['port']
    print(f'city port: {city_port}')
    material_dict = load_material_info_data()
    set_up(city_port)
    if len(request_data['selectedMaterials']) > 0:
        for index, material in enumerate(request_data['selectedMaterials']):
            select_material_list.append(material_dict[material])
            material_priorities[Material[material]] = index + 1
    set_running_state(True)
    if request_data['action'] == 'CONTINUOUS_BUY':
        buy_items(request_data['selectedMaterials'], material_priorities, city_port)
    elif request_data['action'] == 'SELL_WITH_FULL_VALUE':
        sell_materials(select_material_list, city_port, False, True)
    elif request_data['action'] == 'SELL_WITH_ZERO_VALUE':
        sell_materials(select_material_list, city_port, False, False)
    elif request_data['action'] == 'COLLECT_FROM_FACTORY':
        collect_raw_materials(request_data['factoriesCount'], city_port)
    elif request_data['action'] == 'COLLECT_FROM_COMMERCIAL':
        collect_produced_items_from_commercial_buildings(request_data['commercialCount'],city_port)
    elif request_data['action'] == 'COLLECT_SOLD_ITEM_MONEY':
        collect_sold_item_money(1, city_port)
    elif request_data['action'] == 'ADVERTISE_ITEM_ON_TRADE_DEPOT':
        print('no action mapped')

    elif request_data['action'] == 'ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION':
        add_commercial_material_to_production(select_material_list,city_port)
    elif request_data['action'] == 'ADD_RAW_MATERIAL_TO_PRODUCTION':
        add_raw_material_to_production(select_material_list[0], request_data['factoriesCount'], city_port)
    else:
        return jsonify({"message": "unknown action"}), 200
    return jsonify({"message": "action performed"}), 200

@app.route('/action-stop', methods=['GET'])
def stop_action():
    set_running_state(False)
    return jsonify({"message": "action stopped"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
