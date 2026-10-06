"""Validate generated sample assets; does not test the application or call an API."""
from pathlib import Path
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def rounded(value):
    return float(Decimal(str(value)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

def main():
    jobs = read('jobs.json')
    questions = read('interview_questions.json')
    template = read('diagnosis_template.json')
    rules = read('rules.json')
    profiles = read('demo_profiles.json')
    cases = read('validation_cases.json')['cases']
    manifest = read('generation_manifest.json')
    categories = rules['categories']
    for filename, expected in manifest['files'].items():
        require(hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == expected,
                f'File checksum mismatch: {filename}')
    for label, rows in [('jobs', jobs), ('questions', questions), ('profiles', profiles)]:
        require(len({r['code'] for r in rows}) == len(rows), f'Duplicate code: {label}')
        require(all(r['is_demo'] is True for r in rows), f'Missing demo flag: {label}')
    require(Counter(j['category'] for j in jobs) == {k: 10 for k in categories}, 'Job category counts')
    for j in jobs:
        require(j['source_type'] == 'synthetic' and j['source_url'] is None, 'Synthetic source metadata')
        require(j['company'].startswith('演示企业'), 'Company demo prefix')
        require(j['required_skills'] and set(j['required_skills']) <= set(categories[j['category']]['skills']), 'Job skills')
        require(j['job_type'] in ('internship', 'full_time'), 'Job type')
        require(0 <= j['salary_min'] <= j['salary_max'], 'Salary bounds')
        require(200 <= len(j['description']) <= 600, 'Job description length')
    for cat in categories:
        require(Counter(q['difficulty'] for q in questions if q['category'] == cat) == {1: 4, 2: 4, 3: 2}, 'Question level counts')
    for q in questions:
        require(q['prompt'] and q['reference_answer'] and q['rubric']['expected_points'], 'Question content')
        require(q['rubric']['dimensions'] == ['accuracy', 'coverage', 'clarity'], 'Rubric dimensions')
    require([q['id'] for q in template['questions']] == [f'Q{i:02d}' for i in range(1, 11)], 'Question IDs')
    for rule in [rules['recommendation'], rules['interview']]:
        require(sum(Decimal(str(v)) for v in rule['weights'].values()) == Decimal('1'), 'Weight sum')
    profile_map = {p['code']: p for p in profiles}
    for p in profiles:
        a = p['answers']
        require(set(a) == {f'Q{i:02d}' for i in range(1, 11)}, 'Profile answer keys')
        require(set(a['Q04']) == set(categories[a['Q01']]['skills']), 'Profile skill keys')
        require(all(type(v) is int and 0 <= v <= 3 for v in a['Q04'].values()), 'Skill range')
        require(all(type(a[k]) is int and 0 <= a[k] <= 3 for k in ['Q05','Q06','Q07']), 'Answer range')
        require(len(a['Q02']) <= 3 and a['Q08'] in ['internship','full_time','any'], 'Preferences')
        require(type(a['Q09']) is int and 0 <= a['Q09'] <= 40 and len(a['Q10']) <= 500, 'Answer limits')
    for c in cases:
        if c['kind'] == 'diagnosis':
            a = profile_map[c['profile_code']]['answers']
            tech = Decimal(sum(a['Q04'].values())) / Decimal(15) * Decimal(100)
            got = {'technical': rounded(tech)}
            got.update({d: rounded(Decimal(a[k])/Decimal(3)*Decimal(100))
                        for d,k in [('project','Q05'),('expression','Q06'),('learning','Q07')]})
            require(got == c['expected'], f'Diagnosis expected values: {c["id"]}')
        if c['kind'] in ['score_formula', 'interview_dimension_formula']:
            weights = rules['recommendation' if c['kind'] == 'score_formula' else 'interview']['weights']
            value = sum(Decimal(str(c['input'][k]))*Decimal(str(w)) for k,w in weights.items())
            require(rounded(value * (100 if c['kind'] == 'score_formula' else 1)) == c['expected'], 'Weighted example')
        if c['kind'] == 'interview_average':
            require(rounded(Decimal(sum(c['input'])) / Decimal(len(c['input']))) == c['expected'], 'Mean example')
    expected_counts = {'jobs': len(jobs), 'interview_questions': len(questions),
                       'diagnosis_questions': len(template['questions']), 'profiles': len(profiles),
                       'validation_cases': len(cases)}
    require(manifest['counts'] == expected_counts, 'Manifest counts')
    print('PASS: sample schemas, IDs, ranges, counts, file hashes and numeric examples.')
    print('Application tests, MySQL execution, BGE retrieval and live API calls remain to be implemented and tested.')

if __name__ == '__main__':
    main()
