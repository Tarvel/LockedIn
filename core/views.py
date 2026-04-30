"""
Core views for LockedIn MVP.

Handles:
  - Landing page & roadmap generation trigger
  - Auth (signup, login, logout)
  - Dashboard
  - Roadmap detail view
  - HTMX progress-toggle endpoints (node + project)
  - Guest → authenticated roadmap hand-off
"""

import threading
import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import NodeProgress, ProjectProgress, Roadmap, Streak


# ---------------------------------------------------------------------------
# Landing Page
# ---------------------------------------------------------------------------

def landing_page(request):
    """Public landing page with the skill input form."""
    return render(request, "landing_page.html")


# ---------------------------------------------------------------------------
# Roadmap Generation — 2-step flow
# ---------------------------------------------------------------------------
# 1. Form POST  → store input in session → redirect to /loading/
# 2. Loading page → HTMX GET /generate/run/ → blocks until AI done → HX-Redirect
# ---------------------------------------------------------------------------


def generate_roadmap_view(request):
    """
    Step 1: Accepts form POST, stores input in session, redirects to loading.
    """
    if request.method != "POST":
        return redirect("landing")

    user_input = request.POST.get("skill", "").strip()
    if not user_input:
        messages.error(request, "Tell us what you want to learn!")
        return redirect("landing")

    # Store input in session and redirect to the loading screen
    request.session["pending_user_input"] = user_input
    return redirect(f"/loading/?skill={user_input}")


def generate_run(request):
    """
    Step 2: HTMX GET — does the actual AI generation synchronously.
    Blocks until the AI returns, creates the Roadmap, and sends HX-Redirect.
    """
    user_input = request.session.get("pending_user_input", "")
    print(f"[GENERATE] session={request.session.session_key}, input={user_input!r}")

    if not user_input:
        from django.http import JsonResponse
        return JsonResponse({"redirect": "/"})

    # Call the AI (this blocks for ~1-60s)
    try:
        from .ai import generate_roadmap as ai_generate
        roadmap_data = ai_generate(user_input)
        print(f"[GENERATE] AI returned successfully")
    except Exception as e:
        import traceback
        print(f"\n[AI ERROR] {type(e).__name__}: {e}")
        traceback.print_exc()
        roadmap_data = _demo_roadmap(user_input)

    # Clean up session
    request.session.pop("pending_user_input", None)

    # Unwrap the AI envelope
    if "data" in roadmap_data and "phases" in roadmap_data.get("data", {}):
        data = roadmap_data["data"]
    elif "phases" in roadmap_data:
        data = roadmap_data
    else:
        data = roadmap_data

    # Normalize: singular `project` → `projects` array
    phases = data.get("phases", [])
    for phase in phases:
        if "project" in phase and "projects" not in phase:
            phase["projects"] = [phase["project"]]

    skill_display = data.get("skill", user_input)
    overview = data.get("overview", "")
    estimated_duration = data.get("estimated_total_duration", "")

    # Create the roadmap row
    roadmap = Roadmap.objects.create(
        user=request.user if request.user.is_authenticated else None,
        skill_name=skill_display,
        phases=phases,
        overview=overview,
        estimated_duration=estimated_duration,
        user_input=user_input,
    )

    if not request.user.is_authenticated:
        request.session["guest_roadmap_id"] = str(roadmap.id)

    print(f"[GENERATE] Roadmap created: {roadmap.id}")

    # Return JSON with the redirect URL
    from django.http import JsonResponse
    return JsonResponse({"redirect": f"/roadmap/{roadmap.id}/"})


# ---------------------------------------------------------------------------
# Roadmap Detail View
# ---------------------------------------------------------------------------

def roadmap_detail(request, roadmap_id):
    """
    Display a single roadmap with phases, nodes, projects, and
    progress checkmarks (if logged in).
    """
    roadmap = get_object_or_404(Roadmap, id=roadmap_id)

    # Build a set of completed node/project IDs for the current user
    completed_nodes = set()
    completed_projects = set()
    is_owner = False

    if request.user.is_authenticated:
        completed_nodes = set(
            NodeProgress.objects.filter(
                user=request.user, roadmap=roadmap, completed=True
            ).values_list("node_id", flat=True)
        )
        completed_projects = set(
            ProjectProgress.objects.filter(
                user=request.user, roadmap=roadmap, completed=True
            ).values_list("project_id", flat=True)
        )
        is_owner = roadmap.user == request.user

    return render(request, "roadmap_view.html", {
        "roadmap": roadmap,
        "completed_nodes": completed_nodes,
        "completed_projects": completed_projects,
        "is_owner": is_owner,
        "completion_pct": roadmap.completion_percentage if request.user.is_authenticated else 0,
    })


