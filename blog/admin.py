from django.contrib import admin
from blog.models import Article, ArticleCategory, Section, Author, ParagraphBlock, TableBlock, PictureBlock, Block

admin.site.register(Author)
admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(Section)
admin.site.register(ParagraphBlock)
admin.site.register(TableBlock)
admin.site.register(PictureBlock)
admin.site.register(Block)
