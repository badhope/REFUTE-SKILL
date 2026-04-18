#!/usr/bin/env python3
"""
REFUTE Skill - Response Validator
Validates that all responses meet REFUTE quality standards
"""

import re
from typing import Dict, List, Tuple

class RefuteValidator:
    """Validate REFUTE responses against quality standards"""
    
    FORBIDDEN_PHRASES = [
        "你说得对", "有道理", "确实",
        "对不起", "我错了", "抱歉",
        "好的", "谢谢", "明白了",
        "you're right", "good point", "i agree",
        "sorry", "my mistake", "i was wrong"
    ]
    
    REQUIRED_PREFIXES = [
        "笑死", "呵呵", "不对", "不是",
        "会不会", "有没有一种可能",
        "不会吧不会吧", "就我一个人觉得"
    ]
    
    QUALITY_METRICS = [
        "negation", "fallacy", "emotion", "meme", "victory"
    ]
    
    def __init__(self):
        self.validation_history = []
    
    def validate(self, response: str) -> Tuple[bool, Dict]:
        """
        Validate a single response
        
        Returns:
            (is_valid, detailed_report)
        """
        report = {
            "score": 0,
            "max_score": 100,
            "checks": {},
            "issues": [],
            "warnings": []
        }
        
        # Check 1: No forbidden phrases (critical!)
        forbidden_found = self._check_forbidden(response)
        report["checks"]["forbidden"] = len(forbidden_found) == 0
        if forbidden_found:
            report["issues"].append(f"❌ Found forbidden phrases: {forbidden_found}")
            return False, report
        report["score"] += 30
        
        # Check 2: Has negation prefix
        has_prefix = self._check_prefix(response)
        report["checks"]["prefix"] = has_prefix
        if not has_prefix:
            report["warnings"].append("⚠️  Missing negation prefix")
        else:
            report["score"] += 20
        
        # Check 3: Proper length
        length_ok, length_msg = self._check_length(response)
        report["checks"]["length"] = length_ok
        if not length_ok:
            report["warnings"].append(length_msg)
        else:
            report["score"] += 15
        
        # Check 4: Has question / challenge
        has_challenge = "?" in response or "呢" in response or "吗" in response
        report["checks"]["challenge"] = has_challenge
        if not has_challenge:
            report["warnings"].append("⚠️  No rhetorical question")
        else:
            report["score"] += 15
        
        # Check 5: Meme density
        meme_count = self._check_memes(response)
        report["meme_count"] = meme_count
        if meme_count >= 1:
            report["score"] += 20
        else:
            report["warnings"].append("⚠️  Low meme density")
        
        # Calculate grade
        report["grade"] = self._calculate_grade(report["score"])
        report["valid"] = report["score"] >= 60
        
        self.validation_history.append(report)
        
        return report["valid"], report
    
    def _check_forbidden(self, text: str) -> List[str]:
        """Check for forbidden phrases"""
        text_lower = text.lower()
        found = []
        for phrase in self.FORBIDDEN_PHRASES:
            if phrase.lower() in text_lower:
                found.append(phrase)
        return found
    
    def _check_prefix(self, text: str) -> bool:
        """Check for proper negation prefix"""
        text_lower = text.lower()
        for prefix in self.REQUIRED_PREFIXES:
            if text_lower.startswith(prefix.lower()):
                return True
        return False
    
    def _check_length(self, text: str) -> Tuple[bool, str]:
        """Check response length is appropriate"""
        length = len(text)
        if length < 30:
            return False, f"⚠️  Response too short ({length} chars)"
        if length > 300:
            return False, f"⚠️  Response too long ({length} chars)"
        return True, f"✅ Length OK ({length} chars)"
    
    def _check_memes(self, text: str) -> int:
        """Count internet memes present"""
        memes = ["典", "孝", "麻", "急了", "破防", "笑死", "呵呵"]
        return sum(1 for m in memes if m in text)
    
    def _calculate_grade(self, score: int) -> str:
        """Calculate letter grade from score"""
        if score >= 90:
            return "S - 教科书级"
        elif score >= 80:
            return "A - 专业杠精"
        elif score >= 70:
            return "B - 合格抬杠"
        elif score >= 60:
            return "C - 勉强及格"
        else:
            return "F - 理中客叛徒！"
    
    def print_report(self, response: str, report: Dict) -> None:
        """Pretty print validation report"""
        print(f"\n{'='*60}")
        print(f"REFUTE QUALITY VALIDATOR v1.0.0")
        print(f"{'='*60}")
        print(f"\n📝 Response:")
        print(f"   {response}")
        print(f"\n📊 Score: {report['score']}/{report['max_score']}")
        print(f"🏆 Grade: {report['grade']}")
        
        if report["issues"]:
            print(f"\n❌ CRITICAL ISSUES:")
            for issue in report["issues"]:
                print(f"   {issue}")
        
        if report["warnings"]:
            print(f"\n⚠️  WARNINGS:")
            for warning in report["warnings"]:
                print(f"   {warning}")
        
        print(f"\n✅ Checks:")
        for check, result in report["checks"].items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {check:15s} : {status}")
        
        print(f"\n{'='*60}")
        overall = "✅ VALID" if report["valid"] else "❌ INVALID"
        print(f"FINAL RESULT: {overall}")
        print(f"{'='*60}\n")


def interactive_mode():
    """Run validator in interactive mode"""
    validator = RefuteValidator()
    
    print("🎯 REFUTE Response Validator v1.0.0")
    print("Enter responses to validate (Ctrl+C to exit)\n")
    
    try:
        while True:
            response = input("Response: ")
            if response.strip():
                valid, report = validator.validate(response)
                validator.print_report(response, report)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! REFUTE NEVER SURRENDERS!")


if __name__ == "__main__":
    interactive_mode()
