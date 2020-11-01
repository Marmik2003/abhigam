from django.db import models

# Create your models here.

class ADMIT_PATIENT(models.Model):
    PATIENT_ID = models.CharField(max_length=45)
    PATIENT_NAME = models.CharField(max_length=45)
    PATIENT_FHR_HUS_NAME = models.CharField(max_length=45)
    PATIENT_AGE = models.IntegerField()
    PATIENT_ADMIT_DATE_TIME = models.DateTimeField()
    PATIENT_BIRTH_DATE = models.DateTimeField()
    PATIENT_SEX = models.CharField(max_length=7)
    PATIENT_STREET1 = models.CharField(max_length=45)
    PATIENT_STREET2 = models.CharField(max_length=45)
    PATIENT_DISTRICT = models.CharField(max_length=45)
    PATIENT_CITY = models.CharField(max_length=45)
    PATIENT_STATE = models.CharField(max_length=45)
    PATIENT_PINCODE = models.CharField(max_length=45)
    PATIENT_MOB_NUM = models.IntegerField()
    PATIENT_RELATIVE_MOB_NUM = models.IntegerField()
    PATIENT_EMAIL_ID = models.CharField(max_length=45)
    PATIENT_TREATING_DR = models.ForeignKey('PATIENT_TREATING_DR', on_delete=models.CASCADE)
    PATIENT_REFER_BY = models.CharField(max_length=45)
    PATIENT_INFORMATION_GIVEN_BY = models.CharField(max_length=45)
    PATIENT_RELATION = models.CharField(max_length=45)
    PATIENT_MED_CLAIM = models.CharField(max_length=3)
    PATIENT_ROOM_PRICE = models.IntegerField()#Room Category:
    PATIENT_ROOM_TYPE = models.CharField(max_length=45)# Fixed Value Drop Down (HDU – Highly dependency unit / HDU + Isolation)
    PATIENT_PHYSICIAN_CHARGE = models.IntegerField()

    def __str__(self):
        return self.ADMIT_PATIENT


class PATIENT_DEPOSIT(models.Model):
    PATIENT_ID = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    DEPOSIT_DATETIME = models.DateTimeField()
    DEPOSIT_AMOUNT = models.IntegerField()
    def __str__(self):
        return self.PATIENT_DEPOSIT

class PATIENT_DAILY_EXPENSE(models.Model):
    PATIENT_ID = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    EXPENSE_DATETIME = models.DateTimeField()
    RADIOLOGY_EXPENSE = models.IntegerField()
    PATHOLOGY_EXPENSE = models.IntegerField()
    PHARMACY_EXPENSE = models.IntegerField()
    OTHER_EXPENSE = models.IntegerField()
    REMARKS = models.CharField(max_length=45)
    def __str__(self):
        return self.PATIENT_DAILY_EXPENSE

class PATIENT_BILL(models.Model):
    PATIENT_BILL_NO = models.CharField(max_length=45)
    PATIENT_ID = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    # PATIENT_NAME = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    # PATIENT_ADMIT_DATE_TIME = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    PATIENT_DISCHARGE_DATE_TIME = models.DateTimeField()
    # PATIENT_STREET1 = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    # PATIENT_STREET2 = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    # PATIENT_CITY = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    # PATIENT_STATE = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    # PATIENT_PINCODE = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    # PATIENT_MOB_NUM = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    # PATIENT_EMAIL_ID = models.ForeignKey('ADMIT_PATIENT', on_delete=models.CASCADE)
    PAN_NO = models.CharField(max_length=45)
    CIN_NO = models.CharField(max_length=45)

    def __str__(self):
        return self.PATIENT_BILL

class PATIENT_TREATING_DR(models.Model):
    ID = models.CharField(max_length=45)
    TRATING_DR_NAME = models.CharField(max_length=45)
    def __str__(self):
        return self.PATIENT_TREATING_DR