class PackageA(object):
    def __init__(self, bitstream):
        ''' Interpret next bits in BitString'''

        self.bs = bitstream
        # self._test()

        self.head = self.bs.read('uint:8')
        self.imu = self.bs.readlist('9*uint:16')
        self.bar = self.bs.read('uint:20')
        self.temp = self.bs.readlist('3*uint:12')
        self.sc = self.bs.read('uint:12')
        self.sv = self.bs.read('uint:12')
        self.suv = self.bs.read('uint:16')

        # self._parse()

    def __repr__(self):
        result = f"<PackageA(head='{self.head}', "
        result += f"\n\timu='{self.imu}', "
        result += f"\n\tbar='{self.bar}', "
        result += f"\n\ttemp='{self.temp}', "
        result += f"\n\tsc='{self.sc}', "
        result += f"\n\tsv='{self.sv}', "
        result += f"\n\tsuv='{self.suv}')>"

        return result

    def _test(self):
        '''Prints every received byte'''
        while(self.bs.pos < len(self.bs)):
            print(self.bs.read(8).uint)

    def _parse(self):
        pass
