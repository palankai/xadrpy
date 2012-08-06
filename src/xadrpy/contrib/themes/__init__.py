from xadrpy.management.libs import SubCommand

class ThemesCommands(SubCommand):
    
    def register(self):
        _collect = self.command.add_subcommand(self.handle, "themes.collect", help="Collects themes")
    
    def print_header(self):
        self.command.print_header()
        self.stdout.write("Themes functions\n")
        self.stdout.write("\n")
    
    def handle(self, **kwargs):
        self.print_header()
        self.stdout.write("Collecting themes...\n")
