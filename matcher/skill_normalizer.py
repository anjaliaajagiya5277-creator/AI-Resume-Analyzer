class SkillNormalizer:

    SKILL_ALIASES = {

        "nodejs": "node.js",

        "node js": "node.js",

        "node.js": "node.js",

        "reactjs": "react",

        "react js": "react",

        "react.js": "react",

        "vuejs": "vue",

        "vue.js": "vue",

        "angularjs": "angular",

        "ml": "machine learning",

        "ai": "artificial intelligence",

        "dl": "deep learning",

        "postgres": "postgresql",

        "mongo": "mongodb",

        "scikit learn": "scikit-learn",

        "sklearn": "scikit-learn",

        "powerbi": "power bi",

        "ms excel": "excel"

    }

    @classmethod
    def normalize(cls, skill):

        skill = skill.lower().strip()

        return cls.SKILL_ALIASES.get(

            skill,

            skill

        )