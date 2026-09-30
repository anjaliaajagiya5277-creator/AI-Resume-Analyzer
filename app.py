import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from werkzeug.utils import secure_filename

from config import Config

from parser.resume_parser import ResumeParser

from parser.jd_parser import JDParser

from matcher.jd_analyzer import JDAnalyzer

from matcher.matcher import SkillMatcher

from parser.info_extractor import ResumeInfoExtractor

from scorer.ats_scorer import ATSScorer

from ai.gemini_analyzer import GeminiResumeAnalyzer


app = Flask(__name__)

app.config.from_object(Config)


def allowed_resume(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in app.config["ALLOWED_RESUME_EXTENSIONS"]
    )


def allowed_jd(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in app.config["ALLOWED_JD_EXTENSIONS"]
    )


@app.route("/")
def home():

    return render_template(

    "index.html",

    info=None,

    jd_info=None,

    match_result=None,

    ats_score=None,

    ai_recommendation=None

)
@app.route("/upload", methods=["POST"])
def upload():

    jd = request.files.get("job_description")
    resume = request.files.get("resume")

    if not jd or jd.filename == "":
        flash("Please select a Job Description.")
        return redirect(url_for("home"))

    if not resume or resume.filename == "":
        flash("Please select a Resume.")
        return redirect(url_for("home"))

    if not allowed_jd(jd.filename):
        flash("Invalid Job Description format.")
        return redirect(url_for("home"))

    if not allowed_resume(resume.filename):
        flash("Resume must be a PDF.")
        return redirect(url_for("home"))

    jd_name = secure_filename(jd.filename)
    resume_name = secure_filename(resume.filename)

    jd_path = os.path.join(app.config["UPLOAD_FOLDER"], jd_name)
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_name)

    jd.save(jd_path)
    resume.save(resume_path)

    # Extract text
    # ---------------------------------------
    # Extract Text
    # ---------------------------------------

    jd_text = JDParser.extract_text(jd_path)
    resume_text = ResumeParser.extract_text(resume_path)

    # ---------------------------------------
    # Extract Resume Information
    # ---------------------------------------

    extractor = ResumeInfoExtractor(resume_text)
    info = extractor.extract_all()

    # ---------------------------------------
    # Extract Job Description Information
    # ---------------------------------------

    jd_analyzer = JDAnalyzer(jd_text)
    jd_info = jd_analyzer.extract_all()

    # ---------------------------------------
    # Compare Resume & JD
    # ---------------------------------------

    matcher = SkillMatcher(

        info["skills"],

        jd_info["required_skills"]

    )

    match_result = matcher.compare()
    
    analysis_data = {

    "resume_info": info,

    "job_description": jd_text,

    "job_requirements": jd_info,

    "matched_skills": match_result["matched_skills"],

    "missing_skills": match_result["missing_skills"],

    "job_match": match_result["job_match"],

    "decision": match_result["decision"]

    }
    # ---------------------------------------
    # ATS Score Calculation
    # ---------------------------------------

    ats = ATSScorer(
        info,
        jd_info,
        match_result
    )

    ats_score = ats.total_score()
    # ---------------------------------------
    # Gemini AI Recommendation
    # ---------------------------------------

    gemini = GeminiResumeAnalyzer()

    ai_recommendation = gemini.generate_recommendation(

        info,

        jd_text,

        jd_info,

        match_result,

        ats_score

    )

    print("\n" + "=" * 70)
    print("JOB DESCRIPTION SKILLS")
    print("=" * 70)

    if jd_info["skills"]:

        for skill in jd_info["skills"]:

            print(skill)

    else:

        print("No Skills Found")
    print("\n" + "=" * 70)
    print("JOB DESCRIPTION REQUIREMENTS")
    print("=" * 70)

    print("\nEducation")

    print("-" * 10)

    if jd_info["education"]:

        for degree in jd_info["education"]:

            print(degree)

    else:

        print("Not Mentioned")

    print("\nExperience")

    print("-" * 10)

    print(jd_info["experience"])
    print("\n" + "=" * 70)
    print("PREFERRED SKILLS")
    print("=" * 70)

    if jd_info["preferred_skills"]:

        for skill in jd_info["preferred_skills"]:

            print(skill)

    else:

        print("Not Mentioned")


    print("\n" + "=" * 70)
    print("CERTIFICATIONS")
    print("=" * 70)

    if jd_info["certifications"]:

        for cert in jd_info["certifications"]:

            print(cert)

    else:

        print("Not Mentioned")
    print("\n" + "=" * 70)
    print("MATCHED SKILLS")
    print("=" * 70)

    if match_result["matched_skills"]:

        for skill in match_result["matched_skills"]:

            print(skill)

    else:

        print("No Matched Skills")


    print("\n" + "=" * 70)
    print("MISSING SKILLS")
    print("=" * 70)

    if match_result["missing_skills"]:

        for skill in match_result["missing_skills"]:

            print(skill)

    else:

        print("No Missing Skills")
    print("\n" + "=" * 70)
    print("PREFERRED SKILLS")
    print("=" * 70)

    if jd_info["preferred_skills"]:

        for skill in jd_info["preferred_skills"]:

            print(skill)

    else:

        print("No Preferred Skills")
    print("\n" + "=" * 70)
    print("JOB MATCH")
    print("=" * 70)

    print(f"{match_result['job_match']}%")

    print("\n" + "=" * 70)
    print("FINAL DECISION")
    print("=" * 70)

    print(match_result["decision"])

    print("\n" + "=" * 70)
    print("ATS SCORE")
    print("=" * 70)

    print(f"{ats_score}/100")

    print("\n" + "=" * 70)

    print("AI RECOMMENDATION")

    print("=" * 70)

    print(ai_recommendation)
    
    print("\n" + "=" * 70)
    print("EXTRACTED INFORMATION")
    print("=" * 70)

    print(f"Name      : {info['name']}")
    print(f"Email     : {info['email']}")
    print(f"Phone     : {info['phone']}")
    print(f"GitHub    : {info['github']}")
    print(f"LinkedIn  : {info['linkedin']}")
    print(f"Portfolio : {info['portfolio']}")

    print("\n" + "=" * 70)
    print("EXTRACTED SKILLS")
    print("=" * 70)

    for skill in info["skills"]:
        print(skill)

    print("\n" + "=" * 70)
    print("EDUCATION")
    print("=" * 70)

    if info["education"]:
        for degree in info["education"]:
            print(degree)
    else:
        print("Not Found")

    print("\n" + "=" * 70)
    print("EXPERIENCE")
    print("=" * 70)

    if info["experience"]:
        for exp in info["experience"]:
            print(exp)
    else:
        print("Not Found")
    print("\n" + "=" * 70)
    print("PROJECTS")
    print("=" * 70)


    return render_template(

    "index.html",

    info=info,

    jd_info=jd_info,

    match_result=match_result,

    ats_score=ats_score,

    ai_recommendation=ai_recommendation

)
if __name__ == "__main__":

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    app.run(debug=True)

    