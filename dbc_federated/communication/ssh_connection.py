import paramiko
import os
import zipfile
from tqdm import tqdm
#ssh_client=paramiko.SSHClient()
#ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh_client.connect(hostname='114.115.219.202',username='root', port=20050,password='12345678')

#Downloading a file from remote machine

#ftp_client=ssh_client.open_sftp()
#ftp_client.get('remotefileth','localfilepath')
#ftp_client.close()

#Uploading file from local to remote machine

#ftp_client=ssh_client.open_sftp()
#ftp_client.put('/home/brian/Desktop/upload_demo','./upload_demo')
#ftp_client.close()



# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
 
    # setup file paths variable
    filePaths = []
   
    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dirName):
        for filename in files:
            # Create the full filepath by using os module.
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
         
    # return all paths
    return filePaths
  
def viewBar(a,b):
    # original version
    res = a/int(b)*100
    sys.stdout.write('\rComplete precent: %.2f %%' % (res))
    sys.stdout.flush()

def tqdmWrapViewBar(*args, **kwargs):
    try:
        from tqdm import tqdm
    except ImportError:
        # tqdm not installed - construct and return dummy/basic versions
        class Foo():
            @classmethod
            def close(*c):
                pass
        return viewBar, Foo
    else:
        pbar = tqdm(*args, **kwargs)  # make a progressbar
        last = [0]  # last known iteration, start at 0
        def viewBar2(a, b):
            pbar.total = int(b)
            pbar.update(int(a - last[0]))  # update pbar with increment
            last[0] = a  # update last known iteration
        return viewBar2, pbar  # return callback, tqdmInstance
  
def communicate(hostname,username,port,password,folder_dir,target_dir):
    
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname,username=username, port=port,password=password)
    ftp_client=ssh_client.open_sftp()
    
    filePaths = retrieve_file_paths(folder_dir)
   
    # printing the list of all files to be zipped
    print('The following list of files will be zipped:')
    for fileName in filePaths:
        print(fileName)
    folder_name=folder_dir.split('/')[-1] 
    # writing files to a zipfile
    zip_file = zipfile.ZipFile(folder_name+'.zip', 'w')
    with zip_file:
        # writing each file one by one
        for file in filePaths:
            zip_file.write(file)
       
    print(folder_dir+'.zip file is created successfully!')
    cbk, pbar = tqdmWrapViewBar(ascii=True, unit='b', unit_scale=True)  
    
    ftp_client.put(folder_dir+'.zip','./'+target_dir+'/'+folder_name+'.zip',callback=cbk)
                       #ftp_client.put(folder_dir+'.zip','./'+target_dir+'/'+folder_name+'.zip',callback=cbk)
    print("-----------done with uploading-----------------") 
    pbar.close()
    stdin, stdout, stderr = ssh_client.exec_command("cd "+target_dir)
    stdin, stdout, stderr = ssh_client.exec_command("unzip "+folder_name+".zip")
    stdin, stdout, stderr = ssh_client.exec_command("rm "+folder_name+".zip")
    
    ftp_client.close()   
    
