"""
Smart Resume Match System - extracts skills from PDF and compares with job requirements.
Uses Python libraries only (PyPDF2) - no external AI APIs.
"""
import re
from typing import Dict, List, Set

from PyPDF2 import PdfReader


# Comprehensive skill database for extraction and suggestions
SKILL_DATABASE = {
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
    'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css',
    'django', 'flask', 'fastapi', 'spring', 'spring boot', 'react', 'angular',
    'vue', 'vue.js', 'node.js', 'nodejs', 'express', 'next.js', 'bootstrap',
    'tailwind', 'jquery', 'rest api', 'graphql', 'microservices', 'docker',
    'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'gitlab', 'jenkins',
    'ci/cd', 'linux', 'unix', 'mongodb', 'mysql', 'postgresql', 'redis',
    'elasticsearch', 'firebase', 'sqlite', 'oracle', 'data structures',
    'algorithms', 'machine learning', 'deep learning', 'tensorflow', 'pytorch',
    'scikit-learn', 'pandas', 'numpy', 'data analysis', 'data science',
    'artificial intelligence', 'nlp', 'computer vision', 'agile', 'scrum',
    'jira', 'communication', 'leadership', 'teamwork', 'problem solving',
    'analytical thinking', 'project management', 'tableau', 'power bi',
    'excel', 'selenium', 'pytest', 'unit testing', 'api testing', 'postman',
    'swagger', 'oauth', 'jwt', 'websocket', 'rabbitmq', 'kafka', 'hadoop',
    'spark', 'etl', 'devops', 'terraform', 'ansible', 'nginx', 'apache',
    'figma', 'ui/ux', 'android', 'ios', 'flutter', 'react native', 'blockchain',
    'cybersecurity', 'networking', 'cloud computing', 'saas', 'paas', 'iaas',
    'object oriented programming', 'oop', 'design patterns', 'solid principles',
    'mvc', 'mvvm', 'rest', 'soap', 'xml', 'json', 'yaml', 'bash', 'shell scripting',
    'powershell', 'perl', 'lua', 'haskell', 'clojure', 'elixir', 'dart',
    'webpack', 'vite', 'babel', 'sass', 'less', 'redux', 'mobx', 'vuex',
    'pinia', 'prisma', 'sequelize', 'hibernate', 'jpa', 'maven', 'gradle',
    'npm', 'yarn', 'pip', 'conda', 'virtualenv', 'venv', 'celery', 'redis',
    'memcached', 'caching', 'load balancing', 'system design', 'distributed systems',
}


def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text content from a PDF resume file."""
    try:
        reader = PdfReader(file_path)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return '\n'.join(text_parts)
    except Exception:
        return ''


def normalize_skill(skill: str) -> str:
    """Normalize skill name for consistent comparison."""
    return skill.strip().lower()


def extract_skills_from_text(text: str, known_skills: Set[str] = None) -> List[str]:
    """
    Extract skills from resume text using pattern matching against skill database.
    Also checks against known skills from the database.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_skills = set()

    # Match against skill database
    for skill in SKILL_DATABASE:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill.title())

    # Match against known skills from DB
    if known_skills:
        for skill in known_skills:
            skill_lower = skill.lower()
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)

    return sorted(found_skills)


def calculate_match(
    resume_skills: List[str],
    required_skills: List[str],
    all_skills_in_category: List[str] = None,
) -> Dict:
    """
    Calculate resume match percentage and skill gaps.

    Returns:
        - match_percentage: float (0-100)
        - matched_skills: list of skills found in resume
        - missing_skills: list of required skills not in resume
        - suggested_skills: list of related skills to learn
    """
    if not required_skills:
        return {
            'match_percentage': 100.0,
            'matched_skills': [],
            'missing_skills': [],
            'suggested_skills': [],
        }

    resume_set = {normalize_skill(s) for s in resume_skills}
    required_set = {normalize_skill(s) for s in required_skills}

    matched = required_set & resume_set
    missing = required_set - resume_set

    match_percentage = (len(matched) / len(required_set)) * 100 if required_set else 0

    # Suggest related skills from same category not in resume
    suggested = []
    if all_skills_in_category:
        resume_and_matched = resume_set | matched
        for skill in all_skills_in_category:
            skill_norm = normalize_skill(skill)
            if skill_norm not in resume_and_matched and skill_norm not in missing:
                # Suggest skills related to missing ones
                for missing_skill in missing:
                    if _are_skills_related(skill_norm, missing_skill):
                        suggested.append(skill)
                        break

    # Add common complementary skills for missing ones
    complementary = _get_complementary_skills(list(missing))
    for skill in complementary:
        if skill not in suggested and normalize_skill(skill) not in resume_set:
            suggested.append(skill)

    return {
        'match_percentage': round(match_percentage, 2),
        'matched_skills': sorted([s.title() for s in matched]),
        'missing_skills': sorted([s.title() for s in missing]),
        'suggested_skills': sorted(list(set(suggested)))[:10],
    }


def _are_skills_related(skill1: str, skill2: str) -> bool:
    """Check if two skills are in the same technology family."""
    families = [
        {'python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'scikit-learn'},
        {'java', 'spring', 'spring boot', 'hibernate', 'maven', 'gradle'},
        {'javascript', 'typescript', 'react', 'angular', 'vue', 'node.js', 'express'},
        {'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'},
        {'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'sql'},
        {'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'nlp'},
    ]
    for family in families:
        if skill1 in family and skill2 in family:
            return True
    return False


def _get_complementary_skills(missing_skills: List[str]) -> List[str]:
    """Suggest complementary skills based on what's missing."""
    suggestions_map = {
        'python': ['Django', 'Flask', 'Pandas'],
        'java': ['Spring Boot', 'Hibernate', 'Maven'],
        'javascript': ['React', 'Node.js', 'TypeScript'],
        'react': ['Redux', 'JavaScript', 'HTML/CSS'],
        'django': ['Python', 'REST API', 'PostgreSQL'],
        'sql': ['MySQL', 'PostgreSQL', 'Database Design'],
        'docker': ['Kubernetes', 'CI/CD', 'Linux'],
        'aws': ['Cloud Computing', 'Docker', 'Terraform'],
        'machine learning': ['Python', 'TensorFlow', 'Data Analysis'],
        'data structures': ['Algorithms', 'Problem Solving', 'Java/Python'],
    }

    suggestions = []
    for skill in missing_skills:
        skill_lower = skill.lower()
        if skill_lower in suggestions_map:
            suggestions.extend(suggestions_map[skill_lower])

    return list(set(suggestions))[:5]


def process_resume_match(resume_file_path: str, job, known_skills: List[str] = None) -> Dict:
    """
    Full pipeline: extract PDF text, find skills, compare with job requirements.
    """
    text = extract_text_from_pdf(resume_file_path)
    known_set = set(known_skills) if known_skills else set()
    resume_skills = extract_skills_from_text(text, known_set)

    # Also include student's profile skills
    required_skills = list(job.required_skills.values_list('name', flat=True))
    all_skills = list(known_set) if known_set else list(SKILL_DATABASE)

    match_result = calculate_match(resume_skills, required_skills, all_skills)

    return {
        'extracted_text': text,
        'extracted_skills': resume_skills,
        **match_result,
    }
