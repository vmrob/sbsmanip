import sbsmanip.io
import sbsmanip.sector


def test_count():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    assert savefile.sector.entity_count() == 102


def test_sector_entities_generator():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    sector = savefile.sector

    entities = list(sector.entities())
    for e in sector.entities():
        assert hasattr(e, 'id')
        assert type(e.position.x) is float
        assert type(e.position.y) is float
        assert type(e.position.z) is float
    assert len(entities) == 102


def test_sector_single_entity():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    e = savefile.sector.entity('1066294968834912967')

    assert e.id == '1066294968834912967'

    assert e.position.x == -1118.05237
    assert e.position.y == 6167.3833
    assert e.position.z == 6817.74072
    