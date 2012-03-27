class PrettyFloat(float):
    def __repr__(self):
        repr = ('%.6f' % self).rstrip("0")
        if repr.endswith("."):
            repr+="0"
        return repr
