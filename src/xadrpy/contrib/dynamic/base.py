
class Attributes(object):
    def __init__(self, holder):
        self.holder = holder
    
    def __getitem__(self, key):
        return self.holder.get_attribute(key).get_value()

    def __setitem__(self, key, value):
        self.holder.get_attribute(key).set_value(value)

    