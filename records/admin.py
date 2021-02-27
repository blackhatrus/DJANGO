from django.contrib import admin
from .models import Record, Category, Comment, RecordHistory
# Register your models here.



@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('created', 'title', 'slug', 'body',
                    'url', 'online_status', 'added_to_cat', 'stars',
                    'flag', 'category', 'record_status', 'meta_desc'
                    )
    list_display_links = ('created', 'title')
    search_fields = ('created', 'slug')
    list_filter = ('category', 'record_status')
    list_editable = ('online_status',)
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    list_display_links = ('title', 'description')
    search_fields = ('title',)  # tuple => comma is nessesary


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('updated', 'record', 'body', 'author')
    list_display_links = ('updated', 'record')
    search_fields = ('record',)  # tuple => comma is nessesary


@admin.register(RecordHistory)
class RecordHistoryAdmin(admin.ModelAdmin):
    list_display = ('created', 'response', 'headers', 'record')
    list_display_links = ('created', 'response')
    search_fields = ('response', 'created')


