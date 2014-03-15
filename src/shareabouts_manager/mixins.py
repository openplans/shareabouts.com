import json
from django.http import HttpResponse
from django.views.generic import View
from rest_framework.utils.encoders import JSONEncoder


class ValidateInputView (View):
    """
    A different take on django.views.generic.ProcessFormView that will take
    any kind of validator that has a similar interface to Django's forms.
    """
    validator_class = None

    def get_validator_class(self):
        return self.validator_class

    def get_validator(self, validator_class):
        return validator_class(*self.get_validator_args(), **self.get_validator_kwargs())

	def get_validator_args(self):
		return ()

    def get_validator_kwargs(self):
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def on_valid(self, validator):
        raise NotImplementedError

    def on_invalid(self, validator):
        raise NotImplementedError

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context, cls=JSONEncoder)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def post(self, request, *args, **kwargs):
        validator_class = self.get_validator_class()
        validator = self.get_validator(validator_class)
        if validator.is_valid():
            return self.on_valid(validator)
        else:
            return self.on_invalid(validator)