# ---------------------------------------------------------------------------
# Loading Screen
# ---------------------------------------------------------------------------

def loading_screen(request):
    """Show the loading animation while roadmap generates."""
    skill = request.GET.get("skill", "your skill")
    return render(request, "loading_screen.html", {"skill": skill})


# ---------------------------------------------------------------------------
# Authentication Views
# ---------------------------------------------------------------------------

def signup_view(request):
    """Email + password sign up. Handles guest roadmap hand-off."""
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "signup.html")

        # Create user (username = email for simplicity)
        user = User.objects.create_user(
            username=email, email=email, password=password
        )
        login(request, user)

        # Create the initial streak record
        Streak.objects.create(user=user)

        # ---- Guest roadmap hand-off (F6 Req 5) ----
        guest_roadmap_id = request.session.pop("guest_roadmap_id", None)
        if guest_roadmap_id:
            try:
                roadmap = Roadmap.objects.get(id=guest_roadmap_id, user__isnull=True)
                roadmap.user = user
                roadmap.save()
                messages.success(request, "Your roadmap has been saved to your account!")
                return redirect("roadmap_detail", roadmap_id=roadmap.id)
            except Roadmap.DoesNotExist:
                pass

        return redirect("dashboard")

    return render(request, "signup.html")


def login_view(request):
    """Email + password login."""
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            # Recalculate streak on login (F4 Req 4)
            streak, _ = Streak.objects.get_or_create(user=user)

            # ---- Guest roadmap hand-off on login too ----
            guest_roadmap_id = request.session.pop("guest_roadmap_id", None)
            if guest_roadmap_id:
                try:
                    roadmap = Roadmap.objects.get(id=guest_roadmap_id, user__isnull=True)
                    roadmap.user = user
                    roadmap.save()
                    return redirect("roadmap_detail", roadmap_id=roadmap.id)
                except Roadmap.DoesNotExist:
                    pass

            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("landing")


# ---------------------------------------------------------------------------
# Dashboard (F7)
# ---------------------------------------------------------------------------

@login_required
def dashboard_view(request):
    """
    Displays:
      - All of the user's saved roadmaps with completion %
      - Current active streak
    """
    roadmaps = Roadmap.objects.filter(user=request.user)
    streak, _ = Streak.objects.get_or_create(user=request.user)

    roadmap_cards = []
    for rm in roadmaps:
        roadmap_cards.append({
            "roadmap": rm,
            "completion_pct": rm.completion_percentage,
            "total_nodes": rm.total_nodes,
            "completed_count": rm.node_progress.filter(completed=True).count(),
        })

    return render(request, "user_dashboard.html", {
        "roadmap_cards": roadmap_cards,
        "streak": streak,
    })


# ---------------------------------------------------------------------------
# HTMX Progress Endpoints (F3 + F5)
# ---------------------------------------------------------------------------

@require_POST
@login_required
def toggle_node_progress(request):
    """
    HTMX endpoint: POST /progress/node/
    Toggles a node's completion and returns an HTML partial.
    Also triggers the streak update.
    """
    roadmap_id = request.POST.get("roadmap_id")
    node_id = request.POST.get("node_id")

    roadmap = get_object_or_404(Roadmap, id=roadmap_id)

    progress, created = NodeProgress.objects.get_or_create(
        user=request.user,
        roadmap=roadmap,
        node_id=node_id,
    )

    # Toggle
    progress.completed = not progress.completed
    progress.completed_at = timezone.now() if progress.completed else None
    progress.save()

    # Update streak when marking complete (F4)
    if progress.completed:
        streak, _ = Streak.objects.get_or_create(user=request.user)
        streak.update_streak()

    return render(request, "partials/node_checkbox.html", {
        "roadmap": roadmap,
        "node_id": node_id,
        "completed": progress.completed,
        "completion_pct": roadmap.completion_percentage,
    })


