from configparser import ConfigParser

parser = ConfigParser()
print(dir(parser))

a_list = "[1, 2, 3]"

def list_converter(element: str):
    if type(element) != str:
        print("error")
    
    value = element.strip()
    if value[0] != "[" or value[-1] != "]":
        print("error")

    my_list = value[1:-1].split(',')
    for index, value in enumerate(my_list):
        my_list[index] = value.strip()

    print(my_list)

list_converter(a_list)

parser._converters['list'] = list_converter
print(dir(parser))