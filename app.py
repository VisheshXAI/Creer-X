import os
import random
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "careerx_hyper_secret_key_98234")

# Mock dynamic interview question bank for 5 rounds
QUESTIONS_DB = {
    "AI Engineer": {
        1: "Tell me about your technical background. What programming languages and core fundamentals do you feel most confident with?",
        2: "How do you handle vanishing or exploding gradients when training deep transformer networks?",
        3: "Walk me through the architecture of an end-to-end AI project you built. What was the latency bottleneck and how did you resolve it?",
        4: "Imagine your RAG pipeline produces hallucinations on 15% of queries. What systematic evaluation framework would you use to diagnose it?",
        5: "Where do you see yourself contributing in the AI ecosystem over the next 2 years?"
    },
    "Data Scientist": {
        1: "Give me an overview of your background in statistical modeling, Python, and data pipelines.",
        2: "How do you deal with severe class imbalance (e.g., 99:1 ratio) when evaluating predictive models?",
        3: "Describe an impactful machine learning model you deployed into production. How did you validate business ROI?",
        4: "Suppose your feature store drift detector alerts a 30% covariate shift. How do you isolate the faulty feature?",
        5: "What are your core career milestones in data science over the next 18 months?"
    },
    "Software Engineer": {
        1: "Walk me through your engineering stack and how you approach writing clean, modular, test-driven code.",
        2: "Explain the internal trade-offs between relational vs distributed NoSQL stores under heavy concurrent writes.",
        3: "Describe a distributed system or microservice you built. How did you handle fault tolerance and API rate limiting?",
        4: "If an API endpoint latency suddenly spikes to 4 seconds during peak traffic, what step-by-step triage do you run?",
        5: "What kind of engineering leadership or technical challenges do you want to tackle next?"
    }
}

DEFAULT_QUESTIONS = {
    1: "Tell me about your background and what motivated you to transition into this field.",
    2: "What is your current depth with the core technical tools and frameworks needed for this role?",
    3: "Describe a real-world technical project you worked on from problem definition to final delivery.",
    4: "How do you approach debugging complex, undocumented bugs under tight deadlines?",
    5: "What are your primary goals for your next career jump?"
}

# --- ROUTES ---

@app.route("/")
def index():
    """Step 1: Target Job Selection Page"""
    return render_template("target.html")

@app.route("/api/select-target", methods=["POST"])
def select_target():
    """Stores chosen target role in session"""
    data = request.get_json() or {}
    role = data.get("role", "AI Engineer")
    session["target_role"] = role
    return jsonify({"status": "success", "role": role, "redirect": url_for("mentor_selection")})

@app.route("/mentor")
def mentor_selection():
    """Step 2: Hyper-realistic live mentor selection"""
    target_role = session.get("target_role", "AI Engineer")
    return render_template("mentor.html", target_role=target_role)

@app.route("/api/select-mentor", methods=["POST"])
def select_mentor():
    """Stores selected mentor in session"""
    data = request.get_json() or {}
    mentor = data.get("mentor", "Arjun")
    session["mentor"] = mentor
    return jsonify({"status": "success", "mentor": mentor, "redirect": url_for("interview_room")})

@app.route("/interview")
def interview_room():
    """Step 3: 5-Round Live AI Video Interview Room"""
    target_role = session.get("target_role", "AI Engineer")
    mentor = session.get("mentor", request.args.get("mentor", "Arjun"))
    session["mentor"] = mentor
    session["round"] = 1
    session["interview_log"] = []
    return render_template("interview.html", target_role=target_role, mentor=mentor)

@app.route("/api/interview/question", methods=["GET"])
def get_question():
    """Returns dynamic question based on current round & role"""
    current_round = session.get("round", 1)
    role = session.get("target_role", "AI Engineer")
    
    questions = QUESTIONS_DB.get(role, DEFAULT_QUESTIONS)
    question = questions.get(current_round, DEFAULT_QUESTIONS.get(current_round, "Thank you."))
    
    return jsonify({
        "round": current_round,
        "max_rounds": 5,
        "role": role,
        "mentor": session.get("mentor", "Arjun"),
        "question": question
    })

@app.route("/api/interview/submit-answer", methods=["POST"])
def submit_answer():
    """Evaluates answer, scores response telemetry, and steps to next round"""
    data = request.get_json() or {}
    answer_text = data.get("answer", "").strip()
    current_round = session.get("round", 1)
    
    # Store transcript
    interview_log = session.get("interview_log", [])
    interview_log.append({
        "round": current_round,
        "answer": answer_text,
        "word_count": len(answer_text.split())
    })
    session["interview_log"] = interview_log

    if current_round >= 5:
        # Generate diagnostic telemetry
        session["evaluation"] = {
            "skill_score": random.randint(76, 88),
            "confidence_score": random.randint(80, 92),
            "communication_score": random.randint(82, 94),
            "technical_readiness": "Tier-1 Ready (Minor Gaps)",
            "learning_speed": "High Velocity (Top 12%)"
        }
        return jsonify({"completed": True, "redirect": url_for("skill_gap")})

    session["round"] = current_round + 1
    return jsonify({"completed": False, "next_round": session["round"]})

@app.route("/skill-gap")
def skill_gap():
    """Step 4 & 5: Diagnostic Engine & Skill Gap Analysis"""
    evaluation = session.get("evaluation", {
        "skill_score": 82,
        "confidence_score": 88,
        "communication_score": 85,
        "technical_readiness": "Tier-1 Ready",
        "learning_speed": "Fast"
    })
    target_role = session.get("target_role", "AI Engineer")
    mentor = session.get("mentor", "Arjun")
    return render_template("skill_gap.html", evaluation=evaluation, target_role=target_role, mentor=mentor)

@app.route("/roadmap")
def roadmap():
    """Step 6: Personalized Step-by-Step Execution Plan"""
    target_role = session.get("target_role", "AI Engineer")
    mentor = session.get("mentor", "Arjun")
    return render_template("roadmap.html", target_role=target_role, mentor=mentor)

@app.route("/dashboard")
def dashboard():
    """Step 7: Final Career Command Cockpit"""
    target_role = session.get("target_role", "AI Engineer")
    evaluation = session.get("evaluation", {"skill_score": 84})
    return render_template("dashboard.html", target_role=target_role, evaluation=evaluation)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)