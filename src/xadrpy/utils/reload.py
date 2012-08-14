import os
import logging
logger = logging.getLogger("xadrpy.utils.reload") 

def reload_wsgi(request):
    if 'mod_wsgi.process_group' in request.environ and \
        request.environ.get('mod_wsgi.process_group', None) and \
        'SCRIPT_FILENAME' in request.environ and \
        int(request.environ.get('mod_wsgi.script_reloading', '0')):
            try:
                os.utime(request.environ.get('SCRIPT_FILENAME'), None)
            except OSError:
                pass
    # Try auto-reloading via uwsgi daemon reload mechanism
    try:
        import uwsgi #@UnresolvedImport
        # pretty easy right?
        uwsgi.reload()
    except:
        # we may not be running under uwsgi :P
        pass
