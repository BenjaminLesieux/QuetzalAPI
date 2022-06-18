from django.contrib import admin

from elections.models import Candidate, Election, Round, Vote, ElectionProgress, ElectionType, Logs, Participate, Party, \
    Permissions, Submit

admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(Round)
admin.site.register(Vote)
admin.site.register(ElectionProgress)
admin.site.register(ElectionType)
admin.site.register(Logs)
admin.site.register(Participate)
admin.site.register(Party)
admin.site.register(Permissions)
admin.site.register(Submit)
