import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class Roadmap(models.Model):
    """
    Stores the full AI-generated roadmap JSON for a given skill.
    The `phases` field holds the entire roadmap structure including
    phases, nodes, projects, and resource links.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="roadmaps",
        null=True,
        blank=True,  # null for guest-previewed roadmaps before signup
    )
    skill_name = models.CharField(max_length=255)
    phases = models.JSONField(
        help_text="Full roadmap JSON: list of phases with nodes and projects."
    )
    overview = models.TextField(
        blank=True, default="",
        help_text="AI-generated overview/summary of the roadmap.",
    )
    estimated_duration = models.CharField(
        max_length=100, blank=True, default="",
        help_text="Estimated total duration (e.g. '6-8 weeks').",
    )
    user_input = models.TextField(
        blank=True, default="",
        help_text="Original conversational input from the user.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.skill_name} — {self.user or 'Guest'}"

    # ---------- computed helpers ----------

    @property
    def total_nodes(self):
        """Count all nodes across every phase."""
        count = 0
        for phase in self.phases:
            count += len(phase.get("nodes", []))
        return count

    @property
    def completed_nodes(self, user=None):
        """
        Number of nodes this roadmap's owner has completed.
        Uses the related NodeProgress rows.
        """
        return self.node_progress.filter(completed=True).count()

    @property
    def completion_percentage(self):
        total = self.total_nodes
        if total == 0:
            return 0
        return int((self.node_progress.filter(completed=True).count() / total) * 100)

    @property
    def total_projects(self):
        count = 0
        for phase in self.phases:
            # Handle both `projects` (array) and `project` (singular object)
            if "projects" in phase:
                count += len(phase["projects"])
            elif "project" in phase:
                count += 1
        return count


class NodeProgress(models.Model):
    """Tracks per-node completion for a user within a roadmap."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="node_progress",
    )
    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE,
        related_name="node_progress",
    )
    node_id = models.CharField(
        max_length=255, help_text="Unique identifier of the node within the roadmap JSON."
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "roadmap", "node_id")
        ordering = ["node_id"]

    def __str__(self):
        status = "✅" if self.completed else "⬜"
        return f"{status} {self.node_id} — {self.user}"


class ProjectProgress(models.Model):
    """Self-assessed project completion tracking."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_progress",
    )
    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE,
        related_name="project_progress",
    )
    project_id = models.CharField(
        max_length=255,
        help_text="Unique identifier of the project within the roadmap JSON.",
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "roadmap", "project_id")

    def __str__(self):
        status = "✅" if self.completed else "⬜"
        return f"{status} Project {self.project_id} — {self.user}"


class Streak(models.Model):
    """
    Tracks a user's daily learning streak.
    Updated every time a node is marked complete.
    Logic uses calendar days (timezone-aware), NOT 24-hour windows.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="streak",
        primary_key=True,
    )
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"🔥 {self.current_streak}-day streak — {self.user}"

    def update_streak(self):
        """
        Recalculate streak based on calendar days.
        Must be called every time the user completes a node.

        Rules:
          - If already active today → do nothing.
          - If last active yesterday → increment by 1.
          - If missed a day (or first activity ever) → reset to 1.
        """
        today = timezone.localdate()

        if self.last_active_date == today:
            # Already updated today — nothing to do
            return

        if self.last_active_date == today - timezone.timedelta(days=1):
            # Consecutive day — increment
            self.current_streak += 1
        else:
            # Missed a day or first time ever — reset to 1
            self.current_streak = 1

        # Track longest streak
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        self.last_active_date = today
        self.save()
