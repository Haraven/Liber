from django.db import models
from .utils.enums import ReferenceSymbolType

class Article(models.Model):
    published_date = models.DateTimeField()

    def register_references(self):
        current_ref_index = 1
        for paragraph in self.paragraph_set:
            for ref in paragraph.references:
                ref.number = current_ref_index
                current_ref_index += 1

    @classmethod
    def create(cls, published_date, paragraph_set):
        tmp = cls(published_date=published_date, paragraph_set=paragraph_set)
        tmp.register_references()

        return tmp

class Reference(models.Model):
    number = -1
    text = models.CharField(max_length=2048)
    symbol_type = models.CharField(max_length=32, choices=[(symbol, symbol.value) for symbol in ReferenceSymbolType])

    def get_prefix(self):
        if self.symbol_type == ReferenceSymbolType.NUMBER:
            return str(self.number)
        elif self.symbol_type == ReferenceSymbolType.ASTERISK:
            return "*"
        else:
            return "[UNKNOWN PREFIX]"

    def __str__(self):
        prefix = self.get_prefix()

        return prefix + " " + self.text

class Paragraph(models.Model):
    # max_length is some power of 2 that's > 100k
    text = models.TextField(max_length=131072)
    references = models.ManyToManyField(Reference)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
