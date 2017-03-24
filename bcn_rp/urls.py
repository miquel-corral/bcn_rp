"""bcn_rp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from bcn_rp import views

urlpatterns = [
    # django admin application
    url(r'^admin/', admin.site.urls),

    # BCN profile page
    url(r'^bcn_profile/$', views.bcn_profile, name='bcn_profile'),

    # rest api endpoint for assessment
    url(r'^assessment/$', views.Assessment.as_view(), name='assessment'),

    # rest api endpoint parent elements list
    url(r'^parent_elements_list/$', views.ParentElements.as_view(), name='parent_elements_list'),

    # scores urls
    url(r'^parent_assessmentelement_list/$', views.ParentAssessmentElement.as_view(), name='parent_assessmentelement_list'),

    url(r'^assessmentelement_list/$', views.AssessmentElement.as_view(), name='assessmentelement_list'),

    url(r'^child_assessmentelement_list/$', views.ChildAssessmentElement.as_view(), name='child_assessmentelement_list'),

    # hazards
    url(r'^hazard_interdependencies/$', views.hazard_interdependencies, name='hazard_interdependencies'),

    url(r'^hazard_dependencies_list/$', views.HazardDependencies.as_view(), name='hazard_dependencies_list'),

    url(r'^hazard_groups_selected/$', views.HazardGroupsSelected.as_view(), name='hazard_groups_selected'),

    url(r'^hazards_selected/(?P<assessment_id>\d+)/$', views.hazards_selected, name='hazards_selected'),

    url(r'^hazard_impacts_list/$', views.Impacts.as_view(), name='hazard_impacts_list'),

    url(r'^hazard_impact_type_list/$', views.HazardImpactTypes.as_view(), name='hazard_impact_type_list'),

    url(r'^hazard_impacts/(?P<assessment_id>\d+)/$$', views.hazard_impacts, name='hazard_impacts'),


]
