from time import sleep
import requests
import csv
import os
import warnings
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)


### Configuração Cofre ###
ip_cofre       = 'ip do cofre'
url_cofre      = f'https://{ip_cofre}/BeyondTrust/api/public/v3'
workgroupname  = "BeyondTrust Workgroup"
##########################


### Configuração API ###
chave_api = 'xxxxx'
user      = 'user'
headers   = {'Authorization': f'PS-Auth key={chave_api};' f'runas={user};'}

datype  = {'Content-type': 'application/json'}
proxy   = {'http': None,'https': None}
########################


################# Persistencia de Login #################
session             = requests.session()
session.proxies     = proxy
session.trust_env   = False
session.verify      = False
session.headers.update(headers)
#########################################################


################# LogIn #################################
def PostLogIn():
    
    login = session.post(url = f'{url_cofre}/Auth/SignAppin', verify = False) 
    
    info_login = login.json()
    
    userid      = info_login['UserId']
    username    = info_login['UserName']
    name        = info_login['Name']
    
    os.system('cls')
    print('\nLogin Feito com Sucesso! - Codigo =', login.status_code)
    print('\nUserId..:', userid, 
          '\nUserName:', username, 
          '\nName....:', name)
    print()
#########################################################


################# Puxar informações de todos os Assets ##############################
def Get_Assets_by_Name():
    
    cont = 0
    
    with open (r'C:\Users\wsantos\Documents\PortoWorkstation\Assets\.porto.csv') as arquivo:
        
        reader = csv.DictReader(arquivo)
        
        for row in reader:
            sleep(1)
            
            name = row['Name']
    
            url_asset   = url_cofre + f'/Workgroups/{workgroupname}/Assets?name={name}'
            get_asset   = session.get(url = url_asset, verify = False) 
            
            if (get_asset.status_code > 399):
                with open('.falseassets.csv', 'a') as arquivo:
                    arquivo.write(f'{name}\n')
                    
                    print(cont, name)
                    cont += 1
#################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify = False)  

    print('\nUsuario acabou de sair da sessao! - Codigo =', logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Get_Assets_Compair_by_Name()
    PostLogOff()
   
if __name__ == '__main__': 
    main()
