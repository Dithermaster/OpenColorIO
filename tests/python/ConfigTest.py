# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import unittest
import os
import sys

import PyOpenColorIO as OCIO
from UnitTestUtils import TEST_DATAFILES_DIR, TEST_NAMES, TEST_DESCS

# Legacy tests kept for reference.
#
#class ConfigTest(unittest.TestCase):
#
#    SIMPLE_PROFILE = """ocio_profile_version: 1
#
#search_path: luts
#strictparsing: false
#luma: [0.2126, 0.7152, 0.0722]
#
#roles:
#  default: raw
#  scene_linear: lnh
#
#displays:
#  sRGB:
#    - !<View> {name: Film1D, colorspace: vd8}
#    - !<View> {name: Raw, colorspace: raw}
#
#active_displays: []
#active_views: []
#
#colorspaces:
#  - !<ColorSpace>
#    name: raw
#    family: raw
#    equalitygroup: ""
#    bitdepth: 32f
#    description: |
#      A raw color space. Conversions to and from this space are no-ops.
#
#    isdata: true
#    allocation: uniform
#
#  - !<ColorSpace>
#    name: lnh
#    family: ln
#    equalitygroup: ""
#    bitdepth: 16f
#    description: |
#      The show reference space. This is a sensor referred linear
#      representation of the scene with primaries that correspond to
#      scanned film. 0.18 in this space corresponds to a properly
#      exposed 18% grey card.
#
#    isdata: false
#    allocation: lg2
#
#  - !<ColorSpace>
#    name: vd8
#    family: vd8
#    equalitygroup: ""
#    bitdepth: 8ui
#    description: |
#      how many transforms can we use?
#
#    isdata: false
#    allocation: uniform
#    to_reference: !<GroupTransform>
#      children:
#        - !<ExponentTransform> {value: 2.2}
#        - !<MatrixTransform> {matrix: [1, 2, 3, 4, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], offset: [1, 2, 0, 0]}
#        - !<CDLTransform> {slope: [0.9, 1, 1], offset: [0.1, 0.3, 0.4], power: [1.1, 1.1, 1.1], sat: 0.9}
#"""
#
#    def setUp(self):
#
#        osx_hack = ''
#        if osname=="Darwin":
#            osx_hack = """
#// OSX segfault work-around: Force a no-op sampling of the 3D LUT.
#texture3D(lut3d, 0.96875 * out_pixel.rgb + 0.015625).rgb;"""
#
#        self.GLSLResult = """
#// Generated by OpenColorIO
#
#vec4 pytestocio(in vec4 inPixel,
#    const sampler3D lut3d)
#{
#vec4 out_pixel = inPixel;
#out_pixel = out_pixel * mat4(1.0874889, -0.079466686, -0.0080222245, 0., -0.023622228, 1.0316445, -0.0080222245, 0., -0.023622226, -0.079466686, 1.1030889, 0., 0., 0., 0., 1.);
#out_pixel = pow(max(out_pixel, vec4(0., 0., 0., 0.)), vec4(0.90909088, 0.90909088, 0.90909088, 1.));
#out_pixel = out_pixel * mat4(1.1111112, -2., -3., -4., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1.);
#out_pixel = vec4(4.688889, -2.3, -0.40000001, -0.) + out_pixel;
#out_pixel = pow(max(out_pixel, vec4(0., 0., 0., 0.)), vec4(0.45454544, 0.45454544, 0.45454544, 1.));""" \
# + osx_hack + \
#"""
#return out_pixel;
#}
#
#"""
#
#    def test_is_editable(self):
#
#        cfg = OCIO.Config().CreateFromStream(self.SIMPLE_PROFILE)
#        self.assertEqual(cfg.isEditable(), False)
#        cfg = cfg.createEditableCopy()
#        self.assertEqual(cfg.isEditable(), True)
#        ctx = cfg.getCurrentContext()
#        self.assertEqual(ctx.isEditable(), False)
#        ctx = ctx.createEditableCopy()
#        self.assertEqual(ctx.isEditable(), True)
#        ctx.setEnvironmentMode(OCIO.ENV_ENVIRONMENT_LOAD_ALL)
#
#    def test_interface(self):
#
#        _cfge = OCIO.Config().CreateFromStream(self.SIMPLE_PROFILE)
#        _cfge.clearEnvironmentVars()
#        self.assertEqual(0, _cfge.getNumEnvironmentVars())
#        _cfge.addEnvironmentVar("FOO", "test1")
#        _cfge.addEnvironmentVar("FOO2", "test2${FOO}")
#        self.assertEqual(2, _cfge.getNumEnvironmentVars())
#        self.assertEqual("FOO", _cfge.getEnvironmentVarNameByIndex(0))
#        self.assertEqual("FOO2", _cfge.getEnvironmentVarNameByIndex(1))
#        self.assertEqual("test1", _cfge.getEnvironmentVarDefault("FOO"))
#        self.assertEqual("test2${FOO}", _cfge.getEnvironmentVarDefault("FOO2"))
#        self.assertEqual("test2test1", _cfge.getCurrentContext().resolveStringVar("${FOO2}"))
#        self.assertEqual({'FOO': 'test1', 'FOO2': 'test2${FOO}'}, _cfge.getEnvironmentVarDefaults())
#        _cfge.clearEnvironmentVars()
#        self.assertEqual(0, _cfge.getNumEnvironmentVars())
#        self.assertEqual("luts", _cfge.getSearchPath())
#        _cfge.setSearchPath("otherdir")
#        self.assertEqual("otherdir", _cfge.getSearchPath())
#        _cfge.validate()
#        _cfge.setDescription("testdesc")
#        self.assertEqual("testdesc", _cfge.getDescription())
#        self.assertEqual(self.SIMPLE_PROFILE, _cfg.serialize())
#        #self.assertEqual("$07d1fb1509eeae1837825fd4242f8a69:$885ad1683add38a11f7bbe34e8bf9ac0",
#        #                _cfg.getCacheID())
#        con = _cfge.getCurrentContext()
#        self.assertNotEqual(0, con.getNumStringVars())
#        _cfge.setWorkingDir("/foobar")
#        self.assertEqual("/foobar", _cfge.getWorkingDir())
#        self.assertEqual(3, _cfge.getNumColorSpaces())
#        self.assertEqual("lnh", _cfge.getColorSpaceNameByIndex(1))
#        lnh = _cfge.getColorSpace("lnh")
#        self.assertEqual("ln", lnh.getFamily())
#        self.assertEqual(-1, _cfge.getIndexForColorSpace("foobar"))
#        cs = OCIO.ColorSpace()
#        cs.setName("blah")
#        _cfge.addColorSpace(cs)
#        self.assertEqual(3, _cfge.getIndexForColorSpace("blah"))
#        #_cfge.clearColorSpaces()
#        #_cfge.parseColorSpaceFromString("foo")
#        self.assertEqual(False, _cfg.isStrictParsingEnabled())
#        _cfge.setStrictParsingEnabled(True)
#        self.assertEqual(True, _cfge.isStrictParsingEnabled())
#        self.assertEqual(2, _cfge.getNumRoles())
#        self.assertEqual(False, _cfg.hasRole("foo"))
#        _cfge.setRole("foo", "vd8")
#        self.assertEqual(3, _cfge.getNumRoles())
#        self.assertEqual(True, _cfge.hasRole("foo"))
#        self.assertEqual("foo", _cfge.getRoleName(1))
#        self.assertEqual("sRGB", _cfge.getDefaultDisplay())
#        self.assertEqual(1, _cfge.getNumDisplays())
#        self.assertEqual("sRGB", _cfge.getDisplay(0))
#        self.assertEqual("Film1D", _cfge.getDefaultView("sRGB"))
#        self.assertEqual(2, _cfge.getNumViews("sRGB"))
#        self.assertEqual("Raw", _cfge.getView("sRGB", 1))
#        self.assertEqual("vd8", _cfge.getDisplayColorSpaceName("sRGB", "Film1D"))
#        self.assertEqual("", _cfg.getDisplayLooks("sRGB", "Film1D"))
#        _cfge.addDisplay("foo", "bar", "foo", "wee")
#        _cfge.clearDisplays()
#        _cfge.setActiveDisplays("sRGB")
#        self.assertEqual("sRGB", _cfge.getActiveDisplays())
#        _cfge.setActiveViews("Film1D")
#        self.assertEqual("Film1D", _cfge.getActiveViews())
#        luma = _cfge.getDefaultLumaCoefs()
#        self.assertAlmostEqual(0.2126, luma[0], delta=1e-8)
#        _cfge.setDefaultLumaCoefs([0.1, 0.2, 0.3])
#        tnewluma = _cfge.getDefaultLumaCoefs()
#        self.assertAlmostEqual(0.1, tnewluma[0], delta=1e-8)
#        self.assertEqual(0, _cfge.getNumLooks())
#        lk = OCIO.Look()
#        lk.setName("coollook")
#        lk.setProcessSpace("somespace")
#        et = OCIO.ExponentTransform()
#        et.setValue([0.1, 0.2, 0.3, 0.4])
#        lk.setTransform(et)
#        iet = OCIO.ExponentTransform()
#        iet.setValue([-0.1, -0.2, -0.3, -0.4])
#        lk.setInverseTransform(iet)
#        _cfge.addLook(lk)
#        self.assertEqual(1, _cfge.getNumLooks())
#        self.assertEqual("coollook", _cfge.getLookNameByIndex(0))
#        glk = _cfge.getLook("coollook")
#        self.assertEqual("somespace", glk.getProcessSpace())
#        _cfge.clearLooks()
#        self.assertEqual(0, _cfge.getNumLooks())
#
#        #getProcessor(context, srcColorSpace, dstColorSpace)
#        #getProcessor(context, srcName,dstName);
#        #getProcessor(transform);
#        #getProcessor(transform, direction);
#        #getProcessor(context, transform, direction);
#
#        _proc = _cfg.getProcessor("lnh", "vd8")
#        self.assertEqual(False, _proc.isNoOp())
#        self.assertEqual(True, _proc.hasChannelCrosstalk())
#
#        #float packedpix[] = new float[]{0.48f, 0.18f, 0.9f, 1.0f,
#        #                                0.48f, 0.18f, 0.18f, 1.0f,
#        #                                0.48f, 0.18f, 0.18f, 1.0f,
#        #                                0.48f, 0.18f, 0.18f, 1.0f };
#        #FloatBuffer buf = ByteBuffer.allocateDirect(2 * 2 * 4 * Float.SIZE / 8).asFloatBuffer();
#        #buf.put(packedpix);
#        #PackedImageDesc foo = new PackedImageDesc(buf, 2, 2, 4);
#        #_proc.apply(foo);
#        #FloatBuffer wee = foo.getData();
#        #self.assertEqual(-2.4307251581696764E-35f, wee.get(2), 1e-8);
#
#        # TODO: these should work in-place
#        rgbfoo = _proc.applyRGB([0.48, 0.18, 0.18])
#        self.assertAlmostEqual(1.9351077, rgbfoo[0], delta=1e-7);
#        # TODO: these should work in-place
#        rgbafoo = _proc.applyRGBA([0.48, 0.18, 0.18, 1.0])
#        self.assertAlmostEqual(1.0, rgbafoo[3], delta=1e-8)
#        #self.assertEqual("$a92ef63abd9edf61ad5a7855da064648", _proc.getCpuCacheID())
#
#        _cfge.clearSearchPaths()
#        self.assertEqual(0, _cfge.getNumSearchPaths())
#        _cfge.addSearchPath("First/ Path")
#        self.assertEqual(1, _cfge.getNumSearchPaths())
#        _cfge.addSearchPath("D:\\Second\\Path\\")
#        self.assertEqual(2, _cfge.getNumSearchPaths())
#        self.assertEqual("First/ Path", _cfge.getSearchPathByIndex(0))
#        self.assertEqual("D:\\Second\\Path\\", _cfge.getSearchPathByIndex(1))
#
#        del _cfge
#        del _cfg

