import os                           # File System Methods
import time                         # Time Conversion Methods
import sys                          # System Methods
import hashlib                      # Python standard library hashlib

from prettytable import PrettyTable # Pretty Table

if __name__ == '__main__':

    targetDirectory = input("Enter Directory to Walk: ")
    targetExtension = input("Enter File Extension to Match: ")
    targetFilename = input("Enter Filename to Match: ")
    targetHash = input("Enter Hash to Match: ")
    
    tbl = PrettyTable(['HASHMATCH', 'EXTMATCH', 'PATHMATCH', 'AbsPath', 'FileSize', 'LastModified', 'LastAccess', 'CreatedTime', 'HASH']) # Table creation with parameters
    
    if not os.path.isdir(targetDirectory):
        sys.exit("Invalid Directory: ", targetDirectory)
        
    try:
        
        for root, dirList, fileList in os.walk(targetDirectory):
            for nextFile in fileList:
            
                fullPath                = os.path.join(root, nextFile) 
                absPath                 = os.path.abspath(fullPath)
                metaData                = os.stat(absPath) 
                fileSize                = metaData.st_size 
                timeLastAccess          = metaData.st_atime
                timeLastModified        = metaData.st_mtime
                timeCreated             = metaData.st_ctime
                utcTimeLastAccess       = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeLastAccess))
                utcTimeLastModified     = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeLastModified))
                utcTimeCreated          = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeCreated))
                fileName, fileExtension = os.path.splitext(nextFile)
                fileExtension           = fileExtension[1:]
                hashMatch               = "No"
                extMatch                = "No"
                pathMatch               = "No"
                
                if fileExtension == targetExtension or "." + fileExtension == targetExtension:
                    extMatch = "Yes"
                    
                if fileName.lower() == targetFilename.lower():
                    pathMatch = "Yes"
                
                # Hashing Files
                
                with open(absPath, 'rb') as target:
                    
                    fileContents = target.read()
                    
                    sha256Obj = hashlib.sha256()
                    sha256Obj.update(fileContents)
                    hexDigest = sha256Obj.hexdigest()
                    
                    if hexDigest == targetHash:
                        hashMatch = "Yes"
                        
                if hashMatch == "Yes" or extMatch == "Yes" or pathMatch == "Yes":
                    tbl.add_row([hashMatch, extMatch, pathMatch, absPath, fileSize, utcTimeLastModified, utcTimeLastAccess, utcTimeCreated, hexDigest])    
    
        print(f"\n\nSearching {targetDirectory} ...\n")
        print(f"File Extension  : {targetExtension}")
        print(f"Filename        : {targetFilename}")
        print(f"File Hash       : {targetHash}")
        
        # Table Formatting
        
        tbl.align = 'l'
        print(tbl.get_string(sortby='FileSize', reversesort=True))
        
    except Exception as err:
        print("\n\nScript Aborted     ", "Exception =     ", err)
