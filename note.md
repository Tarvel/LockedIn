user can intereract conversationally with the inptut box
i mean like instead of just the key words like for skill its just "python" user can say "i wanna get good at python" and the ai will still be able to understand what the user wants and generate a roadmap accordingly. then separate the text into skill, current level, and target date. such as the json below:
{
  "skill": "Python",
  "user_level": "complete beginner",
  "goal": "learn the skill step by step and build practical confidence",
  "time_commitment": "3 to 5 hours per week",
  "preferred_resource_types": [
    "youtube_video"
  ],
  "language": "English"
}

the output that the json gives is as follows:
Output Schema

{
  "success": true,
  "data": {
    "roadmap_id": "roadmap_python_fe7d06",
    "skill": "Python for Beginners",
    "normalized_skill": "python",
    "overview": "A practical beginner roadmap for learning Python from basic syntax to small projects. It focuses on confidence, repetition, and building useful scripts.",
    "estimated_total_duration": "6-8 weeks",
    "phases": [
      {
        "id": "phase_1",
        "title": "Foundations",
        "level": "beginner",
        "goal": "Understand Python syntax, variables, conditions, and loops.",
        "estimated_duration": "2 weeks",
        "nodes": [
          {
            "id": "phase_1_node_1",
            "title": "Set up and write first scripts",
            "description": "Install Python, run simple scripts, and understand how code is executed. Practice printing values and reading beginner examples.",
            "estimated_completion_time": "2-3 hours",
            "resources": [
              {
                "id": "phase_1_node_1_resource_1",
                "title": "Python for Beginners - Programming with Mosh",
                "url": "https://www.youtube.com/watch?v=kqtD5dpn9C8",
                "type": "youtube_video",
                "source": "YouTube",
                "is_free": true
              },
              {
                "id": "phase_1_node_1_resource_2",
                "title": "Python Tutorial - W3Schools",
                "url": "https://www.w3schools.com/python/",
                "type": "article",
                "source": "Tavily",
                "is_free": true
              }
            ]
          },
          {
            "id": "phase_1_node_2",
            "title": "Variables and data types",
            "description": "Learn strings, numbers, booleans, lists, and dictionaries. Use small examples to see how values change while a program runs.",
            "estimated_completion_time": "2-3 hours",
            "resources": [
              {
                "id": "phase_1_node_2_resource_1",
                "title": "Python Variables - Official Tutorial",
                "url": "https://docs.python.org/3/tutorial/introduction.html",
                "type": "documentation",
                "source": "Tavily",
                "is_free": true
              },
              {
                "id": "phase_1_node_2_resource_2",
                "title": "Python Data Types - Programiz",
                "url": "https://www.programiz.com/python-programming/variables-datatypes",
                "type": "article",
                "source": "Tavily",
                "is_free": true
              }
            ]
          },
          {
            "id": "phase_1_node_3",
            "title": "Conditions and loops",
            "description": "Use if statements and loops to make programs respond to different situations. Practice with short exercises until the flow feels natural.",
            "estimated_completion_time": "3-4 hours",
            "resources": [
              {
                "id": "phase_1_node_3_resource_1",
                "title": "Python If Else - W3Schools",
                "url": "https://www.w3schools.com/python/python_conditions.asp",
                "type": "article",
                "source": "Tavily",
                "is_free": true
              },
              {
                "id": "phase_1_node_3_resource_2",
                "title": "Python For Loops - W3Schools",
                "url": "https://www.w3schools.com/python/python_for_loops.asp",
                "type": "article",
                "source": "Tavily",
                "is_free": true
              }
            ]
          }
        ],
        "project": {
          "id": "phase_1_project_1",
          "phase_id": "phase_1",
          "title": "Simple quiz game",
          "brief": "Build a command-line quiz that asks questions, checks answers, and shows a final score. Keep the questions in a list or dictionary.",
          "tools_needed": [
            "Python",
            "Code editor"
          ],
          "resources": [
            {
              "id": "phase_1_project_1_resource_1",
              "title": "Python for Beginners - Programming with Mosh",
              "url": "https://www.youtube.com/watch?v=kqtD5dpn9C8",
              "type": "youtube_video",
              "source": "YouTube",
              "is_free": true
            },
            {
              "id": "phase_1_project_1_resource_2",
              "title": "Python Lists - W3Schools",
              "url": "https://www.w3schools.com/python/python_lists.asp",
              "type": "article",
              "source": "Tavily",
              "is_free": true
            }
          ]
        }
      },
      {
        "id": "phase_2",
        "title": "Core Skills",
        "level": "beginner",
        "goal": "Use functions, files, and modules to organize useful programs.",
        "estimated_duration": "2-3 weeks",
        "nodes": [
          {
            "id": "phase_2_node_1",
            "title": "Functions",
            "description": "Break repeated logic into functions with inputs and return values. This helps you write cleaner programs that are easier to test.",
            "estimated_completion_time": "3-4 hours",
            "resources": [
              {
                "id": "phase_2_node_1_resource_1",
                "title": "Python Functions - W3Schools",
                "url": "https://www.w3schools.com/python/python_functions.asp",
                "type": "article",
                "source": "Tavily",
                "is_free": true
              },
              {
                "id": "phase_2_node_1_resource_2",
                "title": "Defining Functions - Python Docs",
                "url": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions",
                "type": "documentation",
                "source": "Tavily",
                "is_free": true
              }
            ]
          },
          {
            "id": "phase_2_node_2",
            "title": "Files and errors",
            "description": "Read and write text files, then handle common errors safely. Practice saving simple notes or scores to a local file.",
            "estimated_completion_time": "3-4 hours",
            "resources": [
              {
                "id": "phase_2_node_2_resource_1",
                "title": "Reading and Writing Files - Python Docs",
                "url": "https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files",
                "type": "documentation",
                "source": "Tavily",
                "is_free": true
              },
              {
                "id": "phase_2_node_2_resource_2",
                "title": "Python Try Except - W3Schools",
                "url": "https://www.w3schools.com/python/python_try_except.asp",
                "type": "article",
                "source": "Tavily",
                "is_free": true
              }
            ]
          },
          {
            "id": "phase_2_node_3",
            "title": "Modules and packages",
            "description": "Learn how Python code can be split into modules and reused. Try importing standard library tools before installing third-party packages.",
            "estimated_completion_time": "2-3 hours",
            "resources": [
              {
                "id": "phase_2_node_3_resource_1",
                "title": "Python Modules - Python Docs",
                "url": "https://docs.python.org/3/tutorial/modules.html",
                "type": "documentation",
                "source": "Tavily",
                "is_free": true
              },
              {
                "id": "phase_2_node_3_resource_2",
                "title": "Python Standard Library",
                "url": "https://docs.python.org/3/library/",
                "type": "documentation",
                "source": "Tavily",
                "is_free": true
              }
            ]
          }
        ],
        "project": {
          "id": "phase_2_project_1",
          "phase_id": "phase_2",
          "title": "Personal expense tracker",
          "brief": "Create a command-line expense tracker that lets you add expenses, save them to a file, and show totals by category.",
          "tools_needed": [
            "Python",
            "Text files"
          ],
          "resources": [
            {
              "id": "phase_2_project_1_resource_1",
              "title": "Reading and Writing Files - Python Docs",
              "url": "https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files",
              "type": "documentation",
              "source": "Tavily",
              "is_free": true
            },
            {
              "id": "phase_2_project_1_resource_2",
              "title": "Python Dictionaries - W3Schools",
              "url": "https://www.w3schools.com/python/python_dictionaries.asp",
              "type": "article",
              "source": "Tavily",
              "is_free": true
            }
          ]
        }
      },
      {
        "id": "phase_3",
        "title": "Build Confidence",
        "level": "advanced beginner",
        "goal": "Practice with project structure, debugging, and small real-world tools.",
        "estimated_duration": "2-3 weeks",
        "nodes": [
          {
            "id": "phase_3_node_1",
            "title": "Debugging basics",
            "description": "Learn to read error messages and isolate problems with print statements or a debugger. Debugging is a normal part of programming.",
            "estimated_completion_time": "2-3 hours",
            "resources": [
              {
                "id": "phase_3_node_1_resource_1",
                "title": "Python Errors and Exceptions",
                "url": "https://docs.python.org/3/tutorial/errors.html",
                "type": "documentation",
                "source": "Tavily",
                "is_free": true
              },
              {
                "id": "phase_3_node_1_resource_2",
                "title": "Python Debugging With pdb",
                "url": "https://docs.python.org/3/library/pdb.html",
                "type": "documentation",
                "source": "Tavily",
                "is_free": true
              }
            ]
          },
          {
            "id": "phase_3_node_2",
            "title": "Work with APIs",
            "description": "Use Python to request data from the web and inspect JSON responses. Start with public APIs that do not need authentication.",
            "estimated_completion_time": "3-5 hours",
            "resources": [
              {
                "id": "phase_3_node_2_resource_1",
                "title": "Requests: HTTP for Humans",
                "url": "https://requests.readthedocs.io/en/latest/",
                "type": "documentation",
                "source": "Tavily",
                "is_free": true
              },
              {
                "id": "phase_3_node_2_resource_2",
                "title": "JSON in Python",
                "url": "https://docs.python.org/3/library/json.html",
                "type": "documentation",
                "source": "Tavily",
                "is_free": true
              }
            ]
          },
          {
            "id": "phase_3_node_3",
            "title": "Practice small projects",
            "description": "Build several small tools instead of one large app. Repetition helps you remember syntax and develop problem-solving habits.",
            "estimated_completion_time": "4-6 hours",
            "resources": [
              {
                "id": "phase_3_node_3_resource_1",
                "title": "freeCodeCamp Python Projects",
                "url": "https://www.freecodecamp.org/news/python-projects-for-beginners/",
                "type": "article",
                "source": "Tavily",
                "is_free": true
              },
              {
                "id": "phase_3_node_3_resource_2",
                "title": "Automate the Boring Stuff",
                "url": "https://automatetheboringstuff.com/",
                "type": "free_book",
                "source": "Tavily",
                "is_free": true
              }
            ]
          }
        ],
        "project": {
          "id": "phase_3_project_1",
          "phase_id": "phase_3",
          "title": "Weather summary script",
          "brief": "Build a script that fetches public weather data, parses JSON, and prints a short readable summary for a city.",
          "tools_needed": [
            "Python",
            "Requests",
            "Public API"
          ],
          "resources": [
            {
              "id": "phase_3_project_1_resource_1",
              "title": "Requests: HTTP for Humans",
              "url": "https://requests.readthedocs.io/en/latest/",
              "type": "documentation",
              "source": "Tavily",
              "is_free": true
            },
            {
              "id": "phase_3_project_1_resource_2",
              "title": "JSON in Python",
              "url": "https://docs.python.org/3/library/json.html",
              "type": "documentation",
              "source": "Tavily",
              "is_free": true
            }
          ]
        }
      }
    ],
    "projects": [
      {
        "id": "phase_1_project_1",
        "phase_id": "phase_1",
        "title": "Simple quiz game",
        "brief": "Build a command-line quiz that asks questions, checks answers, and shows a final score. Keep the questions in a list or dictionary.",
        "tools_needed": [
          "Python",
          "Code editor"
        ],
        "resources": [
          {
            "id": "phase_1_project_1_resource_1",
            "title": "Python for Beginners - Programming with Mosh",
            "url": "https://www.youtube.com/watch?v=kqtD5dpn9C8",
            "type": "youtube_video",
            "source": "YouTube",
            "is_free": true
          },
          {
            "id": "phase_1_project_1_resource_2",
            "title": "Python Lists - W3Schools",
            "url": "https://www.w3schools.com/python/python_lists.asp",
            "type": "article",
            "source": "Tavily",
            "is_free": true
          }
        ]
      },
      {
        "id": "phase_2_project_1",
        "phase_id": "phase_2",
        "title": "Personal expense tracker",
        "brief": "Create a command-line expense tracker that lets you add expenses, save them to a file, and show totals by category.",
        "tools_needed": [
          "Python",
          "Text files"
        ],
        "resources": [
          {
            "id": "phase_2_project_1_resource_1",
            "title": "Reading and Writing Files - Python Docs",
            "url": "https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files",
            "type": "documentation",
            "source": "Tavily",
            "is_free": true
          },
          {
            "id": "phase_2_project_1_resource_2",
            "title": "Python Dictionaries - W3Schools",
            "url": "https://www.w3schools.com/python/python_dictionaries.asp",
            "type": "article",
            "source": "Tavily",
            "is_free": true
          }
        ]
      },
      {
        "id": "phase_3_project_1",
        "phase_id": "phase_3",
        "title": "Weather summary script",
        "brief": "Build a script that fetches public weather data, parses JSON, and prints a short readable summary for a city.",
        "tools_needed": [
          "Python",
          "Requests",
          "Public API"
        ],
        "resources": [
          {
            "id": "phase_3_project_1_resource_1",
            "title": "Requests: HTTP for Humans",
            "url": "https://requests.readthedocs.io/en/latest/",
            "type": "documentation",
            "source": "Tavily",
            "is_free": true
          },
          {
            "id": "phase_3_project_1_resource_2",
            "title": "JSON in Python",
            "url": "https://docs.python.org/3/library/json.html",
            "type": "documentation",
            "source": "Tavily",
            "is_free": true
          }
        ]
      }
    ],
    "metadata": {
      "model_used": "demo_fallback",
      "resource_sources": [
        "demo"
      ],
      "generated_at": "2026-04-30T02:00:12.744887Z",
      "cached": true,
      "fallback": true
    }
  }
}
