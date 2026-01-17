from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import select
import re

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validators
    @validates("name")
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Author must have a name")

        existing_author = db.session.execute(
            select(Author).where(Author.name == name)
        ).scalar_one_or_none()

        if existing_author:
            raise ValueError("Author name must be unique")

        return name.strip()

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if not re.fullmatch(r"\d{10}", phone_number):
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validators
    @validates("content")
    def validate_content(self, key, content):
        if content is None or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must be 250 characters or less")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return category

    @validates("title")
    def validate_title(self, key, title):
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait_words):
            raise ValueError("Title is not clickbait-y enough")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title})'
