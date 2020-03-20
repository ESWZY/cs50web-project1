# -*- coding: utf-8 -*-

import requests
import json

def getBookBysearch(q, index=0):
    '''example:
{
    'title': 'Krondor',
    'url': 'https://book.douban.com/subject/2677006/',
    'pic': 'https://img9.doubanio.com/view/subject/s/public/s4755806.jpg',
    'author_name': 'Feist, Raymond E.',
    'year': '1999',
    'type': 'b',
    'id': '2677006',
    'more': {
	'rating': {
		'max': 10,
		'numRaters': 0,
		'average': '0.0',
		'min': 0
	},
	'subtitle': '',
	'author': ['Feist, Raymond E.'],
	'pubdate': '1999-10',
	'tags': [],
	'origin_title': '',
	'image': 'https://img9.doubanio.com/view/subject/m/public/s4755806.jpg',
	'binding': 'Pap',
	'translator': [],
	'catalog': '',
	'pages': '432',
	'images': {
		'small': 'https://img9.doubanio.com/view/subject/s/public/s4755806.jpg',
		'large': 'https://img9.doubanio.com/view/subject/l/public/s4755806.jpg',
		'medium': 'https://img9.doubanio.com/view/subject/m/public/s4755806.jpg'
	},
	'alt': 'https://book.douban.com/subject/2677006/',
	'id': '2677006',
	'publisher': 'Harpercollins',
	'isbn10': '0380795272',
	'isbn13': '9780380795277',
	'title': 'Krondor',
	'url': 'https://api.douban.com/v2/book/2677006',
	'alt_title': '',
	'author_intro': '',
	'summary': 'The RiftWar is done. But a fearsome army of trolls and renegade humans, emboldened by the drug of destruction, has risen in strength from the ashes of defeat.',
	'price': '63.00元'
    }
}'''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}   #must include the header
    a = requests.get(f'https://book.douban.com/j/subject_suggest?q={q}',headers=headers).text
    if json.loads(a):
        ret = json.loads(a)[index]
        id = ret['id']
        info = requests.get(f'http://douban.uieee.com/v2/book/{id}/',headers=headers)   #third party api
        if info.has_key('rating'):
            ret['more'] = json.loads(info.text)
        else:
            ret['more'] = None
        return ret
    else:
        return None

if __name__ == '__main__':
    print(getBookBysearch('0380795272')['pic'])
