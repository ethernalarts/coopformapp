import uuid  # Required for unique instances
import datetime
import os
from django.db import models
from django.conf import settings
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import FileExtensionValidator


# Create your models here.


class CoopForm(models.Model):
    # primary key
    id = models.BigAutoField(primary_key=True, editable=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    # Cooperative Society Details
    society_name = models.CharField(
        "Name of the Society", max_length=50, unique=True, blank=False
    )

    SOCIETY_CATEGORY = [
        ("Arts and Science Society", "Arts and Science Society"),
        ("Business", "Business"),
        ("Caste", ("Caste")),
        ("Charitable Society", ("Charitable Society")),
        ("Company Trusts", ("Company Trusts")),
        ("Crafts", ("Crafts")),
        ("Educational", ("Educational")),
        ("Military", ("Military")),
        ("Political", ("Political")),
        ("Religious", ("Religious")),
        ("Sports", ("Sports")),
        ("Social", ("Social")),
        ("Women and Children", ("Women and Children")),
        ("Welfare Association", ("Welfare Association")),
        ("Youth", ("Youth")),
    ]

    society_category = models.CharField(
        ("Category of the Society"),
        choices=SOCIETY_CATEGORY,
        max_length=50,
        default="Arts and Science Society",
        blank=False,
    )

    LGA = [
        ("Akoko-Edo", ("Akoko-Edo")),
        ("Egor", ("Egor")),
        ("Esan Central", ("Esan Central")),
        ("Esan North-East", ("Esan North-East")),
        ("Esan South-East", ("Esan South-East")),
        ("Esan West", ("Esan West")),
        ("Etsako Central", ("Etsako Central")),
        ("Etsako East", ("Etsako East")),
        ("Etsako West", ("Etsako West")),
        ("Igueben", ("Igueben")),
        ("Ikpoba-Okha", ("Ikpoba-Okha")),
        ("Oredo", ("Oredo")),
        ("Orhiomwon", ("Orhiomwon")),
        ("Ovia North-East", ("Ovia North-East")),
        ("Ovia South-East", ("Ovia South-East")),
        ("Owan East", ("Owan East")),
        ("Owan West", ("Owan West")),
    ]

    # Cooperative Society's Address
    society_house_number = models.IntegerField(
        ("Door/House/Building Number"), null=False, blank=False
    )
    society_street = models.CharField(("Street"), max_length=70, blank=False)
    society_village_city = models.CharField(
        ("Village/City"), max_length=30, blank=False
    )
    society_lga_of_activities = models.CharField(
        "LGA of Activities",
        choices=LGA,
        max_length=30,
        default="Akoko-Edo",
        blank=False,
    )

    def get_upload_path(self, filename):
        return "images/{0}/{1}".format(self.society_name, filename)

    # Logo
    society_logo = models.ImageField(
        "Society's Logo",
        upload_to=get_upload_path,
        default=f"{settings.FORM_STATIC}img/default.png",
        blank=True,
    )

    @property
    def society_logo_default(self):
        return self._meta.get_field("society_logo").get_default()

    # Contact Persons
    first_contact_name = models.CharField(
        ("1st Contact's Name"), max_length=50, blank=False
    )
    first_contact_phone_number = PhoneNumberField(
        ("1st Contact's Phone Number"), blank=False
    )
    first_contact_email = models.EmailField(
        "1st Contact's Email", max_length=100, blank=True
    )

    second_contact_name = models.CharField(
        ("2nd Contact's Name"), max_length=100, blank=False
    )
    second_contact_phone_number = PhoneNumberField(
        ("2nd Contact's Phone Number"), blank=False
    )
    second_contact_email = models.EmailField(
        "2nd Contact's Email", max_length=254, blank=True
    )

    third_contact_name = models.CharField(
        ("3rd Contact's Name"), max_length=100, blank=False
    )
    third_contact_phone_number = PhoneNumberField(
        ("3rd Contact's Phone Number"), blank=False
    )
    third_contact_email = models.EmailField(
        "3rd Contact's Email", max_length=254, blank=True
    )

    # Purpose of registration
    first_purpose = models.CharField(("First Purpose"), max_length=300, blank=False)
    second_purpose = models.CharField(("Second Purpose"), max_length=300, blank=False)
    third_purpose = models.CharField(("Third Purpose"), max_length=300, blank=False)

    # Nature of Registration Sought
    REGISTRATION_TYPE = [
        ("Limited Liability", ("Limited Liability")),
        ("Without Limited Liability", ("Without Limited Liability")),
    ]

    nature_registration = models.CharField(
        ("Nature of Registration"),
        choices=REGISTRATION_TYPE,
        max_length=100,
        blank=False,
    )

    def get_upload_path(self, filename):
        return "documents/{0}/{1}".format(self.society_name, filename)

    # Dates of meetings for formation / Attach Minutes
    first_origin_meeting_date = models.DateField(
        "1st Meeting Date", default=datetime.date.today, null=False, blank=False
    )
    second_origin_meeting_date = models.DateField(
        "2nd Meeting Date", default=datetime.date.today, null=False, blank=False
    )
    attach_first_minute = models.FileField(
        "Attach Minute of First Meeting",
        upload_to=get_upload_path,
        blank=False,
        validators=[
            FileExtensionValidator(["pdf", "doc", "docx", "txt", "png", "jpg"])
        ],
    )
    attach_second_minute = models.FileField(
        "Attach Minute of Second Meeting",
        upload_to=get_upload_path,
        blank=False,
        validators=[
            FileExtensionValidator(["pdf", "doc", "docx", "txt", "png", "jpg"])
        ],
    )

    # 10 Members in the Society
    president_name = models.CharField("President's Name", max_length=100, blank=False)
    president_position = models.CharField(
        "President's Position", max_length=100, blank=True, default="President"
    )
    president_phone_number = PhoneNumberField(
        "President's Phone Number", blank=False, null=False
    )

    secretary_name = models.CharField("Secretary's Name", max_length=100, blank=False)
    secretary_position = models.CharField(
        "Secretary's Position", max_length=100, blank=True, default="Secretary"
    )
    secretary_phone_number = PhoneNumberField("Secretary's Phone Number", blank=False)

    treasurer_name = models.CharField("Treasurer's Name", max_length=100, blank=False)
    treasurer_position = models.CharField(
        "Treasurer's Position", max_length=100, blank=True, default="Treasurer"
    )
    treasurer_phone_number = PhoneNumberField("Treasurer's Phone Number", blank=False)

    fourth_member_name = models.CharField(
        "4th Member's Name", max_length=100, blank=False
    )
    fourth_member_position = models.CharField(
        "4th Member's Position", max_length=100, blank=False
    )
    fourth_member_phone_number = PhoneNumberField(
        "4th Member's Phone Number", blank=False
    )

    fifth_member_name = models.CharField(
        "5th Member's Name", max_length=100, blank=False
    )
    fifth_member_position = models.CharField(
        "5th Member's Position", max_length=100, blank=False
    )
    fifth_member_phone_number = PhoneNumberField(
        "5th Member's Phone Number", blank=False
    )

    sixth_member_name = models.CharField(
        "6th Member's Name", max_length=100, blank=False
    )
    sixth_member_position = models.CharField(
        "6th Member's Position", max_length=100, blank=False
    )
    sixth_member_phone_number = PhoneNumberField(
        "6th Member's Phone Number", blank=False
    )

    seventh_member_name = models.CharField(
        "7th Member's Name", max_length=100, blank=False
    )
    seventh_member_position = models.CharField(
        "7th Member's Position", max_length=100, blank=False
    )
    seventh_member_phone_number = PhoneNumberField(
        "7th Member's Phone Number", blank=False
    )

    eighth_member_name = models.CharField(
        "8th Member's Name", max_length=100, blank=False
    )
    eighth_member_position = models.CharField(
        "8th Member's Position", max_length=100, blank=False
    )
    eighth_member_phone_number = PhoneNumberField(
        "8th Member's Phone Number", blank=False
    )

    ninth_member_name = models.CharField(
        "9th Member's Name", max_length=100, blank=False
    )
    ninth_member_position = models.CharField(
        "9th Member's Position", max_length=100, blank=False
    )
    ninth_member_phone_number = PhoneNumberField(
        "9th Member's Phone Number", blank=False
    )

    tenth_member_name = models.CharField(
        "10th Member's Name", max_length=100, blank=False
    )
    tenth_member_position = models.CharField(
        "10th Member's Position", max_length=100, blank=False
    )
    tenth_member_phone_number = PhoneNumberField(
        "10th Member's Phone Number", blank=False
    )

    # Trustees
    first_trustee_name = models.CharField(
        "1st Trustee's Name", max_length=100, blank=False
    )
    first_trustee_position = models.CharField(
        "1st Trustee's Position", max_length=100, blank=False
    )
    first_trustee_phone_number = PhoneNumberField(
        "1st Trustee's Phone Number", blank=False
    )

    second_trustee_name = models.CharField(
        "2nd Trustee's Name", max_length=100, blank=False
    )
    second_trustee_position = models.CharField(
        "2nd Trustee's Position", max_length=100, blank=False
    )
    second_trustee_phone_number = PhoneNumberField(
        "2nd Trustee's Phone Number", blank=False
    )

    third_trustee_name = models.CharField(
        "3rd Trustee's Name", max_length=100, blank=False
    )
    third_trustee_position = models.CharField(
        "3rd Trustee's Position", max_length=100, blank=False
    )
    third_trustee_phone_number = PhoneNumberField(
        "3rd Trustee's Phone Number", blank=False
    )

    fourth_trustee_name = models.CharField(
        "4th Trustee's Name", max_length=100, blank=False
    )
    fourth_trustee_position = models.CharField(
        "4th Trustee's Position", max_length=100, blank=False
    )
    fourth_trustee_phone_number = PhoneNumberField(
        "4th Trustee's Phone Number", blank=False
    )

    # Bye-laws?
    BYE_LAWS_CHOICES = [("Yes", ("Yes")), ("No", ("No"))]

    have_bye_laws = models.CharField(
        max_length=128, choices=BYE_LAWS_CHOICES, blank=False, default="No"
    )

    # Attach bye-laws
    attach_bye_laws = models.FileField(
        ("Attach a copy of your Bye-Laws"),
        upload_to=get_upload_path,
        blank=True,
        validators=[
            FileExtensionValidator(["pdf", "doc", "docx", "png", "txt", "jpg"])
        ],
    )

    # get society_logo filename
    @property
    def society_logo_filename(self):
        return os.path.basename(self.society_logo.name)

    # get attach_first_minute filename
    @property
    def attach_first_minute_filename(self):
        return os.path.basename(self.attach_first_minute.name)

    # get attach_second_minute filename
    @property
    def attach_second_minute_filename(self):
        return os.path.basename(self.attach_second_minute.name)

    # get attach_bye_laws filename
    @property
    def attach_bye_laws_filename(self):
        return os.path.basename(self.attach_bye_laws.name)

    # Form Details Reverse URL
    def get_absolute_url(self):
        return reverse("formdetails", kwargs={"pk": self.id})

    # Printout Reverse URL
    def get_printout_url(self):
        return reverse("printout", kwargs={"pk": self.id})

    class Meta:
        db_table = "form_coopform"
        permissions = [
            ("view_finish", "Can view Finish"),
        ]

    def __str__(self):
        return f"{self.society_name, self.id}"


# Share Capital Files Model
class shareCapitalFiles(models.Model):
    # primary key
    id = models.BigAutoField(primary_key=True)

    # Foreign key
    coopform = models.ForeignKey(
        CoopForm, on_delete=models.CASCADE, related_name="share_capital_files"
    )

    def get_upload_path(self, filename):
        return "documents/{0}/share_capital_files/{1}".format(
            self.coopform.society_name, filename
        )

    # Attach evidence of share capital
    attach_share_capital = models.FileField(
        "Attach Share Capital",
        upload_to=get_upload_path,
        blank=True,
        validators=[
            FileExtensionValidator(["pdf", "doc", "docx", "txt", "png", "jpg"])
        ],
    )

    # get attach_share_capital filename
    @property
    def attach_share_capital_filename(self):
        return os.path.basename(self.attach_share_capital.name)

    class Meta:
        db_table = "form_sharecapitalfiles"

    def __str__(self):
        return f"{self.attach_share_capital}"
