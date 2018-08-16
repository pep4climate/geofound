import geofound
from geofound import models


def test_vesics():
    """
    values from: Gunaratne, Manjriker. 2006. "Spread Footings: Analysis and Design."
    """
    length = 2
    width = 2
    depth = 1
    phi = 35
    cohesion = 0
    unit_dry_weight = 17
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    fd = geofound.create_foundation(length, width, depth)
    geofound.capacity_vesics_1975(sl, fd, verbose=0)
    assert geofound.isclose(fd.nc_factor, 46.1, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 33.3, rel_tol=0.001)
    assert geofound.isclose(fd.ng_factor, 48.0, rel_tol=0.001)
    assert geofound.isclose(fd.q_ult, 1574.8, rel_tol=0.001)


def test_terzaghi():
    """
    values from: Gunaratne, Manjriker. 2006. "Spread Footings: Analysis and Design."
    - except qult was not validated
    """
    length = 2
    width = 2
    depth = 1
    phi = 35
    cohesion = 0
    unit_dry_weight = 17
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    fd = geofound.create_foundation(length, width, depth)
    geofound.capacity_terzaghi_1943(sl, fd, verbose=0)
    assert geofound.isclose(fd.nc_factor, 57.8, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 41.4, rel_tol=0.001)
    assert geofound.isclose(fd.ng_factor, 47.3, rel_tol=0.001)
    assert geofound.isclose(fd.q_ult, 1347.0, rel_tol=0.001)
    print("DONE")


def test_terzaghi_again():
    """
    values from: Gunaratne, Manjriker. 2006. "Spread Footings: Analysis and Design."
    """
    length = 2
    width = 2
    depth = 2
    phi = 15
    cohesion = 20.0  # kPa
    unit_dry_weight = 17  # kN/m3
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    fd = geofound.create_foundation(length, width, depth)
    geofound.capacity_terzaghi_1943(sl, fd, verbose=0)
    print(fd.q_ult)
    assert geofound.isclose(fd.nc_factor, 12.86, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 4.45, rel_tol=0.001)
    assert geofound.isclose(fd.ng_factor, 2.168, rel_tol=0.001)
    assert geofound.isclose(fd.q_ult, 515.0, rel_tol=0.001)


def test_meyerhof():
    length = 2
    width = 2
    depth = 2
    phi = 15
    cohesion = 20.0  # kPa
    unit_dry_weight = 17  # kN/m3
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    fd = geofound.create_foundation(length, width, depth)
    geofound.capacity_meyerhof_1963(sl, fd, gwl=1000, verbose=0)
    print(fd.ng_factor)
    assert geofound.isclose(fd.nc_factor, 10.97, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 3.94, rel_tol=0.01)
    assert geofound.isclose(fd.ng_factor, 1.13, rel_tol=0.01)
    assert geofound.isclose(fd.q_ult, 573.3, rel_tol=0.001)


def test_meyerhof_using_fabrizio_problem1():
    """
    http:

    :return:
    """

    length = 100000
    width = 4.
    depth = 1.5
    phi = 0.0
    cohesion = 90000  # Pa
    unit_dry_weight = 19000.  # N/m3
    unit_sat_weight = 19000.
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    sl.unit_sat_weight = unit_sat_weight
    fd = geofound.create_foundation(length, width, depth)
    geofound.capacity_meyerhof_1963(sl, fd, verbose=0)
    assert geofound.isclose(fd.q_ult, 526000., rel_tol=0.001), fd.q_ult


