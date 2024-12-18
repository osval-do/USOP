import importlib
import sys

class CachedClassUtil:
    """
    CachedClassUtil is a utility class that provides caching mechanisms for class instances and class objects.
    Class Attributes:
        _instance_cache (dict): A dictionary to cache instances of classes.
        _class_cache (dict): A dictionary to cache class objects.
    Class Methods:
        get_instance(class_path: str) -> object:
            Retrieves an instance of the specified class. If the instance is already cached, it returns the cached instance.
            Otherwise, it imports the module, creates an instance of the class, caches it, and returns the instance.
            Args:
                class_path (str): The full path of the class in the format 'module.submodule.ClassName'.
            Returns:
                object: An instance of the specified class.
        get_class(class_path: str) -> type:
            Retrieves the class object of the specified class. If the class object is already cached, it returns the cached class object.
            Otherwise, it imports the module, retrieves the class object, caches it, and returns the class object.
            Args:
                class_path (str): The full path of the class in the format 'module.submodule.ClassName'.
            Returns:
                type: The class object of the specified class.
    """
    _instance_cache = {}
    _class_cache = {}

    @classmethod
    def get_instance(cls, class_path):
        if class_path in cls._instance_cache:
            return cls._instance_cache[class_path]

        module_name, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        instance = class_()
        cls._instance_cache[class_path] = instance
        return instance
    
    @classmethod
    def get_class(cls, class_path):
        if class_path in cls._class_cache:
            return cls._class_cache[class_path]
        module_name, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        cls._class_cache[class_path] = class_
        return class_
        