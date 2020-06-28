###############################################################################
# Copyright 2020, selfattest Private Limited  All rights reserved.
# You may use this file only in accordance with the license, terms, conditions,
# disclaimers, and limitations in the end user license agreement accompanying
# the software package with which this file was provided.
###############################################################################

from django.conf import settings
from django.conf.urls import url
from django.urls import path, include



urlpatterns = [
    path('api/v1/media/photos/', include('media_photo.api.urls')),

]


if settings.IS_LOCAL:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
