HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'note.elasticsearch2_ik_backend.Elasticsearch2IkSearchEngine',
        'URL': '',
        'INDEX_NAME': 'note_k8s',
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_CUSTOM_HIGHLIGHTER = 'blog.utils.Highlighter'
