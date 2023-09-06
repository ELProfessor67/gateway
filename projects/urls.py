from django.urls import path
from projects import views
app_name = 'projects'

urlpatterns = [
    path('projectsgrid',views.ProjectsGridView.as_view(),name='projects-projectsgrid'),
    path('projectslist',views.ProjectsListView.as_view(),name='projects-projectslist'),
    path('projectoverview',views.ProjectOverviewView.as_view(),name='projects-projectoverview'),
    path('createview',views.CreateViewView.as_view(),name='projects-createview'),
    

    path('report',views.ReportView.as_view(),name='report'),
    path('gift',views.ProjectsListView.as_view(),name='gift'),
    path('batches',views.ProjectsListView.as_view(),name='batches'),
    path('customers',views.ProjectsListView.as_view(),name='customers'),
    path('recurring_list',views.shedule_list.as_view(),name='recurring_list'),
    path('recurring_create',views.create_shedule.as_view(),name='recurring_create'),
    path('send_payment',views.ProjectsListView.as_view(),name='send_payment'),
    path('settings',views.ProjectsListView.as_view(),name='settings'),
    path('help',views.ProjectsListView.as_view(),name='help'),
    path('change_status/<int:id>',views.change_batch_status,name="change status"),
    path('list/<int:id>',views.batch_transaction_list.as_view(),name="change status"),
]