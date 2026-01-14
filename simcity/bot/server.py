from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread, Event
from simcity.bot.enums.material import Material
from simcity.bot.main import buy_items, sell_materials, collect_raw_materials, \
    collect_produced_items_from_commercial_buildings, collect_sold_item_money, \
    add_commercial_material_to_production, add_raw_material_to_production, set_up
from simcity.bot.material_data_loader import load_material_info_data

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# Sample data (simulates a database)
data = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"},
]

running_actions = {}
stop_events = {}

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

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

    if request_data['action'] == 'CONTINUOUS_BUY':
        start_action(
            city_port,
            buy_items,
            (request_data['selectedMaterials'], material_priorities, city_port)
        )

    elif request_data['action'] == 'SELL_WITH_FULL_VALUE':
        start_action(
            city_port,
            sell_materials,
            (select_material_list, city_port, False, True)
        )

    elif request_data['action'] == 'SELL_WITH_ZERO_VALUE':
        start_action(
            city_port,
            sell_materials,
            (select_material_list, city_port, False, False)
        )

    elif request_data['action'] == 'COLLECT_FROM_FACTORY':
        start_action(
            city_port,
            collect_raw_materials,
            (request_data['factoriesCount'], city_port)
        )

    elif request_data['action'] == 'COLLECT_FROM_COMMERCIAL':
        start_action(
            city_port,
            collect_produced_items_from_commercial_buildings,
            (request_data['commercialCount'], city_port)
        )

    elif request_data['action'] == 'COLLECT_SOLD_ITEM_MONEY':
        start_action(
            city_port,
            collect_sold_item_money,
            (1, city_port)
        )

    elif request_data['action'] == 'ADVERTISE_ITEM_ON_TRADE_DEPOT':
        print('no action mapped')

    elif request_data['action'] == 'ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION':
        start_action(
            city_port,
            add_commercial_material_to_production,
            (select_material_list, city_port)
        )

    elif request_data['action'] == 'ADD_RAW_MATERIAL_TO_PRODUCTION':
        start_action(
            city_port,
            add_raw_material_to_production,
            (select_material_list[0], request_data['factoriesCount'], city_port)
        )

    else:
        return jsonify({"message": "unknown action"}), 200

    return jsonify({"message": "action started"}), 200


def start_action(city_port, target, args):
    if city_port in stop_events:
        stop_events[city_port].set()

    stop_event = Event()
    stop_events[city_port] = stop_event

    thread = Thread(
        target=target,
        args=(*args, stop_event),
        daemon=True
    )

    running_actions[city_port] = thread
    thread.start()

@app.route('/action-stop', methods=['POST'])
def stop_action():
    request_data = request.json
    city_port = request_data['port']
    print(f'stop requested for city port: {city_port}')

    if city_port in stop_events:
        stop_events[city_port].set()
        return jsonify({"message": "action stop requested"}), 200

    return jsonify({"message": "no running action for this city"}), 200



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)


