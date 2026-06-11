#!/usr/bin/env python3
"""
Word-Format Skill Evaluation Tool
Based on writing-skills evaluation framework
Total: 130 points
"""

import re
from pathlib import Path

class SkillEvaluator:
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_content = self.skill_path.read_text(encoding='utf-8')
        self.results = {}
        
    def evaluate(self) -> dict:
        """Run all evaluations and return results"""
        self.results = {
            'yaml_frontmatter': self._evaluate_yaml_frontmatter(),
            'structure': self._evaluate_structure(),
            'cso_optimization': self._evaluate_cso(),
            'content_quality': self._evaluate_content_quality(),
            'testing_tdd': self._evaluate_testing(),
            'anti_patterns': self._evaluate_anti_patterns(),
            'token_efficiency': self._evaluate_token_efficiency()
        }
        return self.results
    
    def _evaluate_yaml_frontmatter(self) -> dict:
        """Evaluate YAML frontmatter (20 points)"""
        score = 0
        details = []
        max_score = 20
        
        # Check if frontmatter exists
        if self.skill_content.startswith('---'):
            score += 3
            details.append("[OK] Frontmatter exists (+3)")
        else:
            details.append("[FAIL] No frontmatter found (+0)")
        
        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', self.skill_content, re.DOTALL)
        if not frontmatter_match:
            return {'score': score, 'max': max_score, 'details': details}
        
        frontmatter = frontmatter_match.group(1)
        
        # Check name field
        if 'name:' in frontmatter:
            name_match = re.search(r'name:\s*(.+)', frontmatter)
            if name_match:
                name = name_match.group(1).strip()
                # Check if uses only letters, numbers, hyphens
                if re.match(r'^[a-zA-Z0-9-]+$', name):
                    score += 4
                    details.append(f"[OK] Name '{name}' uses valid characters (+4)")
                else:
                    details.append(f"[WARN] Name '{name}' contains special characters (+0)")
                    
                # Check verb-first/gerund form
                if name.endswith('ing') or name.startswith('format'):
                    score += 3
                    details.append("[OK] Name uses verb/gerund form (+3)")
                else:
                    score += 2  # Partial credit
                    details.append("[WARN] Name not verb-first but acceptable (+2)")
        
        # Check description field
        if 'description:' in frontmatter:
            desc_match = re.search(r'description:\s*(.+?)(?:\n|$)', frontmatter)
            if desc_match:
                desc = desc_match.group(1).strip()
                
                # Check starts with "Use when..."
                if desc.startswith('Use when'):
                    score += 5
                    details.append("[OK] Description starts with 'Use when...' (+5)")
                else:
                    details.append("[FAIL] Description doesn't start with 'Use when...' (+0)")
                
                # Check no workflow summary
                workflow_words = ['Format or produce', 'Create or edit', 'Generate or']
                has_workflow = any(word in desc for word in workflow_words)
                if not has_workflow:
                    score += 3
                    details.append("[OK] Description doesn't contain workflow summary (+3)")
                else:
                    details.append("[FAIL] Description contains workflow summary (+0)")
                
                # Check length
                if len(desc) <= 500:
                    score += 2
                    details.append(f"[OK] Description length {len(desc)} chars <= 500 (+2)")
                else:
                    score += 1
                    details.append(f"[WARN] Description length {len(desc)} chars > 500 (+1)")
        
        return {'score': score, 'max': max_score, 'details': details}
    
    def _evaluate_structure(self) -> dict:
        """Evaluate skill structure (25 points)"""
        score = 0
        details = []
        max_score = 25
        
        # Check required sections
        sections = {
            'Overview': 5,
            'When to Use': 5,
            'Core Workflow': 4,
            'Quick Reference|Formatting Priorities': 4,
            'Common Mistakes': 4,
            'Reference': 3
        }
        
        for section, points in sections.items():
            if re.search(rf'##\s*({section})', self.skill_content, re.IGNORECASE):
                score += points
                details.append(f"[OK] '{section}' section found (+{points})")
            else:
                details.append(f"[FAIL] '{section}' section missing (+0)")
        
        return {'score': score, 'max': max_score, 'details': details}
    
    def _evaluate_cso(self) -> dict:
        """Evaluate CSO Optimization (25 points)"""
        score = 0
        details = []
        max_score = 25
        
        # Extract description
        frontmatter_match = re.match(r'^---\n(.*?)\n---', self.skill_content, re.DOTALL)
        if not frontmatter_match:
            return {'score': 0, 'max': max_score, 'details': ['[FAIL] No frontmatter']}
        
        frontmatter = frontmatter_match.group(1)
        desc_match = re.search(r'description:\s*(.+?)(?:\n|$)', frontmatter)
        desc = desc_match.group(1) if desc_match else ""
        
        # Check trigger keywords
        triggers = ['排版', 'DOCX', 'Word', '实验报告', '课程论文', 'formatting', 'academic']
        found_triggers = [t for t in triggers if t.lower() in desc.lower()]
        trigger_score = min(8, len(found_triggers) * 2)
        score += trigger_score
        details.append(f"[OK] Found {len(found_triggers)} trigger keywords: {found_triggers} (+{trigger_score})")
        
        # Check bilingual support
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', desc))
        has_english = bool(re.search(r'[a-zA-Z]', desc))
        if has_chinese and has_english:
            score += 4
            details.append("[OK] Bilingual triggers (Chinese/English) (+4)")
        elif has_chinese or has_english:
            score += 2
            details.append("[WARN] Single language triggers (+2)")
        
        # Check keyword density in body
        body_keywords = ['A4', '宋体', '黑体', 'Times New Roman', '页边距', '标题', '表格', '公式']
        found_body = [k for k in body_keywords if k in self.skill_content]
        body_score = min(8, len(found_body))
        score += body_score
        details.append(f"[OK] Found {len(found_body)} body keywords (+{body_score})")
        
        # Check naming convention
        if 'name:' in frontmatter:
            name_match = re.search(r'name:\s*(.+)', frontmatter)
            if name_match:
                name = name_match.group(1).strip()
                if '-' in name and not name.startswith('-') and not name.endswith('-'):
                    score += 3
                    details.append("[OK] Name uses hyphen convention (+3)")
                else:
                    score += 1
                    details.append("[WARN] Name doesn't use hyphens (+1)")
        
        # Check description exclusivity (no workflow)
        workflow_indicators = ['Format or produce', 'Create and', 'Generate and', 'Step 1', 'Step 2']
        if not any(ind in desc for ind in workflow_indicators):
            score += 2
            details.append("[OK] Description focuses on triggers only (+2)")
        
        return {'score': score, 'max': max_score, 'details': details}
    
    def _evaluate_content_quality(self) -> dict:
        """Evaluate content quality (20 points)"""
        score = 0
        details = []
        max_score = 20
        
        # Check for examples
        if '## Before/After Example' in self.skill_content or '## Example' in self.skill_content:
            score += 5
            details.append("[OK] Examples section found (+5)")
        else:
            details.append("[FAIL] No examples section (+0)")
        
        # Check for anti-patterns (bad patterns)
        bad_patterns = ['narrative example', 'story about how', 'in session 2025']
        has_bad = any(p in self.skill_content.lower() for p in bad_patterns)
        if not has_bad:
            score += 4
            details.append("[OK] No narrative storytelling (+4)")
        else:
            details.append("[FAIL] Contains narrative storytelling (+0)")
        
        # Check for code blocks with good examples
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', self.skill_content, re.DOTALL)
        if code_blocks:
            score += 4
            details.append(f"[OK] {len(code_blocks)} code blocks found (+4)")
        else:
            details.append("[FAIL] No code blocks (+0)")
        
        # Check for tables (good for reference)
        if '| ' in self.skill_content and ' | ' in self.skill_content:
            score += 4
            details.append("[OK] Tables used for reference material (+4)")
        else:
            details.append("[WARN] No tables for reference (+0)")
        
        # Check for clear deliverables
        if '.docx' in self.skill_content and 'deliver' in self.skill_content.lower():
            score += 3
            details.append("[OK] Clear deliverable format specified (+3)")
        
        return {'score': score, 'max': max_score, 'details': details}
    
    def _evaluate_testing(self) -> dict:
        """Evaluate testing/TDD compliance (20 points)"""
        score = 0
        details = []
        max_score = 20
        
        # Check for testing methodology
        testing_keywords = ['test', 'baseline', 'scenario', 'pressure', 'rationalization']
        found_testing = [k for k in testing_keywords if k.lower() in self.skill_content.lower()]
        
        if len(found_testing) >= 3:
            score += 8
            details.append(f"[OK] Testing methodology documented ({len(found_testing)} keywords) (+8)")
        elif len(found_testing) >= 1:
            score += 4
            details.append(f"[WARN] Partial testing documentation ({len(found_testing)} keywords) (+4)")
        else:
            details.append("[FAIL] No testing methodology documented (+0)")
        
        # Check for TDD cycle
        tdd_keywords = ['RED', 'GREEN', 'REFACTOR', 'failing test', 'baseline']
        found_tdd = [k for k in tdd_keywords if k in self.skill_content]
        if found_tdd:
            score += 6
            details.append(f"[OK] TDD cycle referenced ({found_tdd}) (+6)")
        else:
            details.append("[FAIL] No TDD cycle reference (+0)")
        
        # Check for rationalization table
        if 'rationalization' in self.skill_content.lower() or 'excuse' in self.skill_content.lower():
            score += 4
            details.append("[OK] Rationalization handling found (+4)")
        else:
            details.append("[FAIL] No rationalization table (+0)")
        
        # Check for red flags list
        if 'red flag' in self.skill_content.lower() or '## Red Flags' in self.skill_content:
            score += 2
            details.append("[OK] Red flags section found (+2)")
        else:
            details.append("[FAIL] No red flags section (+0)")
        
        return {'score': score, 'max': max_score, 'details': details}
    
    def _evaluate_anti_patterns(self) -> dict:
        """Evaluate anti-patterns avoidance (10 points)"""
        score = 10  # Start with full score, deduct for issues
        details = []
        max_score = 10
        
        # Check for narrative examples
        if 'In session' in self.skill_content or 'we found' in self.skill_content:
            score -= 3
            details.append("[WARN] Contains narrative example (-3)")
        else:
            details.append("[OK] No narrative examples")
        
        # Check for multi-language code blocks
        code_langs = re.findall(r'```(\w+)', self.skill_content)
        if len(set(code_langs)) > 3:
            score -= 2
            details.append("[WARN] Too many code languages (-2)")
        else:
            details.append("[OK] Appropriate code language variety")
        
        # Check for generic labels
        generic_labels = ['helper1', 'helper2', 'step1', 'step2']
        has_generic = any(label in self.skill_content.lower() for label in generic_labels)
        if has_generic:
            score -= 2
            details.append("[WARN] Contains generic labels (-2)")
        else:
            details.append("[OK] No generic labels")
        
        # Check for code in flowcharts (dot blocks)
        if '```dot' in self.skill_content and 'import' in self.skill_content:
            score -= 2
            details.append("[WARN] Code in flowcharts (-2)")
        else:
            details.append("[OK] No code in flowcharts")
        
        return {'score': max(0, score), 'max': max_score, 'details': details}
    
    def _evaluate_token_efficiency(self) -> dict:
        """Evaluate token efficiency (10 points)"""
        score = 0
        details = []
        max_score = 10
        
        # Count lines
        lines = self.skill_content.split('\n')
        line_count = len(lines)
        
        if line_count <= 200:
            score += 4
            details.append(f"[OK] SKILL.md {line_count} lines <= 200 (+4)")
        elif line_count <= 500:
            score += 3
            details.append(f"[WARN] SKILL.md {line_count} lines <= 500 (+3)")
        else:
            score += 1
            details.append(f"[FAIL] SKILL.md {line_count} lines > 500 (+1)")
        
        # Check word count
        words = len(self.skill_content.split())
        if words <= 500:
            score += 3
            details.append(f"[OK] Word count {words} <= 500 (+3)")
        elif words <= 1000:
            score += 2
            details.append(f"[WARN] Word count {words} <= 1000 (+2)")
        else:
            score += 1
            details.append(f"[FAIL] Word count {words} > 1000 (+1)")
        
        # Check for reference file separation
        if 'references/' in self.skill_content:
            score += 3
            details.append("[OK] Heavy reference in separate file (+3)")
        else:
            details.append("[FAIL] No reference file separation (+0)")
        
        return {'score': score, 'max': max_score, 'details': details}
    
    def get_total_score(self) -> int:
        """Calculate total score"""
        return sum(cat['score'] for cat in self.results.values())
    
    def get_total_max(self) -> int:
        """Get maximum possible score"""
        return sum(cat['max'] for cat in self.results.values())
    
    def display_results(self):
        """Display formatted results"""
        print("\n" + "="*70)
        print("[RESULTS] WORD-FORMAT SKILL EVALUATION RESULTS")
        print("="*70)
        
        total_score = self.get_total_score()
        total_max = self.get_total_max()
        percentage = (total_score / total_max) * 100
        
        # Category scores
        categories = [
            ("1. YAML Frontmatter", 'yaml_frontmatter'),
            ("2. Structure", 'structure'),
            ("3. CSO Optimization", 'cso_optimization'),
            ("4. Content Quality", 'content_quality'),
            ("5. Testing/TDD", 'testing_tdd'),
            ("6. Anti-Patterns", 'anti_patterns'),
            ("7. Token Efficiency", 'token_efficiency')
        ]
        
        print("\n[BREAKDOWN] CATEGORY BREAKDOWN:")
        print("-"*70)
        
        for name, key in categories:
            cat = self.results[key]
            cat_pct = (cat['score'] / cat['max']) * 100
            bar = "#" * int(cat_pct / 5) + "." * (20 - int(cat_pct / 5))
            print(f"{name:25} {cat['score']:2}/{cat['max']:2}  {bar} {cat_pct:5.1f}%")
        
        print("-"*70)
        print(f"{'TOTAL SCORE':25} {total_score:2}/{total_max:2}  {'#' * int(percentage/5)}{'.' * (20-int(percentage/5))} {percentage:5.1f}%")
        
        # Grade
        if percentage >= 90:
            grade = "A+ (Excellent)"
            emoji = "[A+]"
        elif percentage >= 80:
            grade = "A (Very Good)"
            emoji = "[A]"
        elif percentage >= 70:
            grade = "B (Good)"
            emoji = "[B]"
        elif percentage >= 60:
            grade = "C (Acceptable)"
            emoji = "[C]"
        elif percentage >= 50:
            grade = "D (Needs Improvement)"
            emoji = "[WARN]"
        else:
            grade = "F (Poor)"
            emoji = "[FAIL]"
        
        print(f"\n{emoji} GRADE: {grade}")
        
        # Detailed breakdown
        print("\n" + "="*70)
        print("[DETAILS] DETAILED BREAKDOWN:")
        print("="*70)
        
        for name, key in categories:
            print(f"\n{name}:")
            print("-"*40)
            for detail in self.results[key]['details']:
                print(f"  {detail}")
        
        # Summary
        print("\n" + "="*70)
        print("[SUMMARY] SUMMARY:")
        print("="*70)
        
        strengths = []
        improvements = []
        
        for name, key in categories:
            cat = self.results[key]
            if cat['score'] >= cat['max'] * 0.8:
                strengths.append(name)
            elif cat['score'] < cat['max'] * 0.5:
                improvements.append(name)
        
        if strengths:
            print("\n[OK] STRENGTHS:")
            for s in strengths:
                print(f"  - {s}")
        
        if improvements:
            print("\n[WARN]  AREAS FOR IMPROVEMENT:")
            for i in improvements:
                print(f"  - {i}")
        
        print("\n" + "="*70)
        
        return total_score, total_max, percentage


def main():
    skill_path = Path(__file__).parent / "word-format" / "SKILL.md"
    
    if not skill_path.exists():
        print(f"[X] Skill file not found: {skill_path}")
        return
    
    print("[*] Evaluating word-format skill...")
    print(f"[*] Path: {skill_path}")
    
    evaluator = SkillEvaluator(skill_path)
    evaluator.evaluate()
    evaluator.display_results()


if __name__ == "__main__":
    main()
