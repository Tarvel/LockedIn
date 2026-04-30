from django.urls import path
from . import views

urlpatterns = [
    # Landing & generation
    path("", views.landing_page, name="landing"),
    path("generate/", views.generate_roadmap_view, name="generate_roadmap"),
    path("generate/run/", views.generate_run, name="generate_run"),
    path("loading/", views.loading_screen, name="loading"),

    # Auth
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard
    path("dashboard/", views.dashboard_view, name="dashboard"),

    # Roadmap detail
    path("roadmap/<uuid:roadmap_id>/", views.roadmap_detail, name="roadmap_detail"),

    # HTMX progress endpoints
    path("progress/node/", views.toggle_node_progress, name="toggle_node"),
    path("progress/project/", views.toggle_project_progress, name="toggle_project"),

    # Guest auth modal (HTMX)
    path("auth-check/", views.guest_auth_check, name="guest_auth_check"),
]
