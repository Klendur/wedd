def lang(request):
    lang = request.session.get('lang', 'et')
    return {'lang': lang}