@require_POST
@login_required
def toggle_project_progress(request):
    """
    HTMX endpoint: POST /progress/project/
    Toggles a project's completion and returns an HTML partial.
    """
    roadmap_id = request.POST.get("roadmap_id")
    project_id = request.POST.get("project_id")

    roadmap = get_object_or_404(Roadmap, id=roadmap_id)

    progress, created = ProjectProgress.objects.get_or_create(
        user=request.user,
        roadmap=roadmap,
        project_id=project_id,
    )

    progress.completed = not progress.completed
    progress.completed_at = timezone.now() if progress.completed else None
    progress.save()

    return render(request, "partials/project_checkbox.html", {
        "roadmap": roadmap,
        "project_id": project_id,
        "completed": progress.completed,
    })


# ---------------------------------------------------------------------------
# Guest Auth Check (returns modal partial for HTMX)
# ---------------------------------------------------------------------------

def guest_auth_check(request):
    """
    HTMX endpoint hit when an unauthenticated user clicks a node.
    Returns the signup prompt modal partial.    
    """
    if request.user.is_authenticated:
        return HttpResponse("")  # no-op if somehow called while logged in
    return render(request, "partials/auth_modal.html")


# ---------------------------------------------------------------------------
# Demo roadmap data for development
# ---------------------------------------------------------------------------

