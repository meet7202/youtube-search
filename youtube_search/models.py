from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "YT Video Tags"

    def __str__(self):
        return '%s - %s' % (self.id, self.name)

    def __unicode__(self):
        return '%s - %s' % (self.id, self.name)


class YoutubeVideo(models.Model):
    DEFAULT = ""
    HIGH_Q = "hq"
    MED_Q = "mq"

    video = models.CharField(max_length=100, unique=True)
    published_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=500)
    description = models.TextField()
    thumbnail_key = models.CharField(max_length=50)
    key_words = models.ManyToManyField(Tag)

    class Meta:
        ordering = ["published_at"]
        verbose_name_plural = "YT Videos"


    def __unicode__(self):
        return '%s - %s' % (self.id, self.video)

    @property
    def mq_thumb_url(self):
        return self.get_url(self.thumbnail_key, self.MED_Q)

    @property
    def high_q_thumb_url(self):
        return self.get_url(self.thumbnail_key, self.HIGH_Q)

    @property
    def thumb_url(self):
        return self.get_url(self.thumbnail_key, self.DEFAULT)

    def get_url(self, key, quality):
        return "https://i.ytimg.com/vi/"+key+"/"+quality+"default.jpg"

    @staticmethod
    def get_tags(string_obj):
        key_words = list(set([key_word for key_word in string_obj.split(' ')]))
        tags = []
        for key_word in key_words:
            tags.extend(Tag.objects.get_or_create(name=key_word.lower()))
        return tags

    @staticmethod
    def get_thum_key(thumb_obj):
        # format: https://i.ytimg.com/vi/aURgzO1RuQ4/default.jpg
        return thumb_obj["default"]["url"].split('/')[-2]

    @staticmethod
    def add_item(data):
        yt_qs = YoutubeVideo.objects.filter(video=data['id']['videoId'])
        if yt_qs.exists():
            return yt_qs.last()

        tags = []
        print(data["snippet"])
        tags.extend(YoutubeVideo.get_tags(data['snippet']['title']))
        tags.extend(YoutubeVideo.get_tags(data['snippet']['description']))
        yt_video = YoutubeVideo(
            video = data['id']['videoId'],
            published_at = data['snippet']['publishedAt'],
            title = data['snippet']['title'],
            description=data['snippet']['description'],
            thumbnail_key=YoutubeVideo.get_thum_key(data['snippet']['thumbnails'])
        )
        yt_video.save()
        if tags:
            yt_video.key_words.add(*tags)

        return yt_video


