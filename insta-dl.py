import threading
import time
import os
import sys
import json
import hashlib
import re
import requests

try:
    from bs4 import BeautifulSoup as soup
    import pyperclip
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except:
    print('These packages must be installed: bs4 pyperclip colorama\nIn your command line type: pip install bs4 pyperclip colorama')
    sys.exit()

# ---------------------- change this ------------
# set these variables according to your preference

HOME = '.../instagram'
TMP = '/tmp/tmp_insta'
# -----------------------------------------------

args = ' '.join(sys.argv[1:])
atual = os.getcwd()
shutdown = False
lista_url = []
baixadas = []
num = 1
COR1 = Back.WHITE + Fore.BLACK
COR2 = Back.YELLOW + Fore.BLACK
COR3 = Back.RED + Fore.WHITE
COR4 = Fore.WHITE + Style.BRIGHT

# Check if there are files not downloaded and convert them into a list called "lista_tmp"
if os.path.exists(TMP):
    with open(TMP, 'r') as f:
        lista_tmp = f.read().split(',')
        lista_tmp = [ i for i in lista_tmp if i is not '' ]
        if len(lista_tmp) == 0:
            print('Problemas com urls:', lista_tmp)

def bool_check(val):
    return True if val == 'true' else False

def baixar(onde=HOME, item=None):
    global num
    if item is not None:
        url = item

    with requests.Session() as s:
        problema = False
        r = s.get(url)
        if r.status_code == 404:
            problema = True
            print('404 STATUS CODE')
        else:
            html = soup(r.text, "html.parser")
            script_java = html.select('script[type="text/javascript"]')[3]
            if not bool_check(re.findall('"is_private":([^,]*),', script_java.get_text())[0]):
                try:
                    converted = json.loads(script_java.text[21:-1])
                    main_dict = converted['entry_data']['PostPage'][0]['graphql']['shortcode_media']
                    video = converted['entry_data']['PostPage'][0]['graphql']['shortcode_media']['is_video']
                    username = converted['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username']
                except (IndexError, KeyError):
                    print(COR3 + ' ERRO: url provavelmente inválida, não contém <div> com atributo "script" ')
                    problema = True
            else:
                print(COR2 + ' Conta privada ')
                problema = True

        def download(link, url=False):
            global num
            hash_object = hashlib.sha256(link.encode())
            hex_hash = hash_object.hexdigest()
            nome = onde + '/' + username + '_' + hex_hash[::5] + ext
            if not os.path.exists(nome):
                with open(nome, 'wb') as f:
                    file = s.get(link)
                    try:
                        f.write(file.content)
                        print(num, nome)
                        num += 1
                    except:
                        print('\tProblema baixando url:', url)
            else:
                print(COR2 + ' URL já baixada {} '.format(url))
                
        if problema:
            print('\tProblema com a url:', url)
        elif video:
            link = main_dict['video_url']
            ext = '.mp4'
            download(link, url)
        else:
            if 'edge_sidecar_to_children' in main_dict:
                print('Baixando galeria...')
                for item in main_dict['edge_sidecar_to_children']['edges']:
                    link = item['node']['display_url'] 
                    ext = '.jpg'
                    download(link, url)
                print('Galeria baixada!')
            else:
                link = main_dict['display_url'] 
                ext = '.jpg'
                download(link, url)

    baixadas.append(url)

def filtro(url):
    if 'instagram.com' in url and url not in lista_url and 'cdninstagram.com' not in url:
        lista_url.append(url)
        print(url)
        os.system(f'notify-send -u critical -t 90 "COPIADO PARA O CLIPBOARD" "Link copiado: {url}"')

def sair():
    print(COR1 + ' Pressione ENTER para interromper o loop ')
    input('\n')
    global shutdown
    shutdown = True

def circular(onde, problema=False):
    global lista_url
    if problema:
        lista_url = lista_tmp
    
    else:    
        while True:
            url = pyperclip.paste()
            filtro(url.strip('\n'))
            time.sleep(0.7)
            if shutdown:
                print(COR4 + 'Baixando...')
                break

        # Create a list backup
        with open(TMP, 'w') as f:
            for item in lista_url:
                f.write(item + ',')

    print(len(lista_url), 'imagens na fila:')
    for item in lista_url:
        baixar(onde, item)

    for item in baixadas:
        if item in lista_url:
            lista_url.remove(item)

    if len(lista_url) == 0:
        try:
            os.remove(TMP)
        except:
            pass

    else:
        # Update backup list in case still exist not downloaded files
        print('Nem todos as urls foram baixadas')
        with open(TMP, 'w') as f:
            for item in lista_url:
                f.write(item + ',')

# ------------------------ the script actually starts here ---------------

# Check if there are files to be downloaded
if os.path.exists(TMP):
    if len(lista_tmp) > 0:
        print('Problemas com a tentativa de download anterior')
        circular(HOME, problema=True)

# Check if there are parameters passed to the script
if len(args) >= 1:
    if '1' in args and 'd' in args:
        url = pyperclip.paste()
        print('Baixando 1 imagem no CWD...')
        baixar(atual, url)
    
    elif 'd' in args:
        threading.Thread(target=sair).start() 
        circular(atual)
else:
    threading.Thread(target=sair).start() 
    circular(HOME)