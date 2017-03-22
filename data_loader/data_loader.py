# from __future__ import unicode_literals

import csv
import sys
import os
import random

from decimal import Decimal

from django.conf import settings

project_path = "/Users/miquel/UN/0003-CRPTDEV/bcn_rp/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bcn_rp.settings'


# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps
import django
django.setup()

from bcn_rp.models import *

def createEntityWithName(entity, name):
    new = entity()
    new.name = name
    new.save()


def create_assessment_status():
    createEntityWithName(AssessmentStatus, "Open")
    createEntityWithName(AssessmentStatus, "Closed")


def create_assessment_version():
    version = AssessmentVersion()
    version.version = "v1.0"
    version.name = "BCN Preliminar Profile"
    version.save()


def create_assessment():
    a = Assessment()
    a.version = AssessmentVersion.objects.get(version="v1.0")
    a.name = "BCN Preliminar Profile"
    # TODO DELETE 3 dimensions
    a.status = AssessmentStatus.objects.get(name="Open")
    a.save()


def load_entity_single_field_name(file_name, class_name):
    """
    Load file of entities with a single field name
    :param file_name:
    :param class_name:
    :return:
    """
    print("load_entity_single_field_name: " + file_name + " .Start...")
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    for row in data_reader:
        entity = class_name()
        entity.name = row[0].strip()
        try:
            entity.save()
        except:
            print("Unexpected error:", sys.exc_info())
    print("load_entity_single_field_name: " + file_name + " .End.")


