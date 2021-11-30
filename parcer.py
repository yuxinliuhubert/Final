
import time
def gm_time_processor1(string):
    string = str(string)
    # drop_index = string.find(', 1, 332)')
    string = string[0:len(string)-9]
    print(string)
    string = string.replace('(','')
    string = string.replace(')','')
    # print(string)
    for j in range (1,6):
        index = string.find(' ')
        string = "{}{}".format(string[0 : index],string[index + 1 : :])
        # string = string[0 : index] + string[index + 1 : :]

    for i in range (1,6):
        index = string.find(',')
        # print(index)
        if i <= 2:
            # string = string[0 : index] +"/"+string[index + 1 : :]
            string = "{}/{}".format(string[0 : index],string[index + 1 : :])

        elif i <= 3:
            # string = string[0 : index] +" "+ string[index + 1 : :]
            string = "{} at {}".format(string[0 : index],string[index + 1 : :])
        else:
            # string = string[0 : index] +":"+string[index + 1 : :]
            string = "{}:{}".format(string[0 : index], string[index + 1 : :])
    return string


# def utc_2_pst(utctime):


string = time.gmtime()
print(string[1])
result = gm_time_processor1(string)
print(result)
