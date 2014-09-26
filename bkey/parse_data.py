from collections import defaultdict

#parses data from 
def get_sex(field):
    if field == "1":
        return "Male"
    elif field == "2":
        return "Female"
    else:
        return "Unknown"

#this will fail if not found
def get_relationship(field):
    return {
        "0101": "Head/householder",
        "0201": "Spouse",
        "0301": "Child",
        "0303": "Stepchild",
        "0501":	"Parent",
        "0701":	"Sibling",
        "0901":	"Grandchild",
        "1001": "Other relatives",
        "1113":	"Partner/roommate",
        "1114":	"Unmarried partner",
        "1115":	"Housemate/roomate",
        "1241":	"Roomer/boarder/lodger",
        "1242":	"Foster children",
        "1260":	"Other nonrelatives",
        "9100":	"Armed Forces relationship unknown",
        "9200":	"Age under 14 relationship unknown",
        "9900":	"Relationship unknown",
        "9999": "Unknown"		
    }[field]     

def get_marital_status(field):
    return {
        "1": "Married spouse present",
        "2": "Married spouse absent",
        "3": "Separated",
        "4": "Divorced",
        "5": "Widowed",
        "6": "Never married/single",
        "9": "Unknown"
    }[field]

def get_work_class(field):
    return {
        "00": "NIU",
        "10": "Self-employed",
        "13": "Self-employed not incorporated",
        "14": "Self-employed incorporated",
        "20": "Works for wages or salary",
        "21": "Wage/salary private",
        "22": "Private for profit",
        "23": "Private nonprofit",
        "24": "Wage/salary government",
        "25": "Federal government employee",
        "26": "Armed forces",
        "27": "State government employee",
        "28": "Local government employee",
        "29": "Unpaid family worker",
        "99": "Missing/Unknown"
    } [field]

def get_fulltime(field):
    if field == "0":
        return "NIU"
    elif field == "1":
        return "Full-time"
    elif field == "2":
        return "Part-time"
    elif field == "9":
        return "Unknown"
    else:
        print "error " + field
        return "really unknown"

def do_field_transform(field, field_name, keep_raw):
    if keep_raw:
        return feild
    else:
        if field_name == "relationship":
            return get_relationship(field)
        elif field_name == "sex":
            return get_sex(field)
        elif field_name == "marital_status":
            return get_marital_status(field)
        elif field_name == "worker_class":
            return get_work_class(field)
        elif field_name == "fulltime":
            return get_fulltime(field)
        else:
            return field #error?


def read_from_txt(filename, keep_raw):
    house_dict = defaultdict(list)

    with open(filename, "r") as f, open("adults.txt", "w") as outfile:
        for line in f:
            line_list = []
            house_list = []
            
            serial = line[4:9]

            house_list.append(serial) #serial
            line_list.append(serial)

            house_list.append(line[23:33]) #house wgt
            house_list.append(line[19:21]) #fip
            house_list.append(line[21:25]) #metro area
            house_list.append(line[25:30]) #county

            house_dict[serial] = house_list


            line_list.append(line[32:34]) #person number

            line_list.append(line[34:44]) #person wgt

            line_list.append(do_field_transform(line[44:48], "relationship", keep_raw)) #relationship
            age = line[48:50]
            line_list.append(age) #age
            line_list.append(do_field_transform(line[50], "sex", keep_raw)) #sex
            line_list.append(line[51:54]) #race
            line_list.append(do_field_transform(line[54], "marital_status", keep_raw)) #marital status
            line_list.append(line[55:60]) #origin
            line_list.append(line[60:63]) #education
            line_list.append(line[63:65]) #employ status
            line_list.append(line[65:69]) #occupation
            line_list.append(line[69:73]) #industy
            
            line_list.append(do_field_transform(line[73:75], "worker_class", keep_raw)) #worker class
            line_list.append(line[75:77]) #weeks worked
            line_list.append(line[77:79]) #hours worked

            #line_list.append(line[79])
            line_list.append(do_field_transform(line[79], "fulltime", keep_raw)) #full/part

            line_list.append(line[80:]) #income

            outfile.write(",".join(line_list)[:-2] + '\n')

    with open("households.txt", "w") as housefile:
        for k,v in house_dict.iteritems():
            housefile.write(",".join(v) + '\n')
        housefile.close()

        f.close()

if __name__ == "__main__": 
    read_from_txt("cps_00004.dat", False)
 
