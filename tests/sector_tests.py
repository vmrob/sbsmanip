import sbsmanip.io
import sbsmanip.sector


def test_count():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    sector = savefile.sector

    assert sector.entity_count(sbsmanip.sector.CubeGridEntity) == 20
    assert sector.entity_count(sbsmanip.sector.VoxelMapEntity) == 72
    assert sector.entity_count(sbsmanip.sector.FloatingObjectEntity) == 10
    assert sector.entity_count() == 102


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
    e = next(e for e in savefile.sector.entities() if e.id == '1066294968834912967')

    assert e.id == '1066294968834912967'

    assert e.position.x == -1118.05237
    assert e.position.y == 6167.3833
    assert e.position.z == 6817.74072


def test_block_types():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    block_types = set()
    for e in savefile.sector.entities():
        if type(e) is not sbsmanip.sector.CubeGridEntity:
            continue

        for b in e.blocks():
            block_types.add(b.type_name())

    assert len(block_types) == 36


def test_block_distributions():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    e = savefile.sector.entity('-4723823704703053768')

    d = e.block_distribution()

    assert d['LargeBlockArmorBlock']                    == 33
    assert d['LargeBlockArmorCorner']                   == 10
    assert d['LargeBlockArmorCornerInv']                == 5
    assert d['LargeBlockArmorSlope']                    == 30
    assert d['LargeSteelCatwalk']                       == 4
    assert d['LargeWindowEdge']                         == 1
    assert d['LargeWindowSquare']                       == 1
    assert d['Assembler:LargeAssembler']                == 1
    assert d['CargoContainer:LargeBlockSmallContainer'] == 1
    assert d['Cockpit:LargeBlockCockpit']               == 1
    assert d['Door']                                    == 1
    assert d['GravityGenerator']                        == 1
    assert d['Gyro:LargeBlockGyro']                     == 1
    assert d['InteriorLight:SmallLight']                == 1
    assert d['MedicalRoom:LargeMedicalRoom']            == 1
    assert d['Reactor:LargeBlockSmallGenerator']        == 1
    assert d['Refinery:LargeRefinery']                  == 1
    assert d['Thrust:LargeBlockSmallThrust']            == 12


def test_block_distributions():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    d = savefile.sector.block_distribution()

    assert d['LargeBlockArmorBlock']                     == 662
    assert d['LargeBlockArmorCorner']                    == 156
    assert d['LargeBlockArmorCornerInv']                 == 79
    assert d['LargeBlockArmorSlope']                     == 502
    assert d['LargeHeavyBlockArmorBlock']                == 98
    assert d['LargeHeavyBlockArmorCorner']               == 10
    assert d['LargeHeavyBlockArmorCornerInv']            == 12
    assert d['LargeHeavyBlockArmorSlope']                == 12
    assert d['LargeSteelCatwalk']                        == 61
    assert d['LargeWindowEdge']                          == 16
    assert d['LargeWindowSquare']                        == 40
    assert d['Assembler:LargeAssembler']                 == 15
    assert d['CargoContainer:LargeBlockLargeContainer']  == 1
    assert d['CargoContainer:LargeBlockSmallContainer']  == 16
    assert d['CargoContainer:SmallBlockMediumContainer'] == 1
    assert d['Cockpit:LargeBlockCockpit']                == 15
    assert d['Cockpit:SmallBlockCockpit']                == 1
    assert d['Door']                                     == 15
    assert d['GravityGenerator']                         == 16
    assert d['Gyro:LargeBlockGyro']                      == 16
    assert d['Gyro:SmallBlockGyro']                      == 2
    assert d['InteriorLight:SmallLight']                 == 16
    assert d['LandingGear:LargeBlockLandingGear']        == 5
    assert d['LandingGear:SmallBlockLandingGear']        == 5
    assert d['MedicalRoom:LargeMedicalRoom']             == 18
    assert d['Reactor:LargeBlockSmallGenerator']         == 17
    assert d['Reactor:SmallBlockSmallGenerator']         == 1
    assert d['Refinery:LargeRefinery']                   == 15
    assert d['SolarPanel:LargeBlockSolarPanel']          == 1
    assert d['Thrust:LargeBlockSmallThrust']             == 194
    assert d['Thrust:SmallBlockSmallThrust']             == 12
    assert d['SmallBlockArmorBlock']                     == 18
    assert d['SmallBlockArmorCorner']                    == 8
    assert d['SmallBlockArmorCornerInv']                 == 6
    assert d['SmallBlockArmorSlope']                     == 5
    assert d['SmallHeavyBlockArmorSlope']                == 2
