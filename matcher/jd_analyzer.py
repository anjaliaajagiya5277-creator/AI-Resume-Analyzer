import os
import re

class JDAnalyzer:

    def __init__(self, jd_text):

        self.jd_text = jd_text.lower()

        skill_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "skills.txt"
        )

        with open(skill_file, "r", encoding="utf-8") as file:

            self.skill_database = [

                skill.strip()

                for skill in file.readlines()

                if skill.strip()

            ]

    # --------------------------
    # Required Skills
    # --------------------------
    def extract_required_skills(self):

        required_keywords = [

            "required",

            "must have",

            "must-have",

            "essential",

            "mandatory",

            "required skills",

            "requirements",

            "qualifications"

        ]

        preferred_keywords = [

            "preferred",

            "nice to have",

            "nice-to-have",

            "good to have",

            "bonus",

            "plus",

            "desirable",

            "optional"

        ]

        stop_keywords = [

            "preferred skills",

            "nice to have",

            "good to have",

            "bonus skills",

            "optional skills",

            "responsibilities",

            "education",

            "experience",

            "certifications"

        ]

        lines = self.jd_text.split("\n")

        required = []

        current_section = None

        for line in lines:

            current = line.strip()

            lower = current.lower()

            if not current:

                continue

            # -------------------------
            # Required Section
            # -------------------------

            if any(

                keyword in lower

                for keyword in required_keywords

            ):

                current_section = "required"

                continue

            # -------------------------
            # Preferred Section
            # -------------------------

            if any(

                keyword in lower

                for keyword in preferred_keywords

            ):

                current_section = "preferred"

                continue

            # -------------------------
            # Stop Section
            # -------------------------

            if any(

                keyword in lower

                for keyword in stop_keywords

            ):

                current_section = None

                continue

            # -------------------------
            # Extract Skills
            # -------------------------

            for line in lines:

                current = line.strip()
                lower = current.lower()

                if not current:
                    continue

                if any(keyword in lower for keyword in required_keywords):
                    current_section = "required"
                    continue

                if any(keyword in lower for keyword in preferred_keywords):
                    current_section = "preferred"
                    continue

                if any(keyword in lower for keyword in stop_keywords):
                    current_section = None
                    continue

                if current_section == "required":

                    for skill in self.skill_database:

                        skill_lower = skill.lower().strip()

                        pattern = rf"\b{re.escape(skill_lower)}\b"

                        if re.search(pattern, lower):

                            required.append(skill)

            # Fallback (Outside the loop)
            if not required:

                for skill in self.skill_database:

                    if skill.lower() in self.jd_text:

                        required.append(skill)

            return sorted(list(set(required)))
    # --------------------------
    # Education
    # --------------------------

    def extract_education(self):

        education_keywords = [

            "Bachelor of Engineering",
            "Bachelor of Technology",
            "Bachelor's Degree",
            "B.Tech",
            "B.E",
            "M.Tech",
            "M.E",
            "BCA",
            "MCA",
            "B.Sc",
            "M.Sc",
            "MBA",
            "Diploma",
            "PhD"

        ]

        found = []

        for degree in education_keywords:

            if degree.lower() in self.jd_text:

                found.append(degree)

        return list(dict.fromkeys(found))
    # --------------------------
    # Experience
    # --------------------------

    def extract_experience(self):

        import re

        patterns = [

            r"\d+\+?\s*years",

            r"\d+\+?\s*year",

            r"\d+\+?\s*yrs",

            r"\d+\+?\s*yr"

        ]

        for pattern in patterns:

            match = re.search(pattern, self.jd_text)

            if match:

                return match.group()

        return "Not Mentioned"
    # --------------------------
    # Preferred Skills
    # --------------------------

    def extract_preferred_skills(self):

        preferred_keywords = [

            "preferred",

            "nice to have",

            "good to have",

            "bonus",

            "plus",

            "desirable",

            "optional"

        ]

        lines = self.jd_text.split("\n")

        preferred = []

        capture = False

        stop_words = [

            "education",

            "experience",

            "qualification",

            "certification",

            "responsibilities",

            "required skills",

            "requirements"

        ]

        for line in lines:

            current = line.strip()

            lower = current.lower()

            # Start preferred section
            if any(

                keyword in lower

                for keyword in preferred_keywords

            ):

                capture = True

                continue

            # Stop preferred section
            if capture and any(

                word in lower

                for word in stop_words

            ):

                break

            if capture:

                for skill in self.skill_database:

                    skill_lower = skill.lower().strip()

                    pattern = rf"\b{re.escape(skill_lower)}\b"

                    if re.search(pattern, lower):

                        preferred.append(skill)

        return sorted(list(set(preferred)))
    # --------------------------
    # Certifications
    # --------------------------

    def extract_certifications(self):

        certification_keywords = [

            "AWS Certified",

            "AWS Certification",

            "Azure Fundamentals",

            "Microsoft Certified",

            "Google Professional",

            "Oracle Certified",

            "Cisco CCNA",

            "Cisco CCNP",

            "CompTIA",

            "PMP",

            "Scrum Master",

            "Salesforce Certified",

            "Red Hat Certified"

        ]

        found = []

        for cert in certification_keywords:

            if cert.lower() in self.jd_text:

                found.append(cert)

        return list(dict.fromkeys(found))   
    # --------------------------
    # Extract All
    # --------------------------

    def extract_all(self):

        required = self.extract_required_skills()

        preferred = self.extract_preferred_skills()

        return {

            "skills": required,

            "required_skills": required,

            "preferred_skills": preferred,

            "education": self.extract_education(),

            "experience": self.extract_experience(),

            "certifications": self.extract_certifications()

        }