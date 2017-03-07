
# -*- coding: utf-8 -*-

# Test LCC functions and methods.

__all__ = ('Tests',)
__version__ = '17.03.07'

from tests import Tests as _Tests

from geodesy import F_D, F_DMS, Conic, Conics, Datums, Lcc, toLcc


class Tests(_Tests):

    def testConic(self, LatLon, n=''):

        n = 'Snyder' + str(n)
        c = Conic(LatLon(23, -96, datum=Datums.NAD27), 33, 45, E0=0, N0=0, name=n)
        self.test(n, c, "name='%s', lat0=23.0, lon0=-96.0, par1=33.0, par2=45.0, E0=0, N0=0, k0=1, SP=2, datum=(name='NAD27', ellipsoid=Ellipsoids.Clarke1866, transform=Transforms.NAD27)" % (n,))

    def testLcc(self, LatLon):

        lb = Lcc(448251, 5411932.0001)
        self.test('lb1', lb.toStr(4), '448251.0 5411932.0001')
        self.test('lb1', lb.toStr(sep=', '), '448251, 5411932')
        self.test('lb1', lb.conic.name2, 'WRF_Lb.WGS84')

        ll = LatLon(46.5, 3)
        self.test('LatLon', ll, '46.5°N, 003.0°E')
        self.test('LatLon', ll.toStr(form=F_DMS), '46°30′00.0″N, 003°00′00.0″E')
        lb = toLcc(ll, conic=Conics.Fr93Lb)
        self.test('toLcc1', str(lb), '700000 6600000')
        self.test('toLcc1', lb.toLatLon(LatLon), '46.5°N, 003.0°E')

        lb = Lcc(1894410.9, 1564649.5, conic=Snyder)
        self.test('lb2', lb, '1894411 1564650')
        self.test('lb2', lb.conic.datum.ellipsoid.name, 'Clarke1866')
        ll = lb.toLatLon(LatLon)  # Clark1866
        self.test('toLatLon2', ll.toStr(prec=6, form=F_D), '35.0°N, 075.0°W')
        self.test('toLatLon2', ll.toStr(prec=4, form=F_DMS), '35°00′00.0007″N, 074°59′59.9997″W')
        self.test('toLatLon2', ll.datum.name, 'NAD27')
        lb = toLcc(ll, conic=Snyder)
        self.test('toLcc2', lb.toStr(prec=1), '1894410.9 1564649.5')
        self.test('toLcc2', lb.conic.name2, 'Snyder.NAD27')

        for n, c in sorted(Conics.items()):
            d = abs(c.par1 - c.par2)
            if d > 0:  # test corners of the conic
                for ll in (LatLon(c.par1, c.lon0 - d, datum=c.datum),
                           LatLon(c.par1, c.lon0,     datum=c.datum),
                           LatLon(c.par1, c.lon0 + d, datum=c.datum),
                           LatLon(c.par2, c.lon0 - d, datum=c.datum),
                           LatLon(c.par2, c.lon0,     datum=c.datum),
                           LatLon(c.par2, c.lon0 + d, datum=c.datum)):
#                   self.test(n, ll, str(ll))  # PYCHOK expected
                    lb = toLcc(ll, conic=c)
#                   self.test(n, lb, '')
                    ll_ = lb.toLatLon(LatLon)
                    self.test(n, ll, str(ll_))
                    self.test(n, ll.datum.name, ll_.datum.name)


