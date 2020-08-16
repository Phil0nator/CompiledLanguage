

def include(file_indicator, data,cc):
    if(file_indicator.startswith("\"")):
        with open(file_indicator.replace("\"",""), "rb") as f:
            
            return pre_process(f.read().decode(),cc)














def pre_process(data,cc):
    lines = data.split("\n")
    i =0
    for line in lines:
        if(line.startswith("#")):
            if(line[1:8] == "include"):
               lines[i]=include(line.split(" ")[1],data,cc)
            elif(line[1:7] == "define"):
                cc["DEF"][line.split(" ")[1]] = line.split(" ")[2]
                lines[i] = ""




            else:
                print("Unkown Preprocessor Directive: "+line)
                exit(1)
        i+=1

    data = ""
    for line in lines:
        data+=line+"\n"
    return data
