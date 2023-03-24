from superheroes import HeroesChecker
from yandex import YandexDiskUploader
from stackoverflow import StackQuestions

if __name__ == '__main__':
    hero = HeroesChecker(('Hulk', 'Captain America', 'Thanos'))
    hero.print_best()

    stackoverflow_token = input("Please, insert stackoverflow token or leave this field empty:\n")
    stack = StackQuestions(key=stackoverflow_token, tag='python', days=2)
    stack.get_questions()

    yandex_disk_token = input("Please, insert YandexDisk token:\n")
    yandex_disk_uploader = YandexDiskUploader(yandex_disk_token)
    yandex_disk_uploader.upload_file_to_root('questions.json')