if __name__ == '__main__':

    from geodesy import lcc
    from geodesy.ellipsoidalNvector  import LatLon as nLatLon
    from geodesy.ellipsoidalVincenty import LatLon as vLatLon

    # Snyder, pp 297 <https://pubs.er.usgs.gov/djvu/PP/PP_1395.pdf>
    Snyder = Conic(vLatLon(23, -96, datum=Datums.NAD27),
                           33, 45, E0=0, N0=0, name='Snyder')

    t = Tests(__file__, __version__, lcc)
    t.testLcc(nLatLon)
    t.testLcc(vLatLon)
    t.testConic(vLatLon, 1)
    t.testConic(nLatLon, 2)
    t.results()
    t.exit()

    # Typical test results (on MacOS 10.12.3):

    # testing geodesy.lcc version 17.02.14
    # test 1 lb1: 448251.0 5411932.0001
    # test 2 lb1: 448251, 5411932
    # test 3 lb1: WRF_Lb.WGS84
    # test 4 LatLon: 46.5°N, 003.0°E
    # test 5 LatLon: 46°30′00.0″N, 003°00′00.0″E
    # test 6 toLcc1: 700000 6600000
    # test 7 toLcc1: 46.5°N, 003.0°E
    # test 8 lb2: 1894411 1564650
    # test 9 lb2: Clarke1866
    # test 10 toLatLon2: 35.0°N, 075.0°W
    # test 11 toLatLon2: 35°00′00.0007″N, 074°59′59.9997″W
    # test 12 toLatLon2: NAD27
    # test 13 toLcc2: 1894410.9 1564649.5
    # test 14 toLcc2: Snyder.NAD27
    # test 15 Be72Lb: 49.833334°N, 003.034153°E
    # test 16 Be72Lb: NAD83
    # test 17 Be72Lb: 49.833334°N, 004.367487°E
    # test 18 Be72Lb: NAD83
    # test 19 Be72Lb: 49.833334°N, 005.70082°E
    # test 20 Be72Lb: NAD83
    # test 21 Be72Lb: 51.166667°N, 003.034153°E
    # test 22 Be72Lb: NAD83
    # test 23 Be72Lb: 51.166667°N, 004.367487°E
    # test 24 Be72Lb: NAD83
    # test 25 Be72Lb: 51.166667°N, 005.70082°E
    # test 26 Be72Lb: NAD83
    # test 27 Fr93Lb: 49.0°N, 002.0°W
    # test 28 Fr93Lb: WGS84
    # test 29 Fr93Lb: 49.0°N, 003.0°E
    # test 30 Fr93Lb: WGS84
    # test 31 Fr93Lb: 49.0°N, 008.0°E
    # test 32 Fr93Lb: WGS84
    # test 33 Fr93Lb: 44.0°N, 002.0°W
    # test 34 Fr93Lb: WGS84
    # test 35 Fr93Lb: 44.0°N, 003.0°E
    # test 36 Fr93Lb: WGS84
    # test 37 Fr93Lb: 44.0°N, 008.0°E
    # test 38 Fr93Lb: WGS84
    # test 39 MaNLb: 31.73°N, 008.54°W
    # test 40 MaNLb: NTF
    # test 41 MaNLb: 31.73°N, 005.4°W
    # test 42 MaNLb: NTF
    # test 43 MaNLb: 31.73°N, 002.26°W
    # test 44 MaNLb: NTF
    # test 45 MaNLb: 34.87°N, 008.54°W
    # test 46 MaNLb: NTF
    # test 47 MaNLb: 34.87°N, 005.4°W
    # test 48 MaNLb: NTF
    # test 49 MaNLb: 34.87°N, 002.26°W
    # test 50 MaNLb: NTF
    # test 51 MxLb: 17.5°N, 114.0°W
    # test 52 MxLb: WGS84
    # test 53 MxLb: 17.5°N, 102.0°W
    # test 54 MxLb: WGS84
    # test 55 MxLb: 17.5°N, 090.0°W
    # test 56 MxLb: WGS84
    # test 57 MxLb: 29.5°N, 114.0°W
    # test 58 MxLb: WGS84
    # test 59 MxLb: 29.5°N, 102.0°W
    # test 60 MxLb: WGS84
    # test 61 MxLb: 29.5°N, 090.0°W
    # test 62 MxLb: WGS84
    # test 63 PyT_Lb: 45.898939°N, 000.540154°E
    # test 64 PyT_Lb: NTF
    # test 65 PyT_Lb: 45.898939°N, 002.337229°E
    # test 66 PyT_Lb: NTF
    # test 67 PyT_Lb: 45.898939°N, 004.134305°E
    # test 68 PyT_Lb: NTF
    # test 69 PyT_Lb: 47.696014°N, 000.540154°E
    # test 70 PyT_Lb: NTF
    # test 71 PyT_Lb: 47.696014°N, 002.337229°E
    # test 72 PyT_Lb: NTF
    # test 73 PyT_Lb: 47.696014°N, 004.134305°E
    # test 74 PyT_Lb: NTF
    # test 75 Snyder: 33.0°N, 108.0°W
    # test 76 Snyder: NAD27
    # test 77 Snyder: 33.0°N, 096.0°W
    # test 78 Snyder: NAD27
    # test 79 Snyder: 33.0°N, 084.0°W
    # test 80 Snyder: NAD27
    # test 81 Snyder: 45.0°N, 108.0°W
    # test 82 Snyder: NAD27
    # test 83 Snyder: 45.0°N, 096.0°W
    # test 84 Snyder: NAD27
    # test 85 Snyder: 45.0°N, 084.0°W
    # test 86 Snyder: NAD27
    # test 87 USA_Lb: 33.0°N, 108.0°W
    # test 88 USA_Lb: WGS84
    # test 89 USA_Lb: 33.0°N, 096.0°W
    # test 90 USA_Lb: WGS84
    # test 91 USA_Lb: 33.0°N, 084.0°W
    # test 92 USA_Lb: WGS84
    # test 93 USA_Lb: 45.0°N, 108.0°W
    # test 94 USA_Lb: WGS84
    # test 95 USA_Lb: 45.0°N, 096.0°W
    # test 96 USA_Lb: WGS84
    # test 97 USA_Lb: 45.0°N, 084.0°W
    # test 98 USA_Lb: WGS84
    # test 99 WRF_Lb: 33.0°N, 109.0°W
    # test 100 WRF_Lb: WGS84
    # test 101 WRF_Lb: 33.0°N, 097.0°W
    # test 102 WRF_Lb: WGS84
    # test 103 WRF_Lb: 33.0°N, 085.0°W
    # test 104 WRF_Lb: WGS84
    # test 105 WRF_Lb: 45.0°N, 109.0°W
    # test 106 WRF_Lb: WGS84
    # test 107 WRF_Lb: 45.0°N, 097.0°W
    # test 108 WRF_Lb: WGS84
    # test 109 WRF_Lb: 45.0°N, 085.0°W
    # test 110 WRF_Lb: WGS84
    # test 111 lb1: 448251.0 5411932.0001
    # test 112 lb1: 448251, 5411932
    # test 113 lb1: WRF_Lb.WGS84
    # test 114 LatLon: 46.5°N, 003.0°E
    # test 115 LatLon: 46°30′00.0″N, 003°00′00.0″E
    # test 116 toLcc1: 700000 6600000
    # test 117 toLcc1: 46.5°N, 003.0°E
    # test 118 lb2: 1894411 1564650
    # test 119 lb2: Clarke1866
    # test 120 toLatLon2: 35.0°N, 075.0°W
    # test 121 toLatLon2: 35°00′00.0007″N, 074°59′59.9997″W
    # test 122 toLatLon2: NAD27
    # test 123 toLcc2: 1894410.9 1564649.5
    # test 124 toLcc2: Snyder.NAD27
    # test 125 Be72Lb: 49.833334°N, 003.034153°E
    # test 126 Be72Lb: NAD83
    # test 127 Be72Lb: 49.833334°N, 004.367487°E
    # test 128 Be72Lb: NAD83
    # test 129 Be72Lb: 49.833334°N, 005.70082°E
    # test 130 Be72Lb: NAD83
    # test 131 Be72Lb: 51.166667°N, 003.034153°E
    # test 132 Be72Lb: NAD83
    # test 133 Be72Lb: 51.166667°N, 004.367487°E
    # test 134 Be72Lb: NAD83
    # test 135 Be72Lb: 51.166667°N, 005.70082°E
    # test 136 Be72Lb: NAD83
    # test 137 Fr93Lb: 49.0°N, 002.0°W
    # test 138 Fr93Lb: WGS84
    # test 139 Fr93Lb: 49.0°N, 003.0°E
    # test 140 Fr93Lb: WGS84
    # test 141 Fr93Lb: 49.0°N, 008.0°E
    # test 142 Fr93Lb: WGS84
    # test 143 Fr93Lb: 44.0°N, 002.0°W
    # test 144 Fr93Lb: WGS84
    # test 145 Fr93Lb: 44.0°N, 003.0°E
    # test 146 Fr93Lb: WGS84
    # test 147 Fr93Lb: 44.0°N, 008.0°E
    # test 148 Fr93Lb: WGS84
    # test 149 MaNLb: 31.73°N, 008.54°W
    # test 150 MaNLb: NTF
    # test 151 MaNLb: 31.73°N, 005.4°W
    # test 152 MaNLb: NTF
    # test 153 MaNLb: 31.73°N, 002.26°W
    # test 154 MaNLb: NTF
    # test 155 MaNLb: 34.87°N, 008.54°W
    # test 156 MaNLb: NTF
    # test 157 MaNLb: 34.87°N, 005.4°W
    # test 158 MaNLb: NTF
    # test 159 MaNLb: 34.87°N, 002.26°W
    # test 160 MaNLb: NTF
    # test 161 MxLb: 17.5°N, 114.0°W
    # test 162 MxLb: WGS84
    # test 163 MxLb: 17.5°N, 102.0°W
    # test 164 MxLb: WGS84
    # test 165 MxLb: 17.5°N, 090.0°W
    # test 166 MxLb: WGS84
    # test 167 MxLb: 29.5°N, 114.0°W
    # test 168 MxLb: WGS84
    # test 169 MxLb: 29.5°N, 102.0°W
    # test 170 MxLb: WGS84
    # test 171 MxLb: 29.5°N, 090.0°W
    # test 172 MxLb: WGS84
    # test 173 PyT_Lb: 45.898939°N, 000.540154°E
    # test 174 PyT_Lb: NTF
    # test 175 PyT_Lb: 45.898939°N, 002.337229°E
    # test 176 PyT_Lb: NTF
    # test 177 PyT_Lb: 45.898939°N, 004.134305°E
    # test 178 PyT_Lb: NTF
    # test 179 PyT_Lb: 47.696014°N, 000.540154°E
    # test 180 PyT_Lb: NTF
    # test 181 PyT_Lb: 47.696014°N, 002.337229°E
    # test 182 PyT_Lb: NTF
    # test 183 PyT_Lb: 47.696014°N, 004.134305°E
    # test 184 PyT_Lb: NTF
    # test 185 Snyder: 33.0°N, 108.0°W
    # test 186 Snyder: NAD27
    # test 187 Snyder: 33.0°N, 096.0°W
    # test 188 Snyder: NAD27
    # test 189 Snyder: 33.0°N, 084.0°W
    # test 190 Snyder: NAD27
    # test 191 Snyder: 45.0°N, 108.0°W
    # test 192 Snyder: NAD27
    # test 193 Snyder: 45.0°N, 096.0°W
    # test 194 Snyder: NAD27
    # test 195 Snyder: 45.0°N, 084.0°W
    # test 196 Snyder: NAD27
    # test 197 USA_Lb: 33.0°N, 108.0°W
    # test 198 USA_Lb: WGS84
    # test 199 USA_Lb: 33.0°N, 096.0°W
    # test 200 USA_Lb: WGS84
    # test 201 USA_Lb: 33.0°N, 084.0°W
    # test 202 USA_Lb: WGS84
    # test 203 USA_Lb: 45.0°N, 108.0°W
    # test 204 USA_Lb: WGS84
    # test 205 USA_Lb: 45.0°N, 096.0°W
    # test 206 USA_Lb: WGS84
    # test 207 USA_Lb: 45.0°N, 084.0°W
    # test 208 USA_Lb: WGS84
    # test 209 WRF_Lb: 33.0°N, 109.0°W
    # test 210 WRF_Lb: WGS84
    # test 211 WRF_Lb: 33.0°N, 097.0°W
    # test 212 WRF_Lb: WGS84
    # test 213 WRF_Lb: 33.0°N, 085.0°W
    # test 214 WRF_Lb: WGS84
    # test 215 WRF_Lb: 45.0°N, 109.0°W
    # test 216 WRF_Lb: WGS84
    # test 217 WRF_Lb: 45.0°N, 097.0°W
    # test 218 WRF_Lb: WGS84
    # test 219 WRF_Lb: 45.0°N, 085.0°W
    # test 220 WRF_Lb: WGS84
    # test 221 Snyder1: name='Snyder1', lat0=23.0, lon0=-96.0, par1=33.0, par2=45.0, E0=0, N0=0, k0=1, SP=2, datum=(name='NAD27', ellipsoid=Ellipsoids.Clarke1866, transform=Transforms.NAD27)
    # test 222 Snyder2: name='Snyder2', lat0=23.0, lon0=-96.0, par1=33.0, par2=45.0, E0=0, N0=0, k0=1, SP=2, datum=(name='NAD27', ellipsoid=Ellipsoids.Clarke1866, transform=Transforms.NAD27)
    # all geodesy.lcc tests passed (Python 2.7.13 64bit)

    # testing lcc version 17.02.14
    # test 1 lb1: 448251.0 5411932.0001
    # test 2 lb1: 448251, 5411932
    # test 3 lb1: WRF_Lb.WGS84
    # test 4 LatLon: 46.5°N, 003.0°E
    # test 5 LatLon: 46°30′00.0″N, 003°00′00.0″E
    # test 6 toLcc1: 700000 6600000
    # test 7 toLcc1: 46.5°N, 003.0°E
    # test 8 lb2: 1894411 1564650
    # test 9 lb2: Clarke1866
    # test 10 toLatLon2: 35.0°N, 075.0°W
    # test 11 toLatLon2: 35°00′00.0007″N, 074°59′59.9997″W
    # test 12 toLatLon2: NAD27
    # test 13 toLcc2: 1894410.9 1564649.5
    # test 14 toLcc2: Snyder.NAD27
    # test 15 Be72Lb: 49.833334°N, 003.034153°E
    # test 16 Be72Lb: NAD83
    # test 17 Be72Lb: 49.833334°N, 004.367487°E
    # test 18 Be72Lb: NAD83
    # test 19 Be72Lb: 49.833334°N, 005.70082°E
    # test 20 Be72Lb: NAD83
    # test 21 Be72Lb: 51.166667°N, 003.034153°E
    # test 22 Be72Lb: NAD83
    # test 23 Be72Lb: 51.166667°N, 004.367487°E
    # test 24 Be72Lb: NAD83
    # test 25 Be72Lb: 51.166667°N, 005.70082°E
    # test 26 Be72Lb: NAD83
    # test 27 Fr93Lb: 49.0°N, 002.0°W
    # test 28 Fr93Lb: WGS84
    # test 29 Fr93Lb: 49.0°N, 003.0°E
    # test 30 Fr93Lb: WGS84
    # test 31 Fr93Lb: 49.0°N, 008.0°E
    # test 32 Fr93Lb: WGS84
    # test 33 Fr93Lb: 44.0°N, 002.0°W
    # test 34 Fr93Lb: WGS84
    # test 35 Fr93Lb: 44.0°N, 003.0°E
    # test 36 Fr93Lb: WGS84
    # test 37 Fr93Lb: 44.0°N, 008.0°E
    # test 38 Fr93Lb: WGS84
    # test 39 MaNLb: 31.73°N, 008.54°W
    # test 40 MaNLb: NTF
    # test 41 MaNLb: 31.73°N, 005.4°W
    # test 42 MaNLb: NTF
    # test 43 MaNLb: 31.73°N, 002.26°W
    # test 44 MaNLb: NTF
    # test 45 MaNLb: 34.87°N, 008.54°W
    # test 46 MaNLb: NTF
    # test 47 MaNLb: 34.87°N, 005.4°W
    # test 48 MaNLb: NTF
    # test 49 MaNLb: 34.87°N, 002.26°W
    # test 50 MaNLb: NTF
    # test 51 MxLb: 17.5°N, 114.0°W
    # test 52 MxLb: WGS84
    # test 53 MxLb: 17.5°N, 102.0°W
    # test 54 MxLb: WGS84
    # test 55 MxLb: 17.5°N, 090.0°W
    # test 56 MxLb: WGS84
    # test 57 MxLb: 29.5°N, 114.0°W
    # test 58 MxLb: WGS84
    # test 59 MxLb: 29.5°N, 102.0°W
    # test 60 MxLb: WGS84
    # test 61 MxLb: 29.5°N, 090.0°W
    # test 62 MxLb: WGS84
    # test 63 PyT_Lb: 45.898939°N, 000.540154°E
    # test 64 PyT_Lb: NTF
    # test 65 PyT_Lb: 45.898939°N, 002.337229°E
    # test 66 PyT_Lb: NTF
    # test 67 PyT_Lb: 45.898939°N, 004.134305°E
    # test 68 PyT_Lb: NTF
    # test 69 PyT_Lb: 47.696014°N, 000.540154°E
    # test 70 PyT_Lb: NTF
    # test 71 PyT_Lb: 47.696014°N, 002.337229°E
    # test 72 PyT_Lb: NTF
    # test 73 PyT_Lb: 47.696014°N, 004.134305°E
    # test 74 PyT_Lb: NTF
    # test 75 Snyder: 33.0°N, 108.0°W
    # test 76 Snyder: NAD27
    # test 77 Snyder: 33.0°N, 096.0°W
    # test 78 Snyder: NAD27
    # test 79 Snyder: 33.0°N, 084.0°W
    # test 80 Snyder: NAD27
    # test 81 Snyder: 45.0°N, 108.0°W
    # test 82 Snyder: NAD27
    # test 83 Snyder: 45.0°N, 096.0°W
    # test 84 Snyder: NAD27
    # test 85 Snyder: 45.0°N, 084.0°W
    # test 86 Snyder: NAD27
    # test 87 USA_Lb: 33.0°N, 108.0°W
    # test 88 USA_Lb: WGS84
    # test 89 USA_Lb: 33.0°N, 096.0°W
    # test 90 USA_Lb: WGS84
    # test 91 USA_Lb: 33.0°N, 084.0°W
    # test 92 USA_Lb: WGS84
    # test 93 USA_Lb: 45.0°N, 108.0°W
    # test 94 USA_Lb: WGS84
    # test 95 USA_Lb: 45.0°N, 096.0°W
    # test 96 USA_Lb: WGS84
    # test 97 USA_Lb: 45.0°N, 084.0°W
    # test 98 USA_Lb: WGS84
    # test 99 WRF_Lb: 33.0°N, 109.0°W
    # test 100 WRF_Lb: WGS84
    # test 101 WRF_Lb: 33.0°N, 097.0°W
    # test 102 WRF_Lb: WGS84
    # test 103 WRF_Lb: 33.0°N, 085.0°W
    # test 104 WRF_Lb: WGS84
    # test 105 WRF_Lb: 45.0°N, 109.0°W
    # test 106 WRF_Lb: WGS84
    # test 107 WRF_Lb: 45.0°N, 097.0°W
    # test 108 WRF_Lb: WGS84
    # test 109 WRF_Lb: 45.0°N, 085.0°W
    # test 110 WRF_Lb: WGS84
    # test 111 lb1: 448251.0 5411932.0001
    # test 112 lb1: 448251, 5411932
    # test 113 lb1: WRF_Lb.WGS84
    # test 114 LatLon: 46.5°N, 003.0°E
    # test 115 LatLon: 46°30′00.0″N, 003°00′00.0″E
    # test 116 toLcc1: 700000 6600000
    # test 117 toLcc1: 46.5°N, 003.0°E
    # test 118 lb2: 1894411 1564650
    # test 119 lb2: Clarke1866
    # test 120 toLatLon2: 35.0°N, 075.0°W
    # test 121 toLatLon2: 35°00′00.0007″N, 074°59′59.9997″W
    # test 122 toLatLon2: NAD27
    # test 123 toLcc2: 1894410.9 1564649.5
    # test 124 toLcc2: Snyder.NAD27
    # test 125 Be72Lb: 49.833334°N, 003.034153°E
    # test 126 Be72Lb: NAD83
    # test 127 Be72Lb: 49.833334°N, 004.367487°E
    # test 128 Be72Lb: NAD83
    # test 129 Be72Lb: 49.833334°N, 005.70082°E
    # test 130 Be72Lb: NAD83
    # test 131 Be72Lb: 51.166667°N, 003.034153°E
    # test 132 Be72Lb: NAD83
    # test 133 Be72Lb: 51.166667°N, 004.367487°E
    # test 134 Be72Lb: NAD83
    # test 135 Be72Lb: 51.166667°N, 005.70082°E
    # test 136 Be72Lb: NAD83
    # test 137 Fr93Lb: 49.0°N, 002.0°W
    # test 138 Fr93Lb: WGS84
    # test 139 Fr93Lb: 49.0°N, 003.0°E
    # test 140 Fr93Lb: WGS84
    # test 141 Fr93Lb: 49.0°N, 008.0°E
    # test 142 Fr93Lb: WGS84
    # test 143 Fr93Lb: 44.0°N, 002.0°W
    # test 144 Fr93Lb: WGS84
    # test 145 Fr93Lb: 44.0°N, 003.0°E
    # test 146 Fr93Lb: WGS84
    # test 147 Fr93Lb: 44.0°N, 008.0°E
    # test 148 Fr93Lb: WGS84
    # test 149 MaNLb: 31.73°N, 008.54°W
    # test 150 MaNLb: NTF
    # test 151 MaNLb: 31.73°N, 005.4°W
    # test 152 MaNLb: NTF
    # test 153 MaNLb: 31.73°N, 002.26°W
    # test 154 MaNLb: NTF
    # test 155 MaNLb: 34.87°N, 008.54°W
    # test 156 MaNLb: NTF
    # test 157 MaNLb: 34.87°N, 005.4°W
    # test 158 MaNLb: NTF
    # test 159 MaNLb: 34.87°N, 002.26°W
    # test 160 MaNLb: NTF
    # test 161 MxLb: 17.5°N, 114.0°W
    # test 162 MxLb: WGS84
    # test 163 MxLb: 17.5°N, 102.0°W
    # test 164 MxLb: WGS84
    # test 165 MxLb: 17.5°N, 090.0°W
    # test 166 MxLb: WGS84
    # test 167 MxLb: 29.5°N, 114.0°W
    # test 168 MxLb: WGS84
    # test 169 MxLb: 29.5°N, 102.0°W
    # test 170 MxLb: WGS84
    # test 171 MxLb: 29.5°N, 090.0°W
    # test 172 MxLb: WGS84
    # test 173 PyT_Lb: 45.898939°N, 000.540154°E
    # test 174 PyT_Lb: NTF
    # test 175 PyT_Lb: 45.898939°N, 002.337229°E
    # test 176 PyT_Lb: NTF
    # test 177 PyT_Lb: 45.898939°N, 004.134305°E
    # test 178 PyT_Lb: NTF
    # test 179 PyT_Lb: 47.696014°N, 000.540154°E
    # test 180 PyT_Lb: NTF
    # test 181 PyT_Lb: 47.696014°N, 002.337229°E
    # test 182 PyT_Lb: NTF
    # test 183 PyT_Lb: 47.696014°N, 004.134305°E
    # test 184 PyT_Lb: NTF
    # test 185 Snyder: 33.0°N, 108.0°W
    # test 186 Snyder: NAD27
    # test 187 Snyder: 33.0°N, 096.0°W
    # test 188 Snyder: NAD27
    # test 189 Snyder: 33.0°N, 084.0°W
    # test 190 Snyder: NAD27
    # test 191 Snyder: 45.0°N, 108.0°W
    # test 192 Snyder: NAD27
    # test 193 Snyder: 45.0°N, 096.0°W
    # test 194 Snyder: NAD27
    # test 195 Snyder: 45.0°N, 084.0°W
    # test 196 Snyder: NAD27
    # test 197 USA_Lb: 33.0°N, 108.0°W
    # test 198 USA_Lb: WGS84
    # test 199 USA_Lb: 33.0°N, 096.0°W
    # test 200 USA_Lb: WGS84
    # test 201 USA_Lb: 33.0°N, 084.0°W
    # test 202 USA_Lb: WGS84
    # test 203 USA_Lb: 45.0°N, 108.0°W
    # test 204 USA_Lb: WGS84
    # test 205 USA_Lb: 45.0°N, 096.0°W
    # test 206 USA_Lb: WGS84
    # test 207 USA_Lb: 45.0°N, 084.0°W
    # test 208 USA_Lb: WGS84
    # test 209 WRF_Lb: 33.0°N, 109.0°W
    # test 210 WRF_Lb: WGS84
    # test 211 WRF_Lb: 33.0°N, 097.0°W
    # test 212 WRF_Lb: WGS84
    # test 213 WRF_Lb: 33.0°N, 085.0°W
    # test 214 WRF_Lb: WGS84
    # test 215 WRF_Lb: 45.0°N, 109.0°W
    # test 216 WRF_Lb: WGS84
    # test 217 WRF_Lb: 45.0°N, 097.0°W
    # test 218 WRF_Lb: WGS84
    # test 219 WRF_Lb: 45.0°N, 085.0°W
    # test 220 WRF_Lb: WGS84
    # test 221 Snyder1: name='Snyder1', lat0=23.0, lon0=-96.0, par1=33.0, par2=45.0, E0=0, N0=0, k0=1, SP=2, datum=(name='NAD27', ellipsoid=Ellipsoids.Clarke1866, transform=Transforms.NAD27)
    # test 222 Snyder2: name='Snyder2', lat0=23.0, lon0=-96.0, par1=33.0, par2=45.0, E0=0, N0=0, k0=1, SP=2, datum=(name='NAD27', ellipsoid=Ellipsoids.Clarke1866, transform=Transforms.NAD27)
    # all lcc tests passed (Python 3.6.0 64bit)
