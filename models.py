class Reference:
    
    def __init__(self):
        self.id = None
        self.label = None
        self.term = None


class ScriptureReference(Reference):
    
    def __init__(self):
        super().__init__()
        self.volume = None
        self.book = None
        self.chapter = None
        self.verses = []


class HymnReference(Reference):
    
    def __init__(self):
        super().__init__()
        self.number = None


class ConferenceReference(Reference):
    
    def __init__(self):
        super().__init__()
        self.year = None
        self.month = None
        self.session = None
        self.speaker = None
        self.title = None


class Term:
    
    def __init__(self):
        self.id = None
        self.label = None
        self.slug = None
        self.url = None
        self.description = None
        self.source = None
        self.related_terms = []
    
    @classmethod
    def from_response(self, **kwargs):
        self.id = kwargs.get('id')
        self.label = kwargs.get('label')
        self.slug = kwargs.get('slug')
        self.url = kwargs.get('url')
        self.description = kwargs.get('description')
        self.source = kwargs.get('source')
        self.related_terms = kwargs.get('related_terms')


class Source:
    
    def __init__(self):
        self.id = None
        self.slug = None
        self.name = None
        self.url = None
        self.params = None

    @classmethod
    def from_response(self, **kwargs):
        self.id = kwargs.get('id')
        self.slug = kwargs.get('slug')
        self.name = kwargs.get('name')
        self.url = kwargs.get('url')
        self.params = kwargs.get('params')
