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
    e = savefile.sector.entity('1066294968834912967')

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

    assert d['LargeBlockArmorBlock']                                    == 33
    assert d['LargeBlockArmorCorner']                                   == 10
    assert d['LargeBlockArmorCornerInv']                                == 5
    assert d['LargeBlockArmorSlope']                                    == 30
    assert d['LargeSteelCatwalk']                                       == 4
    assert d['LargeWindowEdge']                                         == 1
    assert d['LargeWindowSquare']                                       == 1
    assert d['MyObjectBuilder_Assembler:LargeAssembler']                == 1
    assert d['MyObjectBuilder_CargoContainer:LargeBlockSmallContainer'] == 1
    assert d['MyObjectBuilder_Cockpit:LargeBlockCockpit']               == 1
    assert d['MyObjectBuilder_Door']                                    == 1
    assert d['MyObjectBuilder_GravityGenerator']                        == 1
    assert d['MyObjectBuilder_Gyro:LargeBlockGyro']                     == 1
    assert d['MyObjectBuilder_InteriorLight:SmallLight']                == 1
    assert d['MyObjectBuilder_MedicalRoom:LargeMedicalRoom']            == 1
    assert d['MyObjectBuilder_Reactor:LargeBlockSmallGenerator']        == 1
    assert d['MyObjectBuilder_Refinery:LargeRefinery']                  == 1
    assert d['MyObjectBuilder_Thrust:LargeBlockSmallThrust']            == 12


def test_block_distributions():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    d = savefile.sector.block_distribution()

    assert d['LargeBlockArmorBlock']                                     == 662
    assert d['LargeBlockArmorCorner']                                    == 156
    assert d['LargeBlockArmorCornerInv']                                 == 79
    assert d['LargeBlockArmorSlope']                                     == 502
    assert d['LargeHeavyBlockArmorBlock']                                == 98
    assert d['LargeHeavyBlockArmorCorner']                               == 10
    assert d['LargeHeavyBlockArmorCornerInv']                            == 12
    assert d['LargeHeavyBlockArmorSlope']                                == 12
    assert d['LargeSteelCatwalk']                                        == 61
    assert d['LargeWindowEdge']                                          == 16
    assert d['LargeWindowSquare']                                        == 40
    assert d['MyObjectBuilder_Assembler:LargeAssembler']                 == 15
    assert d['MyObjectBuilder_CargoContainer:LargeBlockLargeContainer']  == 1
    assert d['MyObjectBuilder_CargoContainer:LargeBlockSmallContainer']  == 16
    assert d['MyObjectBuilder_CargoContainer:SmallBlockMediumContainer'] == 1
    assert d['MyObjectBuilder_Cockpit:LargeBlockCockpit']                == 15
    assert d['MyObjectBuilder_Cockpit:SmallBlockCockpit']                == 1
    assert d['MyObjectBuilder_Door']                                     == 15
    assert d['MyObjectBuilder_GravityGenerator']                         == 16
    assert d['MyObjectBuilder_Gyro:LargeBlockGyro']                      == 16
    assert d['MyObjectBuilder_Gyro:SmallBlockGyro']                      == 2
    assert d['MyObjectBuilder_InteriorLight:SmallLight']                 == 16
    assert d['MyObjectBuilder_LandingGear:LargeBlockLandingGear']        == 5
    assert d['MyObjectBuilder_LandingGear:SmallBlockLandingGear']        == 5
    assert d['MyObjectBuilder_MedicalRoom:LargeMedicalRoom']             == 18
    assert d['MyObjectBuilder_Reactor:LargeBlockSmallGenerator']         == 17
    assert d['MyObjectBuilder_Reactor:SmallBlockSmallGenerator']         == 1
    assert d['MyObjectBuilder_Refinery:LargeRefinery']                   == 15
    assert d['MyObjectBuilder_SolarPanel:LargeBlockSolarPanel']          == 1
    assert d['MyObjectBuilder_Thrust:LargeBlockSmallThrust']             == 194
    assert d['MyObjectBuilder_Thrust:SmallBlockSmallThrust']             == 12
    assert d['SmallBlockArmorBlock']                                     == 18
    assert d['SmallBlockArmorCorner']                                    == 8
    assert d['SmallBlockArmorCornerInv']                                 == 6
    assert d['SmallBlockArmorSlope']                                     == 5
    assert d['SmallHeavyBlockArmorSlope']                                == 2
