from __future__ import division

from django.db.models import Model, CharField, ForeignKey, TextField, DateField, IntegerField, \
    BooleanField, DecimalField

from django.utils import timezone


#######################################
#
# Basic abstract classes
#
#######################################


class Common(Model):
    """
    Abstract base class
    """
    # ...
    def underscored_name(self):
        ret = ""
        if self.name:
            ret = self.name.replace(' ', '_').replace('/', '_')
        return ret

    class Meta:
        abstract = True


class BasicName(Common):
    """
    Abstract base class for entities with single "name" field
    """
    name = CharField(max_length=250, null=False, blank=False, unique=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        abstract = True



#######################################
#
# Assessment
#
#######################################

class AssessmentStatus(BasicName):
    """
    Represents the status of an assessment
    """


class AssessmentVersion(Common):
    """
    Represents an assessment version
    """
    version = CharField(max_length=25)
    name = CharField(max_length=250, null=True, blank=True)
    description = TextField(null=True, blank=True)
    date_released = DateField(default=timezone.now)


class Assessment(BasicName):
    """
    Represents an Assessment
    """
    version = ForeignKey(AssessmentVersion)
    date_created = DateField(auto_now=True)
    considerations = TextField()
    status = ForeignKey(AssessmentStatus, null=False, blank=False)
    mov_media = DecimalField(max_digits=15, decimal_places=2, default=0)
    mov_official_document = DecimalField(max_digits=15, decimal_places=2, default=0)
    mov_public_knowledge = DecimalField(max_digits=15, decimal_places=2, default=0)
    completion = DecimalField(max_digits=15, decimal_places=2, default=0)

#######################################
#
# Elements
#
#######################################


class Element(Common):
    """
    Represents an element of the urban model (Ex. Electricity Supply)
    """
    code = CharField(max_length=20)
    name = CharField(max_length=250, null=False, blank=False)
    note = CharField(max_length=250, null=True, blank=True)
    address = CharField(max_length=250, null=True, blank=True)
    order = IntegerField(null=True, blank=True)
    parent = ForeignKey('self', null=True, blank=True)
    version = ForeignKey(AssessmentVersion)


class AssessmentElement(Common):
    """
    Represents an element of the urban element in an Assessment (that could or not be not considered for the analysis)
    """
    assessment = ForeignKey(Assessment)
    element = ForeignKey(Element)
    enabled = BooleanField(default=True)
    score = DecimalField(max_digits=15, decimal_places=2, default=0)


class DependencyType(BasicName):
    """
    Represents the type of dependency between system elements (Ex.: High, Mid, Low - pending definition)
    """


class AEDependencies(Common):
    """
    Represents dependencies between system elements in an assessment
    """
    ae_origin = ForeignKey(AssessmentElement, related_name="element_origin")
    ae_dependent = ForeignKey(AssessmentElement, related_name="element_dependant")
    dependency_type = ForeignKey(DependencyType)
    help_text = CharField(max_length=100, null=True, blank=True)


#######################################
#
# Questions
#
#######################################


class ValueType(BasicName):
    """
    Represents a value type for answers of the assessment
    """


class MoVType(BasicName):
    """
    Represents a type for Means of Verification
    """


class QuestionSimple(Common):
    """
    Represents an statement (not linked to anything)
    """
    version = ForeignKey(AssessmentVersion)
    question_short = CharField(max_length=150, null=True, blank=True)
    question_long = CharField(max_length=500, null=True, blank=True)
    help_text = CharField(max_length=500, null=True, blank=True)
    placeholder = CharField(max_length=250, null=True, blank=True)
    order = IntegerField(null=True, blank=True)
    choices = CharField(max_length=50, null=True, blank=True)
    multi = BooleanField(default=False)
    question_type = CharField(max_length=25, null=True, blank=True)


class AssessmentQuestion(Common):
    """
    Represents a question in the assessment (with answer)
    """
    assessment = ForeignKey(Assessment)
    question = ForeignKey(QuestionSimple)
    response = CharField(max_length=500, null=True, blank=True)
    assessment_element = ForeignKey(AssessmentElement, null=True, blank=True)
    mov_type = ForeignKey(MoVType, null=True, blank=True)


#######################################
#
# Hazards
#
#######################################


class Hazard(Common):
    """
    Abstract class to support hazard classes
    """
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=250)

    class Meta:
        abstract = True


class HazardGroup(Hazard):
    """
    Represents a hazard group
    """
    note = CharField(max_length=250, null=True, blank=True)
    address = CharField(max_length=250, null=True, blank=True)


