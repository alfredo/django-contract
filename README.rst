Django Contract
===============

Usually the work carried on the APIs is done simultaneously on the consumers and the API, this require a contract between them to ensure each part adheres to the requirements: a contract.

APIs should start from the most important part, and the cheaper to make: The documentation.

The purpose of the Django app is to generate a mock API from the RAML documentation.

Installation
------------

Install the package.

Add a `RAML_FILE` setting in the settings file with the path to the documentation. E.g::

    RAML_FILE = os.path.join(BASE_DIR, 'api.raml')


Add the stub path for the `urls.py` file::

    urlpatterns = [
        url('^/v1/', include('django_contract.urls', namespace='docs_v1')),
    ]


TODO
----
- Generate forms to handle defined payloads.
- Validate fields using schema definition.
- Upload package to pypi.