class ConfigTest(unittest.TestCase):

    def test_shared_views(self):
        # Test these Config functions: addSharedView, getSharedViews, removeSharedView.

        cfg = OCIO.Config().CreateRaw()
        views = cfg.getSharedViews()
        self.assertEqual(0, len(views))

        # Shared view has to have a name.
        with self.assertRaises(OCIO.Exception):
            cfg.addSharedView(view='',
                              viewTransformName='',
                              colorSpaceName='c1',
                              looks='',
                              ruleName='',
                              description='')
        # Shared view has to have a color space name.
        with self.assertRaises(OCIO.Exception):
            cfg.addSharedView(view='view1',
                              viewTransformName='',
                              colorSpaceName='',
                              looks='',
                              ruleName='',
                              description='')
        cfg.addSharedView(view='view1',
                          viewTransformName='',
                          colorSpaceName='c1',
                          looks='',
                          ruleName='',
                          description='')
        cfg.addSharedView(view='view2',
                          colorSpaceName='c2',
                          viewTransformName='t2',
                          looks='',
                          ruleName='',
                          description='')
        cfg.addSharedView(view='view3',
                          colorSpaceName='c3',
                          looks='l3',
                          viewTransformName='',
                          ruleName='',
                          description='')
        cfg.addSharedView(view='view4',
                          colorSpaceName='c4',
                          ruleName='r4',
                          looks='',
                          viewTransformName='',
                          description='')
        cfg.addSharedView(view='view5',
                          colorSpaceName='c5',
                          ruleName='',
                          looks='',
                          viewTransformName='',
                          description='description 5')
        cfg.addSharedView('view6', 't6', 'c6', 'l6','r6', 'desc6')
        views = cfg.getSharedViews()
        self.assertEqual(6, len(views))
        self.assertEqual('view1', next(views))
        self.assertEqual('view2', next(views))
        self.assertEqual('view3', next(views))
        self.assertEqual('view4', next(views))
        self.assertEqual('view5', next(views))
        self.assertEqual('view6', next(views))

        self.assertEqual('',   cfg.getDisplayViewTransformName('', 'view1'))
        self.assertEqual('t2', cfg.getDisplayViewTransformName('', 'view2'))
        self.assertEqual('',   cfg.getDisplayViewTransformName('', 'view3'))
        self.assertEqual('',   cfg.getDisplayViewTransformName('', 'view4'))
        self.assertEqual('',   cfg.getDisplayViewTransformName('', 'view5'))
        self.assertEqual('t6', cfg.getDisplayViewTransformName('', 'view6'))

        self.assertEqual('c1', cfg.getDisplayViewColorSpaceName('', 'view1'))
        self.assertEqual('c2', cfg.getDisplayViewColorSpaceName('', 'view2'))
        self.assertEqual('c3', cfg.getDisplayViewColorSpaceName('', 'view3'))
        self.assertEqual('c4', cfg.getDisplayViewColorSpaceName('', 'view4'))
        self.assertEqual('c5', cfg.getDisplayViewColorSpaceName('', 'view5'))
        self.assertEqual('c6', cfg.getDisplayViewColorSpaceName('', 'view6'))

        self.assertEqual('',   cfg.getDisplayViewLooks('', 'view1'))
        self.assertEqual('',   cfg.getDisplayViewLooks('', 'view2'))
        self.assertEqual('l3', cfg.getDisplayViewLooks('', 'view3'))
        self.assertEqual('',   cfg.getDisplayViewLooks('', 'view4'))
        self.assertEqual('',   cfg.getDisplayViewLooks('', 'view5'))
        self.assertEqual('l6', cfg.getDisplayViewLooks('', 'view6'))

        self.assertEqual('',   cfg.getDisplayViewRule('', 'view1'))
        self.assertEqual('',   cfg.getDisplayViewRule('', 'view2'))
        self.assertEqual('',   cfg.getDisplayViewRule('', 'view3'))
        self.assertEqual('r4', cfg.getDisplayViewRule('', 'view4'))
        self.assertEqual('',   cfg.getDisplayViewRule('', 'view5'))
        self.assertEqual('r6', cfg.getDisplayViewRule('', 'view6'))

        self.assertEqual('', cfg.getDisplayViewDescription('', 'view1'))
        self.assertEqual('', cfg.getDisplayViewDescription('', 'view2'))
        self.assertEqual('', cfg.getDisplayViewDescription('', 'view3'))
        self.assertEqual('', cfg.getDisplayViewDescription('', 'view4'))
        self.assertEqual('description 5', cfg.getDisplayViewDescription('', 'view5'))
        self.assertEqual('desc6', cfg.getDisplayViewDescription('', 'view6'))

        # Adding a shared view using an existing name is replacing the existing view.
        cfg.addSharedView(view='view3',
                          colorSpaceName='c3 new',
                          looks='l3 new',
                          viewTransformName='t3 new',
                          ruleName='r3 new',
                          description='desc3 new')
        views = cfg.getSharedViews()
        self.assertEqual(6, len(views))
        self.assertEqual('t3 new',   cfg.getDisplayViewTransformName('', 'view3'))
        self.assertEqual('c3 new', cfg.getDisplayViewColorSpaceName('', 'view3'))
        self.assertEqual('l3 new', cfg.getDisplayViewLooks('', 'view3'))
        self.assertEqual('r3 new',   cfg.getDisplayViewRule('', 'view3'))
        self.assertEqual('desc3 new', cfg.getDisplayViewDescription('', 'view3'))

        # Remove shared views.

        # View has to exist.
        with self.assertRaises(OCIO.Exception):
            cfg.removeSharedView('unknown view')

        # Existing views can be removed.
        cfg.removeSharedView('view3')
        views = cfg.getSharedViews()
        self.assertEqual(5, len(views))
        cfg.removeSharedView('view4')
        cfg.removeSharedView('view5')
        cfg.removeSharedView('view6')
        cfg.removeSharedView('view1')
        cfg.removeSharedView('view2')
        views = cfg.getSharedViews()
        self.assertEqual(0, len(views))

    def test_ruled_views(self):
        # Test these Config functions: getDisplays, getViews, removeDisplayView

        SIMPLE_PROFILE = """ocio_profile_version: 2

search_path: ""
strictparsing: true
luma: [0.2126, 0.7152, 0.0722]

roles:
  default: raw
  scene_linear: c3

file_rules:
  - !<Rule> {name: ColorSpaceNamePathSearch}
  - !<Rule> {name: Default, colorspace: raw}

viewing_rules:
  - !<Rule> {name: Rule_1, colorspaces: c1}
  - !<Rule> {name: Rule_2, colorspaces: [c2, c3]}
  - !<Rule> {name: Rule_3, colorspaces: scene_linear}
  - !<Rule> {name: Rule_4, colorspaces: [c3, c4]}
  - !<Rule> {name: Rule_5, encodings: log}
  - !<Rule> {name: Rule_6, encodings: [log, video]}

shared_views:
  - !<View> {name: SView_a, colorspace: raw, rule: Rule_2}
  - !<View> {name: SView_b, colorspace: raw, rule: Rule_3}
  - !<View> {name: SView_c, colorspace: raw}
  - !<View> {name: SView_d, colorspace: raw, rule: Rule_5}
  - !<View> {name: SView_e, colorspace: raw}

displays:
  sRGB:
    - !<View> {name: View_a, colorspace: raw, rule: Rule_1}
    - !<View> {name: View_b, colorspace: raw, rule: Rule_2}
    - !<View> {name: View_c, colorspace: raw, rule: Rule_2}
    - !<View> {name: View_d, colorspace: raw, rule: Rule_3}
    - !<View> {name: View_e, colorspace: raw, rule: Rule_4}
    - !<View> {name: View_f, colorspace: raw, rule: Rule_5}
    - !<View> {name: View_g, colorspace: raw, rule: Rule_6}
    - !<View> {name: View_h, colorspace: raw}
    - !<Views> [SView_a, SView_b, SView_d, SView_e]

active_displays: []
active_views: []

colorspaces:
  - !<ColorSpace>
    name: raw
    family: ""
    equalitygroup: ""
    bitdepth: unknown
    isdata: false
    allocation: uniform

  - !<ColorSpace>
    name: c1
    family: ""
    equalitygroup: ""
    bitdepth: unknown
    isdata: false
    encoding: video
    allocation: uniform

  - !<ColorSpace>
    name: c2
    family: ""
    equalitygroup: ""
    bitdepth: unknown
    isdata: false
    allocation: uniform

  - !<ColorSpace>
    name: c3
    family: ""
    equalitygroup: ""
    bitdepth: unknown
    isdata: false
    allocation: uniform

  - !<ColorSpace>
    name: c4
    family: ""
    equalitygroup: ""
    bitdepth: unknown
    isdata: false
    encoding: log
    allocation: uniform

  - !<ColorSpace>
    name: c5
    family: ""
    equalitygroup: ""
    bitdepth: unknown
    isdata: false
    encoding: data
    allocation: uniform

  - !<ColorSpace>
    name: c6
    family: ""
    equalitygroup: ""
    bitdepth: unknown
    isdata: false
    encoding: video
    allocation: uniform
"""
        # Create a config.
        cfg = OCIO.Config().CreateFromStream(SIMPLE_PROFILE)
        # Check number of displays.
        displays = cfg.getDisplays()
        self.assertEqual(1, len(displays))
        # Add a view in a new display.
        cfg.addDisplayView('otherDisplay', 'otherView', 'c6', '')
        # Check there is a new display and check view.
        displays = cfg.getDisplays()
        self.assertEqual(2, len(displays))
        self.assertEqual('sRGB', next(displays))
        self.assertEqual('otherDisplay', next(displays))
        views = cfg.getViews('otherDisplay')
        self.assertEqual(1, len(views))
        self.assertEqual('otherView', next(views))
        # Parameter case does not matter.
        views = cfg.getViews('oTHerdISplay')
        self.assertEqual(1, len(views))
        # Add a shared view to the new display.
        cfg.addDisplaySharedView('otherDisplay', 'SView_a')
        views = cfg.getViews('otherDisplay')
        self.assertEqual(2, len(views))
        self.assertEqual('otherView', next(views))
        self.assertEqual('SView_a', next(views))
        # Remove the views (and the display).
        cfg.removeDisplayView('otherDisplay', 'otherView')
        displays = cfg.getDisplays()
        self.assertEqual(2, len(displays))
        cfg.removeDisplayView('otherDisplay', 'SView_a')
        displays = cfg.getDisplays()
        self.assertEqual(1, len(displays))

        # Check shared views defined by config.

        views = cfg.getSharedViews()
        self.assertEqual(5, len(views))
        self.assertEqual('SView_a', next(views))
        self.assertEqual('SView_b', next(views))
        self.assertEqual('SView_c', next(views))
        self.assertEqual('SView_d', next(views))
        self.assertEqual('SView_e', next(views))

        # Check views for sRGB display.

        views = cfg.getViews('sRGB')
        self.assertEqual(12, len(views))

        # Active views are taken into account for getViews.

        cfg.setActiveViews('View_a, View_b, SView_a, SView_b')
        views = cfg.getViews('sRGB')
        self.assertEqual(4, len(views))
        cfg.setActiveViews('')

        # Views filtered by viewing rules.

        views = cfg.getViews('sRGB', 'c3')
        self.assertEqual(8, len(views))
        # View_b rule is Rule_2 that lists c3.
        self.assertEqual('View_b', next(views))
        # View_c rule is Rule_2 that lists c3.
        self.assertEqual('View_c', next(views))
        # View_d rule is Rule_3 that lists c3.
        self.assertEqual('View_d', next(views))
        #/ View_e rule is Rule_4 that lists c3.
        self.assertEqual('View_e', next(views))
        # View_h has no rule.
        self.assertEqual('View_h', next(views))
        # SView_a has rule Rule_2 that lists c3.
        self.assertEqual('SView_a', next(views))
        # SView_b has rule Rule_3 that lists c3.
        self.assertEqual('SView_b', next(views))
        # SView_e has no rule.
        self.assertEqual('SView_e', next(views))

        views = cfg.getViews('sRGB', 'c4')
        self.assertEqual(6, len(views))
        # View_e rule is Rule_4 that lists c4.
        self.assertEqual('View_e', next(views))
        # View_f rule is Rule_5 that lists encoding log, c4 has encoding log.
        self.assertEqual('View_f', next(views))
        # View_g rule is Rule_6 that lists encoding log, c4 has encoding log.
        self.assertEqual('View_g', next(views))
        # View_h has no rule.
        self.assertEqual('View_h', next(views))
        # SView_d rule is Rule_5 that lists encoding log, c4 has encoding log.
        self.assertEqual('SView_d', next(views))
        # SView_e has no rule.
        self.assertEqual('SView_e', next(views))

        views = cfg.getViews('sRGB', 'c6')
        self.assertEqual(3, len(views))
        # View_g rule is Rule_6 that lists encoding video, c6 has encoding video.
        self.assertEqual('View_g', next(views))
        # View_h has no rule.
        self.assertEqual('View_h', next(views))
        # SView_e has no rule.
        self.assertEqual('SView_e', next(views))

    def test_named_transform(self):
        # Test these Config functions: addNamedTransform, getNamedTransforms,
        # getNamedTransformNames, clearNamedTransforms.

        cfg = OCIO.Config().CreateRaw()
        nt_names = cfg.getNamedTransformNames()
        self.assertEqual(0, len(nt_names))
        nts = cfg.getNamedTransforms()
        self.assertEqual(0, len(nts))

        # Add named transform.

        # Missing name.
        nt = OCIO.NamedTransform(forwardTransform = OCIO.RangeTransform())
        with self.assertRaises(OCIO.Exception):
            cfg.addNamedTransform(nt)

        # Missing forward or inverse transform.
        nt = OCIO.NamedTransform(name = "namedTransform")
        with self.assertRaises(OCIO.Exception):
            cfg.addNamedTransform(nt)

        # Legal named transform can be added.
        nt = OCIO.NamedTransform(
            name = "namedTransform",
            forwardTransform = OCIO.RangeTransform())
        cfg.addNamedTransform(nt)

        nt = OCIO.NamedTransform(
            name = "other",
            inverseTransform = OCIO.RangeTransform())
        cfg.addNamedTransform(nt)

        nt_names = cfg.getNamedTransformNames()
        self.assertEqual(2, len(nt_names))
        self.assertEqual('namedTransform', next(nt_names))
        self.assertEqual('other', next(nt_names))

        nts = cfg.getNamedTransforms()
        self.assertEqual(2, len(nts))
        nt = next(nts)
        self.assertEqual('namedTransform', nt.getName())
        cur_tr = nt.getTransform(OCIO.TRANSFORM_DIR_FORWARD)
        self.assertIsInstance(cur_tr, OCIO.RangeTransform)
        cur_tr = nt.getTransform(OCIO.TRANSFORM_DIR_INVERSE)
        self.assertEqual(cur_tr, None)

        nt = next(nts)
        self.assertEqual('other', nt.getName())
        cur_tr = nt.getTransform(OCIO.TRANSFORM_DIR_FORWARD)
        self.assertEqual(cur_tr, None)
        cur_tr = nt.getTransform(OCIO.TRANSFORM_DIR_INVERSE)
        self.assertIsInstance(cur_tr, OCIO.RangeTransform)

        nts = cfg.getNamedTransforms()
        self.assertEqual(2, len(nts))

        cfg.clearNamedTransforms()
        nts = cfg.getNamedTransforms()
        self.assertEqual(0, len(nts))

    def test_inactive_named_transform(self):
        # Test the active/inactive version of these Config functions and classes: getNamedTransforms,
        # getNamedTransformNames, NamedTransformIterator, NamedTransformNameIterator.

        cfg = OCIO.Config().CreateRaw()
        nt_names = cfg.getNamedTransformNames()
        self.assertEqual(0, len(nt_names))
        nts = cfg.getNamedTransforms()
        self.assertEqual(0, len(nts))

        # Add named transforms.

        nt = OCIO.NamedTransform(
            name = "nt1",
            forwardTransform = OCIO.RangeTransform())
        cfg.addNamedTransform(nt)

        nt = OCIO.NamedTransform(
            name = "nt2",
            inverseTransform = OCIO.RangeTransform())
        cfg.addNamedTransform(nt)

        nt = OCIO.NamedTransform(
            name = "nt3",
            forwardTransform = OCIO.RangeTransform())
        cfg.addNamedTransform(nt)

        cfg.setInactiveColorSpaces("nt2")

        # Check the list of active/inactive named transforms.

        nt_names = cfg.getNamedTransformNames()
        self.assertEqual(2, len(nt_names))
        self.assertEqual('nt1', next(nt_names))
        self.assertEqual('nt3', next(nt_names))

        nts = cfg.getNamedTransforms()
        self.assertEqual(2, len(nts))
        nt = next(nts)
        self.assertEqual('nt1', nt.getName())
        nt = next(nts)
        self.assertEqual('nt3', nt.getName())

        nt_names = cfg.getNamedTransformNames(OCIO.NAMEDTRANSFORM_ACTIVE)
        self.assertEqual(2, len(nt_names))
        self.assertEqual('nt1', next(nt_names))
        self.assertEqual('nt3', next(nt_names))

        nts = cfg.getNamedTransforms(OCIO.NAMEDTRANSFORM_ACTIVE)
        self.assertEqual(2, len(nts))
        nt = next(nts)
        self.assertEqual('nt1', nt.getName())
        nt = next(nts)
        self.assertEqual('nt3', nt.getName())

        nt_names = cfg.getNamedTransformNames(OCIO.NAMEDTRANSFORM_ALL)
        self.assertEqual(3, len(nt_names))
        self.assertEqual('nt1', next(nt_names))
        self.assertEqual('nt2', next(nt_names))
        self.assertEqual('nt3', next(nt_names))

        nts = cfg.getNamedTransforms(OCIO.NAMEDTRANSFORM_ALL)
        self.assertEqual(3, len(nts))
        nt = next(nts)
        self.assertEqual('nt1', nt.getName())
        nt = next(nts)
        self.assertEqual('nt2', nt.getName())
        nt = next(nts)
        self.assertEqual('nt3', nt.getName())

        nt_names = cfg.getNamedTransformNames(OCIO.NAMEDTRANSFORM_INACTIVE)
        self.assertEqual(1, len(nt_names))
        self.assertEqual('nt2', next(nt_names))

        nts = cfg.getNamedTransforms(OCIO.NAMEDTRANSFORM_INACTIVE)
        self.assertEqual(1, len(nts))
        nt = next(nts)
        self.assertEqual('nt2', nt.getName())

        cfg.clearNamedTransforms()
        nts = cfg.getNamedTransforms(OCIO.NAMEDTRANSFORM_ALL)
        self.assertEqual(0, len(nts))

    def test_canonical_name(self):
        # Test these Config function: getCanonicalName.

        cfg = OCIO.Config().CreateRaw()

        # add a named transform and a color space.

        nt = OCIO.NamedTransform(
            name = 'nt1',
            aliases = ['alias1', 'test1'],
            forwardTransform = OCIO.RangeTransform())
        cfg.addNamedTransform(nt)
        cs = OCIO.ColorSpace(
            name = 'cs1',
            aliases = ['cs test', 'other'])
        cs.setTransform(OCIO.RangeTransform(), OCIO.COLORSPACE_DIR_TO_REFERENCE)
        cfg.addColorSpace(cs)
        cfg.setRole('role', 'cs1')

        self.assertEqual(cfg.getCanonicalName(''), '')
        self.assertEqual(cfg.getCanonicalName('not found'), '')
        self.assertEqual(cfg.getCanonicalName('roLE'), 'cs1')
        self.assertEqual(cfg.getCanonicalName('CS1'), 'cs1')
        self.assertEqual(cfg.getCanonicalName('Other'), 'cs1')
        self.assertEqual(cfg.getCanonicalName('CS test'), 'cs1')
        self.assertEqual(cfg.getCanonicalName('NT1'), 'nt1')
        self.assertEqual(cfg.getCanonicalName('Alias1'), 'nt1')
        self.assertEqual(cfg.getCanonicalName('Test1'), 'nt1')

    def test_virtual_display(self):
        # Test platform agnostic virtual display interface.

        cfg = OCIO.Config().CreateRaw()
        cfg.addColorSpace(
            OCIO.ColorSpace(OCIO.REFERENCE_SPACE_DISPLAY,
                            "display_cs",
                            toReference=OCIO.CDLTransform(sat=1.5)))
        cfg.addColorSpace(
            OCIO.ColorSpace(OCIO.REFERENCE_SPACE_SCENE,
                            "raw",
                            isData=True))
        cfg.addViewTransform(
            OCIO.ViewTransform(OCIO.REFERENCE_SPACE_SCENE,
                               "default_vt",
                               toReference=OCIO.CDLTransform(sat=1.5)))
        cfg.addViewTransform(
            OCIO.ViewTransform(OCIO.REFERENCE_SPACE_DISPLAY,
                               "display_vt",
                               toReference=OCIO.CDLTransform(sat=1.5)))
        cfg.addDisplayView("sRGB", "Raw", "raw")
        cfg.addDisplayView("sRGB", "view", 
                           viewTransform="display_vt", 
                           displayColorSpaceName="display_cs")
        cfg.addSharedView("sview1", "", "raw")
        cfg.addSharedView("sview2", "", "raw")
        cfg.addDisplaySharedView("sRGB", "sview1")

        # Add virtual display and views
        cfg.addVirtualDisplayView("Raw", "", "raw")
        cfg.addVirtualDisplayView("Film", "display_vt", 
                                  OCIO.OCIO_VIEW_USE_DISPLAY_NAME)
        cfg.addVirtualDisplaySharedView("sview2")

        # Some basic checks
        self.assertEqual(3, len(cfg.getViews("sRGB")))
        self.assertEqual(2, len(cfg.getViews(OCIO.VIEW_DISPLAY_DEFINED, 
                                             "sRGB")))
        self.assertEqual(1, len(cfg.getViews(OCIO.VIEW_SHARED, "sRGB")))

        # Validate the virtual display information
        self.assertEqual(
            2, 
            len(cfg.getVirtualDisplayViews(OCIO.VIEW_DISPLAY_DEFINED)))

        view_name = cfg.getVirtualDisplayViews(OCIO.VIEW_DISPLAY_DEFINED)[0]
        self.assertEqual("Raw", view_name)
        self.assertEqual("", cfg.getVirtualDisplayViewTransformName(view_name))
        self.assertEqual("raw", 
                         cfg.getVirtualDisplayViewColorSpaceName(view_name))
        self.assertEqual("", cfg.getVirtualDisplayViewLooks(view_name))
        self.assertEqual("", cfg.getVirtualDisplayViewRule(view_name))
        self.assertEqual("", cfg.getVirtualDisplayViewDescription(view_name))

        view_name = cfg.getVirtualDisplayViews(OCIO.VIEW_DISPLAY_DEFINED)[1]
        self.assertEqual("Film", view_name)
        self.assertEqual("display_vt", 
                         cfg.getVirtualDisplayViewTransformName(view_name))
        self.assertEqual(OCIO.OCIO_VIEW_USE_DISPLAY_NAME, 
                         cfg.getVirtualDisplayViewColorSpaceName(view_name))
        self.assertEqual("", cfg.getVirtualDisplayViewLooks(view_name))
        self.assertEqual("", cfg.getVirtualDisplayViewRule(view_name))
        self.assertEqual("", cfg.getVirtualDisplayViewDescription(view_name))

        self.assertEqual(1, len(cfg.getVirtualDisplayViews(OCIO.VIEW_SHARED)))
        self.assertEqual("sview2", 
                         cfg.getVirtualDisplayViews(OCIO.VIEW_SHARED)[0])

        # Remove a view from the virtual display
        cfg.removeVirtualDisplayView("Raw")

        self.assertEqual(
            1, 
            len(cfg.getVirtualDisplayViews(OCIO.VIEW_DISPLAY_DEFINED)))
        self.assertEqual(
            "Film", 
            cfg.getVirtualDisplayViews(OCIO.VIEW_DISPLAY_DEFINED)[0])

        self.assertEqual(1, len(cfg.getVirtualDisplayViews(OCIO.VIEW_SHARED)))
        self.assertEqual("sview2", 
                         cfg.getVirtualDisplayViews(OCIO.VIEW_SHARED)[0])

        # Remove a shared view from the virtual display
        cfg.removeVirtualDisplayView("sview2")
        self.assertEqual(
            1, 
            len(cfg.getVirtualDisplayViews(OCIO.VIEW_DISPLAY_DEFINED)))
        self.assertEqual(0, len(cfg.getVirtualDisplayViews(OCIO.VIEW_SHARED)))

        cfg.addVirtualDisplaySharedView("sview2")
        self.assertEqual(
            1, 
            len(cfg.getVirtualDisplayViews(OCIO.VIEW_DISPLAY_DEFINED)))
        self.assertEqual(1, len(cfg.getVirtualDisplayViews(OCIO.VIEW_SHARED)))

        # Remove the virtual display
        cfg.clearVirtualDisplay()
        self.assertEqual(
            0, 
            len(cfg.getVirtualDisplayViews(OCIO.VIEW_DISPLAY_DEFINED)))
        self.assertEqual(0, len(cfg.getVirtualDisplayViews(OCIO.VIEW_SHARED)))
