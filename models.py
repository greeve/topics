class Reference:
    
    def __init__(self):
        self.id = None
        self.label = None
        self.term = None
        
        # scripture, hymn, or conference addess
        self.category = None
        
        # Scripture reference fields
        self.volume = None
        self.book = None
        self.chapter = None
        self.verses = []
        
        # Hymn reference field
        self.number = None
        
        # Conference address fields
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
        self.description = None
        self.source = None
        self.related_terms = []
        self.references = []
    
    @classmethod
    def from_response(self, **kwargs):
        self.id = kwargs.get('id')
        self.label = kwargs.get('label')
        self.slug = kwargs.get('slug')
        self.description = kwargs.get('description')
        self.source = kwargs.get('source')
        self.related_terms = kwargs.get('related_terms')
        self.references = kwargs.get('references')


class Source:
    
    def __init__(self):
        self.id = None
        self.name = None
        self.url = None
        self.params = None

    @classmethod
    def from_response(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.url = kwargs.get('url')
        self.params = kwargs.get('params')
