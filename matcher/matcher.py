from matcher.skill_normalizer import SkillNormalizer
# i will do change in matcher
class SkillMatcher:

    def __init__(self, resume_skills, jd_skills):

        self.resume_skills = {
        skill.lower().strip()
        for skill in resume_skills
        }

        self.jd_skills = {
            skill.lower().strip()
            for skill in jd_skills
        }

    # --------------------------------
    # Matched Skills
    # --------------------------------

    def matched_skills(self):

        return sorted(

            list(

                self.resume_skills.intersection(

                    self.jd_skills

                )

            )

        )

    # --------------------------------
    # Missing Skills
    # --------------------------------

    def missing_skills(self):

        return sorted(

            list(

                self.jd_skills.difference(

                    self.resume_skills

                )

            )

        )

    # --------------------------------
    # Job Match Percentage
    # --------------------------------

    def job_match_percentage(self):

        total_required = len(self.jd_skills)

        matched = len(self.matched_skills())

        if total_required == 0:

            return 0

        percentage = (

            matched / total_required

        ) * 100

        return round(percentage, 2)

    # --------------------------------
    # Skill Coverage
    # --------------------------------

    def skill_coverage(self):

        total_required = len(self.jd_skills)

        missing = len(self.missing_skills())

        if total_required == 0:

            return 0

        coverage = (

            (total_required - missing)

            / total_required

        ) * 100

        return round(coverage, 2)

    # --------------------------------
    # Final Decision
    # --------------------------------

    def final_decision(self):

        score = self.job_match_percentage()

        if score >= 85:
            return "Excellent Match"

        elif score >= 70:
            return "Good Match"

        elif score >= 50:
            return "Average Match"

        else:
            return "Needs Improvement"
    
    # --------------------------------
    # Compare Everything
    # --------------------------------

    def compare(self):

        return {

            "matched_skills": self.matched_skills(),

            "missing_skills": self.missing_skills(),

            "job_match": self.job_match_percentage(),

            "skill_coverage": self.skill_coverage(),

            "decision": self.final_decision()

        }