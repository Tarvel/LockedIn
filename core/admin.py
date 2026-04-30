from django.contrib import admin
from .models import Roadmap, NodeProgress, ProjectProgress, Streak


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ("skill_name", "user", "created_at", "completion_percentage")
    list_filter = ("created_at",)
    search_fields = ("skill_name", "user__email")


@admin.register(NodeProgress)
class NodeProgressAdmin(admin.ModelAdmin):
    list_display = ("node_id", "user", "roadmap", "completed", "completed_at")
    list_filter = ("completed",)


@admin.register(ProjectProgress)
class ProjectProgressAdmin(admin.ModelAdmin):
    list_display = ("project_id", "user", "roadmap", "completed", "completed_at")
    list_filter = ("completed",)


@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = ("user", "current_streak", "longest_streak", "last_active_date")
