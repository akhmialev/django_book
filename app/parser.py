from django.core.exceptions import MultipleObjectsReturned
import json
import datetime
import requests
import os
import pytz

from .models import Book, Category, Author


def data_parser():
    with open('books.json', 'r') as file:
        data = file.read()
        books = json.loads(data)

    for book_data in books:
        published_date_str = book_data.get('publishedDate', {}).get('$date')
        if published_date_str:
            tz = pytz.timezone('UTC')
            published_data = datetime.datetime.strptime(published_date_str, "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(tz)
        else:
            published_data = None

        short_Description = book_data.get('shortDescription', '')
        long_Description = book_data.get('longDescription', '')
        thumbnail_Url = book_data.get('thumbnailUrl', '')
        is_bn = book_data.get('isbn', '')

        try:
            book = Book.objects.get(title=book_data['title'], isbn=is_bn)
        except Book.DoesNotExist:
            book = Book.objects.create(
                title=book_data['title'],
                isbn=is_bn,
                pageCount=book_data['pageCount'],
                publishedDate=published_data,
                thumbnailUrl=thumbnail_Url,
                shortDescription=short_Description,
                longDescription=long_Description,
            )
        except MultipleObjectsReturned:
            book = Book.objects.filter(title=book_data['title'], isbn=is_bn).first()

        authors = []
        for author_name in book_data.get('authors', []):
            author, _ = Author.objects.get_or_create(name=author_name)
            authors.append(author)
        book.authors.set(authors)

        categories = []
        for category_name in book_data.get('categories', []):
            category, _ = Category.objects.get_or_create(name=category_name)
            categories.append(category)

        if not categories:
            new_category, _ = Category.objects.get_or_create(name='Новинки')
            categories.append(new_category)
        book.categories.set(categories)

        image_url = thumbnail_Url
        image_filename = os.path.basename(image_url)
        image_folder = 'image/folder/'
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        save_path = os.path.join(image_folder, image_filename)

        if not os.path.exists(save_path):
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(save_path, 'wb') as file:
                        file.write(response.content)
                else:
                    print('error')
            except Exception as e:
                print(e)
