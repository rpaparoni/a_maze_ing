from typing import Dict, List


def parse_config(filename: str) -> Dict[str, str]:
    """
    Parses the configuration file and returns a dictionary with the settings.
    Handles errors using try/except blocks.
    """
    config: Dict[str, str] = {}
    
    try:
        config_file = open(filename, "r")
        line: str = config_file.readline()
        
        while line != "":
            clean_line: str = line.strip()
            
            # Ignoramos comentarios y lineas vacias
            if clean_line != "" and clean_line[0] != "#":
                parts: List[str] = clean_line.split("=")
                
                if len(parts) == 2:
                    key: str = parts[0].strip()
                    value: str = parts[1].strip()
                    config[key] = value
                    
            line = config_file.readline()
            
        config_file.close()
    except Exception:
        print("Error: Could not read or find the config file.")
        return {}
        
    try:
        # Comprobamos que el archivo tenga TODO lo necesario
        required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE"]
        i: int = 0
        while i < len(required):
            if required[i] not in config:
                raise ValueError(f"Missing required key: {required[i]}")
            i += 1

        width: int = int(config["WIDTH"])
        height: int = int(config["HEIGHT"])
        
        exits: List[str] = config["EXIT"].split(',')
        entries: List[str] = config["ENTRY"].split(',')
        
        if len(exits) != 2 or len(entries) != 2:
            raise ValueError("Invalid ENTRY or EXIT format")
            
        exit_c: int = int(exits[0])
        exit_r: int = int(exits[1])
        entry_c: int = int(entries[0])
        entry_r: int = int(entries[1])
        
        # GPS de seguridad
        if exit_c >= width or exit_r >= height:
            raise ValueError("Exit coordinates are out of bounds")
        if entry_c >= width or entry_r >= height:
            raise ValueError("Entry coordinates are out of bounds")
            
        return config

    except Exception as e:
        print(f"Error: Invalid configuration data. ({str(e)})")
        return {}
