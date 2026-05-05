from toolkit.code_understanding import CodeUnderstandingModule

def test_analyze_code():
    cu = CodeUnderstandingModule()
    result = cu.analyze_code("def foo(x):\n    return x\n")
    assert result["success"] is True
    assert result["data"]["functions"][0]["name"] == "foo"

def test_generate_tests():
    cu = CodeUnderstandingModule()
    result = cu.generate_tests(__file__)
    assert result["success"] is True
    assert "content" in result["data"]