import re
import os
import spacy

nlp = spacy.load("en_core_web_sm")


class ResumeInfoExtractor:

    def __init__(self, text):

        self.text = text

        self.doc = nlp(text)

        skill_file = os.path.join(
            "data",
            "skills.txt"
        )

        with open(
            skill_file,
            "r",
            encoding="utf-8"
        ) as file:

            self.skill_database = [

                skill.strip()

                for skill in file.readlines()

                if skill.strip()

            ]

    # --------------------------
    # Universal Section Extractor
    # --------------------------

    def extract_section(self, section_names):

        lines = self.text.split("\n")

        section_lines = []

        capture = False

        all_sections = [

            "summary",

            "professional summary",

            "career objective",

            "objective",

            "education",

            "technical skills",

            "skills",

            "technical knowledge",

            "technologies",

            "tools and technologies",

            "experience",

            "work experience",

            "professional experience",

            "employment history",

            "work history",

            "projects",

            "certifications",

            "achievements",

            "languages",

            "interests",

            "references"

        ]

        for line in lines:

            current = line.strip()

            lower = current.lower()

            if not current:

                continue

            # --------------------------------
            # Detect requested section
            # --------------------------------

            if any(

                lower == section

                or lower.startswith(section + ":")

                for section in section_names

            ):

                capture = True

                continue

            # --------------------------------
            # Detect next section
            # --------------------------------

            if capture and any(

                lower == section

                or lower.startswith(section + ":")

                for section in all_sections

            ):

                break

            # --------------------------------
            # Store content
            # --------------------------------

            if capture:

                section_lines.append(current)

        return section_lines
    # --------------------------
    # Name
    # --------------------------

    def extract_name(self):

        for ent in self.doc.ents:

            if ent.label_ == "PERSON":

                return ent.text

        return "Not Found"

    # --------------------------
    # Email
    # --------------------------

    def extract_email(self):

        pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

        match = re.search(pattern, self.text)

        if match:

            return match.group()

        return "Not Found"

    # --------------------------
    # Phone
    # --------------------------

    def extract_phone(self):

        pattern = r'(\+?\d[\d\s\-]{8,15}\d)'

        match = re.search(pattern, self.text)

        if match:

            return match.group()

        return "Not Found"

    # --------------------------
    # GitHub
    # --------------------------

    def extract_github(self):

        pattern = r'https?://(?:www\.)?github\.com/[^\s]+'

        match = re.search(pattern, self.text, re.IGNORECASE)

        if match:

            return match.group()

        return "Not Found"

    # --------------------------
    # LinkedIn
    # --------------------------

    def extract_linkedin(self):

        pattern = r'https?://(?:www\.)?linkedin\.com/[^\s]+'

        match = re.search(pattern, self.text, re.IGNORECASE)

        if match:

            return match.group()

        return "Not Found"

    # --------------------------
    # Portfolio
    # --------------------------

    def extract_portfolio(self):

        urls = re.findall(

            r'https?://[^\s]+',

            self.text

        )

        for url in urls:

            if "github" in url.lower():

                continue

            if "linkedin" in url.lower():

                continue

            return url

        return "Not Found"
    # --------------------------
    # Skills
    # --------------------------

    def extract_skills(self):

        found = set()

        text_lower = self.text.lower()

        # Search the entire resume
        for skill in self.skill_database:

            skill_lower = skill.lower().strip()

            pattern = rf"\b{re.escape(skill_lower)}\b"

            if re.search(pattern, text_lower):

                found.add(skill)

        return sorted(found)
    # --------------------------
    # Education
    # --------------------------

    def extract_education(self):

        education_keywords = [

            "Bachelor of Engineering",
            "Bachelor of Technology",
            "B.Tech",
            "B.E",
            "M.Tech",
            "M.E",
            "BCA",
            "MCA",
            "B.Sc",
            "M.Sc",
            "Diploma",
            "MBA",
            "PhD"

        ]

        found = []

        text = self.text

        for keyword in education_keywords:

            if keyword.lower() in text.lower():

                found.append(keyword)

        return list(dict.fromkeys(found))

    # --------------------------
    # Experience
    # --------------------------

    def extract_experience(self):

        return self.extract_section([

            "experience",

            "work experience",

            "professional experience",

            "employment history",

            "work history"

        ])

    # --------------------------
    # Projects
    # --------------------------

    def extract_projects(self):

        return self.extract_section([

            "projects",

            "personal projects",

            "academic projects",

            "professional projects"

        ])
    # --------------------------
    # Extract All
    # --------------------------



    def extract_all(self):

        return {

            "name": self.extract_name(),

            "email": self.extract_email(),

            "phone": self.extract_phone(),

            "github": self.extract_github(),

            "linkedin": self.extract_linkedin(),

            "portfolio": self.extract_portfolio(),

            "skills": self.extract_skills(),

            "education": self.extract_education(),

            "experience": self.extract_experience()

        }