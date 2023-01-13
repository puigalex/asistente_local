import yaml

def read_file(filename, filetype):
    '''
    Funcion para lectura de distintos tipos de archivos.

    Parameters:
        filename (str): Nombre del archivo a leer
        filetype (str): Extension del archivo
    '''
    
    with open("{}.{}".format(filename, filetype), "r") as file:
        try:
            config_data = (yaml.safe_load(file))
        except yaml.YAMLError as exc:
            print(exc)
        return(config_data)

def write_file(data, filename, filetype):
    with open("{}.{}".format(filename, filetype), "a") as file:
        file.write(data)