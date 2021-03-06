"""transport_nantes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from asso_tn.views import AssoView

app_name = 'legal'
urlpatterns = [
    path('mentions_legales', AssoView.as_view(title="Mentions Légales",
                                              template_name='legal/mentions_legales.html'),
         name='TC'),
    #    path('contact', views.contact, name='contact'),
#    path('priv', views.privacy, name='privacy'),
    path('assos', AssoView.as_view(title="Nos confrères",
                                   template_name='legal/aligned_orgs.html'),
         name='aligned_orgs'),
    path('sponsor', AssoView.as_view(title="Sponsor",
                                     template_name='legal/sponsor.html',
                                     hero_image="legal/sponsor.jpg",
                                     hero_title="sponsor"),
         name='sponsor'),
    path('benevolat', AssoView.as_view(
        title="Devenir bénévole | Transport Nantes",
        meta_descr="""<meta name="description" content="Pour une mobilité multimodale qui assure à chaque usagers moins de danger, de contrainte et de stress. Devenez un acteur de la Mobilité !"/>""",
        twitter_title = "Devenir bénévole | Transport Nantes",
        twitter_descr = "Pour une mobilité multimodale qui assure à chaque usagers moins de danger, de contrainte et de stress. Devenez un acteur de la Mobilité !",
        twitter_image = "asso_tn/accueil-mobilité-multimodale.jpg",
        template_name='legal/volunteer.html',
        hero_title="Devenir bénévole",
        hero_image="legal/bénévole.jpg"),
         name='volunteer'),
    path('jobs', AssoView.as_view(title="Jobs",
                                  template_name='legal/jobs.html',),
         name='jobs'),
]
