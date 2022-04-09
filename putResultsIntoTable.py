import pandas as pd
import os

# The frozen layer number will be appended at the end 
# of this e.g. "output_maskrcnn_freeze_1"
folderName = "output_maskrcnn_freeze_" 
resultsFile = "rawResults.json"

#=====================================================
# This will create an overleaf table starting from 
# 'start' until 'end', and will save the table in a  
# text file called "saveFile" in the folder "Tables"  
# (which will be created if it doesn't exist).
#=====================================================
def getResults(start, end, saveFile):

    cont_df = pd.DataFrame()

    # Go through each folder for each number of frozen layers 1-5
    for freezeNum in range(1,6):

        # Get the json file
        fileName = folderName+str(freezeNum)+"/"+resultsFile
        with open(fileName) as f:
            contents = f.read()
            f.close()
        
        # Get rid of junk
        contents = contents.replace(" \"segm\": {", "")
        contents = contents.lstrip("{\"bbox\": {, {")
        contents = contents.rstrip("})])")
        contents = contents.replace("{","")
        contents = contents.replace("}","")

        # Format the results into a list
        listCont = contents.split(",")

        catList = [] # All categories
        valList = [] # All values

        for pos in range(start,end):
            item = listCont[pos]
            split = item.split(":") # split on colons in string
            catList.append(split[0]) # Add next category to list

            # 3 decimal places
            if "NaN" not in split[1] :
                split[1] = str(round(float(split[1]),3))

            valList.append(split[1]) # Add next value to list

        # Get rid of useless characters
        catList = [s.replace("'", "") for s in catList]
        catList = [s.replace("\"", "") for s in catList]
        catList = [s.replace("AP-", "") for s in catList]
        catList = [s.replace("}", "") for s in catList]
        catList = [s.replace(")", "") for s in catList]

        valList[len(valList)-1] = valList[len(valList)-1].rstrip("})")

        if cont_df.empty:
            # Convert into dataframe
            cont_df = pd.DataFrame(
                {'category': catList, 'Freeze1': valList})
            cont_df = cont_df.set_index('category')
        else:
            cont_df["Freeze" + str(freezeNum)] = valList

    print(cont_df)

    # AP table, so transpose
    if start == 0 or start == 86:
        cont_df = cont_df.transpose()

    # Convert df to overleaf table
    overleafTable = cont_df.to_latex(index=True)

    # Create Tables folder if it doesn't exist
    if not os.path.exists("Tables"):
        os.makedirs("Tables")
        print("Tables folder created")

    # Save the overleaf table to a txt file
    with open("Tables/"+saveFile, "w") as f:
        f.write(overleafTable)


# List of start and end positions for each table
tableList = [0,6,86,92,172]

# List of file names to save the tables
savefileNameList = ["bboxAP.txt", "bboxCat.txt","segAP.txt", "segCat.txt"]

# Create 4 tables
for i in range(0,len(tableList)-1):
    getResults(tableList[i], tableList[i+1], savefileNameList[i])


# box: 0
# person: 6, 92
# seg: 86

# Table 1: 0 - 6
# Table 2: 6 - 86
# Table 3: 86 - 92
# Table 4: 92 - 172