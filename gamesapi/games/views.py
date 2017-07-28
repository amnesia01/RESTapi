# from django.shortcuts import render
# API views
# from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer  # 被Response替代
# from rest_framework.parsers import JSONParser  # 使用装饰器后更改
from rest_framework.response import Response  # renders the received data into the appropriate content type
from rest_framework import status, generics
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from .models import Game, GameCategory, PlayerScore, Player
from .serializers import GameSerializer, GameCategorySerializer, PlayerScoreSerializer, PlayerSerializer

'''
第二章中 被Response 替代
class JSONResponse(HttpResponse):
    """
    subclass of django,http.HttpResponse.use string as content.create a JSONRenderer instance
    and calls its render method.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



@api_view(['GET', 'POST'])  # 第二章添加
@csrf_exempt  # ensure that the view sets a Cross-Site Request Forgery(CSRF) cookie
def game_list(request):
    """ 
    lists all the games or creates a new game
    many=True argument to specify that multiple instances have to be serialized and not juse one
    """
    if request.method == 'GET':  # the method attribute provides a string representing the HTTP verb
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return Response(games_serializer.data)
    elif request.method == 'POST':
        # game_data = JSONParser().parse(request) 使用装饰器后更改
        # game_serializer = GameSerializer(data=game_data)
        game_serializer = GameSerializer(data=request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data, status=status.HTTP_201_CREATED)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)
    elif request.method == 'PUT':
        # game_data = JSONParser().parse(request)  # 使用装饰器后更改
        # game_serializer = GameSerializer(game, data=game_data)
        game_serializer = GameSerializer(game, data=request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'players': reverse(PlayerList.name, request=request,),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'games':reverse(GameList.name, request=request)
            'scores' : reverse(PlayerScoreList.name, request=request)
        })

