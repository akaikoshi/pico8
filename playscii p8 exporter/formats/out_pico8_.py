
from art_export import ArtExporter
from art import TileIter

class PICO8Exporter(ArtExporter):
    format_name = 'PICO8'
    format_description = """
PICO8 ASCII exporter by pepe/hmd - 2024
Assumes PICO 8 character set and PICO8 palette.
32x20 output
    """
    file_extension = 'p8'

    def run_export(self, out_filename, options):
        # binary file; encoding into ANSI bytes happens just before write
        # self.outfile = open(out_filename, 'wb')
        self.outfile = open(out_filename, 'w', encoding='utf-8')
        
        #
        self.outfile.write('pico-8 cartridge // http://www.pico-8.com\n')
        self.outfile.write('version 38\n')
        self.outfile.write('__lua__\n')
        self.outfile.write('-- p8 ascii export by pepe 2024\n')
        self.outfile.write('cls()\n')
        self.outfile.write('for i=0,639do\n')
        self.outfile.write('x=4*(i%32)y=6*(i\\32)+2\n')
        self.outfile.write('c=peek(2*i)k=peek(2*i+1)\n')
        self.outfile.write('rectfill(x,y,x+3,y+5,k&15)\n')
        self.outfile.write('if(c>111)c=56+c\\2\n')
        self.outfile.write('?chr(c+16),x,y,(k\\16)&15\n')
        self.outfile.write('end\n')
        self.outfile.write('while 1do end\n')
        self.outfile.write('__gfx__\n')
        hxc="0123456789abcdef"
        i=0
        for frame, layer, x, y in TileIter(self.art):
            # only read from layer 0 of frame 0
            if layer > 0 or frame > 0:
                continue
            ch, fg, bg, _ = self.art.get_tile_at(frame, layer, x, y)
            self.outfile.write(hxc[ch%16])
            self.outfile.write(hxc[(ch//16)%16])
            self.outfile.write(hxc[bg-1])
            self.outfile.write(hxc[fg-1])
            #self.outfile.write('.')
            i=i+1
            if (i%32)==0:
                self.outfile.write('\n')

        self.outfile.write('\n')

        self.outfile.close()
        return True