def _demo_roadmap(user_input):
    """
    Generate placeholder roadmap data matching the real AI pipeline schema.
    Uses `project` (singular) per phase, `estimated_completion_time`,
    `tools_needed`, and real resource structure.
    """
    # Extract a rough skill name from the conversational input
    skill = user_input.strip().rstrip(".!?")
    lower = skill.lower()
    for prefix in [
        "i want to learn ", "i wanna learn ", "i want to get good at ",
        "i wanna get good at ", "help me learn ", "teach me ",
        "i want to become a ", "help me become a ",
        "i'd like to learn ", "i would like to learn ",
        "i want to ", "i wanna ",
    ]:
        if lower.startswith(prefix):
            skill = skill[len(prefix):]
            break

    return {
        "success": True,
        "data": {
            "skill": skill.strip().title(),
            "normalized_skill": skill.strip().lower().replace(" ", "_"),
            "overview": f"A practical beginner roadmap for learning {skill}. Focuses on building confidence through hands-on practice and real projects.",
            "estimated_total_duration": "6-8 weeks",
            "phases": [
                {
                    "id": "phase_1",
                    "title": "Foundations",
                    "level": "beginner",
                    "goal": f"Understand the basics of {skill} — core concepts, syntax, and setup.",
                    "estimated_duration": "2 weeks",
                    "nodes": [
                        {
                            "id": "phase_1_node_1",
                            "title": "Set up and get started",
                            "description": f"Install the tools you need, run your first examples, and get comfortable with the {skill} environment.",
                            "estimated_completion_time": "2-3 hours",
                            "resources": [
                                {
                                    "id": "phase_1_node_1_resource_1",
                                    "title": f"{skill.title()} for Beginners",
                                    "url": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial+beginners",
                                    "type": "youtube_video",
                                    "source": "YouTube",
                                    "is_free": True,
                                },
                                {
                                    "id": "phase_1_node_1_resource_2",
                                    "title": f"{skill.title()} Getting Started Guide",
                                    "url": f"https://www.google.com/search?q={skill.replace(' ', '+')}+getting+started",
                                    "type": "article",
                                    "source": "Tavily",
                                    "is_free": True,
                                },
                            ],
                        },
                        {
                            "id": "phase_1_node_2",
                            "title": "Core concepts and fundamentals",
                            "description": f"Learn the building blocks of {skill}. Focus on understanding the key ideas before trying to build anything complex.",
                            "estimated_completion_time": "3-4 hours",
                            "resources": [
                                {
                                    "id": "phase_1_node_2_resource_1",
                                    "title": f"{skill.title()} Fundamentals",
                                    "url": "#",
                                    "type": "documentation",
                                    "source": "Tavily",
                                    "is_free": True,
                                },
                            ],
                        },
                        {
                            "id": "phase_1_node_3",
                            "title": "Practice exercises",
                            "description": "Work through guided exercises to reinforce what you've learned. Repetition builds confidence.",
                            "estimated_completion_time": "3-4 hours",
                            "resources": [
                                {
                                    "id": "phase_1_node_3_resource_1",
                                    "title": f"{skill.title()} Practice Problems",
                                    "url": "#",
                                    "type": "article",
                                    "source": "Tavily",
                                    "is_free": True,
                                },
                            ],
                        },
                    ],
                    "project": {
                        "id": "phase_1_project_1",
                        "phase_id": "phase_1",
                        "title": f"Mini {skill} project",
                        "brief": f"Build a small, self-contained project using only {skill} fundamentals. Keep it simple — the goal is to prove you can build something from scratch.",
                        "tools_needed": ["Code Editor", "Terminal"],
                        "resources": [
                            {
                                "id": "phase_1_project_1_resource_1",
                                "title": f"{skill.title()} Project Ideas",
                                "url": "#",
                                "type": "article",
                                "source": "Tavily",
                                "is_free": True,
                            },
                        ],
                    },
                },
                {
                    "id": "phase_2",
                    "title": "Core Skills",
                    "level": "beginner",
                    "goal": f"Apply {skill} to solve real problems and build useful tools.",
                    "estimated_duration": "2-3 weeks",
                    "nodes": [
                        {
                            "id": "phase_2_node_1",
                            "title": "Intermediate techniques",
                            "description": f"Learn patterns and tools that working {skill} practitioners use daily.",
                            "estimated_completion_time": "3-4 hours",
                            "resources": [
                                {
                                    "id": "phase_2_node_1_resource_1",
                                    "title": f"Intermediate {skill.title()} Guide",
                                    "url": "#",
                                    "type": "article",
                                    "source": "Tavily",
                                    "is_free": True,
                                },
                            ],
                        },
                        {
                            "id": "phase_2_node_2",
                            "title": "Working with data and APIs",
                            "description": "Connect to external services, handle files, and work with structured data.",
                            "estimated_completion_time": "3-4 hours",
                            "resources": [],
                        },
                        {
                            "id": "phase_2_node_3",
                            "title": "Debugging and problem solving",
                            "description": "Learn to read errors, isolate bugs, and think systematically about problems.",
                            "estimated_completion_time": "2-3 hours",
                            "resources": [],
                        },
                    ],
                    "project": {
                        "id": "phase_2_project_1",
                        "phase_id": "phase_2",
                        "title": f"Practical {skill} tool",
                        "brief": f"Build a useful tool that solves a real problem using {skill}. Focus on clean code and good structure.",
                        "tools_needed": ["Code Editor", "Git", "Terminal"],
                        "resources": [],
                    },
                },
                {
                    "id": "phase_3",
                    "title": "Build Confidence",
                    "level": "advanced beginner",
                    "goal": "Practice with real-world projects and solidify your skills.",
                    "estimated_duration": "2-3 weeks",
                    "nodes": [
                        {
                            "id": "phase_3_node_1",
                            "title": "Project architecture",
                            "description": "Learn how to structure larger projects so they're maintainable and extensible.",
                            "estimated_completion_time": "3-4 hours",
                            "resources": [],
                        },
                        {
                            "id": "phase_3_node_2",
                            "title": "Best practices and code quality",
                            "description": "Write clean, readable code. Learn testing basics and version control workflows.",
                            "estimated_completion_time": "3-5 hours",
                            "resources": [],
                        },
                        {
                            "id": "phase_3_node_3",
                            "title": "Build and ship something real",
                            "description": "Take everything you've learned and build a complete project from start to finish.",
                            "estimated_completion_time": "4-6 hours",
                            "resources": [],
                        },
                    ],
                    "project": {
                        "id": "phase_3_project_1",
                        "phase_id": "phase_3",
                        "title": f"Capstone {skill} project",
                        "brief": f"Design and build a portfolio-worthy project using {skill}. This is your chance to show what you can do.",
                        "tools_needed": ["Code Editor", "Git", "GitHub"],
                        "resources": [],
                    },
                },
            ],
        },
    }

