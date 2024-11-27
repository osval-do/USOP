
class NodeAllocator(object):

    def allocate(self, service) -> str:
        raise NotImplementedError
    
    
    
class DefaultNodeAllocator():
    def allocate(self, service) -> str:
        return "localhost"