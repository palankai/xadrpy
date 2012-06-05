'''
Created on 2012.06.02.

@author: pcsaba
'''

class Application(object):
    '''
    ExtJS core application base class
    '''
    

    def __init__(self, application_js, title="", description=""):
        '''
        Construct application
        '''
        self.application_js = application_js
        self.title = title
        self.description = description

    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_application_js(self):
        return self.application_js