from sqlalchemy.exc import IntegrityError
from app import db, app
from app.models import Color
import requests as rq
from bs4 import BeautifulSoup


def add_color(color):
    with app.app_context():
        db.session.add(color)
        try:
            db.session.commit()
        except IntegrityError as error:
            print(error)
        else:
            print('Successfully added color, hex: {}, image: {}'.format(color.hex, color.image_link))


def format_to_standard_name(s):
    t = s.lower()
    t = t.replace('gray', 'grey')
    t = t.replace('warm', 'war')
    w = t.split()
    if len(w) >= 2 and w[1][0] == '0':
        w = w[1:]
    return ''.join(w)


if __name__ == '__main__':
    main_page = 'https://promolenta.ru/ispolzuemye-vidy-lenty/satinovaya-lenta-s-gladkim-kraem/'
    name2hex_page = 'https://www.easycalculation.com/colorconverter/pantone-to-hex-table.php'

    bs = BeautifulSoup(rq.get(main_page).text)
    bs2 = BeautifulSoup(rq.get(name2hex_page).text)

    name2hex = dict()
    block = bs2.find(name='div', attrs={'class': 'table clearfix'}).table

    for tr_block in block.children:
        try:
            name2hex[format_to_standard_name(tr_block.contents[1].text)] = tr_block.contents[3].text
        except Exception:
            pass

    divs = bs.find_all(attrs={'class': 'su-custom-gallery-slide'})
    cnt_added = 0
    for t in divs:
        image_link = t.a['href']
        id = t.a['title']

        if ' ' in id:
            key = id
        else:
            key = id + ' C'
        key = format_to_standard_name(key)

        if key in name2hex.keys():
            cnt_added += 1
            add_color(Color(image_link=image_link, hex=name2hex[key]))
        else:
            print('Cant find {} color'.format(key))

    print('Added {} from {} existing'.format(cnt_added, len(divs)))