'''
Created on 2012.05.29.

@author: pcsaba
'''
import os
import shutil
from xadrpy import conf

CREATE_SKELETON_PATH = os.path.join(conf.SKELETONS_PATH, "create")


class CLIHandler(object):
    
    def __init__(self, parser):
        pass
    
    def __call__(self, args):
        self.handle(args)
        
    def handle(self, args):
        pass

class CreateHandler(CLIHandler):

    def __init__(self, parser):
        super(CreateHandler, self).__init__(parser)
        parser.add_argument('project_name', help='Project name')
    
    def handle(self, args):
        template_name = "web"
        os.system("django-admin.py startproject --template=%s %s" % (os.path.join(conf.SKELETONS_PATH,template_name,"project_template"),args.project_name))
        os.rename(args.project_name, "main")
        os.mkdir(os.path.join("main",args.project_name,"static","main","css","assets"))
        os.mkdir(os.path.join("main",args.project_name,"static","main","libs"))
        os.mkdir("public")
        os.mkdir("public/static")
        os.mkdir("public/media")
        os.mkdir("public/media/uploads")
        os.mkdir("bin")
        os.mkdir("applications")
        os.mkdir("doc")
        os.mkdir("local-resources")
        os.mkdir("local")
        os.mkdir("local/logs")
        os.mkdir("local/cache")
        os.mkdir("local/tmp")
        os.mkdir("local/indexes")
        os.system("git init")
        shutil.copyfile(os.path.join(conf.SKELETONS_PATH,template_name,"requirements.txt"), "requirements.txt")
        shutil.copyfile(os.path.join(conf.SKELETONS_PATH,template_name,".gitignore"), ".gitignore")
        shutil.copyfile(os.path.join(conf.SKELETONS_PATH,template_name,"robots.txt"), "public/robots.txt")
        shutil.copyfile(os.path.join(conf.SKELETONS_PATH,template_name,"crossdomain.xml"), "public/crossdomain.xml")
        shutil.copytree(os.path.join(conf.SKELETONS_PATH,template_name,"vendor"), "vendor")
        
    def _create_file(self, filename, content=""):
        open(filename,"w").write(content)
    
    def _copy_file(self, src, dst):
        pass 