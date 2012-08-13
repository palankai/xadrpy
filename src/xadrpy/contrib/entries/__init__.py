from xadrpy.management.libs import SubCommand
from xadrpy.utils.jsonlib import JSONEncoder

class EntriesCommands(SubCommand):
    
    def register(self):
        _export_all = self.command.add_subcommand(self.export_all, "entries.export.all", help="Export all content")
    
    def export_all(self, **kwargs):
        result = {
            "columns": self._get_columns(),
            "categories": [],
            "entries": []
        }
        encoder = JSONEncoder()
        self.stdout.write(encoder.encode(result)+"\n")
    
    def _get_columns(self):
        from models import Column
        columns = []
        for column in Column.objects.all():
            columns.append(column.to_dict())
        return columns
            