"""
Created on February 2, 2012

@author: sbobovyc
"""
"""   
    Copyright (C) 2012 Stanislav Bobovych

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import os
from pak_file import PAK_file, PAK_CRYPT_file

parser = argparse.ArgumentParser(description='Tool that can unpack Jagged Alliance: BiA pak/pak.crypt files.')

parser.add_argument('file', nargs='?', help='Input file')
parser.add_argument('outdir', nargs='?', help='Output directory')
parser.add_argument('-i', '--info', default=False, action='store_true', help='Output information about pak file')
parser.add_argument('-d', '--debug', default=False, action='store_true', help='Show debug messages.')


args = parser.parse_args()
file = args.file
outdir = args.outdir
info = args.info
debug = args.debug

if file != None and info != False:
    info_filepath = os.path.abspath(file)
    print "Not implemented yet."
        
elif file != None:      
    extension = os.path.splitext(file)[1][1:].strip()
    pak_filepath = os.path.abspath(file)
    
    print "Unpacking %s" % pak_filepath
    
    if extension == "pak":
        pak_file = PAK_file(filepath=pak_filepath)
    elif extension == "crypt":
        pak_file = PAK_CRYPT_file(filepath=pak_filepath)
    else:
        print "File not pak or pak.crypt" 
    
    if outdir != None:
        output_filepath = os.path.abspath(outdir)
        pak_file.dump(outdir, debug)
    else:
        pak_file.dump(verbose=debug)
            
else:
    print "Nothing happened"
    parser.print_help()
        
