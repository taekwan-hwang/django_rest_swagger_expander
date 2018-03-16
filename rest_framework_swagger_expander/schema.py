from rest_framework.schemas import SchemaGenerator
from urllib.parse import urljoin
from .link import CustomLink
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import yaml
import coreapi


class CustomSchemaGenerator(SchemaGenerator):
    def get_link(self, path, method, view):
        fields = self.get_path_fields(path, method, view)
        yaml_doc = None
        if view and view.__doc__:
            try:
                yaml_doc = yaml.load(view.__doc__)
            except:
                yaml_doc = None

        responses = None

        if yaml_doc and type(yaml_doc) != str:
            _method_desc = yaml_doc.get('description', '')
            fields += self._get_parameters(yaml_doc)
            responses = self._get_responses(yaml_doc)

        else:
            _method_desc = view.__doc__ if view and view.__doc__ else ''
            fields += self.get_serializer_fields(path, method, view)

        fields += self.get_pagination_fields(path, method, view)
        fields += self.get_filter_fields(path, method, view)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, view)
        else:
            encoding = None

        if self.url and path.startswith('/'):
            path = path[1:]

        link = CustomLink(
            url=urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=_method_desc,
            responses_docs=responses if responses else None
        )
        return link

    def _get_parameters(self, yaml_doc):
        params = yaml_doc.get('parameters', [])
        fields = []
        for i in params:
            _name = i.get('name')
            _desc = i.get('description', '')
            _required = i.get('required', False)
            _type = i.get('type', 'string')
            _location = i.get('location', 'form')
            field = coreapi.Field(
                name=_name,
                location=_location,
                required=_required,
                description=_desc,
                type=_type,
            )
            fields.append(field)
        return fields

    def _get_responses(self, yaml_doc):
        responses = yaml_doc.get('responses')
        return responses



def get_swagger_view(title=None, url=None):
    """
    Returns schema view which renders Swagger/OpenAPI
    """

    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            CoreJSONRenderer,
            OpenAPIRenderer,
            SwaggerUIRenderer
        ]

        def get(self, request):
            generator = CustomSchemaGenerator(title=title, url=url)  # this is altered line
            schema = generator.get_schema(request=request)
            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema   Document'
                )
            return Response(schema)
    return SwaggerSchemaView.as_view()