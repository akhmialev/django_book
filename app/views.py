from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import Author, Book
from .parser import data_parser


def parser_view(request):
    data_parser()
    return HttpResponse('Parse competed')


def author_view(request):
    authors = Author.objects.all()
    authors_in_page = 20
    paginator = Paginator(authors, authors_in_page)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    context = {
        'page_objects': page_objects,
        'paginator': paginator,
    }

    return render(request, 'author.html', context)


def books_view(request):
    books = Book.objects.all()
    authors_in_page = 10
    paginator = Paginator(books, authors_in_page)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    context = {
        'page_objects': page_objects,
        'paginator': paginator,
    }

    return render(request, 'books.html', context)