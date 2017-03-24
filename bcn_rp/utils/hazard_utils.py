from __future__ import division

import sys

from bcn_rp.models import HazardGroup, HazardType, AssessmentHazardType, AssessmentElementHazardImpact

class HazardGroupSelected:
    """
    Represents a hazard group with selected hazard types
    """
    def __init__(self):
        self.name = ''
        self.percen = 0,0
        self.hazard_types = {}


def get_hazards_with_impacts(assessment):

    impacts = AssessmentElementHazardImpact.objects.filter(assessment=assessment)
    a_h_ts = []

    for i in impacts:
        try:
            if a_h_ts.index(i) > 0:
                pass
        except:
            a_h_ts.append(i.a_h_type.id)


    return AssessmentHazardType.objects.filter(id__in=a_h_ts)


def get_hazards_selected(assessment):
    """
    Retrieves the answered hazards in an assessment
    :param assessment:
    :return:
    """
    # get hazard types in the assessment
    hazard_types = AssessmentHazardType.objects.filter(assessment=assessment)

    # construct the result
    n_of_hts = 0

    group_dict = {}

    for hg in HazardGroup.objects.all().order_by('id'):
        ht_dict = {}
        for ht in HazardType.objects.filter(hazard_group=hg).order_by('id'):
            for aht in AssessmentHazardType.objects.filter(assessment=assessment, hazard_type=ht).order_by('id'):
                # we consider all ah_type are selected if not, they would not be created
                #if aht.is_selected():
                n_of_hts += 1
                ht_dict[aht.hazard_type.name] = 1
        if len(ht_dict) > 0:
            group_dict[hg.name] = ht_dict

    for key_g in group_dict.keys():
        for key_t in group_dict[key_g].keys():
            group_dict[key_g][key_t] = "{0:.2f}".format(group_dict[key_g][key_t] / n_of_hts * 100)

    return group_dict


def get_hazard_groups_selected(assessment):
    # get hazard types in the assessment
    hazard_types = AssessmentHazardType.objects.filter(assessment=assessment)

    # construct the result
    group_dict = {}
    total_selected_ahts = 0

    for hg in HazardGroup.objects.all().order_by('id'):
        n_of_hts = 0
        for ht in HazardType.objects.filter(hazard_group=hg).order_by('id'):
            for aht in AssessmentHazardType.objects.filter(assessment=assessment, hazard_type=ht).order_by('id'):
                # we consider all ah_type are selected if not, they would not be created
                n_of_hts += 1
                total_selected_ahts += 1

        if (n_of_hts > 0):
            group_dict[hg.name] = n_of_hts

    for key in group_dict.keys():
        group_dict[key] = "{0:.2f}".format(group_dict[key] / total_selected_ahts * 100)

    return group_dict
