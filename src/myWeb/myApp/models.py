# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class CompanySize(models.Model):
    profession_id = models.IntegerField(primary_key=True)
    company_size = models.CharField(max_length=20)
    company_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'company_size'
        unique_together = (('profession_id', 'company_size'),)


class CompanyType(models.Model):
    profession_id = models.IntegerField(primary_key=True)
    company_type = models.CharField(max_length=20)
    number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'company_type'
        unique_together = (('profession_id', 'company_type'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Education(models.Model):
    profession_id = models.IntegerField(primary_key=True)
    education = models.CharField(max_length=20)
    number = models.IntegerField()
    avg_salary = models.FloatField()
    lowest_salary = models.FloatField()
    highest_salary = models.FloatField()

    class Meta:
        managed = False
        db_table = 'education'
        unique_together = (('profession_id', 'education'),)


class Experience(models.Model):
    profession_id = models.IntegerField(primary_key=True)
    experiene = models.CharField(max_length=20)
    avg_salary = models.FloatField()
    lowest_salary = models.FloatField()
    highest_salary = models.FloatField()
    number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'experience'
        unique_together = (('profession_id', 'experiene'),)


class Major(models.Model):
    major_id = models.AutoField(primary_key=True)
    major_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'major'


class MajorPrediction(models.Model):
    major_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'major_prediction'
        unique_together = (('major_id', 'date'),)


class PrimativeData(models.Model):
    position = models.CharField(max_length=10)
    wages = models.FloatField()
    release_date = models.CharField(max_length=20)
    place = models.CharField(max_length=20, blank=True, null=True)
    education = models.CharField(max_length=20, blank=True, null=True)
    work_experience = models.CharField(max_length=20, blank=True, null=True)
    requestion = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=20, blank=True, null=True)
    compare = models.CharField(max_length=20)
    limit_people = models.IntegerField()
    address = models.CharField(max_length=100, blank=True, null=True)
    company_type = models.CharField(max_length=20, blank=True, null=True)
    company_size = models.CharField(max_length=20, blank=True, null=True)
    point_information = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'primative_data'


class Profession(models.Model):
    profession_id = models.AutoField(primary_key=True)
    profession_name = models.CharField(max_length=20)
    major_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'profession'


class ProfessionPrediction(models.Model):
    profession_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'profession_prediction'
        unique_together = (('profession_id', 'date'),)


class Region(models.Model):
    profession_id = models.IntegerField(primary_key=True)
    region = models.CharField(max_length=20)
    number = models.IntegerField()
    lowest_salary = models.FloatField()
    highest_salary = models.FloatField()

    class Meta:
        managed = False
        db_table = 'region'
        unique_together = (('profession_id', 'region'),)


class RegionPrediction(models.Model):
    profession_id = models.IntegerField(primary_key=True)
    region = models.CharField(max_length=20)
    date = models.DateField()
    number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'region_prediction'
        unique_together = (('profession_id', 'region', 'date'),)


class SalaryPrediction(models.Model):
    profession_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    avg_salary = models.FloatField()

    class Meta:
        managed = False
        db_table = 'salary_prediction'
        unique_together = (('profession_id', 'date'),)


class UserMessage(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=10)
    user_password = models.CharField(max_length=30)
    user_email = models.CharField(max_length=30)
    user_signature = models.CharField(max_length=50, blank=True, null=True)
    like_number = models.IntegerField()
    collect_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_message'
