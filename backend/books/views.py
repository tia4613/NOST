from django.shortcuts import get_object_or_404, render
from openai import OpenAI
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Book, Comment, Rating, Chapter
from .serializers import (
    BookSerializer,
    BookLikeSerializer,
    RatingSerializer,
    CommentSerializer,
    ChapterSerializer,
    ElementsSerializer,
)
from django.core import serializers
from django.core.files.base import ContentFile
from .generators import elements_generator, prologue_generator, summary_generator
from .deepL_translation import translate_summary


class BookListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 전체 목록 조회
    def get(self, request):
        books = Book.objects.order_by("-created_at")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    # 새 소설 책 생성
    def post(self, request):
        user_prompt = request.data.get("prompt")
        language = request.data.get("language", "EN-US")
        if not user_prompt:
            return Response(
                {"error": "Missing prompt"}, status=status.HTTP_400_BAD_REQUEST
            )

        content = elements_generator(user_prompt)  # ai로 elements 생성
        translate_content = translate_summary(content, language)
        content["user_id"] = request.user.pk
        serializer = BookSerializer(data=content)  # db에 title, user_id 저장
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={
                    "book_id": serializer.data["id"],
                    "content": translate_content,
                },  # FE에 content 응답
                status=status.HTTP_201_CREATED,
            )


class DALL_EImageAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, book_id):
        client = OpenAI()
        book = get_object_or_404(Book, id=book_id)
        if book.user_id is not request.user:
            return Response(
                {"error": "You don't have permission."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"{book.title}, {book.tone}",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        res = requests.get(response.data[0].url)
        book.image = ContentFile(res.content, name = f'{book.title}.png')
        book.save()

        serializer = BookSerializer(instance=book)
        return Response(serializer.data, status = 200)


class BookDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 상세 조회
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        ratings = Rating.objects.filter(book=book)

        # chapter 내용들 가져오기
        chapters = Chapter.objects.filter(book_id=book_id)
        chapter_serializer = ChapterSerializer(chapters, many=True)

        # 책 전체 내용 직렬화
        book_serializer = BookSerializer(book)

        response_data = book_serializer.data
        response_data["chapters"] = chapter_serializer.data
        return Response(response_data, status=200)

    # chapter(summary) 생성
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if book.user_id != request.user:
            return Response(
                {"error": "You don't have permission."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        language = request.data.get("language", "EN-US")
        chapter = Chapter.objects.filter(book_id=book_id).last()
        if not chapter:
            elements = ElementsSerializer(book)
            chapter_num = 0
            result = prologue_generator(elements.data)
            content = result["prologue"]
        else:
            summary = request.data.get("summary")
            if not summary:
                return Response(
                    {"error": "Missing summary prompt"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            chapter_num = chapter.chapter_num
            result = summary_generator(chapter_num, summary)
            chapter_num += 1
            content = result["final_summary"]

        translated_content = translate_summary(content, language)
        if not translated_content:
            return Response(
                {"error": "Translation failed or empty result"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = ChapterSerializer(
            data={
                "content": translated_content,
                "book_id": book_id,
            }
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            result["book_id"] = book_id
            result["translated_content"] = translated_content
            result["chapter_num"] = chapter_num
            return Response(data=result, status=status.HTTP_201_CREATED)

    # 글 수정
    def put(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if book.user_id != request.user:
            return Response(
                {"error": "You don't have permission."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(status=401)

    # 글 삭제
    def delete(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if book.user_id != request.user:
            return Response(
                {"error": "You don't have permission."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        book.delete()
        return Response("No Content", status=204)


class DeletePrologueAPIView(APIView):
    def delete(self, request, book_id):
        prologue = Chapter.objects.filter(chapter_num=0, book_id=book_id)
        prologue.delete()
        return Response("Prologue deleted successfully", status=204)


class BookLikeAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookLikeSerializer(book)
        return Response(
            {
                "total_likes": book.total_likes(),
                "book": serializer.data,
            },
            status=200,
        )

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        # 좋아요 삭제
        if book.is_liked.filter(id=request.user.id).exists():
            book.is_liked.remove(request.user)
        # 좋아요 추가
        else:
            book.is_liked.add(request.user)
        serializer = BookLikeSerializer(book)
        return Response(
            {
                "total_likes": book.total_likes(),
                "book": serializer.data,
            },
            status=200,
        )


class UserLikedBooksAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        book_likes = (
            user.book_likes.all()
        )  # 역참조를 이용해 사용자가 좋아요한 책 리스트를 가져옴
        serializer = BookSerializer(book_likes, many=True)
        return Response(serializer.data, status=200)


class UserBooksAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        user_books = (
            user.books.all()
        )  # 역참조를 이용해 사용자가 작성한 책 리스트를 가져옴
        serializer = BookSerializer(user_books, many=True)
        return Response(serializer.data, status=200)


class RatingAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        user_rating = Rating.objects.filter(book=book, user_id=request.user.id).first()
        if user_rating:
            serializer = RatingSerializer(user_rating)
            return Response(serializer.data, status=200)
        return Response("User has not rated this book yet.", status=404)

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        rating = request.data.get("rating")

        if rating not in [1, 2, 3, 4, 5]:
            return Response("Rating must be between 1 and 5", status=400)

        existing_rating = Rating.objects.filter(
            book=book, user_id=request.user
        ).exists()
        if existing_rating:
            return Response("You have already rated this book.", status=400)

        serializer = RatingSerializer(data={"rating": rating})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user, book=book)
            return Response(serializer.data, status=200)
        return Response(status=400)


class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        comments = book.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user, book=book)
            return Response(serializer.data, status=201)


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, book_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user_id != request.user:
            return Response(
                {"error": "You don't have permission."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, book_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user_id != request.user:
            return Response(
                {"error": "You don't have permission."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        comment.delete()
        return Response("NO comment", status=204)
