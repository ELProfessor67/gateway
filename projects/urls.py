from django.urls import path
from projects import views
app_name = 'projects'

urlpatterns = [
    path('projectsgrid',views.ProjectsGridView.as_view(),name='projects-projectsgrid'),
    path('projectslist',views.ProjectsListView.as_view(),name='projects-projectslist'),
    path('projectoverview',views.ProjectOverviewView.as_view(),name='projects-projectoverview'),
    path('createview',views.CreateViewView.as_view(),name='projects-createview'),
    

    path('report',views.ProjectsListView.as_view(),name='report'),
    path('gift',views.ProjectsListView.as_view(),name='gift'),
    path('batches',views.ProjectsListView.as_view(),name='batches'),
    path('customers',views.ProjectsListView.as_view(),name='customers'),
    path('recurring',views.ProjectsListView.as_view(),name='recurring'),
    path('send_payment',views.ProjectsListView.as_view(),name='send_payment'),
    path('settings',views.ProjectsListView.as_view(),name='settings'),
    path('help',views.ProjectsListView.as_view(),name='help'),
]