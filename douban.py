# -*- coding: utf-8 -*-

import requests
import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}   # MUST include the header

def getBookByID(id):
    '''
    {
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
	'summary': 'The RiftWar is done. But a fearsome army of trolls and renegade humans, emboldened by the drug of destruction, has risen in strength from the ashes of defeat. There is one, however, who defies the call to battle...  New York Times bestselling fantasist Raymond E. Feist returns to a beleaguered realm of wonders and magic-where war is an enduring legacy; where blood swells the rivers and nourishes the land. Attend to this hitherto untold chapter in the violent history of Midkemia -- a towering saga of great conflicts, brave acts and insidious intrigues. It is the story of a traitor who rejects the brutality of his warlike kind and casts his lot with the human targets of their fierce aggression. It tells of mysterious deaths and sinister machinations -- and signs of a time when the fate of many civilizations rested in the able, unfaltering hands of RiftWar veterans Squire Locklear and cunning their-turned-squire Jimmy the Hand. It chronicles the powerful awakening of Owyn -- apprentice magician of untried strengths -- and celebrates the selfless achievements of Pug, the great sorcerer of two worlds. Welcome now to astonishing new corners of a world you have not yet fully explored-and prepare to experience true excitement, blood chilling terror...and the triumph born from the doom aimed at the beating heart of a kingdom.',
	'price': '63.00元'
    }
    '''
    info = requests.get(f'http://douban.uieee.com/v2/book/{id}/',headers=headers).text   # Third party api
    if 'rating' in eval(info).keys():
        return json.loads(info)
    else:
        return None

def getBookBySearchSuggest(q, index=0):         # No limit
    '''example:
    {
        'title': 'Krondor',
        'url': 'https://book.douban.com/subject/2677006/',
        'pic': 'https://img9.doubanio.com/view/subject/s/public/s4755806.jpg',
        'author_name': 'Feist, Raymond E.',
        'year': '1999',
        'type': 'b',
        'id': '2677006'
    }

    If searched nothing, return None
    '''
    
    a = requests.get(f'https://book.douban.com/j/subject_suggest?q={q}',headers=headers).text
    try:
        if json.loads(a):
            ret = json.loads(a)[index]
            return ret
        else:
            return None
    except Exception:       # When approach a request limit
        return None

def getBookBySearch(q, index=0):
    '''
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
    }
    '''
    
    suggest = getBookBySearchSuggest(q);
    if suggest:
        id = suggest['id']
        detail = getBookByID(id)
        suggest['more'] = detail
        return suggest
    else:
        return None
    
if __name__ == '__main__':
    print(getBookBySearchSuggest('0380795272'))
    print(getBookBySearch('0380795272'))
    print(getBookByID('2677006'))
