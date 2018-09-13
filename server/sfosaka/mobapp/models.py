from django.db import models


#####################################
# Prepopulated bootstrap tables
class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=64)
    # no description. We just have to figure it out.

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=64)
    region = models.CharField(max_length=2)
    language_code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

#####################################
class ContactInfo(models.Model):
    street_number = models.CharField(max_length=1024)
    city = models.CharField(max_length=512)
    state = models.CharField(max_length=2)
    postal = models.CharField(max_length=128)
    country = models.CharField(max_length=512)
    phone = models.CharField(max_length=64)

    def __str__(self):
        return '%s, %s' % (self.street_number, self.phone)

class Organization(models.Model):
    name = models.CharField(max_length=512)
    name_jp = models.CharField(max_length=512)
    category = models.ForeignKey(Category)
    description = models.TextField(max_length=4096)
    description_jp = models.TextField(max_length=4096)
    shortDescription = models.CharField(max_length=1024)
    shortDescription_jp = models.CharField(max_length=1024)
    modificationDate = models.DateTimeField(auto_now=True)
    imageUrl = models.CharField(max_length=512, null=True)
    url = models.CharField(max_length=512, null=True)
    contact = models.ForeignKey(ContactInfo, null=True)

    class Meta:
        abstract = True
        get_latest_by = 'modificationDate'

    def __str__(self):
        return '%s: %s' % (self.name, self.shortDescription)

class Partner(Organization):
    latitude = models.FloatField()
    longitude = models.FloatField()

class Performer(Organization):
    status = models.ForeignKey(Status)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

class AppHighlight(Organization):
    order = models.PositiveSmallIntegerField()
    detail = models.TextField(max_length=4096, null=True)
    detail_jp = models.TextField(max_length=4096, null=True)

# In retrospect, base class for AppHighlight and Transportation would have
# been good. But not worth it to refactor... yet.
class Transportation(Organization):
    order = models.PositiveSmallIntegerField()
    detail = models.TextField(max_length=4096, null=True)
    detail_jp = models.TextField(max_length=4096, null=True)

class DictionaryWord(models.Model):
    word = models.CharField(max_length=128)
    phonetic = models.CharField(max_length=128, null=True)
    language = models.ForeignKey(Language)
    status = models.ForeignKey(Status)
    translations = models.ManyToManyField("self", blank=True)
    # When this is created
    creationDate = models.DateTimeField()
    # Updated when we change the status.
    modificationDate = models.DateTimeField()

    class Meta:
        get_latest_by = 'modificationDate'

    def translation_as_word(self):
        words = ''
        for tran in self.translations.all():
            if len(words) == 0:
                words = tran.word
            else:
                words += ", " + tran.word
        return words
    translation_as_word.short_description = 'Translations (approve at least one)'

    def __str__(self):
        return '%s (%s)' % (self.word, self.language)
