'''
Created on 2012.08.02.

@author: pcsaba
'''
from django.core.management.base import BaseCommand
import argparse
from django.core.management import call_command

class MyHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog,
                 indent_increment=2,
                 max_help_position=24,
                 width=None):
        super(MyHelpFormatter, self).__init__(prog, indent_increment=2, max_help_position=40, width=120)


class Command(BaseCommand):
    
    def run_from_argv(self, argv):
        #print argv
        
        parser = argparse.ArgumentParser(description='xadrpy\n console tools',
                                         prog="manage.py xcmd",formatter_class=MyHelpFormatter)
        
        subparsers = parser.add_subparsers(title="Subcommands", description=None, metavar="subcommand", dest='subcommand')
        setup_parser = subparsers.add_parser('router.test.list', help='router commands')
        setup_parser = subparsers.add_parser('themes', help='themes commands')
        setup_parser = subparsers.add_parser('api', help='api commands')
        setup_parser = subparsers.add_parser('worker.start', help='Start worker server as daemon')
        setup_parser = subparsers.add_parser('worker.stop', help='Stop worker server')
        setup_parser = subparsers.add_parser('worker.status', help='Print worker status')
        setup_parser = subparsers.add_parser('worker.standalone', help='Start worker in standalone mode (not daemonized)')

        #subparsers = setup_parser.add_subparsers(help='other commands help')
        #setup_parser = subparsers.add_parser('create2', help='create django-xadrpy project')
        
        args = parser.parse_args(argv[2:])
        #call_command("shell")
        #args.handler(args)
        
