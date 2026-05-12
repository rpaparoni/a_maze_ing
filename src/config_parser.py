from typing import Dict


def parse_config(filename: str) -> Dict[str, str]:
    # Diccionario donde guardaremos los datos limpios
    config: Dict[str, str] = {}
    
    try:
        config_file = open(filename, "r")
        line = config_file.readline()
        
        # Usamos while para leer línea por línea hasta el final
        while line != "":
            clean_line = line.strip()
            
            # Ignoramos líneas vacías o que empiezan por '#' (comentarios)
            if clean_line != "" and clean_line[0] != "#":
                parts = clean_line.split("=")
                
                # Solo procesamos si hay una clave y un valor exactos
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    config[key] = value
            
            # Avanzamos a la siguiente línea
            line = config_file.readline()
            
        config_file.close()
    except FileNotFoundError:
        print("Error: Config file not found.")
        
    return config
