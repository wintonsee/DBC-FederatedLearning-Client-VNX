from ssh_connection import communicate
def download_model_from_server(saved_dir):
    f= open("client_model_directory.txt","r")

    line=f.readline()
    while line:


        info=line.strip().split(' ')
        communicate(info[0],info[1],info[2],info[3],saved_dir,info[4])
        line=f.readline()


    f.close()


download_model_from_server('./DBC-Client1')
