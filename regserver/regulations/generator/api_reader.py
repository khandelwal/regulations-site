from django.core.cache import get_cache
from regulations.generator import api_client


class ApiCache(object):
    """ Interface with the cache. """
    def __init__(self):
        self.cache = get_cache('api_cache')

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache.set(key, value)

    def generate_key(self, cache_key_elements):
        return '-'.join(cache_key_elements)


class ApiReader(object):
    """ Access the regulations API. Either hit the cache, or if there's a miss,
    hit the API instead and cache the results. """

    def __init__(self):
        self.cache = ApiCache()
        self.client = api_client.ApiClient()

    def regversions(self, label):
        return self._get(
            ['regversions', label],
            'regulation/%s' % label)

    def add_regulation_tree(self, reg_tree, version):
        """ Add keys for all labels of the regulation. """

        tree_id = '-'.join(reg_tree['label'])
        cache_key = self.cache.generate_key(['regulation', tree_id, version])
        self.cache.set(cache_key, reg_tree)

        for child in reg_tree['children']:
            self.add_regulation_tree(child, version)

    def regulation(self, label, version):
        cache_key = self.cache.generate_key(['regulation', label, version])
        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached
        else:
            regulation = self.client.get('regulation/%s/%s' % (label, version))
            #Add the tree to the cache
            if regulation:
                self.add_regulation_tree(regulation, version)
                return regulation

    def _get(self, cache_key_elements, api_suffix, api_params={}):
        """ Retrieve from the cache whenever possible, or get from the API """

        cache_key = self.cache.generate_key(cache_key_elements)
        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached
        else:
            element = self.client.get(api_suffix, api_params)
            self.cache.set(cache_key, element)
            return element

    def layer(self, layer_name, label, version):
        regulation_part = label.split('-')[0]
        return self._get(
            ['layer', layer_name, regulation_part, version],
            'layer/%s/%s/%s' % (layer_name, regulation_part, version))

    def diff(self, label, older, newer):
        """ End point for diffs. """
        return self._get(
            ['diff', label, older, newer],
            "diff/%s/%s/%s" % (label, older, newer))

    def notices(self, part=None):
        """ End point for notice searching. Right now just a list. """
        if part:
            return self._get(
                ['notices', part],
                'notice',
                {'part': part})
        else:
            return self._get("notice")

    def notice(self, document_number):
        """End point for retrieving a single notice."""
        return self._get("notice/%s" % document_number)

    def _get(self, suffix, params=None):
        """Actually make the GET request. Assume the result is JSON. Right
        now, there is no error handling"""
        if not params:
            params = {}
        if self.base_url.startswith('http'):    # API
            r = requests.get(self.base_url + suffix, params=params)
            if r:
                return r.json()
            else:
                return None
            #return requests.get(self.base_url + suffix, params=params).json()
        else:   # file system
            if os.path.isdir(self.base_url + suffix):
                suffix = suffix + "/index.html"
            f = open(self.base_url + suffix)
            content = f.read()
            f.close()
            return json.loads(content)
            return self._get(
                ['notices'],
                'notices')

    def notice(self, fr_document_number):
        """ End point for retrieving a single notice. """
        return self._get(
            ['notice', fr_document_number],
            'notice/%s' % fr_document_number)

    def search(self, query, version=None):
        """Search via the API. Never cache these (that's the duty of the search
        index)"""
        if version:
            return self.client.get('search', {'q': query, 'version': version})
        return self.client.get('search', {'q': query})