def test_meyerhof_using_fabrizio_problem2():
    """
    http:

    :return:
    """

    length = 100000
    width = 4.
    depth = 1.5
    phi = 34.0
    cohesion = 0.0  # kPa
    unit_dry_weight = 18.  # kN/m3
    unit_sat_weight = 20.
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight, pw=9.8)

    sl.unit_sat_weight = unit_sat_weight
    fd = geofound.create_foundation(length, width, depth)

    # problem 2) a)

    geofound.capacity_meyerhof_1963(sl, fd, gwl=20.0, verbose=0)
    # # assert geofound.isclose(fd.nc_factor, 10.97, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 29.4, rel_tol=0.01)
    assert geofound.isclose(fd.ng_factor, 31.1, rel_tol=0.01)
    assert geofound.isclose(fd.q_ult, 2056, rel_tol=0.01)

    # problem 2) b)
    geofound.capacity_meyerhof_1963(sl, fd, gwl=1.5, verbose=0)
    # assert geofound.isclose(fd.nc_factor, 10.97, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 29.4, rel_tol=0.01)
    assert geofound.isclose(fd.ng_factor, 31.1, rel_tol=0.01)
    assert geofound.isclose(fd.q_ult, 1521, rel_tol=0.01), fd.q_ult

    # problem 2) c)
    geofound.capacity_meyerhof_1963(sl, fd, gwl=0.5, verbose=0)
    # assert geofound.isclose(fd.nc_factor, 10.97, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 29.4, rel_tol=0.01)
    assert geofound.isclose(fd.ng_factor, 31.1, rel_tol=0.01)
    assert geofound.isclose(fd.q_ult, 1252, rel_tol=0.03), fd.q_ult


def test_hansen():
    length = 2
    width = 2
    depth = 2
    phi = 15
    cohesion = 20.0  # kPa
    unit_dry_weight = 17  # kN/m3
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    fd = geofound.create_foundation(length, width, depth)
    geofound.capacity_hansen_1970(sl, fd, verbose=0)
    assert geofound.isclose(fd.nc_factor, 10.97, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 3.94, rel_tol=0.01)
    assert geofound.isclose(fd.ng_factor, 1.18, rel_tol=0.01)
    assert geofound.isclose(fd.q_ult, 648.0, rel_tol=0.001)


def test_nzs_vm4():
    """
    values from: NZ Building code Clause B1 VM4 example in Appendix C
    -Retain wall example load case 1 (page 71)
    """
    length = 10000  # Actually should be a strip
    width = 2.65
    depth = 0.4
    phi = 0
    cohesion = 75.0  # kPa
    unit_dry_weight = 18  # kN/m3
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    fd = geofound.create_foundation(length, width, depth)
    h_b = 70.45 * length
    vertical_load = 131.29 * length
    h_eff_b = 1.44
    loc_v_b = 0.848
    geofound.capacity_nzs_vm4_2011(sl, fd, h_b=h_b, vertical_load=vertical_load, h_eff_b=h_eff_b, loc_v_b=loc_v_b,
                                   verbose=0)
    assert geofound.isclose(fd.nc_factor, 5.14, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 1.0, rel_tol=0.01)
    assert geofound.isclose(fd.ng_factor, 0.0, rel_tol=0.01)
    assert geofound.isclose(fd.q_ult, 368.12, rel_tol=0.001)


def test_nzs_vm4_load_case_3():
    """
    values from: NZ Building code Clause B1 VM4 example in Appendix C
    -Retain wall example load case 3
    """
    length = 10000  # Actually should be a strip
    width = 2.65
    depth = 0.4
    phi = 0
    cohesion = 75.0  # kPa
    unit_dry_weight = 18  # kN/m3
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    fd = geofound.create_foundation(length, width, depth)
    h_b = 93.27 * length
    vertical_load = 154.87 * length
    h_eff_b = 1.78
    loc_v_b = 0.854
    geofound.capacity_nzs_vm4_2011(sl, fd, h_b=h_b, vertical_load=vertical_load, h_eff_b=h_eff_b, loc_v_b=loc_v_b,
                                   verbose=0)
    assert geofound.isclose(fd.nc_factor, 5.14, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 1.0, rel_tol=0.01)
    assert geofound.isclose(fd.ng_factor, 0.0, rel_tol=0.01)
    assert geofound.isclose(fd.q_ult, 301.68, rel_tol=0.001)