def load_elements():
    """
    Load elements file
    :return:
    """
    print("load_elements. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Elements.tsv"
    csvfile = open(file_path)
    data_reader = csv.reader(csvfile, dialect='excel-tab')
    next(data_reader);
    #  # to skip headers row

    # TODO: set version
    version = AssessmentVersion.objects.order_by('-date_released')[0]
    for row in data_reader:
        try:
            # check for parent element
            if row[0].strip() == '':
                parent_element = None
                create_element(row, version)
            else:
                parent_element = Element.objects.get(code=row[0])
                create_element(row, version, parent_element)
        except:
            print("Error processing row: " + str(row))
            print(sys.exc_info())

    print("load_elements. End.")


def create_element(row, version, parent_element=None):
    try:
        element = Element()
        element.code = row[1].strip()
        element.name = row[2].strip()
        element.parent = parent_element
        element.version = version
        element.save()
    except:
        print("Error creating element: " + str(row))
        print(sys.exc_info())


def create_assessment_elements():
    # get assessment
    # TODO get assessment
    assessment = Assessment.objects.all()[0]

    # create assesment elements
    for elem in Element.objects.all().order_by('id'):
        ae = AssessmentElement()
        ae.assessment = assessment
        ae.element = elem
        ae.save()

def set_scoring_asessment_elements():
    # TODO get assessment
    assessment = Assessment.objects.all()[0]

    # get assessment elements
    a_es = AssessmentElement.objects.filter(assessment=assessment)

    # process file to get scores
    get_scores_from_file(a_es)


def get_scores_from_file(a_es):
    print("get_scores_from_file. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Elements.tsv"
    csvfile = open(file_path)
    data_reader = csv.reader(csvfile, dialect='excel-tab')
    next(data_reader);
    # to skip headers row

    # process each row
    for row in data_reader:
        try:
            a_e = a_es.get(element__code=row[1])
            a_e.score = Decimal(str(row[3]).replace(',','.'))
            a_e.save()
        except:
            print("Error processing score of element: " + row[1])
            print(sys.exc_info())


    print("get_scores_from_file. End.")


def load_assessment_mov_and_completion():
    print("load_assessment_mov_and_completion. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Assessment_MoV.tsv"
    csvfile = open(file_path)
    data_reader = csv.reader(csvfile, dialect='excel-tab')
    # to skip headers row
    next(data_reader)

    # get assessment
    # TODO get assessment
    a = Assessment.objects.all()[0]

    # load mov and completion
    for row in data_reader:
        try:
            a.mov_media = Decimal(str(row[0]).replace(',','.'))
            a.mov_official_document = Decimal(str(row[1]).replace(',','.'))
            a.mov_public_knowledge = Decimal(str(row[2]).replace(',','.'))
            a.completion = Decimal(str(row[3]).replace(',','.'))
            a.save()
        except:
            print("Error processing mov of element: " + str(row))
            print(sys.exc_info())


    print("load_assessment_mov_and_completion. End.")



def create_type_HML(entity):
    t = entity()
    t.name = "High"
    t.save()

    t = entity()
    t.name = "Mid"
    t.save()

    t = entity()
    t.name = "Low"
    t.save()


def create_ae_dependency(ae, dep_type):
    ae_dependent = AssessmentElement.objects.get(id=random.randint(1,len(AssessmentElement.objects.all())))
    aed = AEDependencies()
    aed.ae_origin = ae
    aed.ae_dependent = ae_dependent
    aed.dependency_type = DependencyType.objects.get(name=dep_type)
    aed.save()


def create_ae_dependencies():
    for ae in AssessmentElement.objects.all():
        if ae.id % 2 == 0:
            create_ae_dependency(ae, "High")
        if ae.id % 3 == 0:
            create_ae_dependency(ae, "Mid")
        if ae.id % 5 == 0:
            create_ae_dependency(ae, "Low")


def load_hazards():
    """
    Load hazards file
    :return:
    """
    print("load_hazards. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Hazards - Hazards.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    next(data_reader);
    #  # to skip headers row

    for row in data_reader:
        # check for hazard group. if not found create it
        try:
            hazard_group = HazardGroup.objects.get(code=row[0].strip())
        except:
            hazard_group = HazardGroup()
            hazard_group.code = row[0].strip()
            hazard_group.name = row[1].strip()
            hazard_group.save()
        # check for hazard type. if not found create it
        try:
            hazard_type = HazardType.objects.get(code=row[2].strip())
        except:
            hazard_type = HazardType()
            hazard_type.code = row[2].strip()
            hazard_type.name = row[3].strip()
            hazard_type.hazard_group = hazard_group
            hazard_type.save()
        # check for hazard subtype. if not found create it
        try:
            hazard_subtype = HazardSubtype.objects.get(code=row[4].strip())
        except:
            hazard_subtype = HazardSubtype()
            hazard_subtype.code = row[4].strip()
            hazard_subtype.name = row[5].strip()
            if len(row)>6:
                if row[7].strip() != "":
                    hazard_subtype.name = hazard_subtype.name + " - " + str(row[7].strip())
            hazard_subtype.hazard_type = hazard_type
            hazard_subtype.save()
        # check for hazard subtype detail. if not found create it
        if row[6].strip() != "":
            try:
                hazard_subtype_detail = HazardSubtypeDetail.objects.get(code=row[6].strip())
            except:
                hazard_subtype_detail = HazardSubtypeDetail()
                hazard_subtype_detail.code = row[6].strip()
                hazard_subtype_detail.name = row[7].strip()
                hazard_subtype_detail.hazard_subtype = hazard_subtype
                hazard_subtype_detail.save()

    print("load_hazards. End.")


def load_assessment_hazards():
    print("load_assessment_hazards. Start.")
    # set bcn new hazard type Strong Wind
    ht = HazardType()
    ht.code = "HT111"
    ht.name = "Strong Wind"
    ht.hazard_group = HazardGroup.objects.get(code="HG20")
    ht.save()

    # TODO get assessment
    a = Assessment.objects.all()[0]

    # process file
    file_path = settings.BASE_DIR + "/files/" + "Assessment_Hazards.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    next(data_reader);
    # to skip headers row
    for row in data_reader:
        try:
            # hazard group and type
            ht = HazardType.objects.get(code=row[2].strip())
            # create assessment hazard type
            at = AssessmentHazardType()
            at.assessment = a
            at.hazard_type = ht
            at.risk_assessment = row[4].strip()
            at.r_a_year = row[5].strip()
            at.contingency_plan = row[6].strip()
            at.c_p_year = row[7].strip()
            at.subtypes = row[8].strip()
            at.enabled = True
            at.save()
            # create assessment hazard subtypes
            if at.subtypes.strip() <> '':
                create_assessment_hazard_subtypes(at)
            # create impacts
            # TODO

        except:
            print("Error processing row: " + str(row))
            print(sys.exc_info())

    print("load_assessment_hazards. End.")


def load_hazard_causes_and_consequences():
    print("load_hazard_causes_and_consequences. Start.")

    # TODO get assessment
    a = Assessment.objects.all()[0]

    # process file
    file_path = settings.BASE_DIR + "/files/" + "Assessment_Hazards.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    next(data_reader);
    # to skip headers row
    for row in data_reader:
        try:
            if row[10] and row[10].strip <> '':
                create_aht_causes(a, row[2].strip(), row[10].strip())
            if row[11] and row[11].strip <> '':
                create_aht_consequences(a, row[2].strip(), row[11].strip())
        except:
            print("Error processing row: " + str(row))
            print(sys.exc_info())

    print("load_hazard_causes_and_consequences. End.")


def create_aht_causes(assessment, aht_code, aht_causes):
    # list of causes
    aht_list = [x for x in aht_causes.split(',') if x and x.strip() <> '']
    if  len(aht_list) > 0:
        # get aht
        ah_type = AssessmentHazardType.objects.get(hazard_type__code=aht_code.strip())
        # create causes

        print("causes")
        print("ah_type: " + ah_type.hazard_type.code)
        print("aht_list: " + str(aht_list))

        for aht in aht_list:
            ah_cause = AssessmentHazardCause()
            ah_cause.assessment = assessment
            ah_cause.a_h_type =  AssessmentHazardType.objects.get(hazard_type__code=aht.strip())
            ah_cause.a_h_type_code = ah_cause.a_h_type.hazard_type.code
            ah_cause.a_h_type_cause = ah_type
            ah_cause.cause_code = ah_type.hazard_type.code
            ah_cause.save()


def create_aht_consequences(assessment, aht_code, aht_consequences):
    # list of causes
    aht_list = [x for x in aht_consequences.split(',') if x and x.strip() <> '']
    if  len(aht_list) > 0:
        # get aht
        ah_type = AssessmentHazardType.objects.get(hazard_type__code=aht_code)

        print("consequences")
        print("ah_type: " + ah_type.hazard_type.code)
        print("aht_list: " + str(aht_list))


        # create consequences
        for aht in aht_list:
            aht_consequence = AssessmentHazardConsequence()
            aht_consequence.assessment = assessment
            aht_consequence.a_h_type =  AssessmentHazardType.objects.get(hazard_type__code=aht.strip())
            aht_consequence.a_h_type_code = aht_consequence.a_h_type.hazard_type.code
            aht_consequence.a_h_type_consequence = ah_type
            aht_consequence.consequence_code = ah_type.hazard_type.code
            aht_consequence.save()


def create_assessment_hazard_subtypes(at):
    try:
        # list of subtypes
        hs_list = [x for x in at.subtypes.split(',') if x and x.strip() <> '']
        # create subtypes
        for hs in hs_list:
            ahs = AssessmentHazardSubtype()
            ahs.assessment = at.assessment
            ahs.enabled = True
            ahs.a_h_type = at
            ahs.h_subtype = HazardSubtype.objects.get(code=hs.strip())
            ahs.save()
    except:
        print("Error processing subtypes: " + str(at.subtypes))
        print(sys.exc_info())


def create_assessment_hazards():
    # get assessment
    assessment = Assessment.objects.all()[0]

    # create assessment hazard types
    for ht in HazardType.objects.all():
        aht = AssessmentHazardType()
        aht.assessment = assessment
        aht.hazard_type = ht
        aht.save()

    # create assessment hazard subtypes
    for aht in AssessmentHazardType.objects.all():
        for hst in HazardSubtype.objects.filter(hazard_type=aht.hazard_type):
            ahst = AssessmentHazardSubtype()
            ahst.assessment = assessment
            ahst.a_h_type = aht
            ahst.h_subtype = hst
            ahst.save()


def create_hazards_causes_and_consequences(entity, cause):
    # create causes
    for aht in AssessmentHazardType.objects.all():
        if aht.id % 5 == 0:
            try:
                a_h_type_cause = AssessmentHazardType.objects.get(id=random.randint(1, len(AssessmentHazardType.objects.all())-1))
            except:
                pass
                continue
            ahc = entity()
            ahc.assessment = aht.assessment
            ahc.a_h_type = aht
            if cause:
                ahc.a_h_type_cause = a_h_type_cause
            else:
                ahc.a_h_type_consequence = a_h_type_cause
            ahc.save()

def create_assessment_hazard_impact(aht, type):
    ae = AssessmentElement.objects.get(id=random.randint(1,len(AssessmentElement.objects.all())))
    ahi = AssessmentElementHazardImpact()
    ahi.assessment = aht.assessment
    ahi.a_h_type = aht
    ahi.a_element = ae
    ahi.impact_type = AssessmentElementImpactType.objects.get(id=random.randint(1,len(AssessmentElementImpactType.objects.all())))
    ahi.save()


def create_assessment_hazard_impacts():
    for aht in AssessmentHazardType.objects.all():
        if aht.id % 2 == 0:
            create_assessment_hazard_impact(aht, "High")
        if aht.id % 3 == 0:
            create_assessment_hazard_impact(aht, "Mid")
        if aht.id % 5 == 0:
            create_assessment_hazard_impact(aht, "Low")


def load_stakeholder_groups():
    """
    Loads the stakeholder groups
    :return:
    """
    print("load_stakeholder_groups. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Stakeholders - Groups.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    next(data_reader)  # to skip headers row

    for row in data_reader:
        hg = StakeholderGroup()
        hg.code = row[0].strip()
        hg.name = row[1].strip()
        hg.description = row[2].strip()
        hg.save()
    print("load_stakeholder_groups. End.")


def load_stakeholder_types():
    """
    Loads stakeholder types and subtypes
    :return:
    """
    print("load_stakeholder_types. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Stakeholders - Types.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    next(data_reader)
    # to skip headers row

    for row in data_reader:
        sg = StakeholderGroup.objects.get(code=row[0].strip())
        try:
            st = StakeholderType.objects.get(code=row[1].strip())
        except:
            st = StakeholderType()
            st.stakeholder_group = sg
            st.code = row[1].strip()
            st.name = row[3].strip()
            st.help_text = row[4].strip()
            st.save()

    print("load_stakeholder_types. End.")


def create_stakeholder_relationship_with_lg():
    types = ["Cooperates", "Informs", "Ignores"]
    for type in types:
        rlg = StakeholderLGRelationshipType()
        rlg.name = type
        rlg.save()


def create_stakeholder_relationship_with_element():
    types = ["Owner", "Operates", "Policy Advisor", "Monitors"]
    for type in types:
        sre = StakeholderElementRelationshipType()
        sre.name = type
        sre.save()


def create_assessment_stakeholder(ae,element_rel_type, to_lg_rel_type, from_lg_rel_type):
    try:
        stakeholder_type = StakeholderType.objects.get(id=random.randint(1, len(StakeholderType.objects.all())))
    except:
        return
    a_s = AssessmentStakeholder()
    a_s.assessment = ae.assessment
    a_s.element = ae
    a_s.stakeholder_type = stakeholder_type
    a_s.name = "Test Stakeholder " + str(ae.id) + str(random.randint(1, 1027))
    a_s.element_rel_type = StakeholderElementRelationshipType.objects.get(name=element_rel_type)
    a_s.to_lg_rel_type = StakeholderLGRelationshipType.objects.get(name=to_lg_rel_type)
    a_s.from_lg_rel_type = StakeholderLGRelationshipType.objects.get(name=from_lg_rel_type)
    a_s.save()



def create_assessment_stakeholders():
    for ae in AssessmentElement.objects.all():
        if ae.id % 5 == 0:
            create_assessment_stakeholder(ae, "Owner", "Cooperates", "Informs")


def create_mov_types():
    types = ["Official Document", "Media", "Public Knowledge"]
    for type in types:
        mov_type = MoVType()
        mov_type.name = type
        mov_type.save()

def create_assessment_question(assessment, i, ):
    q = QuestionSimple()
    q.version = assessment.version
    q.question_short = "Test Question " + str(i)
    q.save()
    aq = AssessmentQuestion()
    aq.question = q
    aq.assessment = assessment
    aq.assessment_element = AssessmentElement.objects.get(id=random.randint(1, len(AssessmentElement.objects.all())))
    aq.mov_type = MoVType.objects.get(id=random.randint(1, len(MoVType.objects.all())))
    aq.save()

def create_assessment_questions():
    assessment = Assessment.objects.all()[0]
    for i in range(1,50):
        create_assessment_question(assessment, i)





if __name__ == "__main__":

    """
    # create Assessment Status
    create_assessment_status()

    # create Assessment Version
    create_assessment_version()

    # create Assessment
    create_assessment()

    # load Elements
    load_elements()

    # create assessment elements
    create_assessment_elements()

    # set scoring for assessment elements
    set_scoring_asessment_elements()


    # load mov types and completion of assessment
    load_assessment_mov_and_completion()


    # create hazard groups, types, subtypes and detail
    load_hazards()

    # load assessment hazards
    load_assessment_hazards()
    """

    # create hazard causes and consequences
    load_hazard_causes_and_consequences()



    """
    # create dependencies types
    create_type_HML(DependencyType)

    # create assessment element dependencies
    create_ae_dependencies()

    # create hazard groups, types, subtypes and detail
    load_hazards()

    # create assessment hazard types, subtypes and detail
    create_assessment_hazards()

    # create hazards causes and consequences
    create_hazards_causes_and_consequences(AssessmentHazardCause, True)
    create_hazards_causes_and_consequences(AssessmentHazardConsequence, False)

    # create type of impacts
    create_type_HML(AssessmentElementImpactType)

    # create assessment hazard impact
    create_assessment_hazard_impacts()

    # load Stakeholders groups and type
    load_stakeholder_groups()
    load_stakeholder_types()

    # create stakeholder relationship type with LG
    create_stakeholder_relationship_with_lg()

    # create stakeholder relationship type with element
    create_stakeholder_relationship_with_element()

    # create assessment stakeholder
    create_assessment_stakeholders()

    # create mov types
    create_mov_types()

    # create assessment questions
    create_assessment_questions()
    """
