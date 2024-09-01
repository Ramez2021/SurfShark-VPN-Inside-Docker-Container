

import subprocess
import time

class IP_Rotations:
    # Reference : https://support.surfshark.com/hc/en-us/articles/360011051133-How-to-set-up-manual-OpenVPN-connection-using-Linux-Terminal

    # openvpn credintials (auth.txt) : 
    # user : KwWYP9wAp2cFGeCQVb7TAKUx
    # pass : MhvswcwyUrd6bzTpkFzhnLfy

    # for running docker image for vpn rotations you should use :
    # docker run --dns=8.8.8.8 --cap-add=NET_ADMIN --device=/dev/net/tun --name=auto_vpn -it auto_vpn:v1
    
    def setup_connection():
        # Update and install openvpn and unzip the configirations files 
        try : 
            subprocess.run(['apt-get', 'update'], check=True)
            subprocess.run(['apt-get', 'install', '-y', 'openvpn', 'unzip'], check=True)
            
            # Download the Surfshark configuration files
            subprocess.run(['wget', 'https://my.surfshark.com/vpn/api/v1/server/configurations', '-O', 'configurations.zip'], check=True)
            
            time.sleep(120)
                
            # Unzip the downloaded configuration files
            subprocess.run(['unzip', 'configurations.zip'], check=True)
            
        except subprocess.CalledProcessError as e :
            print("file setup_vpn.py failed")
            print(f"error {e}")
            
    def berlin_connection():
        # Start OpenVPN using the specific configuration file
        process = subprocess.Popen(['openvpn', '--config', '/app/de-ber.prod.surfshark.com_tcp.ovpn', '--auth-user-pass', 'auth.txt'])
        return process 

    def frankfourth_connection():   
        process = subprocess.Popen(['openvpn', '--config', '/app/de-fra.prod.surfshark.com_tcp.ovpn', '--auth-user-pass', 'auth.txt'])
        return process 

    def terminate_connection(process):
        process.terminate()
        print(f'\n---->>> Connection Terminated \n' )
        
    def get_ip_address():
        result = subprocess.run(['curl', 'ifconfig.me'], capture_output=True, text=True)
        print(f'\n---->>> Current IP :: {result.stdout}\n' )
            
    def wait_time(sec):
        list_allowd_secounds = [x for x in range(0,sec,10)] # this list for print message every 10 secounds
        for i in range(sec):
            time.sleep(1)
            if i in list_allowd_secounds:
                print(f'Remining Time for swich IP ({sec-i}) secounds')
                IP_Rotations.get_ip_address()
                

    def rotation_manger():
        # IP_Rotations.setup_connection()
        for i in range(10):
            process = IP_Rotations.berlin_connection()
            IP_Rotations.wait_time(300)
            IP_Rotations.terminate_connection(process)
            process = IP_Rotations.frankfourth_connection()
            IP_Rotations.wait_time(300)
            IP_Rotations.terminate_connection(process)
            
        # for _ in range(20):  # for IP Rotation for every 10 minutes - 3 hours 
        #     process = IP_Rotations.berlin_connection()
        #     IP_Rotations.wait_time(600)
        #     IP_Rotations.terminate_connection(process)
            


IP_Rotations.rotation_manger()