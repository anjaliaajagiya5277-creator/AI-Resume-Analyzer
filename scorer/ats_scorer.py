class ATSScorer:
# hello i will do change in ats score
    def __init__(self, info, jd_info, match_result):

        self.info = info
        self.jd_info = jd_info
        self.match_result = match_result

    # -----------------------------
    # Skill Score (50 Marks)
    # -----------------------------

    def skill_score(self):

        return (self.match_result["job_match"] * 50) / 100

    # -----------------------------
    # Education Score (20 Marks)
    # -----------------------------

    def education_score(self):

        if self.info["education"]:

            return 20

        return 0

    # -----------------------------
    # Experience Score (20 Marks)
    # -----------------------------

    def experience_score(self):

        if self.info["experience"]:

            return 20

        return 0

    # -----------------------------
    # Contact Score (10 Marks)
    # -----------------------------

    def contact_score(self):

        score = 0

        if self.info["email"] != "Not Found":
            score += 4

        if self.info["phone"] != "Not Found":
            score += 3

        if (
            self.info["linkedin"] != "Not Found"
            or self.info["github"] != "Not Found"
        ):
            score += 3

        return score

    # -----------------------------
    # Total ATS Score
    # -----------------------------

    def total_score(self):

        total = (

            self.skill_score()

            + self.education_score()

            + self.experience_score()

            + self.contact_score()

        )

        return round(total)