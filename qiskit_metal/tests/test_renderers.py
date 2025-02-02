# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable-msg=unnecessary-pass
# pylint: disable-msg=broad-except
# pylint: disable-msg=too-many-public-methods
"""
Qiskit Metal unit tests analyses functionality.
"""

import unittest
import matplotlib.pyplot as _plt

from qiskit_metal import designs
from qiskit_metal.renderers import setup_default
from qiskit_metal.renderers.renderer_ansys.q3d_renderer import QQ3DRenderer
from qiskit_metal.renderers.renderer_ansys.hfss_renderer import QHFSSRenderer
from qiskit_metal.renderers.renderer_base.renderer_base import QRenderer
from qiskit_metal.renderers.renderer_base.renderer_gui_base import QRendererGui
from qiskit_metal.renderers.renderer_gds.gds_renderer import QGDSRenderer
from qiskit_metal.renderers.renderer_mpl.mpl_interaction import MplInteraction
from qiskit_metal.qgeometries.qgeometries_handler import QGeometryTables
from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket
from qiskit_metal import draw


class TestRenderers(unittest.TestCase):
    """
    Unit test class.
    """

    def setUp(self):
        """
        Setup unit test.
        """
        pass

    def tearDown(self):
        """
        Tie any loose ends.
        """
        pass

    def test_renderer_instantiate_qrenderer(self):
        """
        Test instantiation of QRenderer in renderer_base.py.
        """
        design = designs.DesignPlanar()
        try:
            QRenderer(design)
        except Exception:
            self.fail("QRender(design) failed")

        try:
            QRenderer(design, initiate=False)
        except Exception:
            self.fail("QRenderer(design, initiate=False) failed")

        try:
            QRenderer(design, initiate=False, render_template={})
        except Exception:
            self.fail(
                "QRenderer(design, initiate=False, render_template={}) failed")

        try:
            QRenderer(design, initiate=False, render_options={})
        except Exception:
            self.fail(
                "QRenderer(design, initiate=False, render_options={}) failed")

    def test_renderer_instantiate_qrenderer_gui(self):
        """
        Test instantiation of QRendererGui in renderer_gui_base.py.
        """
        design = designs.DesignPlanar()
        try:
            QRendererGui(None, design)
        except Exception:
            self.fail("QRenderGui(None, design) failed")

        try:
            QRendererGui(None, design, initiate=False)
        except Exception:
            self.fail("QRenderGui(None, design, initiate=False) failed")

    def test_renderer_instantiate_gdsrender(self):
        """
        Test instantiation of QGDSRenderer in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        try:
            QGDSRenderer(design)
        except Exception:
            self.fail("QGDSRenderer(design) failed")

        try:
            QGDSRenderer(design, initiate=False)
        except Exception:
            self.fail("QGDSRenderer(design, initiate=False) failed")

        try:
            QGDSRenderer(design, initiate=False, render_template={})
        except Exception:
            self.fail(
                "QGDSRenderer(design, initiate=False, render_template={}) failed"
            )

        try:
            QGDSRenderer(design, initiate=False, render_options={})
        except Exception:
            self.fail(
                "QGDSRenderer(design, initiate=False, render_options={}) failed"
            )

    def test_renderer_instantiate_mplinteraction(self):
        """
        Test instantiation of MplInteraction in mpl_interaction.py.
        """
        try:
            MplInteraction(_plt)
        except Exception:
            self.fail("MplInteraction(None) failed")

    def test_renderer_instantiate_qq3d_renderer(self):
        """
        Test instantiation of QQ3DRenderer in q3d_render.py.
        """
        design = designs.DesignPlanar()
        try:
            QQ3DRenderer(design, initiate=False)
        except Exception:
            self.fail("QQ3DRenderer failed")

    def test_renderer_instantiate_qhfss_renderer(self):
        """
        Test instantiation of QHFSSRenderer in q3d_render.py.
        """
        design = designs.DesignPlanar()
        try:
            QHFSSRenderer(design, initiate=False)
        except Exception:
            self.fail("QHFSSRenderer failed")

    def test_renderer_qq3d_render_options(self):
        """
        Test that defaults in QQ3DRenderer were not accidentally changed.
        """
        design = designs.DesignPlanar()
        renderer = QQ3DRenderer(design, initiate=False)
        options = renderer.q3d_options

        self.assertEqual(renderer.name, 'q3d')

        self.assertEqual(len(options), 4)
        self.assertEqual(len(options['add_setup']), 12)
        self.assertEqual(len(options['get_capacitance_matrix']), 3)
        self.assertEqual(options['material_type'], 'pec')
        self.assertEqual(options['material_thickness'], '200nm')

        self.assertEqual(options['add_setup']['freq_ghz'], '5.0')
        self.assertEqual(options['add_setup']['name'], 'Setup')
        self.assertEqual(options['add_setup']['save_fields'], 'False')
        self.assertEqual(options['add_setup']['enabled'], 'True')
        self.assertEqual(options['add_setup']['max_passes'], '15')
        self.assertEqual(options['add_setup']['min_passes'], '2')
        self.assertEqual(options['add_setup']['min_converged_passes'], '2')
        self.assertEqual(options['add_setup']['percent_error'], '0.5')
        self.assertEqual(options['add_setup']['percent_refinement'], '30')
        self.assertEqual(options['add_setup']['auto_increase_solution_order'],
                         'True')
        self.assertEqual(options['add_setup']['solution_order'], 'High')
        self.assertEqual(options['add_setup']['solver_type'], 'Iterative')

        self.assertEqual(options['get_capacitance_matrix']['variation'], '')
        self.assertEqual(options['get_capacitance_matrix']['solution_kind'],
                         'AdaptivePass')
        self.assertEqual(options['get_capacitance_matrix']['pass_number'], '3')

    def test_renderer_hfss_render_options(self):
        """
        Test that defaults in QHFSSRender were not accidentally changed.
        """
        design = designs.DesignPlanar()
        renderer = QHFSSRenderer(design, initiate=False)
        options = renderer.hfss_options

        self.assertEqual(renderer.name, 'hfss')
        self.assertEqual(len(options), 3)
        self.assertEqual(len(options['drivenmodal_setup']), 8)
        self.assertEqual(len(options['eigenmode_setup']), 9)
        self.assertEqual(options['port_inductor_gap'], '10um')

        self.assertEqual(options['drivenmodal_setup']['freq_ghz'], '5')
        self.assertEqual(options['drivenmodal_setup']['name'], "Setup")
        self.assertEqual(options['drivenmodal_setup']['max_delta_s'], '0.1')
        self.assertEqual(options['drivenmodal_setup']['max_passes'], '10')
        self.assertEqual(options['drivenmodal_setup']['min_passes'], '1')
        self.assertEqual(options['drivenmodal_setup']['min_converged'], '1')
        self.assertEqual(options['drivenmodal_setup']['pct_refinement'], '30')
        self.assertEqual(options['drivenmodal_setup']['basis_order'], '1')

        self.assertEqual(options['eigenmode_setup']['name'], "Setup")
        self.assertEqual(options['eigenmode_setup']['min_freq_ghz'], '1')
        self.assertEqual(options['eigenmode_setup']['n_modes'], '1')
        self.assertEqual(options['eigenmode_setup']['max_delta_f'], '0.5')
        self.assertEqual(options['eigenmode_setup']['max_passes'], '10')
        self.assertEqual(options['eigenmode_setup']['min_passes'], '1')
        self.assertEqual(options['eigenmode_setup']['min_converged'], '1')
        self.assertEqual(options['eigenmode_setup']['pct_refinement'], '30')
        self.assertEqual(options['eigenmode_setup']['basis_order'], '-1')

    def test_renderer_gdsrenderer_options(self):
        """
        Test that default_options in QGDSRenderer were not accidentally changed.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)
        options = renderer.default_options

        self.assertEqual(len(options), 15)
        self.assertEqual(options['short_segments_to_not_fillet'], 'True')
        self.assertEqual(options['check_short_segments_by_scaling_fillet'],
                         '2.0')
        self.assertEqual(options['gds_unit'], '1')
        self.assertEqual(options['ground_plane'], 'True')
        self.assertEqual(options['corners'], 'circular bend')
        self.assertEqual(options['tolerance'], '0.00001')
        self.assertEqual(options['precision'], '0.000000001')
        self.assertEqual(options['width_LineString'], '10um')
        self.assertEqual(options['path_filename'],
                         '../resources/Fake_Junctions.GDS')
        self.assertEqual(options['junction_pad_overlap'], '5um')
        self.assertEqual(options['max_points'], '199')
        self.assertEqual(options['bounding_box_scale_x'], '1.2')
        self.assertEqual(options['bounding_box_scale_y'], '1.2')

        self.assertEqual(len(options['cheese']), 9)
        self.assertEqual(len(options['no_cheese']), 5)

        self.assertEqual(options['cheese']['datatype'], '100')
        self.assertEqual(options['cheese']['shape'], '0')
        self.assertEqual(options['cheese']['cheese_0_x'], '25um')
        self.assertEqual(options['cheese']['cheese_0_y'], '25um')
        self.assertEqual(options['cheese']['cheese_1_radius'], '100um')
        self.assertEqual(options['cheese']['delta_x'], '100um')
        self.assertEqual(options['cheese']['delta_y'], '100um')
        self.assertEqual(options['cheese']['edge_nocheese'], '200um')

        self.assertEqual(options['no_cheese']['datatype'], '99')
        self.assertEqual(options['no_cheese']['buffer'], '25um')
        self.assertEqual(options['no_cheese']['cap_style'], '2')
        self.assertEqual(options['no_cheese']['join_style'], '2')

        self.assertEqual(len(options['cheese']['view_in_file']), 1)
        self.assertEqual(len(options['cheese']['view_in_file']['main']), 1)
        self.assertEqual(options['cheese']['view_in_file']['main'][1], True)

        self.assertEqual(len(options['no_cheese']['view_in_file']), 1)
        self.assertEqual(len(options['no_cheese']['view_in_file']['main']), 1)
        self.assertEqual(options['no_cheese']['view_in_file']['main'][1], True)

    def test_renderer_gdsrenderer_inclusive_bound(self):
        """
        Test functionality of inclusive_bound in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)

        my_list = []
        my_list.append([1, 1, 2, 2])
        my_list.append([3, 3, 5, 5])
        my_list.append([2.2, 2.3, 4.4, 4.9])
        self.assertEqual(renderer.inclusive_bound(my_list), (1, 1, 5, 5))

    def test_renderer_scale_max_bounds(self):
        """
        Test functionality of scale_max_bounds in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)

        actual = renderer.scale_max_bounds('main', [(1, 1, 3, 3)])
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0], (0.8, 0.8, 3.2, 3.2))
        self.assertEqual(actual[1], (1, 1, 3, 3))

    def test_renderer_get_chip_names(self):
        """
        Test functionality of get_chip_names in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)

        qgt = QGeometryTables(design)
        qgt.clear_all_tables()

        transmon_pocket = TransmonPocket(design, 'my_id')
        transmon_pocket.make()
        transmon_pocket.get_template_options(design)

        a_linestring = draw.LineString([[0, 0], [0, 1]])
        a_poly = draw.rectangle(2, 2, 0, 0)
        qgt.add_qgeometry('path',
                          'my_id', {'n_sprial': a_linestring},
                          width=4000)
        qgt.add_qgeometry('poly',
                          'my_id', {'n_spira_etch': a_poly},
                          subtract=True)

        result = renderer.get_chip_names()
        self.assertEqual(result, {'main': {}})

    def test_renderer_setup_renderers(self):
        """
        Test setup_renderers in setup_defauts.py.
        """
        actual = setup_default.setup_renderers()
        self.assertEqual(actual, {})

    def test_renderer_gdsrenderer_high_level(self):
        """
        Test that high level defaults were not accidentally changed in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)

        self.assertEqual(renderer.name, 'gds')
        element_extensions = renderer.element_extensions
        self.assertEqual(len(element_extensions), 1)
        self.assertEqual(len(element_extensions['junction']), 1)
        self.assertEqual(element_extensions['junction']['cell_name'], str)

    def test_renderer_gdsrenderer_update_units(self):
        """
        Test update_units in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)

        renderer.options['gds_unit'] = 12345
        self.assertEqual(renderer.options['gds_unit'], 12345)

        renderer.update_units()
        self.assertEqual(renderer.options['gds_unit'], 0.001)

    def test_renderer_gdsrenderer_midpoint_xy(self):
        """
        Test midpoint_xy in gds_renderer.py.
        """
        actual = QGDSRenderer.midpoint_xy(10, 15, 20, 30)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0], 15.0)
        self.assertEqual(actual[1], 22.5)

    def test_renderer_gdsrenderer_check_qcomps(self):
        """
        Test check_qcomps in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)

        actual = []
        actual.append(renderer.check_qcomps([]))
        actual.append(renderer.check_qcomps(['Q1', 'Q2', 'Q3']))
        actual.append(renderer.check_qcomps(['Q1', 'Q2', 'Q3', 'Q1']))

        expected = []
        expected.append(([], 0))
        expected.append((['Q2', 'Q3', 'Q1'], 1))
        expected.append((['Q2', 'Q3', 'Q1'], 1))

        for x in range(3):
            my_length = len(actual[x][0])
            self.assertEqual(my_length, len(expected[x][0]))
            self.assertEqual(actual[x][1], expected[x][1])

            # note order is not guarenteed - fix this
            # for y in range(my_length):
            #self.assertEqual(actual[x][0][y], expected[x][0][y])

    def test_renderer_mpl_interaction_disconnect(self):
        """
        Test disconnect in MplInteraction in mpl_interaction.py.
        """
        mpl = MplInteraction(_plt)
        mpl.disconnect()
        self.assertEqual(mpl.figure, None)

    def test_renderer_gds_check_cheese(self):
        """
        Test check_cheese in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)

        self.assertEqual(renderer.check_cheese('main', 0), 4)
        self.assertEqual(renderer.check_cheese('main', 1), 1)
        self.assertEqual(renderer.check_cheese('fake', 0), 3)

    def test_renderer_gds_check_no_cheese(self):
        """
        Test check_no_cheese in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)

        self.assertEqual(renderer.check_no_cheese('main', 0), 4)
        self.assertEqual(renderer.check_no_cheese('main', 1), 1)
        self.assertEqual(renderer.check_no_cheese('fake', 0), 3)

    def test_renderer_gds_check_either_cheese(self):
        """
        Test check_either_cheese in gds_renderer.py.
        """
        design = designs.DesignPlanar()
        renderer = QGDSRenderer(design)

        self.assertEqual(renderer.check_either_cheese('main', 0), 6)
        self.assertEqual(renderer.check_either_cheese('main', 1), 1)
        self.assertEqual(renderer.check_either_cheese('fake', 0), 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
