from django.core import paginator
from django.utils.translation import ugettext as _
import sys

class Paginator(paginator.Paginator):
    pass

class Paginated(object):
    
    def __init__(self, object_list, per_page, extra_pages=5, orphans=0, per_page_cookie=None, request=None, page_url=None, sizes=[], required=True, show_last_page_index=False, first_page=None, sizes_title=_("Per page")):
        self.object_list = object_list
        self.per_page = int(per_page)
        if not self.per_page:
            self.per_page = sys.maxint
        self.extra_pages = extra_pages
        self.paginator = Paginator(object_list, self.per_page, orphans=orphans)
        self.page_url = page_url
        if not self.page_url:
            self.page_url = u"?page=%(index)s&size=%(size)s"
        self.request = request
        self.page = None
        self.sizes = sizes
        self.sizes_title = sizes_title
        self.first_page = first_page
        self.required = required

        if per_page_cookie and isinstance(per_page_cookie, basestring):
            self.per_page_cookie = {'key': per_page_cookie}
        elif per_page_cookie and isinstance(per_page_cookie, dict):
            self.per_page_cookie = per_page_cookie
        else:
            self.per_page_cookie = None
            
        self.show_last_page_index = show_last_page_index

    def get_per_page(self):
        return self.per_page

    def set_first_page(self, first_page):
        self.first_page = first_page

    def set_sizes(self, sizes):
        self.sizes = sizes
    
    def get_sizes(self):
        return [(title, self.get_page_url(1,size)) for size, title in self.sizes]

    def get_min_page_size(self):
        min_page_size = self.per_page
        for size, title in self.sizes:
            if size>0 and size<min_page_size:
                min_page_size = size
        return min_page_size
    
    @property
    def need_pager(self):
        if not self.required and self.get_min_page_size()>=self.paginator.count:
            return False
        return True
    
    def set_page(self, index):
        self.index = int(index)
        self.page = self.paginator.page(self.index)
    
    def set_page_url(self, page_url):
        self.page_url = page_url
    
    def get_page_url(self, index, per_page=None):
        if per_page==None: per_page = self.per_page
        if isinstance(self.page_url, basestring):
            return self.page_url % {"index": index, "size": per_page}
        if callable(self.page_url):
            return self.page_url(index, per_page)
        return "#"
    
    def get_first_page_url(self):
        if self.first_page:
            return self.first_page 
        return self.get_page_url(1)

    def get_last_page_url(self):
        return self.get_page_url(self.paginator.num_pages)

    def get_previous_page_url(self):
        return self.get_page_url(self.page.previous_page_number())
    
    def get_next_page_url(self):
        return self.get_page_url(self.page.next_page_number())
    
    def has_previous(self):
        return self.page.has_previous()

    def has_next(self):
        return self.page.has_next()
    
    def num_pages(self):
        return self.paginator.num_pages
    
    def get_pages(self):
        pages = []
        for index in self.paginator.page_range:
            pages.append((index, self.get_page_url(index)))
        return pages

    def store_per_page_cookie(self, response):
        if self.per_page_cookie and self.request:
            if self.request.COOKIES.get(self.per_page_cookie.get("key"))!=self.per_page:
                response.set_cookie(value=self.per_page, **self.per_page_cookie)
    
    def __iter__(self):
        return iter(self.paginator.page(self.index))

from django.core.paginator import InvalidPage, EmptyPage
from django.template.loader import render_to_string
import urllib
from django.http import QueryDict

class ResultList(list):
    pass

def paginatex(request, object_list, page_size):
    extra_pages=5
    try:
        size=int(request.GET.get('size', request.COOKIES.get('page_size', '20')))
    except ValueError:
        size=20
    if size==0:
        size=99999
    paginator=Paginator(object_list, size)
    query=QueryDict("", True)
    query.update(request.GET)
    if 'page' in query: del query['page']
    if 'size' in query: del query['size']
    for i in query: query[i] = urllib.quote(query[i].encode('utf-8'))
    qs=urllib.urlencode(query)
    qs="?%s&" % urllib.unquote(qs) if qs else "?"

    # Make sure page request is an int. If not, deliver first page.                                                                                                                                                                                                              
    try:
        page_num=int(request.GET.get('page', '1'))
    except ValueError:
        page_num=1

    # If page request (9999) is out of range, deliver last page of results.                                                                                                                                                                                                      
    try:
        page=paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page=paginator.page(paginator.num_pages)
    page.num_pages=paginator.num_pages
    page_index=page_num-1
    last_page_index=paginator.num_pages-1

    page.prev_pages=[]
    page.next_pages=[]
    page.has_more_prev_pages=False
    page.has_more_next_pages=False


    if page_index==0:
        page.next_pages=paginator.page_range[1:extra_pages+1]
    if page_index>0:
        page.next_pages=paginator.page_range[page_index+1:page_index+extra_pages+1]
    page.has_more_next_pages=page_index+extra_pages<page.num_pages-2

    if page_index==last_page_index:
        start=page_index-extra_pages
        if start<0: start=0
        page.prev_pages=paginator.page_range[start:page_index]
    if page_index<last_page_index:
        start=page_index-extra_pages
        if start<0: start=0
        page.prev_pages=paginator.page_range[start:page_index]
    page.has_more_prev_pages=page_index-extra_pages>1
    page.qs=qs
#    if page_index and page_index < extra_pages:
#        setattr( page, 'prev_pages', paginator.page_range[0:page_index] )
#        setattr( page, 'next_pages', paginator.page_range[page_num:page_num + extra_pages] )
#
#    if page_index >= extra_pages and page_index <= page_num - extra_pages - 1: # ha valahol kozepen van                                                                                                                                                                          
#        setattr( page, 'prev_pages', paginator.page_range[page_num - extra_pages:page_num - 1] )
#        setattr( page, 'next_pages', paginator.page_range[page_num:page_num + extra_pages - 1] )

    #setattr( page, 'next_pages', paginator.page_range[page_num:page_num + extra_pages] )

    results=ResultList(page.object_list)
    results.paginator_page=page

    return results

def paginator(request_context, page, template="common/paginator.html"):
    if not hasattr(page, "paginator_page"): return ""
    if page.paginator_page.paginator.count < 6: return ""
    #if page.paginator_page.num_pages<2: return ""
    query=dict(request_context['request'].GET)
    context={
        'paginator': page.paginator_page,
        'qs': page.paginator_page.qs
    }
    return render_to_string("common/paginator.html", context, request_context)
