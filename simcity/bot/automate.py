from simcity.automation.commercial_buildings.building_supplies_store import BuildingSupplyStore
from simcity.automation.raw_material.raw_materials import RawMaterials

# Function to calculate max possible production
def calculate_production(available_materials):
    # Dictionary to store maximum production possible for each item
    max_production = {}

    # Iterate through each production item and its recipe
    for item in BuildingSupplyStore:
        recipe = item.recipe  # Access the recipe directly from the enum instance
        # Find the limiting raw material for each production item
        possible_quantity = float('inf')  # Start with a large number

        # Check for each raw material in the recipe
        for material, required_qty in recipe.items():
            # Calculate how many of this item can be produced given available material
            if material in available_materials and available_materials[material] >= required_qty:
                possible_quantity = min(possible_quantity, available_materials[material] // required_qty)
            else:
                possible_quantity = 0  # If a material is missing or insufficient, production is 0
                break

        # Store the maximum possible quantity for this item
        max_production[item.label] = possible_quantity

    return max_production


# Example input: available quantities of raw materials
available_materials = {
    RawMaterials.METAL: 10,
    RawMaterials.WOOD: 10,
    RawMaterials.PLASTIC: 3,
    RawMaterials.MINERALS: 6,
    RawMaterials.CHEMICALS: 3
}

# Call the function to calculate production
max_possible_production = calculate_production(available_materials)

# Output the result
for item, quantity in max_possible_production.items():
    print(f"You can produce {quantity} units of {item}.")
