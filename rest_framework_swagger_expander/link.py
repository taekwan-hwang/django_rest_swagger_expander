from coreapi import Link

class CustomLink(Link):
    def __init__(self, url=None, action=None, encoding=None, transform=None, title=None, description=None, fields=None, responses_docs=None):
        Link.__init__(self, url=url, action=action, encoding=encoding, transform=transform, title=title, description=description, fields=fields)
        self._responses_docs=responses_docs

    @property
    def responses_docs(self):
        return self._responses_docs
