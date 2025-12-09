from simcity.bot.enums.material import Material

RECIPES = {
    Material.NAILS: {Material.METAL: 2},
    Material.PLANKS: {Material.WOOD: 2},
    Material.BRICKS: {Material.MINERALS: 2},
    Material.CEMENT: {Material.MINERALS: 2, Material.CHEMICALS: 1},
    Material.GLUE: {Material.PLASTIC: 1, Material.CHEMICALS: 2},
    Material.PAINT: {Material.METAL: 2, Material.MINERALS: 1, Material.CHEMICALS: 2},

    Material.MEASURING_TAPE: {Material.METAL: 1, Material.PLASTIC: 1},
    Material.SHOVEL: {Material.METAL: 1, Material.WOOD: 1, Material.PLASTIC: 1},
    Material.COOKING_UTENSILS: {Material.METAL: 2, Material.WOOD: 2, Material.PLASTIC: 2},
    Material.LADDER: {Material.METAL: 2, Material.PLANKS: 2},
    Material.DRILL: {Material.METAL: 2, Material.PLASTIC: 2, Material.ELECTRICAL_COMPONENTS: 1},

    Material.VEGETABLES: {Material.SEEDS: 2},
    Material.FLOUR_BAG: {Material.SEEDS: 2, Material.TEXTILES: 2},
    Material.FRUIT_AND_BERRIES: {Material.SEEDS: 2, Material.TREE_SAPLINGS: 1},
    Material.CREAM: {Material.ANIMAL_FEED: 1},
    Material.CORN: {Material.SEEDS: 4, Material.MINERALS: 1},
    Material.CHEESE: {Material.ANIMAL_FEED: 2},
    Material.BEEF: {Material.ANIMAL_FEED: 3},

    Material.CHAIRS: {Material.WOOD: 2, Material.NAILS: 1, Material.HAMMER: 1},
    Material.TABLES: {Material.NAILS: 2, Material.PLANKS: 1, Material.HAMMER: 1},
    Material.HOME_TEXTILES: {Material.TEXTILES: 2, Material.MEASURING_TAPE: 1},
    Material.CUPBOARD: {Material.GLASS: 2, Material.PLANKS: 2, Material.PAINT: 2},
    Material.COUCH: {Material.TEXTILES: 3, Material.GLUE: 1, Material.DRILL: 2},

    Material.GRASS: {Material.SEEDS: 1, Material.SHOVEL: 1},
    Material.TREE_SAPLINGS: {Material.SEEDS: 2, Material.SHOVEL: 1},
    Material.GARDEN_FURNITURE: {Material.PLASTIC: 2, Material.TEXTILES: 1, Material.PLANKS: 1},
    Material.FIRE_PIT: {Material.BRICKS: 2, Material.CEMENT: 2, Material.SHOVEL: 1},
    Material.LAWN_MOWER: {Material.METAL: 3, Material.ELECTRICAL_COMPONENTS: 1, Material.PAINT: 1},
    Material.GARDEN_GNOMES: {Material.CEMENT: 2, Material.GLUE: 1},

    Material.DONUTS: {Material.SUGAR_AND_SPICES: 1, Material.FLOUR_BAG: 1},
    Material.GREEN_SMOOTHIE: {Material.VEGETABLES: 1, Material.FRUIT_AND_BERRIES: 1},
    Material.BREAD_ROLL: {Material.FLOUR_BAG: 2, Material.CREAM: 1},
    Material.CHERRY_CHEESECAKE: {Material.FLOUR_BAG: 1, Material.FRUIT_AND_BERRIES: 1, Material.CHEESE: 1},
    Material.FROZEN_YOGURT: {Material.SUGAR_AND_SPICES: 1, Material.FRUIT_AND_BERRIES: 1, Material.CREAM: 1},
    Material.COFFEE: {Material.SEEDS: 2, Material.SUGAR_AND_SPICES: 1, Material.CREAM: 1},

    Material.CAP: {Material.TEXTILES: 2, Material.MEASURING_TAPE: 1},
    Material.SHOES: {Material.PLASTIC: 1, Material.TEXTILES: 2, Material.GLUE: 1},
    Material.WATCH: {Material.PLASTIC: 2, Material.CHEMICALS: 1, Material.GLASS: 1},
    Material.BUSINESS_SUITS: {Material.TEXTILES: 3, Material.GLUE: 1, Material.MEASURING_TAPE: 1},
    Material.BACKPACK: {Material.PLASTIC: 2, Material.TEXTILES: 2, Material.MEASURING_TAPE: 1},

    Material.ICE_CREAM_SANDWICH: {Material.CREAM: 1, Material.BREAD_ROLL: 1},
    Material.PIZZA: {Material.FLOUR_BAG: 1, Material.CHEESE: 1, Material.BEEF: 1},
    Material.BURGERS: {Material.BEEF: 1, Material.BREAD_ROLL: 1, Material.BBQ_GRILL: 1},
    Material.CHEESE_FRIES: {Material.VEGETABLES: 1, Material.CHEESE: 1},
    Material.LEMONADE_BOTTLE: {Material.SUGAR_AND_SPICES: 2, Material.GLASS: 2, Material.FRUIT_AND_BERRIES: 1},
    Material.POPCORN: {Material.CORN: 2, Material.MICROWAVE_OVEN: 1},

    Material.BBQ_GRILL: {Material.METAL: 3, Material.COOKING_UTENSILS: 1},
    Material.REFRIGERATOR: {Material.PLASTIC: 2, Material.CHEMICALS: 2, Material.ELECTRICAL_COMPONENTS: 2},
    Material.LIGHTING_SYSTEM: {Material.CHEMICALS: 1, Material.GLASS: 1, Material.ELECTRICAL_COMPONENTS: 1},
    Material.TV: {Material.PLASTIC: 2, Material.GLASS: 2, Material.ELECTRICAL_COMPONENTS: 2},
    Material.MICROWAVE_OVEN: {Material.METAL: 4, Material.GLASS: 1, Material.ELECTRICAL_COMPONENTS: 1},


    Material.REUSABLE_BAG: {Material.RECYCLED_FABRIC: 2},
    Material.ECOLOGICAL_SHOES: {Material.RECYCLED_FABRIC: 2, Material.GLUE: 1, Material.MEASURING_TAPE: 1},
    Material.YOGA_MAT: {Material.RECYCLED_FABRIC: 3, Material.HOME_TEXTILES: 2, Material.PAINT: 1},

    Material.MOTOR_OIL: {Material.CRUDE_OIL: 2},
    Material.CAR_TIRE: {Material.CRUDE_OIL: 2, Material.GLUE: 1, Material.NAILS: 3},
    Material.ENGINE: {Material.ELECTRICAL_COMPONENTS: 1, Material.DRILL: 1, Material.NAILS: 3},

    Material.STRING: {Material.SILK: 2},
    Material.FAN: {Material.SILK: 1, Material.WOOD: 1, Material.GLUE: 2},
    Material.ROBE: {Material.SILK: 3, Material.PAINT: 2, Material.TEXTILES: 1},

    Material.COCONUT_OIL: {Material.COCONUT: 2},
    Material.FACE_CREAM: {Material.COCONUT_OIL: 2, Material.CHEMICALS: 2},
    Material.TROPICAL_DRINK: {Material.COCONUT: 2, Material.FRUIT_AND_BERRIES: 2, Material.SUGAR_AND_SPICES: 1},

    Material.CANNED_FISH: {Material.FISH: 1, Material.METAL: 1},
    Material.FISH_SOUP: {Material.FISH: 1, Material.VEGETABLES: 1, Material.COOKING_UTENSILS: 2},
    Material.SALMON_SANDWICH: {Material.FISH: 2, Material.BREAD_ROLL: 1},

    Material.TIRAMISU: {Material.SUGAR_AND_SPICES: 1, Material.VEGETABLES: 1, Material.CREAM: 1},
    Material.CHURROS: {Material.COOKING_UTENSILS: 1, Material.FLOUR_BAG: 2},
    Material.PROFITEROLE: {Material.DONUTS: 2, Material.BREAD_ROLL: 2, Material.CREAM: 1},

    Material.WOOL_SHIRT: {Material.TEXTILES: 4, Material.MEASURING_TAPE: 2, Material.PAINT: 2},
    Material.PICNIC_BASKET: {Material.FRUIT_AND_BERRIES: 4, Material.TEXTILES: 4, Material.GLUE: 2},
    Material.APPLE_JAM: {Material.SEEDS: 4, Material.GLASS: 2, Material.FLOUR_BAG: 4},

    Material.TENNIS_RACKET: {Material.MINERALS: 4, Material.HAMMER: 2},
    Material.SPORTS_DRINK: {Material.SUGAR_AND_SPICES: 2, Material.FRUIT_AND_BERRIES: 4},
    Material.FOOTBALL_SHOES: {Material.SHOES: 1, Material.CHEMICALS: 3},
    Material.PROTEIN_BAR: {Material.SUGAR_AND_SPICES: 2, Material.CHERRY_CHEESECAKE: 1},
    Material.PING_PONG_TABLE: {Material.WOOD: 4, Material.MINERALS: 4, Material.TABLES: 1},

    Material.WROUGHT_IRON: {Material.METAL: 4, Material.CHEMICALS: 2, Material.HAMMER: 2},
    Material.CARVED_WOOD: {Material.PLANKS: 5, Material.MEASURING_TAPE: 2, Material.DRILL: 2},
    Material.CHISELED_STONE: {Material.MINERALS: 6, Material.HAMMER: 2, Material.DRILL: 2},
    Material.TAPESTRY: {Material.TEXTILES: 4, Material.PAINT: 2, Material.GLUE: 2},

    Material.LETTER_BLOCKS: {Material.WOOD: 4, Material.MEASURING_TAPE: 1},
    Material.KITE: {Material.PLANKS: 2, Material.PAINT: 2, Material.HOME_TEXTILES: 2},
    Material.TEDDY_BEAR: {Material.PLASTIC: 2, Material.HOME_TEXTILES: 4},
    Material.GAME_CONSOLE: {Material.WOOD: 4, Material.MINERALS: 4, Material.TABLES: 1},
}