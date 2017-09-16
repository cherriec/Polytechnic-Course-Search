from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CATEGORY_CHOICES = (
    # This defines the list of choices available for the category attribute of the Course object.
    # The first item in the tuple defines the id, while the second is the human-readable name.
    ("ENG", "Engineering"),
    ("SCI", "Science"),
    ("BIZ", "Business"),
    ("IT", "IT"),
    ("MED", "Design & Media"),
    ("HSS", "Humanities"),
    ("ENV", "Environment"),
    ("HEA", "Health"),
    ("MAR", "Maritime"),
    )

L1R4_GROUP_CHOICES = (
    # This defines the list of choices available for the l1r4group attribute of the Course object.
    ("A","A"),
    ("B","B"),
    ("C","C"),
    ("D","D"),
    )

SCHOOL_CHOICES = (
    # This defines the list of choices available for the school attribute of the Course object.
    ("SP", "Singapore Polytechnic"),
    ("NYP", "Nanyang Polytechnic"),
    ("NP", "Ngee Ann Polytechnic"),
    ("RP", "Republic Polytechnic"),
    ("TP", "Temasek Polytechnic"),
    )

GRADE_CHOICES = (
    # This defines the list of choices available for the grade attribute of the Grade object.
    # The first item in the tuple serves as the id and the number of points awarded for that grade,
    # while the second item defines the actual grade classification used for 'O'-Level certification in Singapore.
    ('1',"A1"),
    ('2',"A2"),
    ('3',"B3"),
    ('4',"B4"),
    ('5',"C5"),
    ('6',"C6"),
    ('7',"D7"),
    ('8',"E8"),
    ('9',"F9"),
    )

class Course(models.Model):
    ''' This defines the Course model, which represents a diploma course offered by polytechnics in Singapore.
            name is a string defining the name of the course.
            school defines the school offering the course, and is limited to the SCHOOL_CHOICES tuple.
            category defines the category the course is under, and is limited to the CATEGORY_CHOICES tuple.
            description is a string defining the description of the course.
            cutoff is an integer defining the cut-off points required for admission into the course.
            l1r4group defines the L1R4 grouping used for calculating the cut-off points for the course, and is
            limited to the L1R4_GROUP_CHOICES tuple.
            code defines the unique code used to refer to the course, and also serves as the primary key. '''
    name = models.CharField(max_length=50)
    school = models.CharField(max_length=3,choices=SCHOOL_CHOICES)
    category = models.CharField(max_length=3,choices=CATEGORY_CHOICES)
    description = models.TextField()
    cutoff = models.IntegerField()
    l1r4group = models.CharField(max_length=1,choices=L1R4_GROUP_CHOICES)
    code = models.CharField(max_length=3,primary_key=True)
    def __str__(self):
        return self.name

class Subject(models.Model):
    ''' This defines the Subject model, which represents an 'O'-Level subject taken in Singapore.
            code is an integer defining the unique code used to refer to the subject, and also serves as the primary key.
            name is a string defining the name of the subject. '''
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Interest(models.Model):
    ''' This defines the Interest model, which represents a subject interest area.
            name is a string defining the name of the interest.
            related defines the keywords related to the interest. '''
    name = models.CharField(max_length=50)
    related = models.TextField(blank=True)
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    ''' This defines the Profile model, which represents a user's profile.
            user is the Django User model which has one-to-one relationship with the profile.
            subjects defines the Subject models which have a many-to-many relationship with the profile and represents
            the subjects taken by this user. Each relationship is extended by a Grade model.
            interests defines the Interest models which have a many-to-many relationship with the profile and represents
            the subject interest areas of the user.
            targets defines the Course models which have a many-to-many relationship with the profile and represents
            the target courses of the user. Each relationship is extended by a Target model.
            l1r4_X is an integer defining the calculated L1R4 score of the user, where X is the L1R4 group and ranges from
            A, B, C, to D. '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, through='Grade')
    interests = models.ManyToManyField(Interest)
    targets = models.ManyToManyField(Course, through='Target')
    l1r4_A = models.IntegerField(default=0)
    l1r4_B = models.IntegerField(default=0)
    l1r4_C = models.IntegerField(default=0)
    l1r4_D = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    ''' This function creates new Profile model instance each time a new User model instance is created and
            links the two models together under a one-to-one relationship. '''
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    ''' This function saves the Profile model instance linked to the User model instance whenever the latter
            is saved. '''
    instance.profile.save()

class Grade(models.Model):
    ''' This defines the Grade model, which represents the grade scored by a user for a subject. It is created for
            each many-to-many relationship between a Profile and Subject model.
            profile defines the foreign key to the Profile model.
            subject defines the foreign key to the Subject model.
            grade defines the grade scored for this subject by the user and is limited to the GRADE_CHOICES tuple. '''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)

class Target(models.Model):
    ''' This defines the Target model, which represents the target course of a user. It is created for each
            many-to-many relationship between a Profile model and Course model.
            profile defines the foreign key to the Profile model.
            course defines the foreign key to the Course model.
            rank is an integer defining the rank selected by the user for this target course. '''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rank = models.IntegerField()