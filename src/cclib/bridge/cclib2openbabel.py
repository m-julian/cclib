# This file is part of cclib (http://cclib.github.io), a library for parsing
# and interpreting the results of computational chemistry packages.
#
# Copyright (C) 2009-2015, the cclib development team
#
# The library is free software, distributed under the terms of
# the GNU Lesser General Public version 2.1 or later. You should have
# received a copy of the license along with cclib. You can also access
# the full license online at http://www.gnu.org/copyleft/lgpl.html.

"""Bridge between cclib data and openbabel (http://openbabel.org)."""

import openbabel as ob


def makeopenbabel(atomcoords, atomnos, charge=0, mult=1):
    """Create an Open Babel molecule.

    >>> import numpy, openbabel
    >>> atomnos = numpy.array([1,8,1],"i")
    >>> coords = numpy.array([[-1.,1.,0.],[0.,0.,0.],[1.,1.,0.]])
    >>> obmol = makeopenbabel(coords, atomnos)
    >>> obconversion = openbabel.OBConversion()
    >>> formatok = obconversion.SetOutFormat("inchi")
    >>> print obconversion.WriteString(obmol).strip()
    InChI=1/H2O/h1H2
    """
    obmol = ob.OBMol()
    for i in range(len(atomnos)):
        # Note that list(atomcoords[i]) is not equivalent!!!
        coords = atomcoords[i].tolist()
        atomno = int(atomnos[i])
        obatom = ob.OBAtom()
        obatom.SetAtomicNum(atomno)
        obatom.SetVector(*coords)
        obmol.AddAtom(obatom)
    obmol.ConnectTheDots()
    obmol.PerceiveBondOrders()
    obmol.SetTotalSpinMultiplicity(mult)
    obmol.SetTotalCharge(charge)
    return obmol

def makecclib(mol):
    """Create cclib attributes from an OpenBabel molecule.

    Beyond the numbers, masses and coordinates, we could also set the total charge
    and multiplicity, but often these are calculated from atomic formal charges
    so it is better to assume that would not be correct.
    """

    attributes = {
        'atomcoords':   [],
        'atommasses':   [],
        'atomnos':      [],
        'natom':        mol.NumAtoms(),
    }
    for atom in ob.OBMolAtomIter(mol):
        attributes['atomcoords'].append([atom.GetX(), atom.GetY(), atom.GetZ()])
        attributes['atommasses'].append(atom.GetAtomicMass())
        attributes['atomnos'].append(atom.GetAtomicNum())
    return attributes

def readfile(fname, type):
    """Read a file with OpenBabel and extract cclib attributes."""

    obc = ob.OBConversion()
    obc.SetInFormat(type)
    mol = ob.OBMol()
    obc.ReadFile(mol, fname)
    return makecclib(mol)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
