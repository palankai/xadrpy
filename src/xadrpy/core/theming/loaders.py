from django.template.loader import BaseLoader, get_template
from django.template.base import TemplateDoesNotExist
from libs import get_current_theme
from xadrpy.core.router.base import get_local_request

class Loader(BaseLoader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        theme = get_current_theme()
        if template_name.startswith("@"):
            layout_name = template_name[1:]
            layout_template = theme.get_layout_template(layout_name)
            return get_template(layout_template), None
        request = get_local_request()
        rewrite = theme.get_rewrite(request.theming_layout[1:], request.theming_skin)
        if template_name in rewrite:
            return get_template(rewrite.get(template_name)), None
        raise TemplateDoesNotExist("Layout does not exists")



