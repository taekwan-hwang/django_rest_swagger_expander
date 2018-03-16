from openapi_codec import encode
from . import schema

def _custom_get_responses(link):
    if hasattr(link, 'responses_docs') and link.responses_docs:
        return link.responses_docs
    else: # encode._get_responses
        template = {'description': ''}
        if link.action.lower() == 'post':
            return {'201': template}
        if link.action.lower() == 'delete':
            return {'204': template}
        return {'200': template}

encode._get_responses = _custom_get_responses