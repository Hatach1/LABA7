
from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests
import time
import os


def main_page(request):
    return render(request, 'main\Main.html')

def model_page(request):

    if request.method == 'POST':
        header = {
            #'referer': 'https://www.kinopoisk.ru/showcaptcha?mt=9E4B4BF29ECA31AE6F5BD9B88ADA4D1EB31FFA19F93CCE1DCEAA56A714958A767E4A&retpath=aHR0cHM6Ly93d3cua2lub3BvaXNrLnJ1L2xpc3RzL21vdmllcy90b3AyNTA__cb987325b7d04fceee8307b8906760d4&t=3/1671106720/e34835ccfd4741cd1153fcfd7bef5726&u=7c77169a-314ad3ad-35354d2a-7da9722e&s=b359220bb42b520242e8b60fabf98706',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': '_yasc=13G7ch+pczSCkfQv356UN4u8Lbrq+Vq7t/bVGN04G1W8Vpto5XzHONr5ngqbDOs=; gdpr=0; _ym_uid=16711067211040563817; yandexuid=9982196291661183870; yuidss=9982196291661183870; _ym_visorc=b; _ym_isad=2; spravka=dD0xNjcxMTA2NzM5O2k9ODcuMTE3LjU4LjE1NjtEPUU1NDkwRUE1QzYwNDNBQzNCODU2RDY0QjU4MjlFRjBDQ0NCQUNGNzNFNTI5MjBDNzdCRjFGNjZFNkRFQjI3NTZGMDkwQzYzMTFFM0QzRTk5ODhBRDVEOUU4NDYyNTM1QzIxNkEwNzVGODNDMTt1PTE2NzExMDY3Mzk1OTE1Mjk5NDE7aD1kNjZjN2ZjMjlhNTM3ZWYwZGNmMDhkY2Y1YzllZjcyMQ==; _csrf=IU29jUnwtZrj7R41O8v6k-Tg; desktop_session_key=a1fef1b62bdf407ad077e0e396eacfb5320ae6cf027863dfe47c2f014a2fcd014e962659ae5684478be6836fb6a74f1c38498f8ba63b10cffe48479708073d092045b553d7f08639237acf334beee0905d32e4f4ddc4ac6a2f8b54b34c9adbc8; desktop_session_key.sig=P9FwRDsvDCS-vxldSNR224GFVSY; ya_sess_id=noauth:1671106743; yandex_login=; ys=c_chck.3738810395; i=VzVV6Tjx6eij/Aogd2jFwGNG26XUajxuSPeg7XEeAPHW0LRL0sdM92Ff/DBrV/dvLz3HecTb+bLFrK2WuBAtaVtwywY=; mda2_beacon=1671106743083; sso_status=sso.passport.yandex.ru:synchronized; _ym_d=1671107160; cycada=HUa2V6Ea+1lVRzNIKBmhp6xctnOiEwAgUwDDnp3+q5A='
        }

        #print('POST')
        
        postDict = request.POST.dict()
        keyWord = postDict.get('Key')
        #print(keyWord)
        answer = []

        r = requests.get("https://www.kinopoisk.ru/lists/movies/genre--anime/?b=series&b=top", headers=header)
        bs = BeautifulSoup(r.text, "lxml")
        
        try:
            all_links = bs.find_all("a", class_="base-movie-main-info_link__YwtP1")
        except:
            all_links ='-'
        try:
            all_name = bs.find_all("span", class_="styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj")
        except:
            all_name = '-'
        try:
            all_rating = bs.find_all("span", class_=["styles_kinopoiskValuePositive__vOb2E styles_kinopoiskValue__9qXjg styles_top250Type__mPloU","styles_kinopoiskValuePositive__vOb2E styles_kinopoiskValue__9qXjg"])
        except:
            all_rating = '-'
        for i in range(len(all_links)):
            el = {'link': 'https://www.kinopoisk.ru/'+all_links[i]['href'], 'name': all_name[i].text, 'rating': all_rating[i].text}
            print(el)
            if keyWord in all_name[i].text:
                answer.append(el)
        
        if len(answer) == 0:
            answer.append({'link': '', 'name': 'Похожих фильмов не найдено', 'rating': '-'})
        


    else:
        #print('GET')
        answer = [{'name': ''}]
    return render(request, 'main\Parser.html', {'answer': answer})

def contacts_page(request):
    return render(request, 'main\Contacts.html')