def test_nzs_vm4_load_case_5():
    """
    values from: NZ Building code Clause B1 VM4 example in Appendix C
    -Retain wall example load case 5
    ***looks like there is an error in the calculation of d_c
    ***small discrepancy between Nc, i_c and i_q
    """
    length = 10000  # Actually should be a strip
    width = 2.65
    depth = 0.4
    phi = 25.0
    cohesion = 12.5  # kPa
    unit_dry_weight = 8.2  # kN/m3
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    fd = geofound.create_foundation(length, width, depth)
    h_b = 70.45 * length
    vertical_load = 144.48 * length
    h_eff_b = 1.44
    loc_v_b = 0.813
    geofound.capacity_nzs_vm4_2011(sl, fd, h_b=h_b, vertical_load=vertical_load, h_eff_b=h_eff_b, loc_v_b=loc_v_b,
                                   verbose=0)

    assert geofound.isclose(fd.nc_factor, 20.72, rel_tol=0.001)
    assert geofound.isclose(fd.nq_factor, 10.66, rel_tol=0.01)
    assert geofound.isclose(fd.ng_factor, 9.01, rel_tol=0.01)
    assert geofound.isclose(fd.q_ult, 145.02, rel_tol=0.001)  # 152.70?


def test_from_encn452_2013():
    """
    Values from HW#7 crib ENCN452 course 2013
    """
    length = 6.0  # actually a strip in
    width = 3.0
    depth = 1.5
    phi = 0.0
    cohesion = 40.0
    unit_dry_weight = 18.0
    sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
    fd = geofound.create_foundation(length, width, depth)
    geofound.capacity_terzaghi_1943(sl, fd, verbose=0)
    geofound.capacity_vesics_1975(sl, fd, verbose=0)
    assert geofound.isclose(fd.q_ult, 298.0, rel_tol=0.001)


def test_size_foundations():
    phi = 32
    cohesion = 0
    unit_dry_weight = 20
    fos_values = [3, 5, 10, 20]
    vertical_loads = [500., 800., 1000.]
    methods = geofound.available_methods
    for fos in fos_values:
        for vertical_load in vertical_loads:
            for method in methods:
                sl = geofound.create_soil(phi, cohesion, unit_dry_weight)
                fd = geofound.size_footing_for_capacity(sl, vertical_load=vertical_load, fos=fos, method=method,
                                                        length_to_width=2)
                f_capacity = fd.length * fd.width * fd.q_ult
                actual_fos = f_capacity / vertical_load
                assert geofound.isclose(actual_fos, fos, rel_tol=0.1), (fos, vertical_load, method)


def test_meyerhof_and_hanna_capacity_strong_sand_over_weak_clay():
    # STRONG SAND OVER WEAK CLAY
    length = 1000000.0  # actually a strip in
    width = 1.0
    depth = 0.0
    fd = geofound.create_foundation(length=length, width=width, depth=depth)

    phi_0 = 34.0
    cohesion_0 = 0.0
    unit_dry_weight_0 = 17.0
    sl_0 = geofound.create_soil(phi=phi_0, cohesion=cohesion_0, unit_dry_weight=unit_dry_weight_0)

    phi_1 = 0.0
    cohesion_1 = 30.0
    unit_dry_weight_1 = 17.0
    sl_1 = geofound.create_soil(phi=phi_1, cohesion=cohesion_1, unit_dry_weight=unit_dry_weight_1)
    h0 = 1.5  # m, height of the crust layer

    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, verbose=0)

    assert geofound.isclose(fd.q_ult, 264.74, rel_tol=0.001), fd.q_ult


def test_meyerhof_and_hanna_capacity_strong_sand_over_weak_sand():
    # STRONG SAND OVER WEAK SAND
    length = 1000000.0  # actually a strip in
    width = 1.0
    depth = 0.0
    fd = geofound.create_foundation(length=length, width=width, depth=depth)

    phi_0 = 34.0
    cohesion_0 = 0.0
    unit_dry_weight_0 = 17.0
    sl_0 = geofound.create_soil(phi=phi_0, cohesion=cohesion_0, unit_dry_weight=unit_dry_weight_0)

    phi_1 = 17.0
    cohesion_1 = 0.0
    unit_dry_weight_1 = 17.0
    sl_1 = geofound.create_soil(phi=phi_1, cohesion=cohesion_1, unit_dry_weight=unit_dry_weight_1)
    h0 = 1.5  # m, height of the crust layer

    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, verbose=0)
    assert geofound.isclose(fd.q_ult, 158.32, rel_tol=0.001), fd.q_ult


