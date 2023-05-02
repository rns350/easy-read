# easy-reed
A Python library for easily configuring applications across multiple projects

## The easy_reed.config_object.config object
the core of the easy_reed library is in the easy_reed.config_object.config object.  This class provides an interface to define new configuration fields that an end user can manipulate through a .ini file.  While this functionality exists within the Python library in a module called ConfigParser (Which this library uses), the unique problem that it aims to solve is to provide a single location that different packages can use to define their own configuration, across multiple environments.  To avoid naming conflicts, this libarary implements a NameSpace concept for defining config fields.

For the most part, developers should not instantiate a new Config object.  Instead, this library intializes a Config object to be used by any package within its init file.  This can be imported like so

```
from easy_reed import config
```
Then, a developer can define fields for their library under an easy_reed.namespace.NameSpace object and add them to the Config object.  the Config object acts like a dictionary of dictionaries.  If a developer wishes to access "field1" of namespace "example", they would write
```
config["example"]["field1"]
```
in the .ini file, the final config key will be the namespace name, followed by a '.' character, followed by the field name.
```
[DEFAULT]
example.field1 = "Testing"
```
the .ini file is read once at module startup, but the final config field is not read into the Config Object itself until it is added via a namespace.  This is so that developers can define the expected type for the value and have the Config automatically convert the string into the final type when the NameSpace is added.

## Defining new fields under a project namespace

To define config fields for a library, a developer must define a Namespace
```
from easy_reed.namespace import NameSpace

project_namespace = NameSpace("project")
```
Once that namespace is defined, a developer can then add however many fields they want through the NameSpace.add_entry method.
```
project_namespace.add_entry("field1", str, "example")
```
add_entry takes three parameters:
1. field_name - a string representing the config field key
2. typ - a python type specifying what type to read the field as
3. default - the default value to use if the end_user does not include the field in the .ini file

By default, the config object is able to read in these types
- string
- int
- float
- bool
- list

New type handlers can be added through the Config.add_handler method.  This allows it to parse strings into new types.

Any number of new entries can be added in this way, though all field_names must be unique.
```
project_namespace.add_entry("field2", int, 0)
project_namespace.add_entry("field3", float, 5.5)
project_namespace.add_entry("field4", bool, True)
project_namespace.add_entry("field5", list, ["one", "two", "three"])
```
Once all entries have been defined, the NameSpace can be added to the config via the add_namespace method
```
from easy_reed import config
config.add_namespace(project_namespace)
```
Although the fields are read in by a ConfigParser at module startup, they are not made accessible through the config object until this registration has occured.  This allows the library to convert each field to the correct type underneath the hood with no developer intervention outside of defining the expected type.

## Adding new type parsers
lets look at a class called 'Person'
```
class Person():
    def __init__(self, name: str, age: int):
        self.name: str = name
        self.age: int = age

    def get_name(self) -> str:
        return self.name

    def get_age(self) -> int:
        return self.age
```
Let's say we want to be able to represent a Person object as a string in the config dictionary.  A person consists of a name and an age, so we could represent that with "{name}:{age}" in a string.  Let's define a function that can take a string and parse it to a Person when it is in this format.
```
    def parse_person(person_string: str):
        # the argument must be a string
        if not isinstance(person_string, str):
            raise TypeError(msg)

        # There should be exactly 1 ':' character in the string
        if person_string.count(':') != 1:
            raise ValueError(msg)
        
        parse = person_string.split(':')

        # After splitting by ':', the second element should be readable as int
        if not parse[1].isdigit():
            raise ValueError(msg)
        
        return Person(parse[0], int(parse[1]))
```
Now we can pass this function to the Config object as a new type handler for the Person type.

```
config.add_handler(Person, parse_person)
```
Then we can add it to the NameSpace before passing it to the Config.
```
project_namespace.add_entry("guts", Person, Person("John", 23))
```
Now we could add a person into the .ini file.
```
[DEFAULT]
example.guts = guts:28
```
once the namespace is added, this Person object can be accessed with the following.
```
config["example"]["guts"]
```

## Sections
Since this library uses ConfigParser to read the .ini file, it uses the same format.  This means you can define multiple 'sections'.  This library treats each section like a different environment.
```
[DEFAULT]
field1=hello
field2=yes
field3=0

[LOCAL]
field2=no
field3=1

[QA]
field3=2
```
The section that will be used by the Config object is determined by the __APP_ENVIRONMENT__ environment variable.  If a key is missing from a section but is available under DEFAULT, then the DEFAULT value will be used.