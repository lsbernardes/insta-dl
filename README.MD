insta-dl.py
========


Abstract
--------

**insta-dl.py** is a Python script to download images and videos in instagram URLs. Once executed it checks the system clipboard every second for new URLs and add them to a list to be downloaded. Most of the messages inside the code that will be prompted to the user are in **Portuguese**, change at will if you need :)

The script was written to be used in a Linux box, so if you're gonna use it in a Windows system, maybe you'll have to do some changes.

Dependencies
--------

To use **insta-dl.py** you need to install 3 packages: `pyperclip`, `bs4` and `colorama`.
With pip you can install them with this command::

    pip install bs4 pyperclip colorama

`notify-send` is a linux package used into the script, but I don't think it is a problem if you don't have it installed.

Usage
--------

First thing: you need to change two variables inside the code `HOME` and `TMP`. `HOME` is the default directory to which the images and videos will be downloaded and `TMP` is the temporary directory used by the script. `TMP` by default is set to use `/tmp/` directory, so if you don't want you don't need to change it.

It's simple to use **insta-dl.py**, you need to run it through a python interpreter and once started it gonna check your system clipboard for new URLs. When you're done copying the URLs, press ENTER to start downloading them. Here an example::

    $ python insta-dl.py
     Pressione ENTER para interromper o loop
    
    https://www.instagram.com/p/B8tcuhIHS0I/
    https://www.instagram.com/p/B8pCnzSA5tH/
    https://www.instagram.com/p/B8j_xhyJZoB/

    Baixando...
    3 imagens na fila:
    1 /predetermined/path/justhumansof_d797ed81cb8c1.jpg
    2 /predetermined/path/albertomontt_7f02545133a90.jpg
    3 /predetermined/path/paulnicklen_c3bc8a98229b0.jpg

Additionally, you can pass the parameter `d` to override the default variable and download the URLs in the current directory::

    $ pwd
    /home/persona/Desktop
    
    $ python path/to/insta-dl.py
     Pressione ENTER para interromper o loop
    
    https://www.instagram.com/p/B8tcuhIHS0I/

    Baixando...
    2 imagens na fila:
    1 /home/persona/Desktop/justhumansof_d797ed81cb8c1.jpg
    2 /home/persona/Desktop/albertomontt_7f02545133a90.jpg

