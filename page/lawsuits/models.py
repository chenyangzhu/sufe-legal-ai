from django.db import models

# Create your models here.

class Lawsuit(models.Model):
    CRIME_CHOICE = (
    ('民事','民事'),
    ('刑事','刑事')
    )
    crime_type = models.CharField("案件类型", max_length = 16, choices = CRIME_CHOICE)

    ONEorTWICE = (
    ("一审","一审"),
    ("二审","二审"),
    ("其他","其他"),
    )
    procedure = models.CharField("庭审程序", max_length = 16, choices = ONEorTWICE, default = 0)

    crime_type_detail = models.CharField("案由",max_length = 128, default = None) # 案由

    PROC_TYPE_CHOICE =  (
    ("判决书","判决书"),
    ("裁定书", "裁定书")
    )
    proc_type = models.CharField("文书类型",max_length = 16, choices = PROC_TYPE_CHOICE, default = 1)

    area =  models.CharField("法院名",max_length = 128, default = None) # 城市
    date = models.DateTimeField('判决日期', default = None)
    plaintiff = models.CharField("原告", max_length = 256, default = None)
    defendant = models.CharField("被告", max_length = 256, default = None)
    third_party = models.CharField("第三人", max_length = 256, default = None)

    people_at_party = models.CharField("当事人描述", max_length = 256, default = None)
