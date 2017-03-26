from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import sys

from rest_framework import generics
from rest_framework.views import APIView

from django.http import JsonResponse


from bcn_rp.models import AssessmentElement as AssessmentElementModel, Assessment as AssessmentModel
from bcn_rp.serializers import *
from bcn_rp.utils.hazard_utils import get_hazards_selected, get_hazard_groups_selected, get_hazards_with_impacts

###############################################
#
# Views
#
###############################################
def bcn_profile(request):
    template = loader.get_template("bcn_rp/bcn_profile.html")

    # TODO: filter per assessment
    parent_elements = AssessmentElementModel.objects.filter(element__parent=None)

    assessment = AssessmentModel.objects.all()[0]

    # get hazards selected
    hs_list = get_hazards_selected(assessment)

    # get hazards impacts
    hi_list = get_hazards_with_impacts(assessment)

    context = RequestContext(request, {
        'parent_elements': parent_elements,
        'hazard_selected': hs_list,
        'hi_list': hi_list,
    })
    return HttpResponse(template.render(context))


def hazard_interdependencies(request):
    template = loader.get_template("bcn_rp/hazards/hazard_interdependencies.html")

    # TODO: filter per assessment
    parent_elements = AssessmentElementModel.objects.filter(element__parent=None)

    assessment = AssessmentModel.objects.all()[0]

    # get hazards selected
    hs_list = get_hazards_selected(assessment)

    # get hazards impacts
    hi_list = get_hazards_with_impacts(assessment)

    context = RequestContext(request, {
        'parent_elements': parent_elements,
        'hazard_selected': hs_list,
        'hi_list': hi_list,
    })
    return HttpResponse(template.render(context))


def hazards_selected(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    assessment = AssessmentModel.objects.get(id=assessment_id)

    # get hazards selected
    hs_list = get_hazards_selected(assessment)

    hg_list = get_hazard_groups_selected(assessment)

    # parent elements for menu
    parent_elements = AssessmentElementModel.objects.filter(element__parent=None)

    # get hazards impacts
    hi_list = get_hazards_with_impacts(assessment)

    # return page
    template = loader.get_template("bcn_rp/hazards/hazards_selected.html")
    context = RequestContext(request, {
        'selected': "HAZARDS_SELECTED",
        'parent_elements': parent_elements,
        'hazard_selected': hs_list,
        'hgs_selected': hg_list,
        'hi_list': hi_list,
    })
    return HttpResponse(template.render(context))


def hazard_impacts(request, assessment_id):
    # get assessment
    assessment = AssessmentModel.objects.get(id=assessment_id)

    # parent elements for menu
    parent_elements = AssessmentElementModel.objects.filter(element__parent=None)


    # get hazards selected
    hs_list = get_hazards_selected(assessment)

    # get hazards impacts
    hi_list = get_hazards_with_impacts(assessment)

    # return page
    template = loader.get_template("bcn_rp/hazards/hazard_impacts.html")
    context = RequestContext(request, {
        'parent_elements': parent_elements,
        'hazard_selected': hs_list,
        'hi_list': hi_list,
    })
    return HttpResponse(template.render(context))


def stakeholders(request, assessment_id):
    # get assessment
    assessment = AssessmentModel.objects.get(id=assessment_id)

    # parent elements for menu
    parent_elements = AssessmentElementModel.objects.filter(element__parent=None)


    # get hazards selected
    hs_list = get_hazards_selected(assessment)

    # get hazards impacts
    hi_list = get_hazards_with_impacts(assessment)

    # return page
    template = loader.get_template("bcn_rp/stakeholders.html")
    context = RequestContext(request, {
        'parent_elements': parent_elements,
        'hazard_selected': hs_list,
        'hi_list': hi_list,
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


class HazardGroupsSelected(generics.ListAPIView):
    serializer_class = HazardGroupSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        a_id = self.request.query_params.get('a_id', None)

        if a_id is not None:
            ah_types = AssessmentHazardType.objects.filter(assessment_id=a_id)
            hg_ids = []
            for ah_type in ah_types:
                try:
                    if hg_ids.index(ah_type.hazard_type.hazard_group.id) > 0:
                        pass
                except:
                    hg_ids.append(ah_type.hazard_type.hazard_group.id)

            queryset = self.model.objects.filter(id__in=hg_ids)
            return queryset.order_by('id')

class Impact:

    def __init__(self, source, source_name, target, target_name):

        self.impact_dict = dict()

        self.impact_dict['source'] = source
        self.impact_dict['source_name'] = source_name
        self.impact_dict['target'] = target
        self.impact_dict['target_name'] = target_name
        self.impact_dict['impact_type'] = 3 # TODO: set from DB. Low by default

        # set some High
        if source_name == 'Drought' and target_name in ['Electricity Supply', 'Green', 'Health']:
            self.impact_dict['impact_type'] = 1
        # set some Mid
        if source_name == 'Drought' and target_name in ['Air', 'Telecommunications']:
            self.impact_dict['impact_type'] = 2



class Impacts(APIView):

    def get(self, request, format=None):

        # TODO: get assessment
        assessment = AssessmentModel.objects.all()[0]

        # filter param
        a_h_t_id =  self.request.query_params.get('assessmentElementId', None)

        # Impacts
        impacts = []

        # Filter hazard impacts if needed
        a_e_h_i_s = AssessmentElementHazardImpact.objects.filter(assessment=assessment)
        if a_h_t_id:
            a_e_h_i_s = a_e_h_i_s.filter(a_h_type__id=a_h_t_id)

        for a_i in a_e_h_i_s:
            impact = Impact(a_i.a_h_type.id, a_i.a_h_type.hazard_type.name, a_i.a_element.id, a_i.a_element.element.name)
            impacts.append(impact.impact_dict)


        return JsonResponse(impacts, safe=False)


class HazardImpactTypes(generics.ListAPIView):
    serializer_class = HazardImpactTypeSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        queryset = self.model.objects
        return queryset.order_by('id')


class Dependencies(generics.ListAPIView):
    serializer_class = AEDependenciesSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):

        assesstment_element_id = self.request.query_params.get('assesstmentElementId', None)

        levelparam = self.request.query_params.get('level', 2)

        if assesstment_element_id is not None:
            return self.get_all_children(assesstment_element_id, int(levelparam))
        else:
            return self.model.objects

    def get_all_children(self, ae_id, max_level):
        r = []
        if max_level == 0:
            return r

        dep = self.model.objects.filter(ae_origin_id=ae_id)

        r.extend(dep)

        for c in dep:
            _r = self.get_all_children(c.ae_dependent_id, max_level - 1)
            if 0 < len(_r):
                r.extend(_r)
        return r


class DependencyTypes(generics.ListAPIView):
    serializer_class = DependencyTypeSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        queryset = self.model.objects
        return queryset.order_by('id')


class AssessmentStakeholder(generics.ListAPIView):

    serializer_class = AssessmentStakeholderSerializer
    model = serializer_class.Meta.model



    def get_queryset(self):

        ae_stakeholder_id = self.request.query_params.get('ae_stakeholder_id', None)

        if ae_stakeholder_id is not None:
            queryset = self.model.objects
        else:
            return  self.model.objects

