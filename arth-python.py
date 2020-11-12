import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import subprocess as sp
import smtplib
import getpass

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# change voice (voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("Hii, How may I help you")     
  

def takeCommand():
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)


    try:
        print("Recognizing...")    
        query = r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query


def sendEmail(whom, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('18erecs013.ashish@rietjaipur.ac.in', 'Ashrad99!')
    server.sendmail('18erecs013.ashish@rietjaipur.ac.in', whom, content)
    server.close()

def remove(string): 
    return string.replace(" ", "")

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)


        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            print("opening youtube")
            speak("opening youtube")

        elif 'open google' in query:
            webbrowser.open("google.com")
            print("opening google")
            speak("opening google")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com") 
            print("opening stack overflow")
            speak("opening stack overflow")  


        elif 'play tv series' in query:
            music_dir = 'F:/entertainment/tv series/12 Monkeys/s1'# put you music dir here
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))
            print("opening youtube")
            speak("opening youtube")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            print(f"the time is {strTime}")
            speak(f"the time is {strTime}")



        elif 'run command' in query:
            speak("what you want to run")
            app = remove(takeCommand())
            x = sp.getoutput("start"+" "+"/MIN"+" "+app)

        

        elif 'send mail' in query:
            try:
                speak("Email Please")
                whom = remove(takeCommand())
                speak("What should I say?")
                content = takeCommand()   
                sendEmail(whom, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("There is some issue Try manually")   



##############################################  Hadoop Script start ##################################################################################       

        elif 'setup hadoop' in query:
            speak("your master node ip")
            masterIp = input("Enter your Aws instance IP : ").replace(".", "-")
            passMaster = input("pem file name : ")
            speak("1 to setup namenode  or 2 to run name node")
            value = int(input('''1 to setup namenode:\n 2 to run name node: '''))
            if value == 2:
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo hadoop-daemon.sh start namenode'.format(passMaster, masterIp))
            elif value == 1:     
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo yum install wget -y'.format(passMaster, masterIp))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /home/hadoop-1.2.1-1.x86_64.rpm https://jokker99.s3.ap-south-1.amazonaws.com/hadoop-1.2.1-1.x86_64.rpm'.format(passMaster, masterIp))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /home/jdk-8u171-linux-x64.rpm https://jokker99.s3.ap-south-1.amazonaws.com/softwares/jdk-8u171-linux-x64.rpm'.format(passMaster, masterIp))
                print(os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo rpm -ivh /home/jdk-8u171-linux-x64.rpm'.format(passMaster, masterIp)))
                print(os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo rpm -ivh /home/hadoop-1.2.1-1.x86_64.rpm --force'.format(passMaster, masterIp)))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /etc/hadoop/core-site.xml https://jokker99.s3.ap-south-1.amazonaws.com/master+node/core-site.xml'.format(passMaster, masterIp))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /etc/hadoop/hdfs-site.xml https://jokker99.s3.ap-south-1.amazonaws.com/master+node/hdfs-site.xml?versionId=OJ19K5SOxNfzBg34ykHCPJdNqsIZ2XdR'.format(passMaster, masterIp))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo mkdir /master'.format(passMaster, masterIp))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo hadoop namenode -format -force'.format(passMaster, masterIp))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo hadoop-daemon.sh start namenode'.format(passMaster, masterIp))
            else:
                speak("option not aviliable")
                print("option not aviliable")


            with open('core-site.xml') as f:
                rewrite=f.read().replace('0.0.0.0', masterIp.replace("-","."))
            with open('core-site.xml', "w") as f:
                f.write(rewrite)
            os.system('aws s3 cp core-site.xml s3://jokker99/core-site/ --acl public-read')
            
##---------------------------------------------------------------------------------------------------------------------------------------------##               
            speak("How many nodes do you have")
            listOfNodes = []
            
            no_of_node = int(input("How many nodes do you have: "))
            nodepass = input("pem file name : ")

            for i in range(no_of_node):
                nodeIp = input("Enter your Aws instance IP : ").replace(".", "-")
                listOfNodes.append(nodeIp)


            speak("ENTER YOUR partition size")
            size = input("ENTER YOUR partition size in G for GB and M for MB : ")
            

            

            for i in range(0,no_of_node):
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo yum install wget lvm2 -y'.format(nodepass, listOfNodes[i]))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /home/hadoop-1.2.1-1.x86_64.rpm https://jokker99.s3.ap-south-1.amazonaws.com/hadoop-1.2.1-1.x86_64.rpm'.format(nodepass, listOfNodes[i]))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /home/jdk-8u171-linux-x64.rpm https://jokker99.s3.ap-south-1.amazonaws.com/softwares/jdk-8u171-linux-x64.rpm'.format(nodepass, listOfNodes[i]))
                print(os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo rpm -ivh /home/jdk-8u171-linux-x64.rpm'.format(nodepass, listOfNodes[i])))
                print(os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo rpm -ivh /home/hadoop-1.2.1-1.x86_64.rpm --force'.format(nodepass, listOfNodes[i])))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /etc/hadoop/core-site.xml https://jokker99.s3.ap-south-1.amazonaws.com/core-site/core-site.xml'.format(nodepass, listOfNodes[i]))  
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo mkdir /slave'.format(nodepass, listOfNodes[i]))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /etc/hadoop/hdfs-site.xml https://jokker99.s3.ap-south-1.amazonaws.com/datanode/hdfs-site.xml'.format(nodepass, listOfNodes[i]))
                lvm1 = sp.getstatusoutput('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo fdisk -l | grep -o /dev/xvd[f-p]"'.format(nodepass, listOfNodes[i]))
                lvm2 =  sp.getstatusoutput('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo fdisk -l | grep -o /dev/sd[f-p]"'.format(nodepass, listOfNodes[i]))

                if lvm1[0] == 0:
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo pvcreate {}"'.format(nodepass, listOfNodes[i],lvm1[1]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo pvdisplay {}"'.format(nodepass, listOfNodes[i],lvm1[1]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo vgcreate arth {}"'.format(nodepass, listOfNodes[i],lvm1[1]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo vgdisplay arth"'.format(nodepass, listOfNodes[i]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo lvcreate --size {} --name task arth"'.format(nodepass, listOfNodes[i],size))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo lvdisplay  arth/task"'.format(nodepass, listOfNodes[i]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo mkfs.ext4 /dev/arth/task"'.format(nodepass, listOfNodes[i]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo mount /dev/arth/task /slave"'.format(nodepass, listOfNodes[i]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo hadoop-daemon.sh start namenode'.format(nodepass, listOfNodes[i]))
                    speak("Lvm integrated to slave node")
                

                elif lvm2[0] == 0:
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo pvcreate {}"'.format(nodepass, listOfNodes[i],lvm2[1]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo pvdisplay {}"'.format(nodepass, listOfNodes[i],lvm2[1]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo vgcreate arth {}"'.format(nodepass, listOfNodes[i],lvm2[1]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo vgdisplay arth"'.format(nodepass, listOfNodes[i]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo lvcreate --size {} --name task arth"'.format(nodepass, listOfNodes[i],size))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo lvdisplay  arth/task"'.format(nodepass, listOfNodes[i]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo mkfs.ext4 /dev/arth/task"'.format(nodepass, listOfNodes[i]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com "sudo mount /dev/arth/task /slave"'.format(nodepass, listOfNodes[i]))
                    os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo hadoop-daemon.sh start namenode'.format(nodepass, listOfNodes[i]))
                    speak("Lvm integrated to slave node")

                else:
                    speak("your s3 is not connected to the datanode")
                    pass

##---------------------------------------------------------------------------------------------------------------------------------------------## 
            speak("How many clients do you have")
            listOfClients = []
            no_of_clients = int(input("How many clients do you have: "))
            clientspass = input("pem file name : ")
            for j in range(no_of_clients):
                ClientIp = input("Enter your Aws instance IP : ").replace(".", "-")
                listOfClients.append(ClientIp)
    
            for i in range(0,no_of_clients):   
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo yum install wget -y'.format(clientspass, listOfClients[i]))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /home/hadoop-1.2.1-1.x86_64.rpm https://jokker99.s3.ap-south-1.amazonaws.com/hadoop-1.2.1-1.x86_64.rpm'.format(clientspass, listOfClients[i]))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /home/jdk-8u171-linux-x64.rpm https://jokker99.s3.ap-south-1.amazonaws.com/softwares/jdk-8u171-linux-x64.rpm'.format(clientspass, listOfClients[i]))
                print(os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo rpm -ivh /home/jdk-8u171-linux-x64.rpm'.format(clientspass, listOfClients[i])))
                print(os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo rpm -ivh /home/hadoop-1.2.1-1.x86_64.rpm --force'.format(clientspass, listOfClients[i])))
                os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo wget -O /etc/hadoop/core-site.xml https://jokker99.s3.ap-south-1.amazonaws.com/core-site/core-site.xml'.format(clientspass, listOfClients[i]))
            ##################################
                os.system("aws s3 rm s3://jokker99/core-site/core-site.xml")

            with open('core-site.xml') as f:
                rewrite=f.read().replace(masterIp.replace("-","."),'0.0.0.0')
            with open('core-site.xml', "w") as f:
                f.write(rewrite)
    


####################################################### End of hadoop script #########################################################################
######################################################## LVM START #####################################################################            
        elif 'resize lvm' in query:
            speak("Enter your key")
            nodepass = input("Enter you key")
            speak("ENTER YOUR IP Adress")
            ip = input ("ENTER YOUR IP Adress : ").replace(".", "-")
            speak("Enter size to extend")
            size = input("Enter size to extend : ")
            speak("Enter YOUR partion path")
            lv_path = input("Enter YOUR partion path : ")

            os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo lvextend --size +{} {}'.format(nodepass, ip, size, lv_path))
            os.system('ssh -i "{}" ec2-user@ec2-{}.ap-south-1.compute.amazonaws.com sudo sudo resize2fs {}'.format(nodepass, ip, lv_path))
            speak("L v m rsized")
            print("Lvm resized")
            
#########################################  LVM  End #################################################################################
##############################################   Docker Start  ###################################################################3

        elif 'docker' in query:

            speak("enter ip where you want to perform these operations")
            ip = input("enter ip where you want to perform these operations : ")

            
            os.system('ssh-keygen')

            speak("Provide your ssh-keygen file name you provided")
            key = input("Provide your ssh-keygen file name you provided : ")

            os.system('type {}.pub | ssh root@{} "mkdir -p .ssh; cat > .ssh/authorized_keys; chmod 700 .ssh; chmod 640 .ssh/authorized_keys"'.format(key,ip))

            os.system('ssh -i "{}" root@{} dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo'.format(key,ip))
            

            os.system('ssh -i "{}" root@{} sudo "yum install docker-ce --allowerasing --nobest -y ; systemctl enable docker ; systemctl start docker ; docker images"'.format(key,ip))
            
            speak("Enter Image name")
            osimage = input("Enter Image name : ")
            
            speak("enter name you want to give to your os")
            osname = input("enter name you want to give to your os : ")
            speak("speak install image to install docker image")


            if 'install image' in query:
                speak("Enter Image name to install")
                installimg = input("Enter Image name to install : ")
                os.system('ssh -i "{}" root@{} "sudo docker pull {}"'.format(key,ip,installimg))
            
            os.system('ssh -i "{}" root@{} "sudo docker create -it --name {} {}"'.format(key,ip, osname,osimage))
            os.system('ssh -i "{}" root@{} "sudo docker start {}"'.format(key,ip, osname,))            
            os.system('ssh -i "{}" root@{} "sudo docker ps"'.format(key,ip))


            os.system('ssh -i "{}" root@{} "sudo docker exec -it {} yum install python36 -y"'.format(key,ip, osname))
            os.system('ssh -i "{}" root@{} "sudo docker exec -it {} yum install httpd -y'.format(key,ip,osname))
            os.system('ssh -i "{}" root@{} "sudo docker exec -it {} sytemctl start httpd'.format(key,ip,osname))
            os.system('ssh -i "{}" root@{} "sudo docker exec -it {}  /usr/sbin/httpd'.format(key,ip,osname))

            speak("webserver configured")


########################################################  docker ended ########################################################################
###################################################   AWS STARTED   ########################################################################

        elif 'a w s' in query:
            speak("Welcome To the Menu Program of A W S")
            print("................................//Welcome To the Menu Program of AWS//.............................")
            speak("create key pair")
            print("create key pair")
            speak("delete key pair")
            print("delete key pair")
            speak("create EBS volume")
            print("create EBS volume")
            speak("delete EBS volume")
            print("delete EBS volume")
            speak("create security group")
            print("create security group")
            speak("delete security group")
            print("delete security group")
            speak("Launch instance")
            print("Launch instance")
            speak("attach EBS volume to instance")
            print("attach EBS volume to instance")
            speak("create S3 bucket")
            print("create S3 bucket")
            speak("delete bucket")
            print("delete bucket")
            speak("place object inside S3")
            print("place object inside S3")
            speak("stop instance")
            print("stop instance")
            speak("start instance")
            print("start instance")
            speak("terminate instance")
            print("terminate instance")
            speak("speak your choice of program")
            print("speak your choice of program")
            
            
            while True:
                option = takeCommand().lower()
                if "create key pair" in option:
                    speak("Enter a key name")
                    print("Enter a key name:- ", end='')
                    key_name = input()
                    os.system("aws ec2 create-key-pair --key-name {}".format(key_name))

                elif 'delete key pair' in option:
                    speak("Enter the name of key to be deleted")
                    print("Enter the name of key to be deleted:- ",end='')
                    speak("Note that the key will be deleted permanently, if you agree then proceed")
                    print("Note that the key will be deleted permanently, if you agree then proceed!!",end='')
                    key_name = input()
                    os.system("aws ec2 delete-key-pair --key-name {}".format(key_name))
                    speak("Your desired key has been deleted successfully")
                    print("Your desired key has been deleted successfully....")

                elif 'create e b s volume' in option:
                    speak("Enter the size of the volume size in GB to be created")
                    print("Enter the size of the volume size in GB to be created:- ",end='')
                    size = input()
                    speak("Enter the availability zone that you wish to choose")
                    print("Enter the availability zone that you wish to choose:- ",end='')
                    AZ = input()
                    os.system("aws ec2 create-volume --availability-zone {} --size {}".format(AZ , size))

                elif 'delete e b s volume' in option:
                    speak("type your volume ID")
                    print("type your volume ID", end='')
                    vol_id = input()
                    os.system("aws ec2 delete-volume --volume-id {}".format(vol_id)) 

                elif 'create security group' in option:
                    speak("Enter the security group name")
                    print("Enter the security group name:- ",end='')
                    SG_name = input()
                    speak("Enter the description to be given")
                    print("Enter the description to be given:- ",end='')
                    description = input()
                    speak("Enter the VPC Id")
                    print("Enter the VPC Id:- ",end='')
                    VPC_Id = input()
                    os.system("aws ec2 create-security-group --group-name {} --description {} --vpc-id {}".format(SG_name , description , VPC_Id))

                elif 'delete security group' in option:
                    speak("Enter the security group id that you wish to delete")
                    print("Enter the security group id that you wish to delete:- ",end='')
                    sg_id = input()
                    os.system("aws ec2 delete-security-group --group-id {}".format(sg_id))

                elif 'launch instance' in option:
                    speak("Enter your AMI id for your instance")
                    print("Enter your AMI id for your instance:- ",end='')
                    ami_id = input()
                    speak("Enter the type of instance you wish to launch prefering t2.micro")
                    print("Enter the type of instance you wish to launch(prefering t2.micro):- ",end='')
                    instance_type = input()
                    speak("Enter the count of instances to be launched")
                    print("Enter the count of instances to be launched:- ",end='')
                    count = input()
                    speak("Enter your security group ID")
                    print("Enter your security group ID:- ",end='')
                    SG_ID =input()
                    speak("Enter the key to be attached to your instance")
                    print("Enter the key to be attached to your instance:- ",end='')
                    key = input()
                    speak("Your instance is launching")
                    print("Your instance is launching.......")
                    os.system("aws ec2 run-instances --image-id {} --instance-type {} --count {} --security-group-ids {} --subnet-id subnet-d97a78b1 --key-name {}".format(ami_id , instance_type , count , SG_ID , key))

                elif 'attach e b s volume to instance' in option:
                    speak("Enter the EBS volume ID to be attached to the instance launched")
                    print("Enter the EBS volume ID to be attached to the instance launched:- ",end='')
                    EBS_ID = input()
                    speak("Enter the Instance ID for the volume attaching")
                    print("Enter the Instance ID for the volume attaching:- ",end='')
                    Instance_ID = input()
                    os.system("aws ec2 attach-volume --volume-id {} --instance-id {} --device /dev/sdf".format(EBS_ID , Instance_ID))

                elif 'create S3 bucket' in option:
                    speak("Print a unique bucket name for yourself")
                    print("Print a unique bucket name for yourself:- ",end='')
                    Bucket_name = input()
                    speak("Enter the region where you wish to create your bucket")
                    print("Enter the region where you wish to create your bucket:- ",end='')
                    region_name = input()
                    os.system("aws s3api create-bucket --bucket {} --region {}".format(Bucket_name , region_name))
                        
                elif 'delete bucket' in option:
                    speak("Enter the name of the bucket to be deleted")
                    print("Enter the name of the bucket to be deleted") 
                    Bucket_name = input()
                    speak("Enter the region name whose bucket you wish to delete")
                    print("Enter the region name whose bucket you wish to delete:- ",end='')
                    region_name = input()
                    os.system("aws s3api delete-bucket --bucket {} --region {}".format(Bucket_name , region_name))

                elif 'place object inside S3' in option:
                    speak("Enter the name of object to be placed inside S3")
                    print("Enter the name of object to be placed inside S3:- ",end='')
                    object_name = input()
                    speak("Enter the name of the bucket")
                    print("Enter the name of the bucket")
                    Bucket_name = input()
                    os.system("aws s3 cp /root/{} s3://{} --ac1 public-read".format(object_name , Bucket_name))


                elif 'stop instance' in option:
                    speak("Enter the instance Id that you wish to stop")
                    print("Enter the instance Id that you wish to stop:- ",end='')
                    Instance_ID = input()
                    os.system("aws ec2 stop-instances --instance-ids {}".format(Instance_ID))

                elif 'start instance' in option:
                    speak("Enter the instance id for starting the instance")
                    print("Enter the instance id for starting the instance:- ",end='')
                    Instance_ID = input()
                    os.system("aws ec2 start-instances --instance-ids {}".format(Instance_ID))

                elif 'terminate instance' in option:
                    speak("Enter the instance id for terminating the instance")
                    print("Enter the instance id for terminating the instance:- ",end='')
                    Instance_ID = input()
                    os.system("aws ec2 terminate-instances --instance-ids {}".format(Instance_ID))
                        
                else:

                    speak("Command not found....")
                    print("Command not found....")
                    speak("Try again")
                    print("Try again")
                    exit()

        elif "exit" in query:
            exit()
                