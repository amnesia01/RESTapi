from rest_framework import serializers
from .models import Game, GameCategory, Player, PlayerScore


class GameSerializer(serializers.HyperlinkedModelSerializer):
    """
    use ModelSerializer class to eliminate code
    We want to sidplay the game cagory's name instead of the id       
    """
    game_category = serializers.SlugRelatedField(queryset=GameCategory.objects.all(), slug_field='name')

    class Meta:
        model = Game
        fields = (
            'url',
            'name',
            'release_date',
            'game_category',
            'played')


class GameCategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer generated a field named url with the URL
    for the resource as its value.it repersents the realationships to other 
    model instances with hyperlinks instead of primary key values
    """
    games = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='game-detail'
    )

    class Meta:
        model = GameCategory
        fields = (
            'url',
            'pk',
            'name',
            'games',
        )


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    # We want to display all the details for the game
    game = GameSerializer()
    # We don't include the player because ut will be nested in the player

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'game',
        )


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(
        choices=Player.GENDER_CHOICES
    )
    gender_decription = serializers.CharField(
        source='get_gender_display',
        read_only=True
    )

    class Meta:
        model = Player
        fields = (
            'url',
            'name',
            'gender',
            'gender_decription',
            'scores',
        )


class PlayerScoreSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(queryset=Player.objects.all(),
                                          slug_field='name')
    # We want to display the game's name instead of the id
    game = serializers.SlugRelatedField(queryset=Game.objects.all(),
                                        slug_field='name')

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'player',
            'game',
        )