def test_meyerhof_and_hanna_capacity_strong_clay_over_weak_sand():
    # STRONG CLAY OVER WEAK SAND
    length = 1000000000.0  # actually a strip in
    width = 1.0
    depth = 0.0
    fd = geofound.create_foundation(length=length, width=width, depth=depth)

    phi_0 = 0.0
    cohesion_0 = 85.0
    unit_dry_weight_0 = 16.5
    sl_0 = geofound.create_soil(phi=phi_0, cohesion=cohesion_0, unit_dry_weight=unit_dry_weight_0)

    phi_1 = 17.0
    cohesion_1 = 0.0
    unit_dry_weight_1 = 17.0
    sl_1 = geofound.create_soil(phi=phi_1, cohesion=cohesion_1, unit_dry_weight=unit_dry_weight_1)
    h0 = 1  # m, height of the crust layer

    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, verbose=0)
    assert geofound.isclose(fd.q_ult, 182.97, rel_tol=0.001), fd.q_ult


def test_meyerhof_and_hanna_capacity_sand_over_sand_gwl():
    # STRONG SAND OVER WEAK SAND
    length = 1000000.0  # actually a strip in
    width = 4.0
    depth = 1.5
    fd = geofound.create_foundation(length=length, width=width, depth=depth)

    phi_0 = 34.0
    cohesion_0 = 0.0
    unit_dry_weight_0 = 18000
    sl_0 = geofound.create_soil(phi=phi_0, cohesion=cohesion_0, unit_dry_weight=unit_dry_weight_0)
    sl_0.unit_sat_weight = 20000

    phi_1 = 34.0
    cohesion_1 = 0.0
    unit_dry_weight_1 = 18000
    sl_1 = geofound.create_soil(phi=phi_1, cohesion=cohesion_1, unit_dry_weight=unit_dry_weight_1)
    sl_1.unit_sat_weight = 20000
    h0 = 3.0  # m, height of the crust layer

    # Case 1: GWL at surface
    gwl = 0.0
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.07
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof / 1000)

    # Case 2: GWL at between foundation depth and surface
    gwl = 0.5
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.07
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof / 1000)

    # Case 3: GWL at between foundation depth and foundation depth plus width, and GWL < layer 1 depth
    gwl = 1.8
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.07
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof / 1000)

    # Case 4: GWL at between foundation depth and foundation depth plus width, and GWL > layer 1 depth
    gwl = 4.8
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.03
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof / 1000)

    # Case 5: GWL beyond foundation depth plus width
    gwl = 20.
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.07
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof/1000)


def test_meyerhof_and_hanna_capacity_clay_over_clay_gwl():
    length = 1000000.0  # actually a strip in
    width = 4.0
    depth = 1.5
    fd = geofound.create_foundation(length=length, width=width, depth=depth)

    phi_0 = 0.0
    cohesion_0 = 40.0
    unit_dry_weight_0 = 18000
    sl_0 = geofound.create_soil(phi=phi_0, cohesion=cohesion_0, unit_dry_weight=unit_dry_weight_0)
    sl_0.unit_sat_weight = 20000

    phi_1 = 0.0
    cohesion_1 = 40.0
    unit_dry_weight_1 = 18000
    sl_1 = geofound.create_soil(phi=phi_1, cohesion=cohesion_1, unit_dry_weight=unit_dry_weight_1)
    sl_1.unit_sat_weight = 20000
    h0 = 3.0  # m, height of the crust layer

    # Case 1: GWL at surface
    gwl = 0.0
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.00
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof / 1000)

    # Case 2: GWL at between foundation depth and surface
    gwl = 0.5
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.0
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof / 1000)

    # Case 3: GWL at between foundation depth and foundation depth plus width, and GWL < layer 1 depth
    gwl = 1.8
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.0
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof / 1000)

    # Case 4: GWL at between foundation depth and foundation depth plus width, and GWL > layer 1 depth
    gwl = 4.8
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.0
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof / 1000)

    # Case 5: GWL beyond foundation depth plus width
    gwl = 20.
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    correction = 1.0
    corrected_2layer = fd.q_ult * correction
    assert geofound.isclose(corrected_2layer, q_ult_meyerhof, rel_tol=0.01), (corrected_2layer, q_ult_meyerhof/1000)


