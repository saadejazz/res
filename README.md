# Reverse Image Meta Search  

Performs image search on four popular reverse image searchers:  
* [Google](https://images.google.com/?gws_rd=ssl)  
* [Bing](https://www.bing.com/?scope=images&nr=1&FORM=NOFORM)  
* [Yandex](https://www.yandex.com/images/)  
* [TinEye](https://tineye.com/)

## Getting Started  

* Pull this repository (to allow for updates).   
    ```bash
    mkdir res
    cd res
    git init
    git remote add origin https://www.github.com/saadejazz/res
    git pull origin master
    cd ..
    ```

* Install Python dependencies.  
    ```bash
    python -m pip install selenium bs4 validators billiard
    ```

* Download chromedriver and set its path in *conf.py*.  
    ```python
    # Path to chromedriver
    EXECUTABLE_PATH = 'path/where/chromedriver/installed'
    ```

## Usage  

Requires a URL for an image on the internet or the directory for one saved locally.  

**Code:**

```python
import res.image_search.reverse_search as rSearch

url = "/some/path/locally
# OR
# url = "https://media.wired.com/photos/5b8999943667562d3024c321/master/w_2560%2Cc_limit/trash2-01.jpg"

results = rSearch(url = url)
print(res)
```

**Output:**

```python
{'possible_description': '',
 'keywords': ['дизайн иконка',
  'корзина значок',
  'Логотип',
  'иконка мусорки',
  'значки'],
 'image_text': '',
 'similar_images': ['https://im0-tub-com.yandex.net/i?id=9badc4ff49a34b60b10908ff62ab5c27&n=24',
  'https://im0-tub-com.yandex.net/i?id=f7456bf7774e23a8b2ee70cb9f81ea30&n=24',
  'https://im0-tub-com.yandex.net/i?id=9dc9ea2f22784c00db0240054d850408&n=24',...],
 'article_links': [{'title': 'Google Wants to Kill the URL - ANITH',
   'url': 'http://www.yandex.com/clck/jsredir?from=www.yandex.com%3Bimages%2Fsearch%3Bimages%3B%3B&text=&etext=8905.gfb-RzqY66TRAfpRQsweacAvtIVqqH1Kd1eKzDZLoFI.a4b779d7ae642cb4e3b001bf2b0a1eeafc880f1e&uuid=&state=tid_Wvm4RM35w_KF6_gYfMtmgS4f5d81OW-g6ZRMBJsI3GF_Hm08bQ,,&data=UlNrNmk5WktYejY4cHFySjRXSWhXRDh2bjVGdlBxbnNlUF9OM0ppaW9lLXFSOUMzaWU4bXZKQWpqbkNzVnl3SW5ZMWNyTXFBVjJZeTJtQlppSEdPalpiVVZTdmNubjd3M1BJWE5WWWxiQ3VTMVdrb3BsZnJaUTlsc2piQ1lzenAyT2FVZjZMb3NzYyw,&sign=aa477d0b6e376b116201a8c9495f676c&keyno=0&b64e=2&l10n=en'},...
  ]}
```