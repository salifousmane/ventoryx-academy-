from django.shortcuts import render, get_object_or_404
from .models import Article, Categorie


def index(request):
    articles = Article.objects.filter(statut='publie').order_by('-date_publication')
    articles_recents = articles[:3]
    categories = Categorie.objects.all()
    return render(request, 'pages/support/blog.html', {
        'articles': articles,
        'articles_recents': articles_recents,
        'categories': categories,
        'page_title': 'Blog',
    })


def detail(request, slug):
    article = get_object_or_404(Article, slug=slug, statut='publie')
    article.vues += 1
    article.save(update_fields=['vues'])
    articles_recents = Article.objects.filter(statut='publie').exclude(pk=article.pk).order_by('-date_publication')[:3]
    return render(request, 'pages/support/article_detail.html', {
        'article': article,
        'articles_recents': articles_recents,
        'page_title': article.titre,
    })
