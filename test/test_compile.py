from pkg_resources import Requirement

from qer.compile import _merge_requirements


def test_combine_reqs_conditions_and_markers():
    req1 = Requirement.parse('pylint<2;platform_system=="Windows"')
    req2 = Requirement.parse('pylint>1;python_version<"3.0"')

    assert _merge_requirements(req1, req2) == \
           Requirement.parse('pylint>1,<2;platform_system=="Windows" and python_version<"3.0"')


def test_combine_no_specs():
    req1 = Requirement.parse('pylint')
    req2 = Requirement.parse('pylint;python_version<"3.0"')

    assert _merge_requirements(req1, req2) == \
           Requirement.parse('pylint;python_version<"3.0"')


def test_combine_dup_specs():
    req1 = Requirement.parse('pylint==1.0.1')
    req2 = Requirement.parse('pylint==1.0.1;python_version<"3.0"')

    assert _merge_requirements(req1, req2) == \
           Requirement.parse('pylint==1.0.1;python_version<"3.0"')


def test_combine_multiple_specs():
    req1 = Requirement.parse('pylint~=3.1')
    req2 = Requirement.parse('pylint>2,>3')

    assert _merge_requirements(req1, req2) == \
           Requirement.parse('pylint~=3.1,>2,>3')


def test_combine_identical_reqs():
    req1 = Requirement.parse('pylint>=3.1')
    req2 = Requirement.parse('pylint>=3.1')

    assert _merge_requirements(req1, req2) == \
           Requirement.parse('pylint>=3.1')


def test_combine_diff_specs_identical_markers():
    req1 = Requirement.parse('pylint>=3.1; python_version>"3.0"')
    req2 = Requirement.parse('pylint>=3.2; python_version>"3.0"')

    assert _merge_requirements(req1, req2) == \
           Requirement.parse('pylint>=3.1,>=3.2; python_version>"3.0"')


def test_combine_and_compare_identical_reqs():
    req1 = Requirement.parse('pylint>=3.1')
    req2 = Requirement.parse('pylint>=3.1')

    assert _merge_requirements(req1, req2) == \
           req1


def test_combine_with_extras_markers():
    req1 = Requirement.parse('pylint; extra=="test"')
    req2 = Requirement.parse('pylint; python_version>"3.0" and extra=="test"')

    result = _merge_requirements(req1, req2)
    assert result == Requirement.parse('pylint; python_version>"3.0" and extra=="test"')
