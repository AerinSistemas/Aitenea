from rest_framework import serializers
from django.contrib.auth.models import User
from pline.models import Pline, Step, AiteneaClass


class AiteneaClassSerializer(serializers.ModelSerializer):
    options = serializers.JSONField()
    html_options = serializers.JSONField()
    genetic_parameters = serializers.JSONField()
    html_genetic_parameters = serializers.JSONField()
    class Meta:
        model = AiteneaClass
        fields = ['id', 'class_name', 'type', 'module_name', 'options', 'html_options', 'genetic_parameters', 'html_genetic_parameters']


class StepSerializer(serializers.ModelSerializer):
    step_options = serializers.JSONField()
    step_genetic_parameters = serializers.JSONField()
    class Meta:
        model = Step
        fields = ['id', 'pline_id', 'step_number', 'step_name', 'step_type', 'module_name', 'step_options', 'step_genetic_parameters']


class PlineSerializer(serializers.ModelSerializer):
    metadata = serializers.JSONField()
    class Meta:
        model = Pline
        fields = ['id', 'name', 'description', 'fitted', 'owner', 'creation_timestamp', 'steps', 'metadata']
        # depth = 2


class PlineSerializerFull(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    
    class Meta:
        model = Pline
        fields = ['id', 'name', 'description', 'owner', 'creation_timestamp', 'steps']

    def create(self, validated_data):
        steps_data = validated_data.pop('steps')

        if isinstance(validated_data['owner'], User):
            pass
        else:
            user = User.objects.filter(id = validated_data['owner'])[0]
            validated_data['owner'] = user
        pline = Pline.objects.create(**validated_data)

        for step_data in steps_data:
            step_data['pline_id'] = pline
            # step_data['owner'] = validated_data['owner']
            Step.objects.create(**step_data)
        return pline

