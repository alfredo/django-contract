from django_contract import views


def test_resource_path_is_converted_in_absolute_path():
    result = views._get_resource_path('books/abc123')
    assert result == '/books/abc123'


def test_clean_key_returns_string_without_curly_braces():
    result = views._clean_key('/books/add')
    assert result == '/books/add'


def test_key_with_curly_brackets_is_transformed_into_a_pattern():
    result = views._clean_key('/books/{book_id}')
    assert result == '/books/(?P<book_id>[-\w]+)'


def test_key_with_spaces_is_transformed_into_a_pattern():
    result = views._clean_key('/books/{ book_id }')
    assert result == '/books/(?P<book_id>[-\w]+)'


class ResourceDouble():

    def __init__(self, resources, name=''):
        self.name = name
        self.resources = resources


def _get_resource(resources, name=''):
    """Generate a resource double."""
    return ResourceDouble(resources, name)


def test_raml_urls_are_transformed_in_patterns():
    urls = {
        '/book': _get_resource({}),
        '/book/{id}': _get_resource({}),
    }
    result = views.get_raml_urls(urls)
    key_list = [p[0] for p in result]
    assert sorted(key_list) == sorted(['^/book$', '^/book/(?P<id>[-\\w]+)$'])


def test_nested_resources_are_transformed_in_patterns():
    urls = {
        '/book': _get_resource({
            '/{id}': _get_resource({})
        })
    }
    result = views.get_raml_urls(urls)
    key_list = [p[0] for p in result]
    assert sorted(key_list) == sorted(['^/book$', '^/book/(?P<id>[-\\w]+)$'])


def test_get_definition_finds_the_right_pattern():
    urls = {
        '/book': _get_resource({}, name='book'),
        '/book/{id}': _get_resource({}, name='book_id'),
    }
    result = views.get_definition('book/abc123', urls)
    assert isinstance(result, ResourceDouble)
    assert result.name == 'book_id'


def test_existing_method_definition_is_returned():
    result = views.get_method_definition('GET', {
        'get': {}
    })
    assert result == {}


def test_missing_method_definition_returns_none():
    result = views.get_method_definition('POST', {
        'get': {}
    })
    assert result == None


def test_existing_code_response_is_returned():
    result = views.get_code_response(200, {200: 'ok'})
    assert result == 'ok'


def test_missing_code_response_returns_none():
    result = views.get_code_response(400, {200: 'ok'})
    assert result == None
