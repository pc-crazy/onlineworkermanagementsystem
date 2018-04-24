from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

class WorkerCheckMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.type != 'WO':
            return HttpResponseForbidden("403 Forbidden , you don't have access")
        return super(WorkerCheckMixin, self).dispatch(request, *args, **kwargs)



class ContractorCheckMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.type != 'CO':
            return HttpResponseForbidden("403 Forbidden , you don't have access")
        return super(ContractorCheckMixin, self).dispatch(request, *args, **kwargs)