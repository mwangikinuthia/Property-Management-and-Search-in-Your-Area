from haystack import indexes
from .models import houseDesc,Plot


class HouseIndex(indexes.SearchIndex, indexes.Indexable):
    # text field is what the user inputs,document=Trues specifies is the field will be getting our query from
    # Each item queried will come with a signature of when it was registered
    text=indexes.CharField(document=True, use_template=True)
    registered=indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return houseDesc
    
    def index_queryset(self, using=None):
        return self.get_model().approved.all()


class PlotIndex(indexes.SearchIndex, indexes.Indexable):
    text=indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Plot

    def index_queryset(self, using=None):
        return self.get_model().approved.all()
