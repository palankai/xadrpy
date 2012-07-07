class Native(str):
    def __repr__(self):
        return "x"
    
    def __str__(self):
        return "y"
    
    def __unicode__(self):
        return u"z"
    
class PrettyFloat(float):
    def __repr__(self):
        repr = ('%.6f' % self).rstrip("0")
        if repr.endswith("."):
            repr+="0"
        return repr
