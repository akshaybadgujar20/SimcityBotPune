from simcity.bot.enums.material import Material

def get_materials():
    return ['STORAGE_BARS', 'STORAGE_LOCK', 'STORAGE_CAMERA']

def get_material_properties():
    return {
        Material.STORAGE_BARS: 1,
        Material.STORAGE_LOCK: 2,
        Material.STORAGE_CAMERA: 3,
    }

# def get_materials():
#     return ['NAILS']
#
# def get_material_properties():
#     return {
#         Material.NAILS: 1
#     }