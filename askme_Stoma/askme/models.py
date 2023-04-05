from django.db import models

# Create your models here.
QUESTIONS = [
    {
    'id': i,
    'title': f'Question {i}',
    'text': f'{i} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...',
    'tags': [
        {
        'id': i,
        'text': f'tag {i}',
        } for i in range(3)
    ]
    } for i in range(12)
]

ANSWERS = [
    {
    'text': f'{i} Ultrices gravida dictum fusce ut placerat orci nulla pellentesque dignissim. Pretium nibh ipsum consequat nisl vel pretium lectus quam. Molestie nunc non blandit massa enim nec. Vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor.'
    } for i in range(3)
]

TAGS = [
    {
    'id': i,
    'text': f'tag {i}',
    } for i in range(3)
]