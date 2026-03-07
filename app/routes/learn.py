"""
Learning platform routes: Introduction, Problem Statement, Expert Design,
Flask Concepts, Interview Prep, Assessment (MCQ), Revision, and API for assessment.
"""
import os
import json
import random
from flask import Blueprint, render_template, request, jsonify

learn_bp = Blueprint("learn", __name__)

# Path to data files (project root)
def _data_path(filename):
    # From app/routes/learn.py -> go up to task_management_system (3 levels)
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, "data", filename)


# --- Page routes ---

@learn_bp.route("/")
def intro():
    return render_template("learn/intro.html")


@learn_bp.route("/learn/problem")
def problem():
    return render_template("learn/problem.html")


@learn_bp.route("/learn/design")
def design():
    return render_template("learn/design.html")


@learn_bp.route("/learn/flask")
def flask_concepts():
    return render_template("learn/flask_concepts.html")


@learn_bp.route("/learn/flask/routing")
def flask_routing():
    return render_template("learn/concepts/routing.html")


@learn_bp.route("/learn/flask/templates")
def flask_templates():
    return render_template("learn/concepts/templates.html")


@learn_bp.route("/learn/flask/blueprints")
def flask_blueprints():
    return render_template("learn/concepts/blueprints.html")


@learn_bp.route("/learn/flask/request-response")
def flask_request_response():
    return render_template("learn/concepts/request_response.html")


@learn_bp.route("/learn/flask/configuration")
def flask_configuration():
    return render_template("learn/concepts/configuration.html")


@learn_bp.route("/learn/flask/forms")
def flask_forms():
    return render_template("learn/concepts/forms.html")


@learn_bp.route("/learn/flask/database")
def flask_database():
    return render_template("learn/concepts/database.html")


@learn_bp.route("/learn/interview")
def interview():
    return render_template("learn/interview.html")


@learn_bp.route("/learn/interview/preparation")
def interview_preparation():
    return render_template("learn/interview_preparation.html")


@learn_bp.route("/learn/interview/assessment")
def interview_assessment():
    return render_template("learn/interview_assessment.html")


@learn_bp.route("/learn/revision")
def revision():
    return render_template("learn/revision.html")


# --- API: Interview questions (by difficulty) ---

@learn_bp.route("/api/learn/interview/questions", methods=["GET"])
def api_interview_questions():
    difficulty = request.args.get("difficulty", "easy")
    path = _data_path("interview_preparation.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        questions = data.get(difficulty, [])
        return jsonify({"questions": questions, "difficulty": difficulty}), 200
    except FileNotFoundError:
        return jsonify({"error": "Questions file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- API: Assessment (MCQ) ---

@learn_bp.route("/api/learn/assessment/questions", methods=["GET"])
def api_assessment_questions():
    count = int(request.args.get("count", 10))
    level = request.args.get("level", "beginner")
    path = _data_path("assessment_questions.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_questions = data.get("questions", [])
        if level in ("interns", "beginner"):
            easy = [q for q in all_questions if q.get("difficulty") == "easy"]
            medium = [q for q in all_questions if q.get("difficulty") == "medium"]
            n_easy = min(int(count * 0.7), len(easy))
            n_medium = count - n_easy
            selected = random.sample(easy, n_easy) + random.sample(medium, min(n_medium, len(medium)))
        elif level == "intermediate":
            medium = [q for q in all_questions if q.get("difficulty") == "medium"]
            hard = [q for q in all_questions if q.get("difficulty") == "hard"]
            n_med = min(int(count * 0.6), len(medium))
            n_hard = count - n_med
            selected = random.sample(medium, n_med) + random.sample(hard, min(n_hard, len(hard)))
        elif level == "expert":
            hard = [q for q in all_questions if q.get("difficulty") == "hard"]
            expert = [q for q in all_questions if q.get("difficulty") == "expert"]
            n_hard = min(int(count * 0.5), len(hard))
            n_exp = count - n_hard
            selected = random.sample(hard, n_hard) + random.sample(expert, min(n_exp, len(expert)))
        else:
            selected = random.sample(all_questions, min(count, len(all_questions)))
        random.shuffle(selected)
        for q in selected:
            q.pop("correct_answer", None)
            q.pop("explanation", None)
        return jsonify({"questions": selected, "total": len(selected), "level": level}), 200
    except FileNotFoundError:
        return jsonify({"error": "Assessment file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@learn_bp.route("/api/learn/assessment/submit", methods=["POST"])
def api_assessment_submit():
    answers = request.json.get("answers", {})
    path = _data_path("assessment_questions.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_questions = {q["id"]: q for q in data.get("questions", [])}
        correct = 0
        total = len(answers)
        results = []
        for q_id, user_answer in answers.items():
            question = all_questions.get(q_id)
            if not question:
                continue
            correct_answer = question.get("correct_answer")
            is_correct = user_answer == correct_answer
            if is_correct:
                correct += 1
            results.append({
                "question_id": q_id,
                "question": question.get("question"),
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question.get("explanation", ""),
                "difficulty": question.get("difficulty", "unknown"),
            })
        pct = (correct / total * 100) if total > 0 else 0
        if pct >= 90:
            grade = "Excellent"
        elif pct >= 75:
            grade = "Good"
        elif pct >= 60:
            grade = "Average"
        else:
            grade = "Needs Improvement"
        return jsonify({
            "score": correct,
            "total": total,
            "percentage": round(pct, 2),
            "grade": grade,
            "results": results,
        }), 200
    except FileNotFoundError:
        return jsonify({"error": "Assessment file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
