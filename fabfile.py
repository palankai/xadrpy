from fabric.api import local, prompt
import os

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
    local("rm -rf sandbox/local")

def sandbox_run():
    """
    Run sandbox developer server
    """
    if not os.path.exists("sandbox/local"):
        sandbox_setup()
    local("python sandbox/manage.py runserver")

def docs_cleanup():
    local("rm -rf docs/build/*")

def setup_cleanup():
    local("rm -rf dist")
    local("rm -rf build")
    remove_egg_info = prompt('Remove *.egg-info to (y/n):', default="n", validate=r'^[yn]$')
    if remove_egg_info == "y":
        local("rm -rf `find . -name '*.egg-info'`")

def cleanup():
    local("python setup.py clean")
    local("rm `find . -name '*.pyc'`")
    sandbox_cleanup()
    docs_cleanup()
    setup_cleanup()
    
        