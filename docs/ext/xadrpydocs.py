def setup(app):
    return 
    from sphinx.highlighting import lexers 
    from pygments.lexers.compiled import JavaLexer
    from pygments.filters import VisibleWhitespaceFilter 
    myLexer = JavaLexer()
    myLexer.add_filter(VisibleWhitespaceFilter(spaces=' ')) 
    app.add_lexer('python', myLexer);
