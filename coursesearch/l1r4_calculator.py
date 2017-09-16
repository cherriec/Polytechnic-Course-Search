def calcL1R4(profile,group):
    """ This function calculates and returns the L1R4 score of a user, based on the L1R4 group required.
        It takes the best score in English, two relevant subjects, and two other best subjects to calculate the L1R4.
        It takes in two parameters,
        a Profile object as profile,
        and a character as group,
        and returns an integer. """
    e1 = [11, 21]
    r1 = []
    r1.append([77, 58, 63, 61, 60, 76, 69, 70, 38, 71, 72, 73, 74, 78, 40, 32])
    r1.append([41, 42])
    r1.append(r1[1])
    r1.append(r1[1])
    r2 = []
    r2.append([42, 77, 58, 22, 63, 61, 37, 36, 29, 60, 41, 81, 76, 69, 12, 13, 14, 70, 75, 38, 71, 72, 73, 74, 23, 78, 62,
             24, 32, 40])
    r2.append([77, 58, 61, 63, 60, 76, 69, 70, 75, 38, 71, 72, 73, 74, 32, 40, 78, 62])
    r2.append([54, 48, 46, 30, 45, 49, 59, 37, 36, 44, 81, 39, 43, 47, 50, 51, 52, 53])
    r2.append([43, 48, 77, 46, 30, 45, 49, 59, 37, 36, 29, 44, 81, 39, 43, 69, 47, 54, 32, 40, 50, 51, 52, 53])
    l1r4 = 0
    check = False

    if profile.subjects.count()<5:
        return 0
    else:
        user_grades = list(profile.grade_set.all().order_by('grade'))
        if group == 'a':
            i = 0
        elif group == 'b':
            i = 1
        elif group == 'c':
            i = 2
        elif group == 'd':
            i = 3
        else:
            return 0
        while True:
            score = calcBestR(user_grades,e1)
            if not score:
                break
            l1r4 += score
            score = calcBestR(user_grades, r1[i])
            if not score:
                break
            l1r4 += score
            score = calcBestR(user_grades, r2[i])
            if not score:
                break
            l1r4 += score
            l1r4 += calcBestB(user_grades)
            l1r4 += calcBestB(user_grades)
            return l1r4
        return 0



def calcBestR(user_grades,group):
    best = "9"
    for user_grade in user_grades:
        if user_grade.subject.code in group and user_grade.grade<best:
            best = user_grade.grade
            user_grades.remove(user_grade)
            return int(best)
    return 0

def calcBestB(user_grades):
    best = user_grades[0].grade
    user_grades.remove(user_grades[0])
    return int(best)