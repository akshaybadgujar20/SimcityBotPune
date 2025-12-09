from fontTools.misc.cython import returns

from simcity.bot.enums.building import Building
from simcity.bot.enums.material import Material


def get_commercial_data():
    # Example Usage
    return [
        {
            "name": Building.BUILDING_SUPPLIES_STORE,
            "produces": [
                {
                    "material": Material.NAILS,
                    "production_time": 300,
                },
                {
                    "material": Material.PLANKS,
                    "production_time": 1800,
                },
                {
                    "material": Material.BRICKS,
                    "production_time": 1200,
                },
                {
                    "material": Material.CEMENT,
                    "production_time": 3000,
                },
                {
                    "material": Material.GLUE,
                    "production_time": 3600,
                },
                {
                    "material": Material.PAINT,
                    "production_time": 3600,
                }
            ]
        },
        {
            "name": Building.HARDWARE_STORE,
            "produces": [
                {
                    "material": Material.HAMMER,
                    "production_time": 840,
                },
                {
                    "material": Material.MEASURING_TAPE,
                    "production_time": 1200,
                },
                {
                    "material": Material.SHOVEL,
                    "production_time": 1800,
                },
                {
                    "material": Material.COOKING_UTENSILS,
                    "production_time": 2700,
                },
                {
                    "material": Material.LADDER,
                    "production_time": 3600,
                },
                {
                    "material": Material.DRILL,
                    "production_time": 7200,
                }
            ]
        },
        {
            "name": Building.FARMER_S_MARKET,
            "produces": [
                {
                    "material": Material.VEGETABLES,
                    "production_time": 1200,
                },
                {
                    "material": Material.FLOUR_BAG,
                    "production_time": 1800,
                },
                {
                    "material": Material.FRUIT_AND_BERRIES,
                    "production_time": 5400,
                },
                {
                    "material": Material.CREAM,
                    "production_time": 4500,
                },
                {
                    "material": Material.CORN,
                    "production_time": 3600,
                },
                {
                    "material": Material.CHEESE,
                    "production_time": 6300,
                },
                {
                    "material": Material.BEEF,
                    "production_time": 9000,
                }
            ]
        },
        {
            "name": Building.FURNITURE_STORE,
            "produces": [
                {
                    "material": Material.CHAIRS,
                    "production_time": 1200,
                },
                {
                    "material": Material.TABLES,
                    "production_time": 1800,
                },
                {
                    "material": Material.HOME_TEXTILES,
                    "production_time": 4500,
                },
                {
                    "material": Material.CUPBOARD,
                    "production_time": 2700,
                },
                {
                    "material": Material.COUCH,
                    "production_time": 9000,
                }
            ]
        },
        {
            "name": Building.GARDENING_SUPPLIES,
            "produces": [
                {
                    "material": Material.GRASS,
                    "production_time": 1800,
                },
                {
                    "material": Material.TREE_SAPLINGS,
                    "production_time": 5400,
                },
                {
                    "material": Material.GARDEN_FURNITURE,
                    "production_time": 8100,
                },
                {
                    "material": Material.FIRE_PIT,
                    "production_time": 14400,
                },
                {
                    "material": Material.LAWN_MOWER,
                    "production_time": 7200,
                },
                {
                    "material": Material.GARDEN_GNOMES,
                    "production_time": 5400,
                }
            ]
        },
        {
            "name": Building.DONUT_SHOP,
            "produces": [
                {
                    "material": Material.DONUTS,
                    "production_time": 2700,
                },
                {
                    "material": Material.GREEN_SMOOTHIE,
                    "production_time": 1800,
                },
                {
                    "material": Material.BREAD_ROLL,
                    "production_time": 3600,
                },
                {
                    "material": Material.CHERRY_CHEESECAKE,
                    "production_time": 5400,
                },
                {
                    "material": Material.FROZEN_YOGURT,
                    "production_time": 14400,
                },
                {
                    "material": Material.COFFEE,
                    "production_time": 3600,
                }
            ]
        },
        {
            "name": Building.DONUT_SHOP,
            "produces": [
                {
                    "material": Material.CAP,
                    "production_time": 3600,
                },
                {
                    "material": Material.SHOES,
                    "production_time": 4500,
                },
                {
                    "material": Material.WATCH,
                    "production_time": 5400,
                },
                {
                    "material": Material.BUSINESS_SUITS,
                    "production_time": 12600,
                },
                {
                    "material": Material.BACKPACK,
                    "production_time": 9000,
                }
            ]
        },
        {
            "name": Building.FAST_FOOD_RESTAURANT,
            "produces": [
                {
                    "material": Material.ICE_CREAM_SANDWICH,
                    "production_time": 840,
                },
                {
                    "material": Material.PIZZA,
                    "production_time": 1440,
                },
                {
                    "material": Material.BURGERS,
                    "production_time": 2100,
                },
                {
                    "material": Material.CHEESE_FRIES,
                    "production_time": 1200,
                },
                {
                    "material": Material.LEMONADE_BOTTLE,
                    "production_time": 3600,
                },
                {
                    "material": Material.POPCORN,
                    "production_time": 1800,
                }
            ]
        },
        {
            "name": Building.HOME_APPLIANCES,
            "produces": [
                {
                    "material": Material.BBQ_GRILL,
                    "production_time": 9900,
                },
                {
                    "material": Material.REFRIGERATOR,
                    "production_time": 12600,
                },
                {
                    "material": Material.LIGHTING_SYSTEM,
                    "production_time": 6300,
                },
                {
                    "material": Material.TV,
                    "production_time": 9000,
                },
                {
                    "material": Material.MICROWAVE_OVEN,
                    "production_time": 7200,
                }
            ]
        },
        {
            "name": Building.ECO_SHOP,
            "produces": [
                {
                    "material": Material.REUSABLE_BAG,
                    "production_time": 1200,
                },
                {
                    "material": Material.ECOLOGICAL_SHOES,
                    "production_time": 7200,
                },
                {
                    "material": Material.YOGA_MAT,
                    "production_time": 14400,
                }
            ]
        },
        {
            "name": Building.CAR_PARTS,
            "produces": [
                {
                    "material": Material.MOTOR_OIL,
                    "production_time": 1200,
                },
                {
                    "material": Material.CAR_TIRE,
                    "production_time": 7200,
                },
                {
                    "material": Material.ENGINE,
                    "production_time": 14400,
                }
            ]
        },
        {
            "name": Building.SILK_STORE,
            "produces": [
                {
                    "material": Material.STRING,
                    "production_time": 1200,
                },
                {
                    "material": Material.FAN,
                    "production_time": 9000,
                },
                {
                    "material": Material.ROBE,
                    "production_time": 14400,
                }
            ]
        },
        {
            "name": Building.TROPICAL_PRODUCTS_STORE,
            "produces": [
                {
                    "material": Material.COCONUT_OIL,
                    "production_time": 1200,
                },
                {
                    "material": Material.FACE_CREAM,
                    "production_time": 5400,
                },
                {
                    "material": Material.TROPICAL_DRINK,
                    "production_time": 15000,
                }
            ]
        },
        {
            "name": Building.FISH_MARKETPLACE,
            "produces": [
                {
                    "material": Material.CANNED_FISH,
                    "production_time": 1200,
                },
                {
                    "material": Material.FISH_SOUP,
                    "production_time": 7200,
                },
                {
                    "material": Material.SALMON_SANDWICH,
                    "production_time": 10800,
                }
            ]
        },
    ]