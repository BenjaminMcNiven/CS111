# Provided code
# This function checks to ensure that a list is of length
# 8 and that each element is type float
# Parameters:
# row - a list to check
# Returns True if the length of row is 8 and all elements are floats
def check_row_types(row):
    if len(row) != 8:
        print("Length incorrect! (should be 8): " + str(row))
        return False
    ind = 0
    while ind < len(row):
        if type(row[ind]) != float:
            print("Type of element incorrect: " + str(row[ind]) + " which is " + str(type(row[ind])))
            return False
        ind += 1
    return True
	
# define your functions here

def grade_improvement(grade):
    for x in range(len(grade)-1):
        if(grade[x+1]<grade[x]):
            return False
    return True

def grade_outlier(grades):
    test=sorted(grades)
    if test[0]+20<test[1]:
        return True
    else:
        return False

def calculate_score_improved(student):
    score=calculate_score(student)
    outlier=is_outlier(student)
    if score>=6 or outlier:
        return True
    else:
        return False

def is_outlier(student):
    if student[2]==0:
        return True
    elif student[0]/160+2<student[1]*2:
        return True
    else:
        return False

def calculate_score(student):
    score=.3*(student[0]/160)+.4*(student[1]*2)+.1*student[2]+.2*student[3]
    return score

def convert_row_types(student):
    for x in range(len(student)):
        student[x]=float(student[x])

def main():
    # Change this line of code as needed but 
    # make sure to change it back to "superheroes_tiny.csv"
    # before turning in your work!
    filename = "superheroes_tiny.csv"
    input_file = open(filename, "r")    
    
    
    print("Processing " + filename + "...")
    # grab the line with the headers
    headers = input_file.readline()
    
    # TODO: loop through the rest of the file
    rows,names,qualities,semesters=[[],[],[],[]]
    results=open('student_scores.csv', 'w')
    chosen=open('chosen_students.txt', 'w')
    outliers=open('outliers.txt', 'w')

    for line in input_file:
        rows.append(line.strip().split(','))
        x=len(rows)-1
        names.append(rows[x][0])
        rows[x].pop(0)
        convert_row_types(rows[x])
        qualities.append(rows[x][0:4])
        semesters.append(rows[x][4:len(rows[x])])
        score=calculate_score(qualities[x])
        results.write(f"{names[x]},{score:.2f}\n")
        if score>=6:
            chosen.write(f'{names[x]}\n')
        if is_outlier(qualities[x]):
            outliers.write(f'{names[x]}\n')

    # TODO: Part 3 Tasks 3
    improved=open('chosen_improved.txt','w')
    for x in range(len(qualities)):
        score=calculate_score(qualities[x])
        outlier=is_outlier(qualities[x])
        if score>=6:
            improved.write(f'{names[x]}\n')
        elif score>=5 and outlier:
            improved.write(f'{names[x]}\n')

    # TODO: Part 4
    newchosen=open('improved_chosen.csv', 'w')
    for x in range(len(qualities)):
        if calculate_score_improved(qualities[x]):
            newchosen.write('{0},{1},{2},{3},{4}\n'.format(names[x], qualities[x][0], qualities[x][1], qualities[x][2], qualities[x][3]))

    # TODO: Part 5
    final=open('extra_improved_chosen.txt','w')
    for x in range(len(names)):
        score=calculate_score(qualities[x])
        if score>=6:
            final.write(f'{names[x]}\n')
        elif score>=5:
            if is_outlier(qualities[x]):
                final.write(f'{names[x]}\n')
            elif grade_outlier(semesters[x]):
                final.write(f'{names[x]}\n')
            elif grade_improvement(semesters[x]):
                final.write(f'{names[x]}\n')

    # TODO: make sure to close all files you've opened!
    final.close()
    input_file.close()
    results.close()
    outliers.close()
    improved.close()
    print("done!")

# this bit allows us to both run the file as a program or load it as a
# module to just access the functions
if __name__ == "__main__":
    main()