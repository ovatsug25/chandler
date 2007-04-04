#!/usr/bin/env python
#   Copyright (c) 2006-2007 Open Source Applications Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
rt.py -- Run Chandler tests
"""

#
# TODO Add Signal checks so if main program is halted all child programs are killed
#

import sys, os
import string
import glob
import time
import math
from optparse import OptionParser
import build_lib


log         = build_lib.log
failedTests = []

    # When the --ignoreEnv option is used the following
    # list of environment variable names will be deleted

_ignoreEnvNames = [ 'PARCELPATH',
                    'CHANDLERWEBSERVER',
                    'PROFILEDIR',
                    'CREATE',
                    'CHANDLERNOCATCH',
                    'CHANDLERCATCH',
                    'CHANDLERNOSPLASH',
                    'CHANDLERLOGCONFIG',
                    'CHANDLEROFFLINE',
                    'CHANDLERNONEXCLUSIVEREPO',
                    'NOMVCC',
                  ]


def stddev(values):
    """
    Return standard deviation of the values.
    
    See http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance,
    Algorithm III (Knuth) for the variance.
    """
    if len(values) < 2:
        return 0.0
    
    n = 0
    mean = 0.0
    S = 0.0
    
    for x in values:
      n = n + 1
      delta = x - mean
      mean = mean + delta / n
      S = S + delta * (x - mean)
    
    variance = S / (n - 1)

    return math.sqrt(variance)


def parseOptions():
    """
    parse options
    
    >>> options = parseOptions()
    >>> d = eval(str(options))
    >>> keys = d.keys()
    >>> keys.sort()
    >>> for key in keys:
    ...     print key, d[key],
    args [] dryrun False func False funcSuite False help False mode None noEnv False noStop False perf False profile False recorded False selftest True single  tbox False unit False unitSuite False verbose False
    """
    _configItems = {
        'mode':      ('-m', '--mode',               's', None,  'debug or release; by default attempts both'),
        'noStop':    ('-C', '--continue',           'b', False, 'Continue even after test failures'),
        'unit':      ('-u', '--unit',               'b', False, 'unit tests each in own process'),
        'unitSuite': ('-U', '--unitSuite',          'b', False, 'all unit tests in single process'),
        'verbose':   ('-v', '--verbose',            'b', False, 'Verbose output'),
        'funcSuite': ('-f', '--funcSuite',          'b', False, 'Functional test suite'),
        'func':      ('-F', '--func',               'b', False, 'Functional tests each in own process'),
        'perf':      ('-p', '--perf',               'b', False, 'Performance tests'),
        'single':    ('-t', '--test',               's', '',    'Run test(s) (comma separated list)'),
        'noEnv':     ('-i', '--ignoreEnv',          'b', False, 'Ignore environment variables'),
        'help':      ('-H', '',                     'b', False, 'Extended help'),
        'dryrun':    ('-d', '--dryrun',             'b', False, 'Do all of the prep work but do not run any tests'),
        'selftest':  ('',   '--selftest',           'b', False, 'Run self test'),
        'profile':   ('-P', '--profile',            'b', False, 'Profile performance tests with hotshot'),
        'tbox':      ('-T', '--tbox',               'b', False, 'Tinderbox mode'),
        'recorded':  ('-r', '--recordedScript',     'b', False, 'Run the Chandler recorded scripts'),
        #'restored':  ('-R', '--restoredRepository', 'b', False, 'unit tests with restored repository instead of creating new for each test'),
        #'config':    ('-L', '',                     's', None,  'Custom Chandler logging configuration file'),
    }

    # %prog expands to os.path.basename(sys.argv[0])
    usage  = "usage: %prog [options]\n"
    parser = OptionParser(usage=usage, version="%prog")

    for key in _configItems:
        (shortCmd, longCmd, optionType, defaultValue, helpText) = _configItems[key]

        if optionType == 'b':
            parser.add_option(shortCmd,
                              longCmd,
                              dest=key,
                              action='store_true',
                              default=defaultValue,
                              help=helpText)
        else:
            parser.add_option(shortCmd,
                              longCmd,
                              dest=key,
                              default=defaultValue,
                              help=helpText)

    (options, args) = parser.parse_args()
    options.args    = args

    if args:
        implicitSingle = False
        for key in _configItems.keys():
            if getattr(options, key) != _configItems[key][3]:
                break
            implicitSingle = True
        if implicitSingle:
            options.single = ' '.join(args)
            options.args = ''

    return options


def checkOptions(options):
    """
    Sanity check options. Some options may be changed, and some combinations
    will be warned about while some combinations will result in program exit.
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> d = eval(str(options))
    >>> keys = d.keys()
    >>> keys.sort()
    >>> for key in keys:
    ...     print key, d[key],
    args [] chandlerBin ... chandlerHome ... dryrun False func False funcSuite False help False mode None noEnv False noStop False parcelPath tools/QATestScripts/DataFiles perf False profile False profileDir test_profile recorded False runchandler {'debug': '.../debug/RunChandler...', 'release': '.../release/RunChandler...'} runpython {'debug': '.../debug/RunPython...', 'release': '.../release/RunPython...'} selftest True single  tbox False toolsDir tools unit False unitSuite False verbose False
    """
    if options.help:
        print __doc__
        sys.exit(2)

    if options.dryrun:
        options.verbose = True

    if 'CHANDLERHOME' in os.environ:
        options.chandlerHome = os.path.realpath(os.environ['CHANDLERHOME'])
    else:
        options.chandlerHome = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    if 'CHANDLERBIN' in os.environ:
        options.chandlerBin = os.path.realpath(os.environ['CHANDLERBIN'])
    else:
        options.chandlerBin = options.chandlerHome

    options.toolsDir = os.path.join('tools')
    options.parcelPath = os.path.join(options.toolsDir, 'QATestScripts', 'DataFiles')
    options.profileDir = os.path.join('test_profile')

    if not os.path.isdir(options.chandlerBin):
        log('Unable to locate CHANDLERBIN directory', error=True)
        sys.exit(3)

    if options.single and \
       (options.unit or options.unitSuite or options.funcSuite or \
        options.func or options.perf):
        log('Single test run (-t) only allowed by itself', error=True)
        sys.exit(1)

    if options.single:
        newsingle = []
        for single in options.single.split(','):
            if single[-3:] != '.py':
                newsingle.append(single + '.py')
            else:
                newsingle.append(single)
        options.single = ','.join(newsingle)

    options.runpython   = {}
    options.runchandler = {}

    for mode in [ 'debug', 'release' ]:
        if os.name == 'nt' or sys.platform == 'cygwin':
            options.runpython[mode]   = os.path.join(options.chandlerBin, mode, 'RunPython.bat')
            options.runchandler[mode] = os.path.join(options.chandlerBin, mode, 'RunChandler.bat')
        else:
            options.runpython[mode]   = os.path.join(options.chandlerBin, mode, 'RunPython')
            options.runchandler[mode] = os.path.join(options.chandlerBin, mode, 'RunChandler')

    if options.noEnv:
        for item in _ignoreEnvNames:
            try:
                if item in os.environ:
                    os.environ.pop(item)
            except:
                log('Unable to remove "%s" from the environment' % item)


def findTestFiles(searchPath, excludeDirs, includePattern):
    """
    Find test files.
    
    @param searchPath:     The path to search files from.
    @type searchPath:      str
    @param excludeDirs:    Do not search these directories.
    @type excludeDirs:     list
    @param includePattern: Pattern to match files against.
    @type includePattern:  str
    
    >>> findTestFiles('.', [], 'Application.py')
    [...]
    """
    result = []

    for pattern in includePattern.split(','):
        for item in glob.glob(os.path.join(searchPath, pattern)):
            result.append(item)

    for item in os.listdir(searchPath):
        dirname = os.path.join(searchPath, item)

        if os.path.isdir(dirname):
            if item != '.svn' and dirname not in excludeDirs:
                result += findTestFiles(dirname, excludeDirs, includePattern)

    return result


def buildTestList(options, excludeTools=True):
    """
    Build test list from singles or collect all unit tests.
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    
    Find a unit test:
    
    >>> options.single  = 'TestCrypto.py'
    >>> buildTestList(options)
    ['application/tests/TestCrypto.py']
    
    Try to find a functional test:
    
    >>> options.single  = 'TestCreateAccounts.py'
    >>> buildTestList(options)
    []

    Include tools in search:

    >>> buildTestList(options, excludeTools=False)
    ['tools/cats/Functional/TestCreateAccounts.py']
    
    Unit test and perf test:
    
    >>> options.single  = 'TestCrypto.py,PerfLargeDataSharing.py'
    >>> l = buildTestList(options, False)
    >>> l.sort()
    >>> l
    ['application/tests/TestCrypto.py', 'tools/QATestScripts/Performance/PerfLargeDataSharing.py']
    
    Check that we don't look in projects:
    
    >>> options.single  = 'TestI18nAmazon.py'
    >>> buildTestList(options)
    []
    """
    if len(options.single) > 0:
        includePattern = options.single
    else:
        includePattern = 'Test*.py'

    excludeDirs = []
    exclusions  = ['util', 'projects', 'plugins', 'build', 'Chandler.egg-info']

    if excludeTools:
        exclusions.append('tools')

    for item in exclusions:
        excludeDirs.append('%s/%s' % (options.chandlerHome, item))

    for item in [ 'release', 'debug' ]:
        excludeDirs.append('%s/%s' % (options.chandlerBin, item))

    tests = findTestFiles(options.chandlerHome, excludeDirs, includePattern)

    # make all of the test paths relative to chandlerHome
    # this is done to solve in a simple manner the horror that is
    # cygwin running a windows python binary
    result = []
    l      = len(options.chandlerHome) + 1
    for test in tests:
        if test.startswith(options.chandlerHome):
            result.append(test[l:])
        else:
            result.append(test)

    for pattern in includePattern.split(','):
        if pattern in ('startup.py', 'startup_large.py'):
            result.append(pattern[:-3])

    return result


def runSingles(options):
    """
    Run the test(s) specified with the options.single parameter.
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    >>> options.modes   = ['release']
    
    >>> options.single  = 'ThisTestDoesNotExist'
    >>> runSingles(options)
    Test(s) not found
    False
    
    >>> options.modes   = ['release', 'debug']
    >>> options.single  = 'TestCrypto.py'
    >>> runSingles(options)
    /.../release/RunPython... application/tests/TestCrypto.py -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /.../debug/RunPython... application/tests/TestCrypto.py -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    
    >>> options.modes   = ['release']
    >>> options.single  = 'TestCreateAccounts.py'
    >>> runSingles(options)
    /.../RunChandler... --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --chandlerTests=TestCreateAccounts -D2 -M0
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    
    >>> options.single  = 'PerfLargeDataSharing.py'
    >>> runSingles(options)
    /.../RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --catsPerfLog=test_profile/time.log --scriptFile=tools/QATestScripts/Performance/PerfLargeDataSharing.py --restore=test_profile/__repository__.001
    PerfLargeDataSharing.py                           0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    False
    
    >>> options.single  = 'startup_large.py'
    >>> runSingles(options)
    Creating repository for startup time tests
    /.../RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/quit.py --restore=test_profile/__repository__.001
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /...time... --format=%e -o test_profile/time.log .../release/RunChandler --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/end.py
    Startup_with_large_calendar ...
    ...
    False
    
    >>> options.single  = 'TestCrypto.py,TestSchemaAPI.py'
    >>> runSingles(options)
    /.../RunPython... application/tests/TestCrypto.py -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /.../RunPython... application/tests/TestSchemaAPI.py -v
    ...
    """
    failed = False
    tests  = buildTestList(options, False)

    if not tests:
        log('Test(s) not found')
    else:
        for test in tests:
            dirname, name = os.path.split(test)

            if os.path.split(dirname)[1] == 'Functional':
                if runFuncTest(options, name[:-3]):
                    failed = True
            elif name.startswith('Perf'):
                if runPerfTests(options, [test]):
                    failed = True
            elif name in ('startup', 'startup_large'):
                if runPerfTests(options, [name]):
                    failed = True
            else:
                if runUnitTests(options, [test]):
                    failed = True

            if failed and not options.noStop:
                break

    return failed


def runUnitTests(options, testlist=None):
    """
    Locate any unit tests (-u) or any of the named test (-t) and run them
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    >>> options.modes   = ['release']
    
    >>> options.unit    = True
    >>> runUnitTests(options)
    ...
    /.../RunPython... repository/tests/TestMixins.py -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    ...
    False
    
    >>> runUnitTests(options, [])
    No unit tests found to run
    False
    
    >>> options.modes   = ['release', 'debug']
    >>> runUnitTests(options, ['foobar'])
    /.../release/RunPython... foobar -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /.../debug/RunPython... foobar -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    """
    failed = False

    if testlist is None:
        testlist = buildTestList(options)

    if len(testlist) == 0:
        log('No unit tests found to run')
    else:
        for mode in options.modes:
            for test in testlist:
                cmd = [ options.runpython[mode], test ]

                if options.verbose:
                    cmd.append('-v')
                    log(' '.join(cmd))

                if options.dryrun:
                    result = 0
                else:
                    result = build_lib.runCommand(cmd, timeout=600)

                if result != 0:
                    log('***Error exit code=%d' % result)
                    failed = True
                    failedTests.append(test)

                    if not options.noStop:
                        break

                log('- + ' * 15)

            if failed and not options.noStop:
                break

    return failed


def runUnitSuite(options):
    """
    Run all unit tests in a single process
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    >>> options.modes   = ['release', 'debug']
    
    >>> runUnitSuite(options)
    /.../release/RunPython... tools/run_tests.py -v application i18n osaf repository
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /.../debug/RunPython... tools/run_tests.py -v application i18n osaf repository
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    """
    failed = False

    for mode in options.modes:
        cmd = [options.runpython[mode],
               os.path.join('tools', 'run_tests.py')]

        if options.verbose:
            cmd += ['-v']

        cmd += ['application', 'i18n', 'osaf', 'repository']

        if options.verbose:
            log(' '.join(cmd))

        if options.dryrun:
            result = 0
        else:
            result = build_lib.runCommand(cmd, timeout=3600)

        if result != 0:
            log('***Error exit code=%d' % result)
            failed = True
            failedTests.append('unitSuite')

        if failed and not options.noStop:
            break

        log('- + ' * 15)

    return failed


def runPluginTests(options):
    """
    Locate any plugin tests (-u)
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    >>> options.modes   = ['release', 'debug']
    
    >>> runPluginTests(options)
    /.../release/RunPython... setup.py test -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    ...
    /.../debug/RunPython... setup.py test -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    ...
    False
    """
    failed   = False
    testlist = findTestFiles(os.path.join(options.chandlerHome, 'projects'), [], 'setup.py')

    if len(testlist) == 0:
        log('No plugin tests found to run')
    else:
        saveCWD = os.getcwd()
        env     = os.environ.copy()

        try:
            for mode in options.modes:
                for test in testlist:
                    #if [ "$OSTYPE" = "cygwin" ]; then
                    #    C_HOME=`cygpath -aw $C_DIR`
                    #    PARCEL_PATH=`cygpath -awp $PARCELPATH:$C_DIR/plugins`
                    #else
                    #    C_HOME=$C_DIR
                    #    PARCEL_PATH=$PARCELPATH:$C_DIR/plugins
                    #fi
                    #cd `dirname $setup`
                    #PARCELPATH=$PARCEL_PATH CHANDLERHOME=$C_HOME $CHANDLERBIN/$mode/$RUN_PYTHON
                    #   `basename $setup` test 2>&1 | tee $TESTLOG

                    cmd = [ options.runpython[mode], os.path.basename(test), 'test' ]

                    if options.verbose:
                        cmd.append('-v')
                        log(' '.join(cmd))

                    if options.dryrun:
                        result = 0
                    else:
                        os.chdir(os.path.dirname(test))
                        env['PARCELPATH'] = os.path.join('..', '..', 'plugins')

                        result = build_lib.runCommand(cmd, timeout=600, env=env)

                    if result != 0:
                        log('***Error exit code=%d' % result)
                        failed = True
                        failedTests.append(test)

                        if not options.noStop:
                            break

                    log('- + ' * 15)

                if failed and not options.noStop:
                    break
        finally:
            os.chdir(saveCWD)

    return failed


def runFuncTest(options, test='FunctionalTestSuite.py'):
    """
    Run functional test
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    >>> options.modes   = ['release', 'debug']
    
    >>> runFuncTest(options)
    /.../release/RunChandler... --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/cats/Functional/FunctionalTestSuite.py -D2 -M0
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /.../debug/RunChandler... --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/cats/Functional/FunctionalTestSuite.py -D2 -M0
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    
    >>> runFuncTest(options, 'TestCreateAccounts.py')
    /.../release/RunChandler --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --chandlerTests=TestCreateAccounts.py -D2 -M0
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /.../debug/RunChandler --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --chandlerTests=TestCreateAccounts.py -D2 -M0
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    
    >>> options.noStop = True
    >>> runFuncTest(options, 'TestCreateAccounts.py')
    /.../release/RunChandler --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --chandlerTests=TestCreateAccounts.py -F -D2 -M0
    ...
    """
    # $CHANDLERBIN/$mode/$RUN_CHANDLER --create --catch=tests $FORCE_CONT --profileDir="$PC_DIR" --parcelPath="$PP_DIR" --scriptTimeout=720 --scriptFile="$TESTNAME" -D1 -M2 2>&1 | tee $TESTLOG
    failed = False

    for mode in options.modes:
        cmd  = [ options.runchandler[mode],
                 '--create', '--catch=tests',
                 '--profileDir=%s' % options.profileDir,
                 '--parcelPath=%s' % options.parcelPath]

        if test == 'FunctionalTestSuite.py':
            cmd += ['--scriptFile=%s' % os.path.join('tools', 'cats', 'Functional', test)]
            timeout = 1200
        else:
            cmd += ['--chandlerTests=%s' % test]
            timeout = 900

        if options.noStop:
            cmd += [ '-F' ]

        if options.verbose or test != 'FunctionalTestSuite.py':
            cmd += ['-D2', '-M0']
        elif not options.verbose:
            cmd += ['-D1', '-M2']

        if options.verbose:
            log(' '.join(cmd))

        if options.dryrun:
            result = 0
        else:
            result = build_lib.runCommand(cmd, timeout=timeout)

        if result != 0:
            log('***Error exit code=%d' % result)
            failed = True
            failedTests.append(test)

            if not options.noStop:
                break

        log('- + ' * 15)

    return failed


def runFuncTestsSingly(options):
    """
    Run functional tests each in its own process.
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    >>> options.modes   = ['release', 'debug']
    
    >>> runFuncTestsSingly(options)
    /.../release/RunChandler... --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --chandlerTests=TestCreateAccounts -D2 -M0
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /.../debug/RunChandler... --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --chandlerTests=TestCreateAccounts -D2 -M0
    ...
    """
    failed   = False
    testlist = []

    for item in glob.glob(os.path.join('tools', 'cats', 'Functional', 'Test*.py')):
        testlist.append(os.path.split(item)[1][:-3])

    # XXX How to strip disabled tests?

    for test in testlist:
        if runFuncTest(options, test):
            failed = True

        if failed and not options.noStop:
            return failed

    return failed


def runRecordedScripts(options):
    """
    Run recorded script tests
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    >>> options.modes   = ['release', 'debug']
    
    >>> runRecordedScripts(options)
    /.../release/RunPython... Chandler.py --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --recordedTest all
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /.../debug/RunPython... Chandler.py --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --recordedTest all
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    """
    failed = False

    for mode in options.modes:
        cmd  = [ options.runpython[mode], 'Chandler.py',
                 '--create', '--catch=tests',
                 '--profileDir=%s' % options.profileDir,
                 '--parcelPath=%s' % options.parcelPath,
                 '--recordedTest', 'all' ]

        if options.verbose:
            log(' '.join(cmd))

        if options.dryrun:
            result = 0
        else:
            result = build_lib.runCommand(cmd, timeout=1200)

        if result != 0:
            log('***Error exit code=%d' % result)
            failed = True
            failedTests.append('recordedTest all')

            if not options.noStop:
                break

        log('- + ' * 15)

    return failed


def runScriptPerfTests(options, testlist, largeData=False, repeat=1, logger=log):
    """
    Run script performance tests.
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    
    >>> runScriptPerfTests(options, ['foobar'])
    /.../release/RunChandler --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --catsPerfLog=test_profile/time.log --scriptFile=foobar --create
    foobar                                            0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    False
    
    >>> runScriptPerfTests(options, ['foobar'], largeData=True)
    /.../release/RunChandler --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --catsPerfLog=test_profile/time.log --scriptFile=foobar --restore=test_profile/__repository__.001
    foobar                                            0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    False
    
    >>> options.profile = True
    >>> runScriptPerfTests(options, ['foobar.py'])
    /.../release/RunChandler --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --catsPerfLog=test_profile/time.log --scriptFile=foobar.py --catsProfile=test_profile/foobar.hotshot --create
    foobar.py                                         0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    False
    """
    failed = False
    l = len(options.chandlerHome) + 1
    timeLog = os.path.join(options.profileDir, 'time.log')
    if repeat == 1:
        just = 20
    elif repeat == 2:
        just = 13
    else:
        just = 6

    for item in testlist:
        #$CHANDLERBIN/release/$RUN_CHANDLER --create --catch=tests
        #                                   --profileDir="$PC_DIR"
        #                                   --catsPerfLog="$TIME_LOG"
        #                                   --scriptTimeout=600
        #                                   --scriptFile="$TESTNAME" &> $TESTLOG
        if item.startswith(options.chandlerHome):
            item = item[l:]

        name    = item[item.rfind('/') + 1:]

        cmd = [ options.runchandler['release'],
                '--catch=tests',
                '--profileDir=%s'  % options.profileDir,
                '--parcelPath=%s'  % options.parcelPath,
                '--catsPerfLog=%s' % timeLog,
                '--scriptFile=%s'  % item ]

        if options.profile:
            cmd += ['--catsProfile=%s.hotshot' % os.path.join(options.profileDir, name[:-3])]

        if not largeData:
            cmd += ['--create']
        else:
            cmd += ['--restore=%s' % os.path.join(options.profileDir, 
                                                  '__repository__.001')]

        if options.verbose:
            log(' '.join(cmd))
    
        values = []
        log(name.ljust(33), newline=' ')
        
        for _x in range(repeat):
            if not options.dryrun:
                if os.path.isfile(timeLog):
                    os.remove(timeLog)

            if options.dryrun:
                result = 0
            else:
                tempLogger = DelayedLogger()
                result = build_lib.runCommand(cmd, timeout=1800, logger=tempLogger)
    
            if result != 0:
                log('***Error exit code=%d, %s' % (result, name))
                failed = True
                failedTests.append(item)
    
                if not options.noStop:
                    break
            else:
                if options.dryrun:
                    value = 0.00
                else:
                    if os.path.isfile(timeLog):
                        value = float(open(timeLog).readline()[:-1])
                    else:
                        log('timeLog [%s] not found' % timeLog)
                        value = 0.00
                    
                log(('%02.2f' % value).rjust(just), newline=' ')
                if not options.dryrun:
                    values.append((value, tempLogger))
                else:
                    values.append((value, None))
            if options.dryrun:
                log('- + ' * 15)
            else:
                tempLogger('- + ' * 15)
        else:
            try:
                values.sort()
                value = values[repeat/2]
    
                log(' | ', newline='')
                log(('%02.2f' % value[0]).rjust(6) , newline='')
                log(u' \u00B1 '.encode('utf8'), newline='') # Unicode PLUS-MINUS SIGN
                log(('%02.2f' % stddev([x for x, _y in values])).rjust(6))
                
                if not options.dryrun:
                    for args, kw in value[1].delayed:
                        logger(*args, **kw)
            except IndexError:
                if not options.noStop:
                    raise

        if failed and not options.noStop:
            break

    return failed


def runStartupPerfTests(options, timer, largeData=False, repeat=3, logger=log):
    """
    Run startup time tests.
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    
    >>> runStartupPerfTests(options, '/usr/bin/time')
    Creating repository for startup time tests
    /.../release/RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/quit.py --create
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /usr/bin/time --format=%e -o test_profile/time.log .../release/RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/end.py
    Startup                             0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
      0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
      0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    False
    
    >>> runStartupPerfTests(options, '/usr/bin/time', repeat=1)
    Creating repository for startup time tests
    /.../release/RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/quit.py --create
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /usr/bin/time --format=%e -o test_profile/time.log /home/heikki/workspace/chandler/release/RunChandler --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/end.py
    Startup                             0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    False
    
    >>> runStartupPerfTests(options, '/usr/bin/time', largeData=True)
    Creating repository for startup time tests
    /.../release/RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/quit.py --restore=test_profile/__repository__.001
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /usr/bin/time --format=%e -o test_profile/time.log .../release/RunChandler --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/end.py
    Startup_with_large_calendar         0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
      0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
      0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    False
    
    >>> options.tbox = True
    >>> runStartupPerfTests(options, '/usr/bin/time')
    Creating repository for startup time tests
    /.../release/RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/quit.py --create
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /usr/bin/time --format=%e -o test_profile/time.log .../release/RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/QATestScripts/Performance/end.py
    Startup                             0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
      0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
      0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    <BLANKLINE>
    Startup [#TINDERBOX# Status = PASSED]
    OSAF_QA: Startup | ... | 0.00
    #TINDERBOX# Testname = Startup
    #TINDERBOX# Status = PASSED
    #TINDERBOX# Time elapsed = 0.00 (seconds)
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    """
    # Create test repo
    if options.verbose:
        log('Creating repository for startup time tests')
    cmd = [ options.runchandler['release'],
            '--catch=tests',
            '--profileDir=%s'  % options.profileDir,
            '--parcelPath=%s'  % options.parcelPath,
            '--scriptFile=%s'  % os.path.join('tools', 'QATestScripts', 'Performance', 'quit.py') ]

    if not largeData:
        cmd += ['--create']

        timeout = 180
        name    = 'Startup'
    else:
        cmd += ['--restore=%s' % os.path.join(options.profileDir, 
                                              '__repository__.001')]
        timeout = 600
        name    = 'Startup_with_large_calendar'

    if options.verbose:
        log(' '.join(cmd))

    if options.dryrun:
        result = 0
    else:
        result = build_lib.runCommand(cmd, timeout=timeout, logger=logger)

    if result != 0:
        log('***Error exit code=%d, creating %s repository' % (result, name))
        failedTests.append(name)
        return True

    if options.dryrun:
        log('- + ' * 15)
    else:
        logger('- + ' * 15)

    # Time startup
    values  = []
    timeLog = os.path.join(options.profileDir, 'time.log')

    if not options.dryrun:
        if os.path.isfile(timeLog):
            os.remove(timeLog)

    cmd = [ timer, r'--format=%e', '-o', timeLog,
            options.runchandler['release'],
            '--catch=tests',
            '--profileDir=%s'  % options.profileDir,
            '--parcelPath=%s'  % options.parcelPath,
            '--scriptFile=%s'  % os.path.join('tools', 'QATestScripts', 'Performance', 'end.py') ]

    if options.verbose:
        log(' '.join(cmd))

    log(name.ljust(33), newline=' ')

    for _x in range(repeat):
        if options.dryrun:
            result = 0
        else:
            result = build_lib.runCommand(cmd, timeout=180, logger=logger)

        if result == 0:
            if options.dryrun:
                line = '0.0'
            else:
                line = open(timeLog).readline()[:-1]

            try:
                value = float(line)
            except ValueError, e:
                log('| %s' % str(e))
                failedTests.append(name)
                return True

            log(('%02.2f' % value).rjust(6), newline=' ')
            values.append(value)
        else:
            log('| failed')
            failedTests.append(name)
            return True

        if options.dryrun:
            log('- + ' * 15)
        else:
            logger('- + ' * 15)
    else:
        values.sort()
        value = values[repeat/2]

        log(' | ', newline='')
        log(('%02.2f' % value).rjust(6) , newline='')
        log(u' \u00B1 '.encode('utf8'), newline='') # Unicode PLUS-MINUS SIGN
        log(('%02.2f' % stddev(values)).rjust(6))

        if options.tbox:
            revision = getattr(build_lib.loadModuleFromFile(os.path.join(options.chandlerHome, 'version.py'), 'vmodule'), 'revision', '')

            log('')
            log('%s [#TINDERBOX# Status = PASSED]' % name)
            log('OSAF_QA: %s | %s | %02.2f' % (name, revision, value))
            log('#TINDERBOX# Testname = %s' % name)
            log('#TINDERBOX# Status = PASSED')
            log('#TINDERBOX# Time elapsed = %02.2f (seconds)' % value)

            if options.dryrun:
                log('- + ' * 15)
            else:
                logger('- + ' * 15)

    return False


class DelayedLogger:
    """
    Delayed logger can be used to suppress logger calls until later time.
    
    >>> logger = DelayedLogger()
    >>> logger('foobar')
    >>> logger('barfoo', True)
    >>> logger.logAll()
    foobar
    barfoo
    """
    def __init__(self):
        self.delayed = []

    def __call__(self, *args, **kw):
        self.delayed.append((args, kw))

    def logAll(self):
        for args, kw in self.delayed:
            log(*args, **kw)


def runPerfTests(options, tests=None):
    """
    Run the Performance Test Suite
    
    >>> options = parseOptions()
    >>> checkOptions(options)
    >>> options.dryrun  = True
    >>> options.verbose = True
    >>> options.modes   = ['debug']
    
    >>> runPerfTests(options)
    Skipping Performance Tests - release mode not specified
    False
    
    >>> options.modes   = ['release']
    >>> runPerfTests(options)
    /.../release/RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --catsPerfLog=test_profile/time.log --scriptFile=tools/QATestScripts/Performance/PerfImportCalendar.py --create
    PerfImportCalendar.py                             0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    ...
    /.../release/RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --catsPerfLog=test_profile/time.log --scriptFile=tools/QATestScripts/Performance/PerfLargeDataResizeCalendar.py --restore=test_profile/__repository__.001
    PerfLargeDataResizeCalendar.py                    0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    ...
    Creating repository for startup time tests
    ...
    Startup ...
    ...
    Creating repository for startup time tests
    ...
    Startup_with_large_calendar ...
    ...
    Showing performance log in 5 seconds, Ctrl+C to stop tests
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    """
    failed  = False
    savePWD = os.getcwd()

    try:
        if 'release' in options.modes:
            delayedLogger = DelayedLogger()

            if not options.dryrun:
                os.chdir(options.chandlerHome)

                if tests is None:
                    for item in glob.glob(os.path.join(options.profileDir, '__repository__.0*')):
                        if os.path.isdir(item):
                            build_lib.rmdirs(item)
                        else:
                            os.remove(item)

            testlist      = []
            testlistLarge = []

            if tests is None:
                testlistStartup = ['startup', 'startup_large']

                for item in glob.glob(os.path.join(options.chandlerHome, 'tools', 'QATestScripts', 'Performance', 'Perf*.py')):
                    if 'PerfLargeData' in item:
                        testlistLarge.append(item)
                    else:
                        testlist.append(item)
            else:
                testlistStartup = []

                for item in tests:
                    if 'PerfLargeData' in item:
                        testlistLarge.append(item)
                    elif item in ('startup', 'startup_large'):
                        testlistStartup.append(item)
                    else:
                        testlist.append(item)

            repeat = 1
            if options.tbox:
                repeat = 3
                
            # small repo tests
            if testlist:
                failed = runScriptPerfTests(options, testlist, repeat=repeat,
                                            logger=delayedLogger)

            # large repo tests
            if testlistLarge and (not failed or options.noStop):
                if runScriptPerfTests(options, testlistLarge, largeData=True,
                                      repeat=repeat, logger=delayedLogger):
                    failed = True

            # startup tests
            if testlistStartup and (not failed or options.noStop):
                if os.name == 'nt' or sys.platform == 'cygwin':
                    t = build_lib.getCommand(['which', 'time.exe'])
                    if not t:
                        log('time.exe not found, skipping startup performance tests')
                elif sys.platform == 'darwin':
                    t = build_lib.getCommand(['which', 'gtime'])
                    if not t:
                        log('gtime not found, skipping startup performance tests')
                        log('NOTE: gtime is not part of OS X, you need to compile one' + \
                            'yourself (get source from http://directory.fsf.org/time.html)' + \
                            'or get it from darwinports project.')
                else:
                    t = '/usr/bin/time'

                if os.path.isfile(t):
                    if 'startup' in testlistStartup and runStartupPerfTests(options, t, logger=delayedLogger):
                        failed = True

                    if not failed: # Don't continue even if noStop, almost certain these won't work
                        if 'startup_large' in testlistStartup and runStartupPerfTests(options, t, largeData=True, logger=delayedLogger):
                            failed = True
                else:
                    log('time command not found, skipping startup performance tests')

            if not tests:
                log('Showing performance log in 5 seconds, Ctrl+C to stop tests')
                if not options.dryrun:
                    try:
                        time.sleep(5)
                    except KeyboardInterrupt:
                        sys.exit(0)
                log('- + ' * 15)

            delayedLogger.logAll()
        else:
            log('Skipping Performance Tests - release mode not specified')

    finally:
        os.chdir(savePWD)

    return failed


def main(options):
    """
    >>> options = parseOptions()
    >>> options.dryrun  = True
    >>> options.verbose = True
    >>> main(options)
    False
    
    Try and run a test that does not exist
    
    >>> options.single = 'TestFoo.py'
    >>> main(options)
    Test(s) not found
    False
    
    Try different single tests
    
      single unit test:
    
    >>> options.single = 'TestCrypto'
    >>> main(options)
    /.../RunPython... application/tests/TestCrypto.py -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    
      unit test and functional test:
    
    >>> options.single = 'TestCrypto,TestSharing'
    >>> main(options)
    /.../RunChandler... --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --chandlerTests=TestSharing -D2 -M0
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    /.../RunPython... application/tests/TestCrypto.py -v
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    
      unit, functional and two perf tests, one of which is a startup test:
    
    >>> options.single = 'TestCrypto,TestSharing,PerfImportCalendar,startup_large'
    >>> main(options)
    /.../RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --catsPerfLog=test_profile/time.log --scriptFile=tools/QATestScripts/Performance/PerfImportCalendar.py --create
    PerfImportCalendar.py                             0.00 - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
     |   0.00 ...   0.00
    /.../RunChandler... --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --chandlerTests=TestSharing -D2 -M0
    ...
    /.../RunPython... application/tests/TestCrypto.py -v
    ...
    Creating repository for startup time tests
    ...
    Startup_with_large_calendar ...
    ...
    False
    
    Try and specify an invalid mode
    
    >>> options.single = ''
    >>> options.mode   = 'foo'
    >>> main(options)
    foo removed from mode list
    False
    
    Run unit tests with --dryrun
    
    >>> options.mode = None
    >>> options.unit = True
    >>> main(options)
    /.../RunPython... .../tests/TestReferenceAttributes.py -v
    ...
    /.../RunPython... setup.py test -v
    ...
    False
    
    Run unitSuite with --dryrun
    
    >>> options.mode = None
    >>> options.unit = False
    >>> options.unitSuite = True
    >>> main(options)
    /.../RunPython... tools/run_tests.py -v application i18n osaf repository
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    
    Run functional tests with --dryrun
    
    >>> options.unit      = False
    >>> options.unitSuite = False
    >>> options.funcSuite = True
    >>> main(options)
    /.../RunChandler... --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --scriptFile=tools/cats/Functional/FunctionalTestSuite.py -D2 -M0
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    False
    
    Run functional tests each in its on process
    >>> options.funcSuite = False
    >>> options.func      = True
    >>> main(options)
    /.../RunChandler... --create --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --chandlerTests=TestCreateAccounts -D2 -M0
    - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + 
    ...
    False
    
    Run performance tests with --dryrun
    
    >>> options.func      = False
    >>> options.perf      = True
    >>> options.profile   = False
    >>> main(options)
    /.../RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --catsPerfLog=test_profile/time.log --scriptFile=tools/QATestScripts/Performance/PerfImportCalendar.py --create
    PerfImportCalendar.py ...
    ...
    /.../RunChandler... --catch=tests --profileDir=test_profile --parcelPath=tools/QATestScripts/DataFiles --catsPerfLog=test_profile/time.log --scriptFile=tools/QATestScripts/Performance/PerfLargeDataResizeCalendar.py --restore=test_profile/__repository__.001
    PerfLargeDataResizeCalendar.py ...
    ...
    Creating repository for startup time tests
    ...
    Startup ...
    ...
    False
    """
    checkOptions(options)

    if options.mode is None:
        options.modes = modes = ['release', 'debug']

        # silently clear any missing modes if default list is specified
        for mode in modes:
            if not os.path.isdir(os.path.join(options.chandlerBin, mode)):
                options.modes.remove(mode)
    else:
        options.mode  = options.mode.strip().lower()
        options.modes = [ options.mode ]

        # complain about any missing modes if mode was explicitly stated
        if not os.path.isdir(os.path.join(options.chandlerBin, options.mode)):
            options.modes.remove(options.mode)
            log('%s removed from mode list' % options.mode)

    failed = False

    try:
        # Empty the log file so that we won't be confused by old results later
        f = open(os.path.join(options.profileDir, 'chandler.log'), 'w')
        f.close()
    except IOError:
        pass

    # Remove old perf log files (we leave the the latest)
    for f in glob.glob(os.path.join(options.profileDir, '*.log.*')):
        try:
            os.remove(f)
        except OSError:
            pass

    if options.single:
        failed = runSingles(options)
    else:
        if options.unit:
            failed = runUnitTests(options)
            if not failed or options.noStop:
                if runPluginTests(options):
                    failed = True

        if options.unitSuite and (not failed or options.noStop):
            if runUnitSuite(options):
                failed = True

        if options.funcSuite and (not failed or options.noStop):
            if runFuncTest(options):
                failed = True

        if options.func and (not failed or options.noStop):
            if runFuncTestsSingly(options):
                failed = True

        if options.recorded and (not failed or options.noStop):
            if runRecordedScripts(options):
                failed = True

        if options.perf and (not failed or options.noStop):
            if runPerfTests(options):
                failed = True

    if len(failedTests) > 0:
        log('+-' * 32)
        log('The following tests failed:')
        log('\n'.join(failedTests))
        log('')

    return failed


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        import doctest
        doctest.testmod(optionflags=doctest.ELLIPSIS)
        sys.exit(0)

    if main(parseOptions()):
        sys.exit(1)

