import datetime
from rest_framework import serializers
from form.models import CoopForm, shareCapitalFiles


# All Cooperatives List
class CooperativesListSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = CoopForm
        fields = '__all__'


# Register
class RegisterCooperativeSerializer(serializers.ModelSerializer):
    attach_share_capital = serializers.SerializerMethodField()
    # first_origin_meeting_date = serializers.CharField(format="%B %d, %Y", blank=False, default=datetime.date.today)

    class Meta():
        model = CoopForm
        model_fields = list(f.name for f in CoopForm._meta.fields)
        extra_fields = ['attach_share_capital']
        fields = model_fields + extra_fields

    def create(self, validated_data):
        return CoopForm.objects.create(**validated_data)

    def get_attach_share_capital(self, obj):
        attach_share_capital = shareCapitalFiles.objects.filter(coopform=obj)
        return ShareCapitalSerializer(attach_share_capital, many=True, read_only=False).data
    

# Update
class UpdateCooperativeSerializer(serializers.ModelSerializer):
    # society_category_display = serializers.CharField(source='get_society_category_display')
    REGISTRATION_TYPE = serializers.SerializerMethodField()
    #SOCIETY_CATEGORY = serializers.SerializerMethodField()
    BYE_LAWS_CHOICES = serializers.SerializerMethodField()
    LGA = serializers.SerializerMethodField()
    attach_share_capital = serializers.SerializerMethodField()

    class Meta:
        model = CoopForm
        model_fields = list(f.name for f in CoopForm._meta.fields)
        extra_fields = ['REGISTRATION_TYPE', 'SOCIETY_CATEGORY',
                        'BYE_LAWS_CHOICES', 'LGA', 'attach_share_capital']
        fields = model_fields + extra_fields

    def create(self, validated_data):
        return CoopForm.objects.create(**validated_data)

    def get_attach_share_capital(self, obj):
        attach_share_capital = shareCapitalFiles.objects.filter(coopform=obj)
        return ShareCapitalSerializer(attach_share_capital, many=True, read_only=False).data

    def get_REGISTRATION_TYPE(self, obj):
        return list(obj.REGISTRATION_TYPE)

    # def get_SOCIETY_CATEGORY(self, obj):
    #     return list(obj.SOCIETY_CATEGORY)

    def get_BYE_LAWS_CHOICES(self, obj):
        return list(obj.BYE_LAWS_CHOICES)

    def get_LGA(self, obj):
        return list(obj.LGA)

    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        society_logo = {
            "url": representation.pop("society_logo"),
            "filename": instance.society_logo_filename,
        }        
        attach_first_minute = {
            "url": representation.pop("attach_first_minute"),
            "filename": instance.attach_first_minute_filename,
        }
        attach_second_minute = {
            "url": representation.pop("attach_second_minute"),
            "filename": instance.attach_second_minute_filename,
        }
        attach_bye_laws = {
            "url": representation.pop("attach_bye_laws"),
            "filename": instance.attach_bye_laws_filename,
        }
        
        representation['society_logo'] = society_logo
        representation['attach_first_minute'] = attach_first_minute
        representation['attach_second_minute'] = attach_second_minute
        representation['attach_bye_laws'] = attach_bye_laws
        
        return representation


# Attach Share Capital
class ShareCapitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = shareCapitalFiles
        fields = ['id', 'coopform', 'attach_share_capital']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        attach_share_capital = {
            "url": representation.pop("attach_share_capital"),
            "size": instance.attach_share_capital.size,
            "name": instance.attach_share_capital_filename,
        }
        
        representation['attach_share_capital'] = attach_share_capital
        return representation


# Retrieve Profile Details
class RetrieveCooperativeSerializer(serializers.ModelSerializer):
    first_origin_meeting_date = serializers.DateField(format="%B %d, %Y")
    second_origin_meeting_date = serializers.DateField(format="%B %d, %Y")
    created = serializers.DateTimeField(format="%a, %b %d, %Y, %I:%M %p")
    updated = serializers.DateTimeField(format="%a, %b %d, %Y, %I:%M %p")

    class Meta:
        model = CoopForm
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        attach_first_minute = {
            "url": representation.pop("attach_first_minute"),
            "filename": instance.attach_first_minute_filename,
        }
        attach_second_minute = {
            "url": representation.pop("attach_second_minute"),
            "filename": instance.attach_second_minute_filename,
        }
        attach_bye_laws = {
            "url": representation.pop("attach_bye_laws"),
            "filename": instance.attach_bye_laws_filename,
        }
        
        representation['attach_first_minute'] = attach_first_minute
        representation['attach_second_minute'] = attach_second_minute
        representation['attach_bye_laws'] = attach_bye_laws
        
        return representation
    
    
# Delete Profile Details
class DeleteCooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoopForm
        fields = '__all__'

    # attach_share_capital = shareCapitalFiles.objects.prefetch_related('share_capital_files')
