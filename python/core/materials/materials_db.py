from .materials import *

def select_material(material:str) -> Material:
    """
    Select a material from the materials database.
    
    Args:
        material (str): The name of the material to select.
        
    Returns:
        str: The selected material.
    """
    match material:
        case "S235":
            return S235()
        case "S275":
            return S275()
        case "S355":
            return S355()
        case "S450":
            return S450()
        
        case _:
            raise ValueError(f"Material {material} not found in the database.")
    