def generate_suggestions(skill_gap):
    suggestions = []

    critical=skill_gap.get("critical_missing", [])
    optional=skill_gap.get("optional_missing", [])

    if critical:
        suggestions.append(
            f"Focus first on critical skills: {', '.join(critical)}"
        )

    if optional:
        suggestions.append(
            f"Improve profile by learning: {', '.join(optional)}"
        )
    if not suggestions:
        suggestions.append(
            "Excellent match! Your resume aligns well with the job role."
        )

    return suggestions
def generate_suggestions(priority):
    suggestions=[]
    high=priority.get("high_priority", [])
    medium=priority.get("medium_priority", [])
    low=priority.get("low_priority", [])

    for skill in high:
        suggestions.append(
            f"🔥 **High Priority**: Focus on learning **{skill}**. "
            f"Add at least one project or hands-on example involving {skill} to your resume."
        )
    
    for skill in medium:
        suggestions.append(
            f"⚠️ **Medium Priority**: Gain working knowledge of **{skill}**"
            f"Consider adding it under skills or mentioning it in a project."
        )
    if not suggestions:
        suggestions.append(
            "✅ Your resume already covers all required skills for this role. "
            "Focus on improving project depth and explanations."
        )
    return suggestions