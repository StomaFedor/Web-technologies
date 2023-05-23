from django.core.management.base import BaseCommand
from askme_Stoma.askme import models


class Command(BaseCommand):
    help = 'Random filling of the database'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Указывает сколько пользователей необходимо создать')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        self.generateUser(ratio)
        self.generateProfile(ratio)
        self.generateQuestion()
        self.generateAnswer()

    def generateUser(self, ratio):
        list = []
        for i in range(ratio):
            newUser = models.User(username=f'abobaUser{i}', email=f'aboba{i}@crazymail.com', password=f'mypassword{i}')
            list.append(newUser)
        models.User.objects.bulk_create(list)

    def generateProfile(self, ratio):
        profiles = [models.Profile(user=models.User.objects.filter(id=i)[0], avatar='gigachad-avatar.jpg') for i in range(1, ratio + 1)]
        models.Profile.objects.bulk_create(profiles)

    def generateQuestion(self):
        count = 1
        j = 0
        for abobaUser in models.Profile.objects.all():
            questions = [models.Question(user=abobaUser, name=f'Awesome Question{i}', text=f'{i} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...',
                                        like=models.Like.objects.create(rating=i)) for i in range((count - 1) * 10,(count - 1) * 10 + 10)]
            
            for question in questions:
                for i in range(j, j + 3):
                    question.save()
                    tag = models.Tag.objects.get_or_create(name=f'tag {i}')
                    question.tags.add(tag[0])
            count += 1
            if (count % 3 == 0):
                j = count
        
    def generateAnswer(self):
        count = 1
        for abobaQuestion in models.Question.objects.all():
            answers = [models.Answer(question=abobaQuestion, text=f'{i} Ultrices gravida dictum fusce ut placerat orci nulla pellentesque dignissim. Pretium nibh ipsum consequat nisl vel pretium lectus quam. Molestie nunc non blandit massa enim nec. Vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor.',
                                    like=models.Like.objects.create(rating=i)) for i in range((count - 1) * 10,(count - 1) * 10 + 10)]
            count += 1
            models.Answer.objects.bulk_create(answers)
