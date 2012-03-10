from fabric.api import local

def sandbox_setup():
    """
    Basic local setup for sandbox (remove old local files!)
    
    - Create necessarry local folders
    - Create sandbox database
    """
    sandbox_cleanup()
    local("mkdir -p sandbox/local/cache")
    local("mkdir -p sandbox/local/logs")
    local("mkdir -p sandbox/local/media")
    local("mkdir -p sandbox/local/static")
    local("python sandbox/manage.py syncdb")

def sandbox_cleanup():
    """
    Clean sandbox directories
    """
    local("rmdir -p --ignore-fail-on-non-empty sandbox/local")