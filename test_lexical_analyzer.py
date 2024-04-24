# test_lexical_analyzer.py
from lexical_analyzer import LexicalAnalyzer

def test_lexical_analyzer():
    analyzer = LexicalAnalyzer()
    # Configurar los AFDs aquí, usualmente cargarían desde una configuración inicial

    test_cases = [
        ("123 + 456", "Numbers and operator", ['number', 'operator', 'number']),
        ("helloWorld", "Identifier", ['identifier']),
        ("if (x > 10) { return x; }", "Conditions and blocks", ['identifier', 'operator', 'number', 'operator', 'identifier', 'operator']),
        ("123abc456", "Invalid identifier", ['number', 'identifier', 'number']),
        ("/* This is a comment */", "Comments ignored", []),
        ("\"string with spaces\"", "String with spaces", ['string']),
        ("5.67", "Floating point number", ['number'])
    ]

    for input_text, description, expected_tokens in test_cases:
        print(f"\nTesting input: {input_text}\nExpected: {description}")
        results = analyzer.analyze(input_text)
        print("Tokens found:")
        for expected in expected_tokens:
            if expected in results:
                print(f"{expected.capitalize()}: {results[expected]}")
            else:
                print(f"{expected.capitalize()}: None")

if __name__ == "__main__":
    test_lexical_analyzer()