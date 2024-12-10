import language_tool_python

class LanguageAnalyzer:
    def __init__(self):
        self.tool = language_tool_python.LanguageTool('en-US')
        
    def analyze(self, text):
        # Get grammar and style mistakes
        matches = self.tool.check(text)
        
        errors = []
        for match in matches:
            error = {
                'message': match.message,
                'context': match.context,
                'suggestions': match.replacements,
                'category': match.category,
                'type': match.ruleIssueType,
                'start': match.offset,
                'end': match.offset + match.errorLength
            }
            errors.append(error)
            
        return errors
    
    def get_suggestions(self, text):
        suggestions = []
        matches = self.tool.check(text)
        
        for match in matches:
            if match.replacements:
                suggestion = {
                    'original': text[match.offset:match.offset + match.errorLength],
                    'replacements': match.replacements[:3],  # Top 3 suggestions
                    'explanation': match.message
                }
                suggestions.append(suggestion)
                
        return suggestions
    
    def correct_text(self, text):
        return self.tool.correct(text)
