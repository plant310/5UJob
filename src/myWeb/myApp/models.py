# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class Profession(models.Model):
    profession_id = models.IntegerField(primary_key=True)
    profession_name = models.CharField(max_length=20)
    major = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'profession'


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