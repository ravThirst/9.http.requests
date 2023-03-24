import requests

class HeroesChecker:
    def __init__(self, heroes_list):
        self.heroes = heroes_list
        self.url = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api'

    def print_best(self):
        raw_data = requests.get(f'{self.url}/all.json').json()
        data = []
        for hero in raw_data:
            if hero['name'] in self.heroes:
                data.append([hero['name'], hero['powerstats']['intelligence']])
        data.sort(key=lambda i: -i[1])
        print(f'Самый умный супергерой - {data[0][0]}\n'
              f'Intelligence - {data[0][1]}')
