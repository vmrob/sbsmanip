import sbsmanip.io


def test_count():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    assert savefile.total_objects() == 102