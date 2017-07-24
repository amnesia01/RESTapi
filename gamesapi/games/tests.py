from django.test import TestCase

# Create your tests here.

from datetime import datetime
from django.utils import timezone
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from games.models import Game
from games.serializers import GameSerializer

'''
create two instances of the Game model and save them.
'''
gamedatetime = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
game1 = Game(name='Smurfs Jungle', release_date=gamedatetime, game_category='2D mobile arcade', played=False)
game1.save()
game2 = Game(name='Angry Birds RPG', release_date=gamedatetime, game_category='3D RPG', played=False)
game2.save()

'''check the value'''
print(game1.pk)
print(game1.name)
print(game1.created)
print(game2.pk)
print(game2.name)
print(game2.created)


# serialize the first ganme instance(game1)
game_serializer1 = GameSerializer(game1)
game_serializer2 = GameSerializer(game2)
print(game_serializer1.data)

# create an instance of this class and then calls the render method to render the dictionaries hold
# in the data attribute into JSON.

renderer = JSONRenderer()
rendered_game1 = renderer.render(game_serializer1.data)
rendered_game2 = renderer.render(game_serializer2.data)
print(rendered_game1)
print(rendered_game2)

# from serialized data to the population of a Game instance
# 1.创建字符串JSON
json_string_for_new_game = '{"name":"Tomb Raider Extreme Edition", "release_date":"2016-05-18T03:02:00.776594Z",' \
                           '"game_category":"3D RPG", "played":false}'
# 2.转换到字节码
json_bytes_for_new_game = bytes(json_string_for_new_game, encoding='UTF-8')
# 3.BytesIO 提供缓存区，创建一个流
stream_for_new_game = BytesIO(json_bytes_for_new_game)
# 4.反序列化和解析流到python models，保存成python 字典形式
parser = JSONParser()
parsed_new_game = parser.parse(stream_for_new_game)
print(parsed_new_game)

# use GameSerializer class to generate a fully opulated Game instance named new_game from the directionary
new_game_serializer = GameSerializer(data=parsed_new_game)
if new_game_serializer.is_valid():
    new_game = new_game_serializer.save()
    print(new_game.name)
