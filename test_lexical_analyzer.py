# Importa la clase LexicalAnalyzer del archivo generado
from lexical_analyzer import LexicalAnalyzer

def test_lexical_analyzer():
    analyzer = LexicalAnalyzer()

    # Lista de pruebas con texto de entrada y una descripción de lo que se espera encontrar
    test_cases = [
        ("123 + abc * 456", "Expected tokens: Numbers, operators, and identifiers"),
        ("helloWorld", "Expected token: Identifier"),
        ("if (x > 10) { return x; }", "Complex test with conditions and blocks"),
        ("123abc456", "Expected error: Invalid identifier"),
        ("/* This is a comment */", "Expected: Comments to be ignored"),
        ("\"string with spaces\"", "Expected token: String with spaces"),
        ("5.67", "Expected token: Floating point number")
    ]

    for input_text, description in test_cases:
        print(f"\nTesting input: {input_text}")
        print(description)
        try:
            results = analyzer.analyze(input_text)
            print("Tokens found:", results)
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    test_lexical_analyzer()