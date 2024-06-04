from django.db.models import Avg
from rest_framework import serializers
from .models import Book, Chapter, Comment, Rating

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    user_nickname = serializers.SerializerMethodField()
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

    def get_average_rating(self, book):
        return Rating.objects.filter(book=book).aggregate(Avg("rating"))["rating__avg"]

    def get_user_nickname(self, book):
        return book.user_id.nickname

    def get_chapters(self,book) :
        return book.full_text.content

class BookLikeSerializer(BookSerializer):
    total_likes = serializers.IntegerField(read_only=True)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
        read_only_fields = ("book", "user_id")


class ElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "title",
            "genre",
            "theme",
            "tone",
            "setting",
            "characters",
        )


class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("book", "user_id")

        def to_representation(self, instance):
            ret = super().to_representation(instance)
            ret.pop("article")
            return ret

    def get_user_nickname(self, comment):
        return comment.user_id.nickname