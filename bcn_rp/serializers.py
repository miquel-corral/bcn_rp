from rest_framework import serializers
from bcn_rp.models import *


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ('name', 'version', 'status', 'mov_media', 'mov_official_document', 'mov_public_knowledge', 'completion')



class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('code', 'name', "address", "note")


class HazardGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HazardGroup
        fields = ('code', 'name', "address", "note")


class AssessmentElementSerializer(serializers.ModelSerializer):
    element = ElementSerializer(read_only=True)

    class Meta:
        model = AssessmentElement
        fields = ('id', 'enabled', 'element', 'score')


class AEDependenciesSerializer(serializers.ModelSerializer):
    ae_origin = AssessmentElementSerializer(read_only=True)
    ae_dependent = AssessmentElementSerializer(read_only=True)

    class Meta:
        model = AEDependencies
        fields = ('ae_origin', 'ae_dependent', 'dependency_type')


class DependencyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DependencyType
        fields = ('id', 'name')


class HazardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HazardType
        fields = ('id', 'code', 'name')


class AssessmentHazardCauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentHazardCause
        fields = ('id', 'a_h_type_cause', 'cause_code', 'a_h_type_code')


class AssessmentHazardConsequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentHazardConsequence
        fields = ('id', 'a_h_type_consequence', 'consequence_code', 'a_h_type_code')


class AssessmentHazardTypeSerializer(serializers.ModelSerializer):
    # TODO: review serializer to avoid need of codes in causes and consequences
    hazard_type = HazardTypeSerializer(read_only=True)
    ht_cause = AssessmentHazardCauseSerializer(many=True, read_only=True)
    ht_consequence = AssessmentHazardConsequenceSerializer(many=True, read_only=True)

    class Meta:
        model = AssessmentHazardType
        fields = ('id', 'assessment', 'hazard_type', 'ht_cause', 'ht_consequence')


class HazardImpactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentElementImpactType
        fields = ('id', 'name')
