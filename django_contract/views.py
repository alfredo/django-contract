import re

from django.conf import settings
from django.http import Http404, HttpResponseForbidden, HttpResponse
from pyraml import parser


def _load_all_definitions(definition_path):
    if not definition_path:
        raise ValueError('Missing setting value" `RAML_PATH`.')
    return parser.load(definition_path)


def _get_resource_path(path):
    """Transform the path into a URL."""
    return u'/%s' % path


def _clean_key(key):
    """Transforms the key in a python regex when appropriate."""
    # TODO handle multiple keys and duplicate names:
    pattern = re.search(r'{(?P<name>[-\w\s]+)}', key)
    if pattern:
        name = pattern.group('name')
        key = key.replace('{%s}' % name, '(?P<%s>[-\w]+)' % name.strip())
    return key


def get_raml_urls(resources, prefix=''):
    """Transform the resources into a list of URLs.

    Resources URL come nested, by having them flat they can be regexed
    and the resource can be easily found."""
    url_list = []
    for key, value in resources.items():
        full_key = '%s%s' % (prefix, _clean_key(key))
        url_list.append((r'^%s$' % full_key, value))
        if value.resources:
            url_list += get_raml_urls(value.resources, prefix=full_key)
    return url_list


def get_definition(path, resources):
    path = _get_resource_path(path)
    raml_urls = get_raml_urls(resources)
    for pattern, value in raml_urls:
        print pattern, path
        if re.search(pattern, path):
            return value
    return None


def get_method_definition(method, definition):
    method_list = [m.upper() for m in definition.keys()]
    if method not in method_list:
        return None
    method_definition = definition[method.lower()]
    return method_definition


def get_code_response(status_code, definition):
    if definition and (status_code in definition):
        return definition[status_code]
    return None


def get_content_type_response(response, content_type='application/json'):
    if content_type in response:
        return response[content_type].example
    return None


def serve(request, path, definition_path=None, content_type='application/json'):
    """View that process the given request based in the RAML definitions."""
    if not definition_path:
        # Use a setting value if path is not provided:
        definition_path = settings.RAML_FILE
    all_definitions = _load_all_definitions(definition_path)
    definition = get_definition(path, all_definitions.resources)
    if not definition:
        raise Http404('Resource not found: `%s`' % path)
    method_definition = get_method_definition(request.method, definition.methods)
    if not method_definition:
        return HttpResponseForbidden('Invalid method: `%s`' % request.method)
    # TODO: Sort out these assumptions:
    response = get_code_response(200, method_definition.responses)
    if not response:
        return HttpResponseForbidden('Response not found: `200`')
    response_body = get_content_type_response(response.body, content_type)
    if not response_body:
        return HttpResponseForbidden(
            'Response not found for: `%s`' % content_type)
    return HttpResponse(response_body, content_type)
