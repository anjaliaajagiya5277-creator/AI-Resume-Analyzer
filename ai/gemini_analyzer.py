import google.generativeai as genai

from config import Config


class GeminiResumeAnalyzer:

    def __init__(self):

        genai.configure(

            api_key=Config.GEMINI_API_KEY

        )

        self.model = genai.GenerativeModel(

            Config.MODEL_NAME

        )

    def generate_recommendation(self,info,jd_text,jd_info,match_result,ats_score):
        prompt = f"""
        You are a Senior Technical Recruiter and ATS Expert.

        Your task is to evaluate the candidate based ONLY on the provided information.

        Do not invent missing information.

        =========================
        JOB DESCRIPTION
        =========================

        Required Skills:
        {", ".join(jd_info["required_skills"])}
        ==============================
        FULL JOB DESCRIPTION
        ==============================

        {jd_text}

        Preferred Skills:
        {", ".join(jd_info["preferred_skills"])}

        Education:
        {", ".join(jd_info["education"])}

        Experience:
        {jd_info["experience"]}

        Certifications:
        {", ".join(jd_info["certifications"])}

        =========================
        CANDIDATE
        =========================

        Name:
        {info["name"]}

        Education:
        {", ".join(info["education"])}

        Experience:
        {", ".join(info["experience"]) if info["experience"] else "Not Mentioned"}

        Skills:
        {", ".join(info["skills"])}

        =========================
        MATCH RESULT
        =========================

        Job Match:
        {match_result["job_match"]}%

        ATS Score:
        {ats_score}/100

        Matched Skills:
        {", ".join(match_result["matched_skills"])}

        Missing Skills:
        {", ".join(match_result["missing_skills"])}

        =========================
        Instructions
        =========================

        Return your response in EXACTLY the following format.

        ## Candidate Summary
        (2-3 sentences)

        ## Strengths
        - ...
        - ...
        - ...

        ## Missing Skills
        - ...
        - ...

        ## Resume Improvements
        - ...
        - ...
        - ...

        ## Interview Readiness
        One sentence.

        ## Hiring Recommendation
        Choose ONLY one:

        Highly Recommended
        Recommended
        Consider After Upskilling
        Not Recommended

        Keep the response below 250 words.
        Use professional language.
        Never mention skills that are not listed above.
        """
        try:

            response = self.model.generate_content(prompt)

            if hasattr(response, "text") and response.text:

                return response.text

            return "No AI recommendation generated."

        except Exception as e:

            return f"AI Recommendation Error: {str(e)}"