def test_capacity_sp_meyerhof_and_hanna_1978():
    length = 1000000.0  # actually a strip in
    width = 16.0
    depth = 0.0
    fd = geofound.create_foundation(length=length, width=width, depth=depth)

    phi_0 = 0.0
    cohesion_0 = 50000
    unit_dry_weight_0 = 18000
    sl_0 = geofound.create_soil(phi=phi_0, cohesion=cohesion_0, unit_dry_weight=unit_dry_weight_0)
    sl_0.unit_sat_weight = 20000

    phi_1 = 25
    cohesion_1 = 0.0
    unit_dry_weight_1 = 18000
    sl_1 = geofound.create_soil(phi=phi_1, cohesion=cohesion_1, unit_dry_weight=unit_dry_weight_1)
    sl_1.unit_sat_weight = 20000
    h0 = 2.0  # m, height of the crust layer
    # c_a = 0.0
    # k=1.7

    # Case 1: GWL at surface
    gwl = 2.0
    sp = models.SoilProfile()
    sp.add_layer(0, sl_0)
    sp.add_layer(h0, sl_1)
    q_ult_meyerhof = geofound.capacity_meyerhof_1963(sl_0, fd, gwl=gwl)
    # q_ult_meyerhof_and_hanna = geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=gwl, verbose=0)
    geofound.capacity_sp_meyerhof_and_hanna_1978(sp, fd, gwl=gwl, verbose=0)
    correction_lower_layer = 1.1
    expected = q_ult_meyerhof * correction_lower_layer
    assert geofound.isclose(expected, fd.q_ult, rel_tol=0.01), (expected / 1000, fd.q_ult / 1000)


# def test_meyerhof_and_hanna_capacity_strong_clay_over_weak_sand_vs_limitstategeo():
# # STRONG CLAY OVER WEAK SAND
# length = 1000000.0  # actually a strip in
#     width = 10.0
#     depth = 0.0
#     fd = geofound.create_foundation(length=length, width=width, depth=depth)
#
#     phi_0 = 0.0
#     cohesion_0 = 50.0
#     unit_dry_weight_0 = 19.
#     sl_0 = geofound.create_soil(phi=phi_0, cohesion=cohesion_0, unit_dry_weight=unit_dry_weight_0)
#
#     phi_1 = 3.
#     cohesion_1 = 0.0
#     unit_dry_weight_1 = 19.
#     sl_1 = geofound.create_soil(phi=phi_1, cohesion=cohesion_1, unit_dry_weight=unit_dry_weight_1)
#     h0 = 2.  # m, height of the crust layer
#     #c_a = 54.4
#     #k = 1.7
#
#     geofound.capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, verbose=0)
#     #print(sl_0.nc_factor_0)
#     #print(fd.q_ult)
#
#     #print("q_b= " + str(fd.q_b))
#     print("q_b_limitstategeo= " + str(fd.q_b))
#     print("q_t_limitstategeo= " + str(fd.q_t))
#     print("q_ult_limitstategeo= " + str(fd.q_ult))
#     assert geofound.isclose(fd.q_ult, 26.45, rel_tol=0.001), fd.q_ult

def load_soil_sample_data(sl0):
    """
    Sample data for the Soil object
    :param sl0: Soil Object
    :return:
    """
    # soil
    sl0.height = 1.5  # [m]
    sl0.phi = 34  # [degrees]
    sl0.unit_dry_weight = 17000  # [N/m3]
    sl0.c_a = 0
    sl0.cohesion = 0  # [Pa]


def load_soil_sample_data2(sl1):
    """
    Sample data for the Soil object
    :param sl1: Soil Object
    :return:
    """
    # soil
    sl1.cohesion = 30  # [Pa]
    sl1.phi = 0  # [degrees]
    sl1.unit_dry_weight = 17000  # [N/m3]


if __name__ == '__main__':
    test_meyerhof_using_fabrizio_problem2()
    # test_meyerhof_and_hanna_capacity_sand_over_sand_gwl()
    # test_meyerhof_and_hanna_capacity_strong_clay_over_weak_sand()
