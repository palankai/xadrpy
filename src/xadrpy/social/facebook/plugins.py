'''
Created on 2012.07.29.

@author: pcsaba
'''
from xadrpy.templates.libs import Plugin

class FacebookActivityPlugin(Plugin):
    alias = "x-facebook_activity"
    template = "xadrpy/social/facebook/plugins/facebook_activity.html"
    
    def render(self, context, width=200, height=300, router=None):
        context.update({"width": width, "height": height})
        return self.get_template().render(context)
            
class FacebookCommentsPlugin(Plugin):
    alias = "x-facebook-comments"
    template = "xadrpy/social/facebook/plugins/facebook_comments.html"
    
    def render(self, context, width="650", num_posts=5, router=None):
        context.update({"width": width, "num_posts": num_posts})
        return self.get_template().render(context)
            
