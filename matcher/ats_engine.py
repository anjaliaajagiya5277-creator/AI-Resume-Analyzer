class ATSEngine:

    def __init__(
        self,
        resume_skills,
        jd_skills,
        experience,
        education,
        projects,
        certifications,
        resume_info
    ):

        self.resume_skills = set(skill.lower() for skill in resume_skills)
        self.jd_skills = set(skill.lower() for skill in jd_skills)

        self.experience = experience
        self.education = education
        self.projects = projects
        self.certifications = certifications
        self.resume_info = resume_info

    def calculate(self):

        if len(self.jd_skills):

            matched = self.resume_skills.intersection(self.jd_skills)

            missing = self.jd_skills.difference(self.resume_skills)

            skill_score = (len(matched) / len(self.jd_skills)) * 40

        else:

            matched = set()

            missing = set()

            skill_score = 0

        experience_score = min(self.experience * 4, 20)

        education_score = 15 if self.education else 0

        project_score = min(self.projects * 2, 10)

        certification_score = min(len(self.certifications), 5)

        completeness = 0

        if self.resume_info.get("name") != "Not Found":
            completeness += 3

        if self.resume_info.get("email") != "Not Found":
            completeness += 3

        if self.resume_info.get("phone") != "Not Found":
            completeness += 4

        total = round(

            skill_score +

            experience_score +

            education_score +

            project_score +

            certification_score +

            completeness

        )

        return {

            "score": min(total,100),

            "matched_skills": sorted(list(matched)),

            "missing_skills": sorted(list(missing)),

            "breakdown":{

                "skills":round(skill_score),

                "experience":round(experience_score),

                "education":education_score,

                "projects":project_score,

                "certifications":certification_score,

                "completeness":completeness

            }

        }