from django.forms import modelformset_factory
from .models import Child

ChildFormSet = modelformset_factory(Child, fields=("first_name", "last_name"))