class HazardType(Hazard):
    """
    Represents a Hazard Type
    """
    hazard_group = ForeignKey(HazardGroup)
    description = CharField(max_length=800, null=True, blank=True)


class HazardSubtype(Hazard):
    """
    Represents a Hazard Subtype
    """
    hazard_type = ForeignKey(HazardType)


class HazardSubtypeDetail(Hazard):
    """
    Represents a Hazard Subtype Detail
    """
    hazard_subtype = ForeignKey(HazardSubtype)


#######################################
#
# Assessment - Hazards
#
#######################################


class AssessmentHazardType(Common):
    """
    Represents a hazard type in an assessment
    """
    assessment = ForeignKey(Assessment)
    hazard_type = ForeignKey(HazardType)
    risk_assessment = CharField(max_length=50, null=True, blank=True)
    r_a_year = CharField(max_length=50, null=True, blank=True)
    contingency_plan = CharField(max_length=50, null=True, blank=True)
    c_p_year = CharField(max_length=50, null=True, blank=True)
    subtypes = CharField(max_length=250, null=True, blank=True)
    enabled = BooleanField(default=False)


class AssessmentHazardSubtype(Common):
    """
    Represents a hazard subtype in an assessment
    """
    assessment = ForeignKey(Assessment)
    a_h_type = ForeignKey(AssessmentHazardType)
    h_subtype = ForeignKey(HazardSubtype)
    enabled = BooleanField(default=False)


class AssessmentHazardCause(Common):
    """
    Represents a hazard cause in an assessment
    """
    # TODO: review serializer to avoid need of codes for causes & consequences graph
    assessment = ForeignKey(Assessment)
    a_h_type = ForeignKey(AssessmentHazardType)
    a_h_type_code = CharField(max_length=20, unique=False, null=True)
    a_h_type_cause = ForeignKey(AssessmentHazardType, related_name="ht_cause")
    cause_code =  CharField(max_length=20, unique=False, null=True)


class AssessmentHazardConsequence(Common):
    """
    Represents a hazard consequence in an assessment
    """
    # TODO: review serializer to avoid need of codes for causes & consequences graph
    assessment = ForeignKey(Assessment)
    a_h_type = ForeignKey(AssessmentHazardType)
    a_h_type_code = CharField(max_length=20, unique=False, null=True)
    a_h_type_consequence = ForeignKey(AssessmentHazardType, related_name="ht_consequence")
    consequence_code =  CharField(max_length=20, unique=False, null=True)


class AssessmentElementImpactType(BasicName):
    """
    Represents the type of impact of a hazard in a system element (Ex: High, Mid, Low - pending definition)
    """


class AssessmentElementHazardImpact(Common):
    """
    Represents an impact on a system element in an assessment
    """
    assessment = ForeignKey(Assessment)
    a_h_type = ForeignKey(AssessmentHazardType)
    a_element = ForeignKey(AssessmentElement)
    impact_type = ForeignKey(AssessmentElementImpactType)


#######################################
#
# Stakeholders
#
#######################################


class AbstractStakeholder(Common):
    """
    Abstract class to support stakeholders
    """
    code = CharField(max_length=250, unique=True)
    name = CharField(max_length=250)

    class Meta:
        abstract = True


class StakeholderGroup(AbstractStakeholder):
    """
    Represents Stakeholders groups
    """
    description = CharField(max_length=500, null=True, blank=True)


class StakeholderType(AbstractStakeholder):
    """
    Represents Stakeholder types
    """
    stakeholder_group = ForeignKey(StakeholderGroup)


class StakeholderElementRelationshipType(BasicName):
    """
    Represents the type of relation of a Stakeholder with a System Element
    """

class StakeholderLGRelationshipType(BasicName):
    """
    Represents the type of relation of a Stakeholder with the Local Government
    """

class AssessmentStakeholder(Common):
    """
    Represents Stakeholders in the Assessment
    """
    name = CharField(max_length=250, null=False, blank=False, unique=False)
    assessment = ForeignKey(Assessment)
    stakeholder_type = ForeignKey(StakeholderType)
    element = ForeignKey(AssessmentElement, null=True, blank=True, related_name='stakeholders')
    element_rel_type = ForeignKey(StakeholderElementRelationshipType, null=True, blank=True)
    to_lg_rel_type = ForeignKey(StakeholderLGRelationshipType, related_name="to_lg_rel_type", null=True, blank=True)
    from_lg_rel_type = ForeignKey(StakeholderLGRelationshipType, related_name="from_lg_rel_type", null=True, blank=True)







