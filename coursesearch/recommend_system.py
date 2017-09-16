from operator import itemgetter
from .models import Course

def recommend(profile, limit, weight):
    """ This function recommends a list of courses based on a user's profile, by finding the course(s) with the
        best matches to the user's interests and cut-off points lower than and closest to the user's L1R4 score.
        It takes in three parameters,
        a Profile object as profile,
        an integer as limit,
        and a float as weight,
        and returns a list of Course codes, which is the primary key of the Course model. """

    if profile.interests.count() == 0:
        return 0
    else:
        coursecode_all = list(Course.objects.all().order_by('code').values_list('code',flat=True))
        keywords = []
        hits = [[coursecode_all[i],0] for i in range(len(coursecode_all))]
        interests = list(profile.interests.values_list('name', 'related'))
        for interest in interests:
            keywords.append(interest[0])
            related = interest[1].split()
            keywords += related

        i = 0

        for course in Course.objects.all().order_by('code'):
            if course.l1r4group == 'A':
                if profile.l1r4_A == 0:
                    hits[i][1] = 0
                    i += 1
                    continue
                else:
                    l1r4 = profile.l1r4_A
            elif course.l1r4group == 'B':
                if profile.l1r4_B == 0:
                    hits[i][1] = 0
                    i += 1
                    continue
                else:
                    l1r4 = profile.l1r4_B
            elif course.l1r4group == 'C':
                if profile.l1r4_C == 0:
                    hits[i][1] = 0
                    i += 1
                    continue
                else:
                    l1r4 = profile.l1r4_C
            elif course.l1r4group == 'D':
                if profile.l1r4_D == 0:
                    hits[i][1] = 0
                    i += 1
                    continue
                else:
                    l1r4 = profile.l1r4_D

            if course.cutoff < l1r4:
                hits[i][1] = 0
                i += 1
                continue

            for k in keywords:
                if k.lower() in course.name.lower():
                    hits[i][1] += weight

            if hits[i][1] == 0:
                i += 1
                continue

            if course.cutoff - l1r4 <= 5:
                diff = course.cutoff - l1r4
                hits[i][1] += (5-diff) * weight

            i += 1

        hits = sorted(hits, key=itemgetter(1), reverse=True)

        recs=[]
        i = 0
        while(i < len(hits)):
            if hits[i][1] > 0:
                recs.append(hits[i])
                i += 1
            else:
                break

        if len(recs) > limit:
            return [recs[j][0] for j in range(limit) if recs[j][1]!=0]
            # return recs
        else:
            return [recs[j][0] for j in range(len(recs))]
            # return recs
