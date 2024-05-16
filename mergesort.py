import sys

def print_out(lns,output):
    with open(output,'w') as outpt:
        for ln in lns:
            outpt.write(f'{ln}\n')

def merger(l1,l2):
    def merger_helper(l1,l2):
        print(l1,"\n",l2)
        if int(l2[0])<int(l1[0]):
            return l2.pop(0)
        else:
            return l1.pop(0)
    
    result=[]
    while l1!=[] and l2!=[]:
        result.append(merger_helper(l1,l2))
    if l1==[]:
        result+=l2
    else:
        result+=l1
    return result
        
def sorting(lst):
    if len(lst)==1:
        return lst
    if len(lst)==2:
        if int(lst[0])>int(lst[1]):
            return [lst[1],lst[0]]
        else:
            return lst
    else:    
        firsthalf=lst[:len(lst)//2]
        secondhalf=lst[len(lst)//2:]
        firsthalf=sorting(firsthalf)
        secondhalf=sorting(secondhalf)
        lst=merger(firsthalf,secondhalf)
        return lst




if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        lines=[]
        for line in f:
            lines.append(line.strip())
        lst_sorted=sorting(lines)
        print_out(lst_sorted,sys.argv[2])