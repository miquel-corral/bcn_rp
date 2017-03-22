from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from rest_framework import generics

from bcn_rp.models import AssessmentElement as AssessmentElementModel
from bcn_rp.serializers import *

###############################################
#
# Views
#
###############################################
def bcn_profile(request):
    template = loader.get_template("bcn_rp/bcn_profile.html")

    # TODO: filter per assessment
    parent_elements = AssessmentElementModel.objects.filter(element__parent=None)

    context = RequestContext(request, {
        'parent_elements': parent_elements,
    })
    return HttpResponse(template.render(context))


def hazard_interdependencies(request):
    template = loader.get_template("bcn_rp/hazards/hazard_interdependencies.html")

    # TODO: filter per assessment
    parent_elements = AssessmentElementModel.objects.filter(element__parent=None)

    context = RequestContext(request, {
        'parent_elements': parent_elements,
    })
    return HttpResponse(template.render(context))


###############################################
#
# Classes for REST API
#
###############################################
class Assessment(generics.ListAPIView):
    serializer_class = AssessmentSerializer
    model = serializer_class.Meta.model

    # TODO: filter by id
    def get_queryset(self):
        return self.model.objects.order_by('id')



class ParentElements(generics.ListAPIView):
    serializer_class = ElementSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        queryset = self.model.objects.filter(parent=None)
        return queryset.order_by('id')




class ParentAssessmentElement(generics.ListAPIView):
    serializer_class = AssessmentElementSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.filter(element__parent=None).order_by('id')


class AssessmentElement(generics.ListAPIView):
    serializer_class = AssessmentElementSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        if id is not None:
            return self.model.objects.filter(element__id=id).order_by('id')
        else:
            return self.model.objects.order_by('id')


class ChildAssessmentElement(generics.ListAPIView):
    serializer_class = AssessmentElementSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        if id is not None:
            return self.model.objects.filter(element__parent=id)


class HazardDependencies(generics.ListAPIView):
    serializer_class = AssessmentHazardTypeSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = self.model.objects.filter(assessment=id)
            return queryset.order_by('id')

