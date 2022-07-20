from django.contrib import admin
from elections.models import *

admin.site.register(Vote)
admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(ElectionType)
admin.site.register(Round)
admin.site.register(Party)
