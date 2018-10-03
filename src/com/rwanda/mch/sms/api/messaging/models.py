#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError


##Start of SMSReport
class SMSReport(models.Model):

    """
        This guide you building your own SMS Report ... the syntax of an SMS please, 
        don't think about other constraints your are not even able to figure out before you go into the DB  

    """
    SEPARATOR_CHOICES = (
        (' ','WhiteSpace ( )'),
        (',','Comma (,)'),
        (';','Semicolon (;)'),
        (':','Colon (:)'),
        ('*','Asterisk (*)'),
    )


    id = models.AutoField(primary_key=True, db_column='indexcol')
    ### This has to be recognized in the language supported
        
    ##START OF SMSReport LANGUAGES
    
    title_en = models.TextField(null = True, blank = True, help_text = 'Title in English ', db_column='name')


    title_rw = models.TextField(null = True, blank = True, help_text = 'Title in Kinyarwanda ', db_column='rw')
    ##END OF SMSReport LANGUAGES
    
    keyword = models.CharField(max_length=30, unique=True, db_column='code')

    description =  models.TextField(max_length=255,
                               help_text="Why do we need this SMS Report?", db_column='rw')

    field_separator = models.CharField(max_length=1, choices=SEPARATOR_CHOICES, null=True, blank=True,
                                 help_text="What is the separator of your SMS Report Fields?")

    case_sensitive = models.BooleanField(default=False,
                                 help_text="Do we need our SMS Report to react on either Upper or Lower Case?")

    in_use = models.BooleanField(default=True,
                                 help_text="Do we still use this SMS Report?")
    
    syntax_regex = models.TextField(blank = True, null = True,
                                help_text="For Developer ... Don't show on ADMIN SITE")
    
    url = models.TextField(blank = True, null = True,
                                help_text="WEb SITE URL")

    module_pk = models.PositiveSmallIntegerField(validators = [MinValueValidator(1)])
    """

    ### This has to be recognized in the language supported, language tables
    success_response = models.TextField(blank = True, null = True,
                                help_text="You need to define a SMS to be sent to acknowledge the message has been received successfully.")

    
    ### This has to be recognized in the language supported, language tables
    failure_response = models.TextField(blank = True, null = True,
                                help_text="You need to define a SMS to be sent to acknowledge the message has been received with errors.")

    ### This has to be recognized in the language supported, language tables
    failure_reason = models.TextField(blank = True, null = True,
                                help_text="You need to define a SMS to be sent to show the reason of failure.")
    
    """
    
    created = models.DateTimeField(auto_now_add=True, db_column='created_at')
    
    
    def __unicode__(self):
        return "%s(%s)" % (self.title_en, self.keyword)

    class Meta:
        db_table = 'endresource'


##End of SMSReport

##Start of SMSReportField
class SMSReportField(models.Model):


    VALUE_TYPE_CHOICES = (

        ('integer','Integer'),
        ('float','Float'),
        ('date','Date'),
        ('string','String'),
        ('string_digit','String Digit'),
    )

    DEPEDENCY_CHOICES = (
                            ('greater', 'Greater than'),
                            ('greater_or_equal', 'Greater than or Equal'),
                            ('equal', 'Equal'),
                            ('different', 'Different'),
                            ('less', 'Less than'),
                            ('less_or_equal', 'Less than or Equal'),
                            ('jam', 'Jam'),
                         )
    
    id = models.AutoField(primary_key=True, db_column='indexcol')
    sms_report = models.ForeignKey(SMSReport, db_column='sms_report_pk')

    ##START OF SMSReportField LANGUAGES
    
    title_en = models.TextField(null = True, blank = True, help_text = 'Title in English ', db_column='name_en')

    category_en = models.TextField(null = True, blank = True, help_text = 'Category in English ')
    

    title_rw = models.TextField(null = True, blank = True, help_text = 'Title in English ', db_column='name_rw')

    category_rw = models.TextField(null = True, blank = True, help_text = 'Category in Kinyarwanda ')
    ##END OF SMSReportField LANGUAGES
    
    prefix = models.CharField(max_length=5, null=True, blank=True,
                                      help_text="Do You prefix this field? E.G: WT50.8")
    key = models.CharField(max_length=30, null=True, blank=True,
                                      help_text="What is the unique key code for this Field", db_column='code')
    description = models.TextField(max_length=255,
                               help_text="Why do we need this SMS Report Field?")
    type_of_value =  models.CharField(max_length=20, choices=VALUE_TYPE_CHOICES, null=True, blank=True,
                                 help_text="The type of value the field will have.")
    
    upper_case = models.BooleanField(default=False,
                                 help_text="This SMS Report Field must be Upper Case.")
    lower_case = models.BooleanField(default=False,
                                 help_text="This SMS Report Field must be Lower Case.")
    
    minimum_value = models.FloatField(blank = True, null=True, 
                                      help_text="What is the minimum value for this SMS Report Field?")
    maximum_value = models.FloatField(blank = True, null=True, 
                                      help_text="What is the maximum value for this SMS Report Field?")
    
    minimum_length = models.FloatField(blank = True, null=True, 
                                      help_text="What is the minimum length for this SMS Report Field?")
    maximum_length = models.FloatField(blank = True, null=True, 
                                      help_text="What is the maximum length for this SMS Report Field?")
    
    position_after_sms_keyword = models.PositiveSmallIntegerField(validators = [MinValueValidator(1)])
    depends_on_value_of = models.ForeignKey("SMSReportField", null=True, blank=True, db_column = 'depends_on_value_of_pk', 
                                            related_name="dependent", help_text = "Does this SMS Report Field depend on another?")
    
    dependency = models.CharField(max_length=30, choices=DEPEDENCY_CHOICES, null=True, blank=True,
                                 help_text="How does this SMS Report Field depend on that?")
    
    allowed_value_list = models.TextField(max_length=255, null=True, blank=True,
                               help_text="Does this SMS Report Field have a list of values only allowed? Separate them with semi-colon (;)")
    only_allow_one =  models.BooleanField(default=False,
                                 help_text="Do we only allow one value of the above list for this SMS Report Field?")
    
    required =  models.BooleanField(default=True,
                                 help_text="Is this SMS Report Field mandatory?")
    
    created = models.DateTimeField(auto_now_add=True, db_column='created_at')
    
    unique_together = (("sms_report", "key", "position_after_sms_keyword"))
    
    def __unicode__(self):
        return "%s-%s" % (self.sms_report, self.title_en)

    class Meta:
        db_table = 'smsfield'
    
##End of SMSReportField
    
##Start of SMSLanguage
class SMSLanguage(models.Model):
    
    id = models.AutoField(primary_key=True, db_column='indexcol')
    name = models.CharField(max_length=30, unique = True,
                                 help_text="Language Name or Title")
    
    iso_639_1_code = models.CharField(max_length = 5, unique = True,
                                 help_text="Language Code based on ISO 639-1",
                                 db_column='code',
                                 verbose_name='Codes')
    
    description = models.TextField(max_length=255, null=True, blank=True,
                               help_text="Description of the language")

    created = models.DateTimeField(auto_now_add=True, db_column='created_at')
    
    def __unicode__(self):
        return "%s(%s)" % (self.name, self.iso_639_1_code) 

    class Meta:
        db_table = 'language'  
    
    
##End of SMSLanguage
    
