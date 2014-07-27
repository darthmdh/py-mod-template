"""
compute product version information.

Based on similar component of Fabric;
https://github.com/fabric/fabric
Copyright (c) 2009-2014 Jeffrey E. Forcier
Copyright (c) 2008-2009 Christian Vest Hansen
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

        * Redistributions of source code must retain the above copyright notice,
          this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice,
          this list of conditions and the following disclaimer in the documentation
          and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
"""
from subprocess import check_output, CalledProcessError
from pathlib import Path

VERSION=(0,0,1,'alpha',0)

def git_sha():
    """ Return the short SHA of the current git checkout."""
    loc = Path(__file__).resolve().parent
    try:
        cmd = "cd \"{}\" && git log -1 --format=format:%%h".format(loc)
        p = check_output(cmd.split(), shell=True)
        return p.decode('utf-8')
    except CalledProcessError:
        return None


def get_version(style='short'):
    """
    Return a version string for this package, based on `VERSION`.

    Takes a single argument, ``style``, which should be one of the following
    strings:
        * ``branch``: just the major + minor, e.g. "1.0"
        * ``short`` (default): compact, e.g. "0.9rc1" for package filenames.
        * ``normal``: human readable, e.g. "0.9 beta 1". For documentation.
        * ``verbose``: like normal but fully explicit, e.g. "0.9 final".
        * ``all``: Returns all of the above as a dict.
    """
    versions = {}
    (b1, b2, tertiary, type_, type_num) = VERSION
    branch = '{}.{}'.format(b1, b2)
    final = (type_ == 'final')
    firsts = ''.join([x[0] for x in type_.split()])
    sha = git_sha()
    sha1 = (" (%s)" % sha) if sha else ""

    # Branch
    versions['branch'] = branch

    #Short
    v = branch
    if (tertiary or final):
        v += '.{}'.format(str(tertiary))
    if not final:
        v += firsts
        if type_num:
            v += str(type_num)
        else:
            v += sha1
    versions['short'] = v

    # Normal and Verbose are almost identical, so use a constructor func.
    def _get_norm_verb(branch=branch, tertiary=tertiary, final=final, type_=type_, type_num=type_num, sha1=sha1):
        v = branch
        if tertiary:
            v += '.{}'.format(str(tertiary))
        if not final:
            if type_num:
                v += " {} {}".format(type_, type_num)
            else:
                v += " pre-{}{}".format(type_, sha1)
        return v
    # Normal
    versions['normal'] = str(_get_norm_verb())
    # Verbose
    versions['verbose'] = str(_get_norm_verb())
    if final:
        versions['verbose'] += ' final'

    try:
        return versions[style]
    except KeyError:
        if style == 'all':
            return versions
        raise TypeError('"{}" is not a valid style specifier.'.format(style))

__version__ = get_version('short')

if __name__ == '__main__':
    print(get_version('all'))
