from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ajax_select.admin import AjaxSelectAdmin
from ajax_select.helpers import make_ajax_form

from .models import Channel, Video, Chapter, License, AnnotationType, Annotation, Comment, Resource, Newsitem, Activity

admin.site.register(License)
admin.site.register(Resource)
admin.site.register(Newsitem)


class CreatorMixin(object):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        obj.contributor = request.user
        obj.save()

# Common fieldsets for all Elements
ELEMENT_FIELDSETS = [
    (None,               {'fields': [('slug', 'state')]}),
    (_("Metadata"),      {'fields': [('creator', 'created', 'contributor', 'modified')], 'classes': ['collapse']}),
    (_("Content"),       {'fields': [('title', 'thumbnail'), 'description']}),
    (_("Tags"),         {'fields': ['tags']})
]
USERCONTENT_FIELDSETS = [
    (_("User content"), {'fields': [('visibility', 'contenttype'),
                                    'contentdata']}),
]


class ElementAdmin(AjaxSelectAdmin, CreatorMixin, admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)

    prepopulated_fields = {'slug': ('title',)}
    list_select_related = True

    def object_link(self, item):
        return u'<a target="_blank" href="{url}">\u25ce</a>'.format(url=item.get_absolute_url())
    object_link.short_description = 'View'
    object_link.allow_tags = True


@admin.register(Video)
class VideoAdmin(ElementAdmin):
    list_display = ('pk', 'object_link', 'title', 'slug', 'creator', 'duration', 'created', 'thumbnail')
    list_editable = ('title', 'slug', 'creator', 'duration', 'thumbnail')
    list_display_links = ('pk',)
    list_filter = ('creator',)
    search_fields = ('title', 'slug')

    form = make_ajax_form(Video, {'creator': 'user',
                                  'contributor': 'user'})
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        (_("Video specific"),
         {'fields': [('url', 'duration'),
                     ('activity', 'slides'),
                     ('license')]}),
    ] + ELEMENT_FIELDSETS


@admin.register(Channel)
class ChannelAdmin(ElementAdmin):
    list_display = ('pk', 'object_link', 'title', 'slug', 'creator', 'created', 'thumbnail', 'category')
    list_editable = ('title', 'slug', 'creator', 'created', 'thumbnail', 'category')
    list_display_links = ('pk',)
    list_filter = ('creator', 'category')
    search_fields = ('title',)

    form = make_ajax_form(Channel, {'creator': 'user',
                                    'contributor': 'user'})
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = [
        (_("Channel specific"), {'fields': ['category', 'syllabus']}),
    ] + ELEMENT_FIELDSETS


@admin.register(Chapter)
class ChapterAdmin(ElementAdmin):
    list_display = ('pk', 'object_link', 'title', 'slug', 'creator', 'created', 'thumbnail', 'channel')
    list_editable = ('title', 'slug', 'creator', 'created', 'thumbnail', 'channel')
    list_display_links = ('pk',)
    list_filter = ('creator', 'channel')
    search_fields = ('title',)

    form = make_ajax_form(Chapter, {'channel': 'channel',
                                    'creator': 'user',
                                    'contributor': 'user'})
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        (None, {'fields': [('channel', 'teachers')]}),
    ] + ELEMENT_FIELDSETS


@admin.register(Activity)
class ActivityAdmin(ElementAdmin):
    list_display = ('pk', 'object_link', 'title', 'slug', 'creator', 'created', 'thumbnail', 'chapter')
    list_editable = ('title', 'slug', 'creator', 'created', 'thumbnail', 'chapter')
    list_display_links = ('pk',)
    list_filter = ('creator', 'chapter')
    search_fields = ('title',)

    form = make_ajax_form(Activity, {'chapter': 'chapter',
                                     'creator': 'user',
                                     'contributor': 'user'})
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        (None, {'fields': ['chapter']}),
    ] + ELEMENT_FIELDSETS


@admin.register(Annotation)
class AnnotationAdmin(ElementAdmin):
    list_display = ('pk', 'object_link', 'begin', 'title', 'description', 'annotationtype', 'group', 'video_name', 'creator', 'created',)
    list_editable = ('begin', 'title', 'description', 'group', 'annotationtype')
    list_display_links = ('pk',)
    list_filter = ('annotationtype', 'group', 'video')
    search_fields = ('title', 'description',)

    form = make_ajax_form(Annotation, {'video': 'video',
                                       'creator': 'user',
                                       'contributor': 'user'})
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        (None, {'fields': [('begin', 'end', 'video'),
                           ('annotationtype', 'group')]}),
    ] + USERCONTENT_FIELDSETS + ELEMENT_FIELDSETS

    def video_name(self, a):
        return a.video.title


@admin.register(AnnotationType)
class AnnotationTypeAdmin(ElementAdmin):
    list_display = ('pk', 'title', 'creator', 'created',)
    list_editable = ('title',)
    list_display_links = ('pk',)
    list_filter = ('creator',)
    search_fields = ('title',)

    form = make_ajax_form(AnnotationType, {'creator': 'user',
                                           'contributor': 'user'})
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [(None,               {'fields': [('slug', 'state')]}),
                 (_("Metadata"),      {'fields': [('creator', 'created', 'contributor', 'modified')], 'classes': ['collapse']}),
                 (_("Content"),       {'fields': [('title', 'thumbnail'), 'description']})]


@admin.register(Comment)
class CommentAdmin(ElementAdmin):
    list_display = ('pk', 'title', 'creator', 'created',)
    list_editable = ('title',)
    list_display_links = ('pk',)
    list_filter = ('creator',)
    search_fields = ('title',)

    form = make_ajax_form(Comment, {'creator': 'user',
                                    'contributor': 'user'})
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        (None, {'fields': ['group', ('parent_annotation', 'parent_video', 'parent_comment')]}),
    ] + USERCONTENT_FIELDSETS + ELEMENT_FIELDSETS
