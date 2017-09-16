from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from coursesearch.models import Course, Subject, Interest

cat_dict = {'APPLIED SCIENCES':'SCI','BUILT ENVIRONMENT':'ENV','BUSINESS & MANAGEMENT':'BIZ','ENGINEERING':'ENG','HEALTH SCIENCES':'HEA','HUMANITIES':'HSS','MARITIME STUDIES':'MAR','MEDIA & DESIGN':'MED','INFORMATION & DIGITAL TECHNOLOGIES':'IT'}

class Command(BaseCommand):
    def handle(self, *args, **options):
        import csv
        sel = input("a: initialize course data\nb: update course data\nc: initialize subjects/interests: ")
        if sel=='a':
            csv_filepathname="./coursesearch/data/allpoly_2017courseslist_20170202_3.csv"
            dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
            count = 0
            for row in dataReader:
                if row[0] != 'COURSE_ACAD_YR':
                    new_course = Course()
                    new_course.school = row[1]
                    new_course.code = row[2]
                    new_course.name = row[3]
                    new_course.category = cat_dict[row[4]]
                    new_course.description = row[7]
                    new_course.cutoff = row[5]                
                    new_course.save()
                    count+=1
            print(count, "entries added to COURSE.",)
        elif sel=='b':
            csv_filepathname="./coursesearch/data/sp-full-time-diplomas-for-2016.csv"
            dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
            count = 0
            for row in dataReader:
                if row[4]!='' and row[3]!='':
                    try:
                        new_course = Course.objects.get(code=row[4])
                        new_course.description = row[3]
                        new_course.save()
                        count+=1
                    except ObjectDoesNotExist:
                        pass                      
            print(count, "COURSE entries updated.",)
        elif sel=='c':
            txt_file_object=open("./coursesearch/data/interests.txt",'r')
            count = 0;
            for line in txt_file_object:
                interest = line.split(':')
                new_interest = Interest()
                new_interest.name = interest[0]
                new_interest.related = interest[1]
                new_interest.save()
                count+=1
            print(count,"entries added to INTEREST.",)
        else:
            print("Invalid option.")
