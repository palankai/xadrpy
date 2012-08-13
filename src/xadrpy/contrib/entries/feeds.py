'''
Created on 2012.07.23.

@author: pcsaba
'''
from django.contrib.syndication.views import Feed

class ColumnEntriesFeed(Feed):
    
    def __init__(self, column):
        self.column = column

    def items(self):
        return self.column.get_entries().order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_excerpt()
    
    def title(self):
        return self.column.get_title()
    
    def link(self):
        return self.column.get_absolute_url()
    
    def description(self):
        return self.column.get_meta_description()
