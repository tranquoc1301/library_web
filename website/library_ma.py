from .db import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "fullname"
                  "username", "email", "role", "created_on", "updated_on", "is_active")


class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "category_id", "title", "publish_year",
                  "author", "publisher", "summary", "cover", "view_count", "download_count", "file_path", "average_rating")


class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "category", "image")


class CommentSchema(ma.Schema):
    class Meta:
        fields = ("id", "book_id", "user_id",
                  "content", "created_on", "updated_on")


class FavoriteSchema(ma.Schema):
    class Meta:
        fields = ("id", "book_id", "user_id", "added_on")


class RatingSchema(ma.Schema):
    class Meta:
        fields = ("id", "book_id", "user_id",
                  "rating", "created_on", "updated_on")
