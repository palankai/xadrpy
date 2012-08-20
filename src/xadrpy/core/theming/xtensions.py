import conf

if not conf.SELECTED_THEME:
    from libs import get_theme_store
    theme_store = get_theme_store()
    
    theme_store.register("main", {'static_path': "main",'template_path': "main",'base': "base.html"})

